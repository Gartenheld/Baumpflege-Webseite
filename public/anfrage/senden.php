<?php
declare(strict_types=1);

// Empfänger des Anfrageformulars (/kontakt/). Prüft die Eingaben, schützt vor Spam ohne externen Dienst
// und sendet die Anfrage per SMTP an das Postfach des Betriebs. Fotos werden nur als Mailanhang verschickt,
// nicht auf dem Server gespeichert. Keine Cookies, keine Sitzung.

use PHPMailer\PHPMailer\PHPMailer;

require __DIR__ . '/lib/anfrage.php';
require __DIR__ . '/lib/PHPMailer/Exception.php';
require __DIR__ . '/lib/PHPMailer/PHPMailer.php';
require __DIR__ . '/lib/PHPMailer/SMTP.php';

const MAX_FOTOS = 8;
const MAX_FOTO_BYTES = 10 * 1024 * 1024;   // je Foto
const MAX_GESAMT_BYTES = 15 * 1024 * 1024; // alle Fotos zusammen, damit die Mail unter etwa 25 MB bleibt
const ERLAUBT = [
    'image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp',
    'image/heic' => 'heic', 'image/heif' => 'heif',
];

header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');

function weiter(string $pfad): never
{
    header('Location: ' . $pfad, true, 303); // nach dem Absenden auf eine normale Seite weiterleiten
    exit;
}

/** Fehlerseite im Design der Website (Vorlage /kontakt/fehler/), mit einfacher Ersatzseite, falls die Vorlage fehlt. */
function fehler(int $status, array $meldungen): never
{
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    $vorlage = @file_get_contents(dirname(__DIR__) . '/kontakt/fehler/index.html');
    // Die Vorlage enthält <li …>__FEHLERLISTE__</li>; das <li> trägt Stil-Attribute, die übernommen werden
    if ($vorlage !== false && preg_match('~(<li[^>]*>)__FEHLERLISTE__</li>~', $vorlage, $treffer)) {
        $liste = implode('', array_map(fn ($m) => $treffer[1] . htmlspecialchars($m, ENT_QUOTES) . '</li>', array_unique($meldungen)));
        echo str_replace($treffer[0], $liste, $vorlage);
    } else {
        $liste = implode('', array_map(fn ($m) => '<li>' . htmlspecialchars($m, ENT_QUOTES) . '</li>', array_unique($meldungen)));
        echo '<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            . '<meta name="robots" content="noindex"><title>Anfrage noch nicht gesendet | Baumpflege Happe</title></head><body>'
            . '<h1>Ihre Anfrage wurde noch nicht gesendet</h1><ul>' . $liste . '</ul>'
            . '<p>Bitte gehen Sie mit der Zurück-Taste zum Formular oder rufen Sie uns an.</p><p><a href="/kontakt/">Zum Formular</a></p></body></html>';
    }
    exit;
}

// 0. Zugangsdaten vorhanden?
$cfg = anfrage_config();
if ($cfg === null) {
    fehler(500, ['Das Formular ist gerade nicht erreichbar. Bitte rufen Sie uns an oder schreiben Sie uns per WhatsApp.']);
}

// 1. Nur POST und nur von der eigenen Website
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    weiter('/kontakt/');
}
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '') {
    $host = parse_url($origin, PHP_URL_HOST) . (parse_url($origin, PHP_URL_PORT) ? ':' . parse_url($origin, PHP_URL_PORT) : '');
    if (strcasecmp($host, (string) ($_SERVER['HTTP_HOST'] ?? '')) !== 0) {
        fehler(403, ['Die Anfrage kam nicht von unserer Website.']);
    }
}

