<?php
declare(strict_types=1);

// Gemeinsame Funktionen für Formularseite (Zeitstempel) und Versand.
// Kein session_start(): Es werden keine Cookies gesetzt.

/** Zugangsdaten liegen außerhalb des Webordners: public_html/anfrage/lib -> drei Ebenen höher. */
function anfrage_config(): ?array
{
    static $c = false;
    if ($c === false) {
        $datei = dirname(__DIR__, 3) . '/anfrage-config.php';
        $c = is_file($datei) ? require $datei : null;
        if (is_array($c)) {
            $c['data_dir'] ??= dirname($datei) . '/anfrage-daten';
        }
    }
    return is_array($c) ? $c : null;
}

function b64url(string $bin): string
{
    return rtrim(strtr(base64_encode($bin), '+/', '-_'), '=');
}

/** Zeitstempel mit Signatur: zeigt, dass das Formular von unserer Seite kam und wann es geladen wurde. */
function anfrage_token(): string
{
    $cfg = anfrage_config();
    if ($cfg === null) {
        return '';
    }
    $ts = (string) time();
    return $ts . '.' . b64url(hash_hmac('sha256', 'anfrage|' . $ts, $cfg['secret'], true));
}

/** @return string|null Fehlercode oder null, wenn gültig */
function anfrage_token_pruefen(string $token, int $minSek = 3, int $maxSek = 86400): ?string
{
    if (!preg_match('/^(\d{10})\.([A-Za-z0-9_-]{43})$/', $token, $m)) {
        return 'token';
    }
    $soll = b64url(hash_hmac('sha256', 'anfrage|' . $m[1], anfrage_config()['secret'], true));
    if (!hash_equals($soll, $m[2])) {
        return 'token';
    }
    $alter = time() - (int) $m[1];
    if ($alter < $minSek) {
        return 'zu_schnell';
    }
    if ($alter > $maxSek) {
        return 'abgelaufen';
    }
    return null;
}

/**
 * Kennung für das Rate-Limit: IPv4 komplett, IPv6 nur das /64-Präfix (ein Anschluss).
 * Gespeichert wird nur ein HMAC mit Tagesschlüssel: nicht umkehrbar, nicht über Tage verknüpfbar.
 */
function ip_kennung(): string
{
    $bin = @inet_pton($_SERVER['REMOTE_ADDR'] ?? '');
    if ($bin !== false && strlen($bin) === 16) {
        $bin = substr($bin, 0, 8);
    }
    return hash_hmac('sha256', (string) $bin, anfrage_config()['secret'] . date('Y-m-d'));
}

/** Zählt Anfragen in einem Zeitfenster. true = Grenze überschritten. Einträge älter als 24 Stunden werden gelöscht. */
function rate_limit(string $dir, string $key, int $max, int $fenster): bool
{
    if (!is_dir($dir)) {
        mkdir($dir, 0700, true);
    }
    foreach (glob($dir . '/*.json') ?: [] as $f) {
        if (filemtime($f) < time() - 86400) {
            @unlink($f);
        }
    }
    $fh = fopen($dir . '/' . $key . '.json', 'c+');
    flock($fh, LOCK_EX);
    $zeiten = json_decode(stream_get_contents($fh) ?: '[]', true) ?: [];
    $jetzt = time();
    $zeiten = array_values(array_filter($zeiten, fn ($t) => $t > $jetzt - $fenster));
    $zuViel = count($zeiten) >= $max;
    if (!$zuViel) {
        $zeiten[] = $jetzt;
    }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($zeiten));
    flock($fh, LOCK_UN);
    fclose($fh);
    return $zuViel;
}

/** Text bereinigen: gültiges UTF-8, keine Steuerzeichen (Zeilenumbrüche nur, wo erlaubt), Länge begrenzen. */
function feld(string $name, int $max, bool $mehrzeilig = false): string
{
    $v = $_POST[$name] ?? '';
    if (!is_string($v) || !mb_check_encoding($v, 'UTF-8')) {
        return '';
    }
    $v = $mehrzeilig
        ? preg_replace('/[^\P{C}\n]/u', '', str_replace("\r\n", "\n", $v))
        : preg_replace('/\p{C}/u', '', $v);
    return mb_substr(trim((string) $v), 0, $max);
}

/** Nur technische Fehler protokollieren, keine Formularinhalte (Datensparsamkeit). */
function protokoll(string $text): void
{
    $cfg = anfrage_config();
    if ($cfg !== null) {
        @file_put_contents($cfg['data_dir'] . '/fehler.log', date('c') . ' ' . $text . "\n", FILE_APPEND | LOCK_EX);
    }
}
