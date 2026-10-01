# Liveschaltung: Checkliste

Reihenfolge von oben nach unten. **Du** = Schritte im Hostinger-, STRATO-, GitHub- oder Google-Konto, die nur du machen kannst. **Ich** = Schritte, die ich übernehme, sobald die Voraussetzungen da sind. Details stehen jeweils im Konzept [01-technik-und-deployment.md](01-technik-und-deployment.md).

Stand der Website: Alle Seiten sind fertig und freigegeben (Schritt 4). Lighthouse auf dem Handy-Profil: 99 bis 100 Punkte in Leistung, Barrierefreiheit, Best Practices und SEO auf allen geprüften Seiten (lokal gemessen, ohne echte Fotos).

## A. Konten und Hosting (du)

- [ ] **Hostinger:** Tarif Premium oder höher, EU-Rechenzentrum (Konzept 6).
- [ ] **Domain** `baumpflege-happe.de` registrieren, am einfachsten bei Hostinger. Automatische Verlängerung an.
- [ ] **Website anlegen** im hPanel als leere PHP/HTML-Website, PHP 8.x, SSH einschalten (Konzept 6, Punkte 1 bis 4).
- [ ] **PHP-Optionen:** `upload_max_filesize` mindestens 12M, `post_max_size` mindestens 20M, `max_file_uploads` mindestens 10. Danach die Werte noch einmal ablesen.
- [ ] **Postfächer:** eines für Anfragen (z. B. `info@`), ideal ein zweites nur zum Versenden (`website@`). SPF, DKIM und DMARC so eintragen, wie das hPanel sie anzeigt.
- [ ] **GitHub-Repository auf privat stellen** (Konzept 7.3).

## B. Technik verbinden (du, ich helfe)

- [ ] **Deploy-Schlüssel** erzeugen und im hPanel hinterlegen, Fingerabdruck festhalten (Konzept 7.2). Den privaten Schlüssel nie per Chat oder Mail schicken, nur in GitHub als Secret eintragen.
- [ ] **GitHub Secrets und Variablen** anlegen (Konzept 7.3): `HOSTINGER_SSH_KEY`, `HOSTINGER_KNOWN_HOSTS`, `HOSTINGER_SSH_HOST`, `HOSTINGER_SSH_PORT`, `HOSTINGER_SSH_USER`, `DEPLOY_PATH`, `SITE_URL`, `NOINDEX` = `true`, `DEPLOY_ENABLED` = `true`, optional `PREVIEW_HTPASSWD_PATH`.
- [ ] **Formular-Zugangsdaten:** `anfrage-config.php` nach Vorlage [server/anfrage-config.beispiel.php](../server/anfrage-config.beispiel.php) eine Ebene **über** `public_html` anlegen, z. B. `/home/u123456789/domains/baumpflege-happe.de/anfrage-config.php`. Passwort des Versand-Postfachs eintragen, als `secret` eine lange Zufallsfolge (z. B. aus dem Passwortmanager, 64 Zeichen). `test_modus` auf `false`.
- [ ] **Ich:** Pull Request von meinem Branch nach `main`. Nach deinem Merge lädt GitHub die Vorschau hoch (noindex, optional mit Passwort).

## C. Vorschau testen (wir beide)

- [ ] **Ich:** Seiten, Weiterleitungen (`http` und `www` auf `https://baumpflege-happe.de`), Sicherheits-Header, robots.txt und Sitemap auf dem Server prüfen.
- [ ] **Du:** je eine Testanfrage vom iPhone, von einem Android-Handy und vom Rechner, einmal mit Fotos und Rückrufwunsch. Mail kommt an, „Antworten“ geht an den Absender, Fotos hängen an.
- [ ] **Ich:** In der Testmail SPF, DKIM und DMARC prüfen (Kopfzeilen „pass“). Zwei Aufrufe von `/kontakt/` liefern unterschiedliche Zeitstempel (kein Server-Cache).

## D. Inhalte fertigstellen (du, ich setze ein)

Der Live-Build bricht ab, solange irgendwo „Platzhalter“ oder die Nummer aus lauter Nullen steht. Das Wort „Platzhalter“ in Vorlagen und Kommentaren stört nicht.