// 2. Upload größer als post_max_size: PHP liefert dann leere Formulardaten
if (empty($_POST) && (int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 0) {
    fehler(413, ['Die Fotos sind zusammen zu groß. Bitte wählen Sie weniger oder kleinere Fotos aus.']);
}

// 3. Honeypot: Das Feld ist für Menschen unsichtbar. Bots bekommen scheinbar Erfolg.
if (($_POST['website'] ?? '') !== '') {
    weiter('/kontakt/danke/');
}

// 4. Zeitsperre mit signiertem Zeitstempel (frühestens 3 Sekunden, höchstens 24 Stunden nach dem Laden)
$t = anfrage_token_pruefen((string) ($_POST['t'] ?? ''));
if ($t === 'zu_schnell' || $t === 'token') {
    weiter('/kontakt/danke/'); // typisch für Bots: still verwerfen
}
if ($t === 'abgelaufen') {
    fehler(400, ['Das Formular war sehr lange geöffnet. Bitte laden Sie die Seite neu und senden Sie die Anfrage erneut.']);
}

// 5. Eingaben prüfen
$name      = feld('name', 100);
$email     = feld('email', 254);
$telefon   = feld('telefon', 40);
$ort       = feld('ort', 100);
$leistung  = feld('leistung', 80);
$nachricht = feld('nachricht', 5000, true);
$rueckruf  = ($_POST['rueckruf'] ?? '') === 'ja';
$zeit      = in_array($_POST['rueckruf_zeit'] ?? '', ['egal', 'vormittags', 'nachmittags'], true) ? $_POST['rueckruf_zeit'] : 'egal';

$f = [];
if (mb_strlen($name) < 2) $f[] = 'Bitte geben Sie Ihren Namen an.';
if ($email !== '' && !PHPMailer::validateAddress($email)) $f[] = 'Die E-Mail-Adresse ist nicht gültig.';
if ($telefon !== '' && !preg_match('/^[0-9 +()\/.\-]{6,40}$/', $telefon)) $f[] = 'Die Telefonnummer enthält ungültige Zeichen.';
if ($email === '' && $telefon === '') $f[] = 'Bitte geben Sie eine E-Mail-Adresse oder Telefonnummer an.';
if ($rueckruf && $telefon === '') $f[] = 'Für einen Rückruf benötigen wir Ihre Telefonnummer.';
if (mb_strlen($nachricht) < 10) $f[] = 'Bitte beschreiben Sie kurz Ihr Anliegen.';

// 6. Viele Links oder Link-Markup sprechen für Spam
$links = preg_match_all('~(https?://|www\.)~i', $nachricht . ' ' . $name);
if ($links > 2 || preg_match('~\[url|<a\s~i', $nachricht) || preg_match('~https?://|www\.~i', $name)) {
    fehler(400, ['Ihre Nachricht enthält zu viele Links. Bitte entfernen Sie die Links oder rufen Sie uns an.']);
}

// 7. Fotos: Anzahl, Größe und echter Dateityp (nicht die Endung)
$fotos = [];
$summe = 0;
$up = $_FILES['fotos'] ?? null;
if (is_array($up) && is_array($up['name'] ?? null)) {
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    foreach ($up['error'] as $i => $err) {
        if ($err === UPLOAD_ERR_NO_FILE) continue;
        if ($err === UPLOAD_ERR_INI_SIZE || $err === UPLOAD_ERR_FORM_SIZE) { $f[] = 'Ein Foto ist zu groß (höchstens 10 MB je Foto).'; continue; }
        if ($err !== UPLOAD_ERR_OK || !is_uploaded_file($up['tmp_name'][$i])) { $f[] = 'Ein Foto konnte nicht übertragen werden.'; continue; }
        $mime = $finfo->file($up['tmp_name'][$i]) ?: '';
        if (!isset(ERLAUBT[$mime])) { $f[] = 'Bitte nur Fotos als JPEG, PNG, WebP oder HEIC senden.'; continue; }
        if ($up['size'][$i] > MAX_FOTO_BYTES) { $f[] = 'Ein Foto ist zu groß (höchstens 10 MB je Foto).'; continue; }
        $summe += $up['size'][$i];
        $fotos[] = [$up['tmp_name'][$i], 'foto-' . (count($fotos) + 1) . '.' . ERLAUBT[$mime], $mime];
    }
}
if (count($fotos) > MAX_FOTOS) $f[] = 'Bitte senden Sie höchstens ' . MAX_FOTOS . ' Fotos.';
if ($summe > MAX_GESAMT_BYTES) $f[] = 'Die Fotos sind zusammen zu groß (höchstens 15 MB). Bitte wählen Sie weniger Fotos aus.';
if ($f) fehler(400, $f);

// 8. Rate-Limit erst nach bestandener Prüfung (Tippfehler zählen nicht):
//    je Anschluss 3 in 10 Minuten und 10 am Tag, insgesamt 50 am Tag
$rl = $cfg['data_dir'] . '/ratelimit';
$id = ip_kennung();
if (rate_limit($rl, $id . '-10m', 3, 600) || rate_limit($rl, $id . '-1d', 10, 86400) || rate_limit($rl, 'gesamt', 50, 86400)) {
    fehler(429, ['Es wurden zu viele Anfragen in kurzer Zeit gesendet. Bitte versuchen Sie es später erneut oder rufen Sie uns an.']);
}

// 9. Mail an den Betrieb. Absender ist das eigene Postfach (SPF, DKIM, DMARC passen), Antworten gehen per Reply-To an den Kunden.
$m = new PHPMailer(true);
try {
    $m->isSMTP();
    $m->Host = $cfg['smtp_host'];
    $m->Port = (int) $cfg['smtp_port'];
    $m->SMTPSecure = (int) $cfg['smtp_port'] === 465 ? PHPMailer::ENCRYPTION_SMTPS : PHPMailer::ENCRYPTION_STARTTLS;
    $m->SMTPAuth = true;
    $m->Username = $cfg['smtp_user'];
    $m->Password = $cfg['smtp_pass'];
    $m->CharSet = PHPMailer::CHARSET_UTF8;
    $m->setFrom($cfg['from'], $cfg['from_name']);
    $m->addAddress($cfg['to']);
    if ($email !== '') {
        $m->addReplyTo($email, $name);
    }
    $m->Subject = 'Anfrage über die Website: ' . ($leistung ?: 'allgemein') . ($ort !== '' ? ', ' . $ort : '') . ($rueckruf ? ' (Rückruf)' : '');
    $m->isHTML(false); // nur Text: keine Kundeneingaben als HTML in der Mail
    $m->Body = "Name: $name\nE-Mail: " . ($email ?: '-') . "\nTelefon: " . ($telefon ?: '-')
        . "\nRückruf gewünscht: " . ($rueckruf ? "ja, $zeit" : 'nein')
        . "\nOrt des Grundstücks: " . ($ort ?: '-') . "\nAnliegen: " . ($leistung ?: '-')
        . "\nFotos: " . count($fotos) . "\n\nNachricht:\n$nachricht\n";
    foreach ($fotos as [$tmp, $dateiname, $mime]) {
        $m->addAttachment($tmp, $dateiname, PHPMailer::ENCODING_BASE64, $mime);
    }
    if (!empty($cfg['test_modus'])) {
        // Nur für Tests: Mail nicht senden, sondern als Datei ablegen
        $m->preSend();
        if (!is_dir($cfg['data_dir'])) {
            mkdir($cfg['data_dir'], 0700, true);
        }
        file_put_contents($cfg['data_dir'] . '/test-' . bin2hex(random_bytes(4)) . '.eml', $m->getSentMIMEMessage());
    } else {
        $m->send();
    }
} catch (\Throwable $e) {
    protokoll('Versand fehlgeschlagen: ' . $m->ErrorInfo);
    fehler(500, ['Ihre Anfrage konnte wegen eines technischen Fehlers nicht gesendet werden. Bitte rufen Sie uns an oder schreiben Sie uns per WhatsApp.']);
}

weiter('/kontakt/danke/');
