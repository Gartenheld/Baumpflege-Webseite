<?php
// Zugangsdaten für das Anfrageformular.
//
// Diese Datei NICHT ins Repository und NICHT in public_html legen.
// Auf dem Server als "anfrage-config.php" eine Ebene über public_html anlegen, z. B.:
//   /home/u123456789/domains/baumpflege-happe.de/anfrage-config.php
// (im hPanel: Dateimanager, Ordner der Domain, neue Datei).
return [
    'smtp_host'  => 'smtp.hostinger.com',
    'smtp_port'  => 465,                              // 465 = SSL; alternativ 587 (STARTTLS), siehe hPanel unter E-Mail
    'smtp_user'  => 'website@baumpflege-happe.de',    // Postfach nur für den Versand der Formularmails
    'smtp_pass'  => 'HIER-DAS-POSTFACH-PASSWORT',
    'from'       => 'website@baumpflege-happe.de',
    'from_name'  => 'Website Baumpflege Happe',
    'to'         => 'info@baumpflege-happe.de',       // hier kommen die Anfragen an
    // Zufälliger Geheimschlüssel, einmalig erzeugen, z. B. per SSH: php -r 'echo bin2hex(random_bytes(32));'
    'secret'     => 'HIER-64-ZUFAELLIGE-HEXZEICHEN',
    // Optional: Ordner für Rate-Limit und Fehlerprotokoll (Standard: anfrage-daten neben dieser Datei)
    // 'data_dir' => __DIR__ . '/anfrage-daten',
    // Nur für Tests: true legt Mails als Datei ab, statt sie zu senden
    'test_modus' => false,
];