- [ ] **Betriebsdaten** in [src/config/betrieb.ts](../src/config/betrieb.ts): Telefon (Anzeige und Wählnummer), WhatsApp-Nummer, E-Mail, Erreichbarkeit, Antwortzeit, USt-IdNr., Google-Bewertungen (Durchschnitt, Anzahl, Stand), Profil-Links.
- [ ] **Häufige Fragen** mit offenen Angaben:
  - [src/inhalte/faq/kosten-ersteinschaetzung.md](../src/inhalte/faq/kosten-ersteinschaetzung.md): Antwortzeit und ob die Besichtigung kostenlos ist
  - [src/inhalte/faq/kosten-angebot.md](../src/inhalte/faq/kosten-angebot.md): Abrechnungsart und Zahlungsbedingungen
- [ ] **Impressum:** Satz zur Verbraucherschlichtung in [src/pages/impressum.astro](../src/pages/impressum.astro) bestätigen.
- [ ] **Datenschutzerklärung** aus einem Generator in [src/inhalte/seiten/datenschutz.md](../src/inhalte/seiten/datenschutz.md) einfügen. Angaben dafür: Konzept 9.4 (Hosting bei Hostinger, Server-Logs, Kontaktformular mit Fotos und Mailversand, WhatsApp-Link, keine Cookies, kein Tracking, keine externen Schriften).
- [ ] **Fotos:** mindestens das Startseitenfoto, besser auch Über uns, Baumpflege und Baumfällung (Anleitung in [src/bilder/README.md](../src/bilder/README.md)). Ohne Foto zeigt die Live-Seite eine ruhige Fläche mit dem Baumsymbol statt „Foto folgt“.
- [ ] **Referenzen und Bewertungen:** zum Start gern zwei bis drei echte Referenzen und drei bis vier echte Google-Bewertungen. Ohne freigegebene Einträge blendet die Live-Seite die Bewertungen aus, die Referenzseite nennt „in Kürze“.
- [ ] **Offene Fragen** aus der Freigabe von Schritt 4 beantworten: Kronenpflege ohne Seilklettertechnik, Wurzelstock-Gerät, Partner, Rollrasen, Zusagen wie Mulch und Rahmenvertrag.
- [ ] **Ich:** Baumschutzsatzung je Ort prüfen und `baumschutz.status` sowie `geprueft` in den Ortsdateien setzen.

## E. Starttag (Abend)

- [ ] **Du:** In GitHub `NOINDEX` auf `false`, `PREVIEW_HTPASSWD_PATH` leeren, `SITE_URL` = `https://baumpflege-happe.de`. Dann *Actions -> Build und Deployment -> Run workflow*.
- [ ] **Ich:** Live-Seite prüfen: kein noindex, robots.txt mit Sitemap, Canonical-Adressen, Formular-Testanfrage, höchstens zwei Weiterleitungssprünge.
- [ ] **Ich:** HSTS in `public/.htaccess` zunächst kurz einschalten (`max-age=300`), sobald HTTPS sicher läuft.
- [ ] **Alte Domain** gartenheldservice.com umstellen nach Konzept 13.3 (Variante B): Weiterleitungs-Website bei Hostinger, A-Records bei STRATO. Weiterleitungen testen.

## F. Google (du, ich begleite)

- [ ] **Search Console:** Domain-Property für `baumpflege-happe.de` per DNS bestätigen, Sitemap `https://baumpflege-happe.de/sitemap-index.xml` einreichen, Startseite zur Indexierung anmelden (Konzept 12).
- [ ] **Adressänderung** in der Property der alten Domain (Konzept 13.6).
- [ ] **Google-Unternehmensprofil:** Website-Adresse auf die neue Domain. Namensänderung erst, wenn Fahrzeug, Kleidung und Rechnungen den neuen Namen tragen (Konzept 13.5).
- [ ] **Verzeichnisse** (Gelbe Seiten, Das Örtliche, Social Media) auf neuen Namen, neue Domain und neue Mailadresse.

## G. Nach zwei bis vier Wochen

- [ ] Search Console beider Domains ansehen: indexierte Seiten, Fehler, alte Adressen ohne Weiterleitung nachtragen.
- [ ] HSTS auf ein Jahr erhöhen, DMARC der neuen Domain von `p=none` auf `quarantine`.
- [ ] Workflow „Qualität“ (Lighthouse, jeden Montag) kontrollieren: Mit echten Fotos ändern sich die Ladezeiten.
