# Technik und Deployment

Schritt 1 von 5: Technikvorschlag und Deployment-Plan für die Website „Baumpflege Happe“.
Stand: 1. Oktober 2026.

Dieses Dokument erklärt dir, womit wir die Website bauen, wie sie zu Hostinger kommt, wie das Formular funktioniert, was wir für Datenschutz und Suchmaschinen tun und wie wir mit der alten Domain gartenheldservice.com umgehen. Am Ende stehen der Fahrplan und die Fragen, die du beantworten musst.

**So sind die Angaben gekennzeichnet**

- Ohne Zusatz: geprüft, entweder an der Primärquelle (Hersteller-Repository, Gesetzestext, npm) oder durch eigene Tests.
- **Bitte prüfen**: nicht sicher belegbar, meist Tarifdetails, Menüpfade oder Preise von Hostinger, IONOS, STRATO und Google. Diese Angaben ändern sich oft. Du siehst sie im jeweiligen Kundenbereich nach, bevor du etwas kaufst oder umstellst.
- Platzhalter: `NEUE-DOMAIN.de` steht für die noch offene neue Domain. Telefon, E-Mail, WhatsApp-Nummer und Erreichbarkeitszeiten sind ebenfalls Platzhalter.

Keine der Aussagen zu Recht und Datenschutz ist Rechtsberatung.

---

## 1. Kurzfassung

- **Technik:** Astro 7 als statischer Website-Generator. Heraus kommt reines HTML, CSS und Bilder, ohne Datenbank und ohne Login. Nur das Anfrageformular läuft als kleines PHP-Skript auf dem Server.
- **Hosting:** Hostinger, Mindesttarif **Premium** (Web Premium). Vor dem Kauf im Tarifvergleich prüfen: SSH-Zugang, mindestens 2 Websites, E-Mail-Postfächer.
- **Deployment:** Du änderst eine Datei auf github.com, GitHub Actions prüft und baut die Seite und lädt sie per rsync über SSH zu Hostinger. Fehler stoppen den Vorgang, die alte Version bleibt online. Fallback: die Git-Funktion im hPanel.
- **Formular:** PHP mit PHPMailer, Versand per SMTP über ein Hostinger-Postfach. Spamschutz mit Honeypot, Zeitsperre und Rate-Limit, ohne reCAPTCHA. Bis zu 8 Fotos. Keine Cookies, funktioniert auch ohne JavaScript.
- **Datenschutz:** keine Cookies, kein Tracking, keine externen Ressourcen (Schriften, Videos, Karte alles lokal). Damit ist nach unserer Einschätzung kein Cookie-Banner nötig.
- **SEO:** strukturierte Daten (LocalBusiness als Untertyp `HomeAndConstructionBusiness`, Service, BreadcrumbList, FAQPage), Sitemap, robots.txt, Canonical, Open Graph, eigener Title und eigene Description je Seite. Bewusst kein Bewertungs-Sterne-Markup.
- **Alte Domain:** gartenheldservice.com bleibt beim bisherigen Anbieter. Nur die Adresseinträge (A-Records) zeigen künftig auf Hostinger, dort leitet eine fertige, lokal getestete `.htaccess` jede alte Seite per 301 auf die passende neue. Die E-Mail auf der alten Domain bleibt unberührt. Ein Umzug der Domain zu Hostinger bringt für die Weiterleitungen nichts, gefährdet aber die E-Mail (Abschnitt 13.2). Domain dauerhaft behalten.
- **Vorher klären:** Laut DNS liegen Nameserver und E-Mail von gartenheldservice.com bei **STRATO**, nur die Webserver im Netz von IONOS. Das prüfst du bitte zuerst (Frage 1 in Abschnitt 15).
- **Schon umgesetzt:** Grundgerüst mit Astro 7 und Platzhalterseite, zentrale Betriebsdaten mit Platzhaltern, `robots.txt` mit Vorschau-Sperre, Sitemap, Content-Security-Policy ohne Fremdquellen, `.htaccess` mit Sicherheits-Headern und Cache-Regeln (lokal auf Apache getestet), Deployment-Workflow (Prüfung und Build laufen auf GitHub grün, der Upload startet, sobald Hostinger eingerichtet ist) und die fertige Weiterleitungsdatei für die alte Domain.

---

## 2. Technikentscheidung

### Empfehlung: Astro, PHP nur für das Formular

Astro (aktuell Version 7.3.5 vom 24.09.2026) baut aus Vorlagen und Inhaltsdateien fertige HTML-Seiten. Auf dem Server liegt danach nur noch statisches HTML. Das passt zu deinen Anforderungen:

- **Schnell und sicher:** Kein Programmcode läuft beim Seitenaufruf, außer dem Formularskript. Es gibt nichts, was gehackt oder aktualisiert werden muss wie bei WordPress. Sicherheitslücken in Astro wirken sich bei einer rein statischen Seite fast nur beim Bauen aus.
- **Bilder automatisch optimiert:** Astro erzeugt aus deinen Fotos AVIF und WebP in mehreren Größen, mit Breite und Höhe (verhindert Layoutsprünge). Ohne Alt-Text bricht der Build ab.
- **Schriften lokal:** Die eingebaute Fonts-Funktion (stabil seit Astro 6) bindet die Schrift vom eigenen Server ein, mit Preload und passender Ersatzschrift.
- **Kein JavaScript nötig:** Ohne eigenes Skript liefert Astro 0 JavaScript-Dateien aus (im Test bestätigt). Kleine Skripte, etwa für die Videosteuerung, bekommen automatisch eine Prüfsumme in der Content-Security-Policy.
- **Inhalte als Dateien mit Prüfung:** Texte, Orte, Referenzen und Bewertungen liegen als einfache Textdateien im Repository. Fehlt ein Pflichtfeld oder ist ein Title zu lang, bricht der Build mit einer deutschen Fehlermeldung ab, statt eine fehlerhafte Seite zu veröffentlichen.
- **Sitemap und Sicherheits-Header** sind eingebaut bzw. vorbereitet.

Das Grundgerüst im Repository nutzt Astro bereits. Die Version ist per `package-lock.json` festgeschrieben. Wir aktualisieren ein- bis zweimal im Jahr bewusst, weil Astro einen schnellen Versionstakt hat (6.0 im März 2026, 7.0 im Juni 2026). Node.js: Version 24 (steht in `.nvmrc`), unterstützt bis 30.04.2028.

### Verworfene Alternativen

| Alternative | Warum nicht |
|---|---|
| Handgeschriebenes HTML/CSS | Lohnt sich nur bei 3 bis 5 Seiten. Wir haben rund 30 Seiten mit vielen gleichen Bausteinen (Kopf, Fuß, Kontaktblock, FAQ, Bewertungen, strukturierte Daten). Eine Telefonnummer stünde an 30 Stellen, Bilder müssten von Hand in allen Formaten exportiert werden. Fehleranfällig für die Pflege durch dich. |
| Eleventy | Technisch machbar und stabil, aber Inhaltsprüfung, Verweise zwischen Inhalten, Schrift-Ersatzmetriken und CSP müssten wir selbst bauen. Das Projekt wird gerade umbenannt („Build Awesome“), Version 4 ist noch Alpha. |
| WordPress oder Baukasten | Datenbank, Login, Plugins und laufende Updates. Mehr Angriffsfläche, langsamer, und viele Themes und Plugins laden Fremdressourcen oder setzen Cookies. Baukästen erlauben oft weder eigene PHP-Skripte noch saubere `.htaccess`-Regeln. Beides passt nicht zu „keine Cookies, kein Tracking, sehr gute Core Web Vitals“. |

---

## 3. Geplante URL-Struktur

Regeln für alle Adressen:

- immer `https://`, **ohne www** (kürzer auf Fahrzeug und Kleidung; `www.` leitet per 301 um)
- Kleinbuchstaben, Umlaute transliteriert (ä -> ae, ö -> oe, ü -> ue, ß -> ss)
- jede Seite ist ein Verzeichnis mit `index.html`, die Adresse endet **immer mit „/“**

| Seite | URL | Hinweis |
|---|---|---|
| Startseite | `/` | |
| Leistungen (Übersicht) | `/leistungen/` | |
| Baumpflege | `/leistungen/baumpflege/` | |
| Baumfällung | `/leistungen/baumfaellung/` | |
| Seilklettertechnik | `/leistungen/seilklettertechnik/` | per Schalter ausblendbar, nur sichtbar, wenn SKT-A zum Start vorliegt |
| Landschaftspflege und Heckenschnitt | `/leistungen/landschaftspflege-heckenschnitt/` | mit Abschnitt zu kleinen Gartenprojekten ohne große Maschinen |
| Rollrasen | `/leistungen/rollrasen/` | |
| Häckselarbeiten | `/leistungen/haeckselarbeiten/` | |
| Wurzelstockentfernung | `/leistungen/wurzelstockentfernung/` | |
| Sturmschadenbeseitigung | `/leistungen/sturmschadenbeseitigung/` | |
| Gewerbe und Hausverwaltungen | `/gewerbe-hausverwaltungen/` | |
| Einsatzgebiet (Übersicht) | `/einsatzgebiet/` | |
| Bornheim | `/einsatzgebiet/bornheim/` | |
| Alfter | `/einsatzgebiet/alfter/` | |
| Bonn | `/einsatzgebiet/bonn/` | |
| Brühl | `/einsatzgebiet/bruehl/` | |
| Köln | `/einsatzgebiet/koeln/` | |
| Wesseling | `/einsatzgebiet/wesseling/` | |
| Hürth | `/einsatzgebiet/huerth/` | |
| Erftstadt | `/einsatzgebiet/erftstadt/` | |
| Weilerswist | `/einsatzgebiet/weilerswist/` | |
| Referenzen | `/referenzen/` | |
| Über uns | `/ueber-uns/` | mit Qualifikationen und Ausstattung |
| FAQ | `/faq/` | |
| Kontakt und Anfrage | `/kontakt/` | Anfrageformular. Technisch eine `index.php` (wegen des Spamschutzes, siehe Abschnitt 8), die Adresse bleibt `/kontakt/` |
| Danke-Seite | `/kontakt/danke/` | noindex, nicht in der Sitemap |
| Impressum | `/impressum/` | |
| Datenschutz | `/datenschutz/` | Platzhalter, bis der Generator-Text da ist |

Technische Adressen ohne eigenen Inhalt:

- `/404.html`: Fehlerseite „Seite nicht gefunden“
- `/kontakt/fehler/`: Vorlage für Fehlermeldungen des Formulars, noindex, nicht in der Sitemap
- `/anfrage/senden.php`: Empfänger des Formulars, für Suchmaschinen gesperrt
- `/robots.txt`, `/sitemap-index.xml` (mit `/sitemap-0.xml`), `/sitemap.xml` leitet auf `/sitemap-index.xml` um

**Kein Blog, kein Ratgeber:** Dafür gibt es weder Seitentyp noch Inhaltsart. Informationsinhalte stehen in den FAQ und auf den Leistungsseiten.

---

## 4. Inhaltsmodell

Alles, was du später selbst änderst, liegt in zwei Bereichen: `src/inhalte/` und `src/config/betrieb.ts`. Jeder Eintrag ist eine eigene Datei. Markdown (`.md`) für Seiten mit Fließtext, YAML (`.yaml`) für kurze Listeneinträge.

### Betriebsdaten zentral in einer Datei

`src/config/betrieb.ts` enthält Name, Unterzeile, Claim, Anschrift, Telefon, WhatsApp-Nummer, E-Mail, Erreichbarkeitszeiten, Antwortzeit, USt-IdNr., Links zu Google-Profil und Social Media sowie Durchschnittsbewertung, Anzahl und Stand der Google-Bewertungen. Jede Angabe steht nur dort und wird überall verwendet: im Kopf, im Footer, in der Handy-Leiste, im Impressum, im Formular und in den strukturierten Daten. Alles mit `PLATZHALTER` muss vor der Liveschaltung ersetzt werden.

### Inhaltsarten

| Inhalt | Ordner (eine Datei pro Eintrag) | Wichtige Felder | Wo es erscheint |
|---|---|---|---|
| Leistungen | `src/inhalte/leistungen/*.md` | Titel, Seitentitel, Description, H1, Reihenfolge, benötigte Qualifikation, Bild mit Alt-Text, Kostenfaktoren, verwandte Leistungen; Fließtext mit Nutzen, Vorgehen, Technik | Leistungsseiten, Übersicht, Navigation, strukturierte Daten |
| Orte | `src/inhalte/orte/*.md` | Ort, Seitentitel, Description, H1, Anfahrt aus Bornheim, Baumschutz (Satzung ja/nein/unklar, Link zur Stadt, geprüft am), Nachbarorte; eigener Fließtext | Ortsseiten, Einsatzgebiet. Referenzen aus dem Ort erscheinen automatisch. |
| Referenzen | `src/inhalte/referenzen/<jahr-monat-ort-baum>/index.md` plus Fotos im selben Ordner | Titel, Ort, Leistungen, Baumart, Datum, Bilder (vorher, nachher, Arbeit) mit Alt-Text, `veroeffentlichen` | Referenzseite, passende Orts- und Leistungsseiten |
| FAQ | `src/inhalte/faq/*.md` | Frage (endet mit „?“), Thema, zugehörige Leistungen, auf FAQ-Seite ja/nein, Reihenfolge; Antwort als Fließtext | FAQ-Seite und verteilt auf die Leistungsseiten |
| Bewertungen | `src/inhalte/bewertungen/*.yaml` | Name gekürzt (Vorname und Anfangsbuchstabe), Sterne, Datum, Text, `veroeffentlichen` | Startseite, ggf. Leistungsseiten |
| Qualifikationen | `src/inhalte/qualifikationen/*.yaml` | Titel, Erklärung in einem Satz für Laien, `vorhanden`, Reihenfolge | Über uns, Schalter für Leistungen |
| Seiten | `src/inhalte/seiten/*.md` | Seitentitel, Description, H1, je nach Seite Listen (z. B. Ablauf-Schritte, Ausstattung) | Startseite, Über uns, Gewerbe, Einsatzgebiet, Kontakt, Datenschutz |

Grundsätze:

- **Eine Datei pro Eintrag.** Ein Tippfehler in einer Datei stoppt den Build mit Dateiname und Zeile. (Getestet: Bei einer Sammeldatei für alle Bewertungen würde ein Fehler stillschweigend alle Bewertungen verschwinden lassen. Deshalb keine Sammeldateien.)
- **Dateinamen ohne Umlaute**, z. B. `baumfaellung.md`, `koeln.md`. Der Dateiname wird zur Adresse.
- **Vorlagen** beginnen mit Unterstrich (`_vorlage`) und werden nie veröffentlicht.
- **Platzhalter gehen nie live:** Referenzen und Bewertungen sind standardmäßig `veroeffentlichen: false`. In der Entwicklung sind sie sichtbar, auf der Live-Seite nicht. Zusätzlich bricht der Live-Build ab, wenn irgendwo noch das Wort `PLATZHALTER` steht.
- **Mindestanzahl:** Ist eine Inhaltsart unerwartet leer, bricht der Build ab.

### Schalter für Seilklettertechnik

Die Seite Seilklettertechnik ist an die Qualifikation SKT-A gekoppelt:

```yaml
# src/inhalte/qualifikationen/skt-a.yaml
titel: SKT-A
erklaerung: PLATZHALTER Ein Satz für Laien.
vorhanden: false   # auf true setzen, sobald der Nachweis vorliegt
reihenfolge: 3
```

Die Leistungsdatei `seilklettertechnik.md` trägt `benoetigt: skt-a`. Solange `vorhanden: false` gilt, wird die Seite nicht gebaut, nicht verlinkt, nicht in die Sitemap aufgenommen, und SKT-A erscheint nicht unter den Qualifikationen (getestet). Ein Schalter, eine Stelle. Den bisherigen Schalter `schalter.seilklettertechnik` in `betrieb.ts` ersetzen wir in Schritt 4 durch diese Kopplung, damit nicht zwei Schalter auseinanderlaufen.

Weitere Qualifikationen sind einfach eine neue Datei. `skt-b.yaml` legen wir gleich mit `vorhanden: false` an. Wichtig: Der Schalter ändert keine Texte. Die SKT-Seite verspricht keine Motorsägenarbeit im Baum. Kommt später SKT-B dazu, überarbeiten wir den Text bewusst.

---

## 5. Projektstruktur

```
Baumpflege-Webseite/
  .github/workflows/
    deploy.yml                 Prüfen, bauen, zu Hostinger hochladen
    qualitaet.yml              Lighthouse und Barriere-Test (neu, blockiert nicht)
  docs/
    01-technik-und-deployment.md
    02-weiterleitungen.md
  redirects/gartenheldservice.com/
    .htaccess                  Weiterleitungen der alten Domain (Kopie, wird von Hand hochgeladen)
  public/                      wird unverändert ausgeliefert
    .htaccess                  Serverregeln, Sicherheits-Header, Cache
    _astro/.htaccess           1 Jahr Cache für Dateien mit Prüfsumme
    anfrage/
      .htaccess                nur senden.php erreichbar
      senden.php               Formular-Empfänger
      lib/
        .htaccess              gesperrt
        anfrage.php            Token, Rate-Limit, Feldprüfung
        PHPMailer/             Exception.php, PHPMailer.php, SMTP.php, LICENSE
    favicon.svg, apple-touch-icon.png
  scripts/
    formular-php.mjs           macht nach dem Build aus der Kontaktseite eine index.php
    pruefe-links.mjs           findet tote interne Links
  src/
    config/
      betrieb.ts               zentrale Betriebsdaten und Platzhalter
      navigation.ts            Hauptmenü und Footer-Links
    content.config.ts          Inhaltsarten und Prüfregeln
    inhalte/                   alles, was du änderst
      seiten/                  startseite.md, ueber-uns.md, gewerbe-hausverwaltungen.md, ...
      leistungen/              baumpflege.md, baumfaellung.md, seilklettertechnik.md, ...
      orte/                    bornheim.md, alfter.md, bonn.md, bruehl.md, koeln.md, ...
      referenzen/              _vorlage/index.md, 2026-09-bornheim-eiche/index.md mit Fotos
      faq/                     faellgenehmigung.md, schonzeit.md, kosten-abrechnung.md, ...
      bewertungen/             _vorlage.yaml, 2026-08-vorname-n.yaml, ...
      qualifikationen/         as-baum-1.yaml, as-baum-2.yaml, skt-a.yaml, skt-b.yaml
    assets/
      fotos/                   Originalfotos (JPEG)
      videos/                  Hero-Video und Clips (MP4, optional WebM)
      fonts/                   Schriftdateien (WOFF2) und Lizenz
      logo/                    Logo als SVG (Schritt 2)
    components/                Bausteine: Kopf, Fuß, Handy-Leiste, Formular, FAQ, Bewertungen, ...
    layouts/                   Grundlayout mit Title, Description, Canonical, Open Graph
    lib/                       Hilfsfunktionen (sichtbare Leistungen, FAQ je Leistung, ...)
    pages/                     Seitenvorlagen, eine pro Seitentyp
    styles/                    Farben, Abstände, Schriftgrößen; kein CSS-Framework
  astro.config.mjs, package.json, package-lock.json, .nvmrc, tsconfig.json
  README.md                    Pflegeanleitung für dich
```

---

## 6. Hosting bei Hostinger

### Mindesttarif: Premium

**Bitte prüfen:** Alle Tarifdetails unten stammen aus Hostinger-Hilfeseiten und deutschen Testberichten aus der Suche. Sie waren hier nicht an der Quelle überprüfbar, und Hostinger hat die Tarife seit Ende 2025 mehrfach umgebaut. Vor dem Kauf im Tarifvergleich nachsehen, nach dem Kauf im hPanel unter den Tarifdetails.

Was wir brauchen und warum Premium das Minimum ist:

| Anforderung | Wofür | Single | Premium | Business |
|---|---|---|---|---|
| SSH-Zugang (rsync) | automatisches Hochladen aus GitHub | laut Recherche nein | laut Recherche ja | ja |
| Mehrere Websites | neue Website plus kleine Weiterleitungs-Website für gartenheldservice.com | 1 | laut Hostinger-Limits seit 12/2025: 3 | 50 |
| E-Mail-Postfächer | Anfragen empfangen, Formular versenden | 1 | 2 je Website (im 1. Jahr gratis, laut Recherche) | mehr |
| PHP 8.x | Formularskript | ja | ja | ja |
| Kostenloses SSL | HTTPS | ja | ja | ja |
| Backups | Sicherung auf dem Server | wöchentlich | wöchentlich (täglich als Zusatz) | täglich |

- **Single** reicht nicht: kein SSH, nur eine Website. Ginge nur mit dem Fallback-Weg und Notlösungen.
- **Business** lohnt sich nur, wenn du tägliche Backups willst. Für uns kaum wichtig: Der gesamte Code liegt in GitHub. Auf dem Server liegen nur die Formular-Zugangsdaten. Node.js und mehr Rechenleistung bringen einer statischen Seite nichts.
- **Preise (ungefähr, Bitte prüfen):** laut deutschen Testberichten (Stand 2026) Premium ca. 3 Euro im Monat netto als Aktionspreis bei 48 Monaten Vorauszahlung, Verlängerung ca. 10 Euro im Monat. Der Aktionspreis gilt nur für die vorab bezahlte Laufzeit. Den Verlängerungspreis im Warenkorb ansehen. Quellen: stark.marketing, hosttest.de (siehe Abschnitt 16).
- **E-Mail (Bitte prüfen):** Die Postfächer im Tarif sind laut Hostinger-Hilfe eine Testphase von einem Jahr, danach kostenpflichtig. Wann dein Postfach abläuft und welche Limits es hat, steht im hPanel unter E-Mail.
- **Neue Domain:** Bei Hostinger mit Tarif ab 12 Monaten laut Recherche im ersten Jahr gratis, danach Normalpreis.

### Was im hPanel einzurichten ist

Menüpfade auf Englisch, die deutsche Oberfläche kann anders heißen.

1. **Website anlegen:** *Websites -> Add website -> Empty PHP/HTML website*. Solange die Domain offen ist, mit der temporären Adresse `*.hostingersite.com`.
2. **Rechenzentrum:** EU-Standort wählen, Deutschland, falls angeboten. Der Standort wird bei der ersten Website festgelegt.
3. **SSH aktivieren:** *Websites -> Dashboard -> Advanced -> SSH Access*. Server-IP, Port und Benutzername (`u...`) notieren. Den Port ablesen, nicht raten (laut Recherche 65002). Den Deploy-Schlüssel unter *SSH keys* hinterlegen (Abschnitt 7.2).
4. **PHP:** unter *PHP Configuration* die neueste angebotene 8.x-Version wählen (laut Hostinger-Hilfe 8.2 bis 8.5, Bitte prüfen). Unter *PHP options* setzen: `upload_max_filesize` mindestens 12M, `post_max_size` mindestens 20M, `max_file_uploads` mindestens 10, `display_errors` aus, `session.auto_start` aus. Danach die Werte noch einmal ablesen: Hostinger kappt Werte über dem Tarifmaximum ohne Meldung (belegt in der Hostinger-API-Doku).
5. **E-Mail:** Postfach für Anfragen anlegen (z. B. `anfrage@NEUE-DOMAIN.de`), ideal ein zweites nur zum Versenden (`website@NEUE-DOMAIN.de`). SMTP-Daten unter E-Mail ablesen.
6. **Formular-Zugangsdaten:** im Dateimanager die Datei `anfrage-config.php` **außerhalb** von `public_html` anlegen (Abschnitt 8).
7. **Domain:** registrieren oder verbinden, danach den **SSL-Status prüfen** und das Zertifikat bei Bedarf installieren. Erst wenn es aktiv ist, unter *Security -> SSL* „Force HTTPS“ einschalten. **Bitte prüfen:** Ob der Schalter selbst in die `.htaccess` schreibt, ist nicht belegt. Nach dem nächsten Deployment testen, ob `http://` weiter auf `https://` umleitet. Falls nicht, kommt die Regel in unsere `.htaccess`.
8. **Nicht nutzen:** die hPanel-Werkzeuge *Redirects* und *Password Protect Directories* für den Website-Ordner. Sie schreiben vermutlich in die `.htaccess`, und die wird bei jedem Deployment überschrieben. Alle Regeln pflegen wir im Repository.
9. **CDN:** zunächst aus lassen. Für Kunden zwischen Köln und Bonn bringt es wenig. Einschalten nur nach Test: keine Cookies, Formular-Token wird nicht zwischengespeichert, Rate-Limit sieht echte Besucher-IPs.
10. **Auftragsverarbeitung:** Die Datenschutz-Vereinbarung von Hostinger (Data Processing Addendum, hostinger.com/legal/dpa) zum Vertragsdatum als PDF herunterladen und ablegen. Laut Recherche ist Vertragspartner die Hostinger International Ltd., Zypern (beim Herunterladen prüfen). Beim Support schriftlich erfragen, wie lange Server-Logs gespeichert werden. Beides brauchst du für die Datenschutzerklärung.

---

## 7. Deployment

### 7.1 Ablauf

```
Du änderst eine Datei auf github.com (oder wir übertragen Code)
    |
    v
GitHub Actions startet automatisch (Branch main)
    |
    |-> Abhängigkeiten installieren (npm ci)
    |-> Inhalte und Code prüfen (astro check)
    |-> Website bauen (astro build)
    |-> Prüfungen: PHP-Syntax, tote Links, keine Platzhalter auf der Live-Seite
    |
    |-- Fehler? -> Abbruch. Die bisherige Version bleibt online.
    |              GitHub schickt dir eine E-Mail.
    v
Upload per rsync über SSH -> Hostinger, Ordner public_html
    |
    v
Neue Version ist online (nach etwa 2 bis 4 Minuten)
```

Der Workflow liegt in `.github/workflows/deploy.yml`. Er prüft bei jedem Push auf jedem Branch, hochgeladen wird nur von `main` aus und nur, wenn die Variable `DEPLOY_ENABLED` auf `true` steht.

### 7.2 Hauptweg: rsync über SSH (einmalige Einrichtung)

1. In Hostinger SSH aktivieren (Abschnitt 6, Punkt 3).
2. Einen eigenen Schlüssel nur für GitHub erzeugen (am eigenen Rechner, ohne Passphrase):
   ```sh
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ./hostinger_deploy -N ""
   ```
   Den Inhalt von `hostinger_deploy.pub` im hPanel unter *SSH Access -> SSH keys -> Add SSH key* einfügen.
3. Den Server-Fingerabdruck festhalten und den Zugang testen:
   ```sh
   ssh-keyscan -p <PORT> <SERVER-IP> > known_hosts_hostinger
   ssh -i ./hostinger_deploy -p <PORT> <BENUTZER>@<SERVER-IP> 'pwd; command -v rsync'
   ```
4. Secrets und Variablen in GitHub anlegen (7.3). Danach die private Schlüsseldatei lokal löschen oder in einen Passwortmanager legen.

Warum rsync: Es überträgt nur Änderungen, entfernt gelöschte Dateien (`--delete`) und tauscht die Dateien fast gleichzeitig aus. Der Server-Fingerabdruck ist fest hinterlegt (`StrictHostKeyChecking=yes`), damit sich niemand dazwischenschalten kann. Fertige Deploy-Actions schalten diese Prüfung teils ab, deshalb nutzen wir einen eigenen kurzen Schritt.

Wichtig wegen `--delete`: Im Website-Ordner darf nichts liegen, was nur auf dem Server existiert. Formular-Zugangsdaten und Rate-Limit-Daten liegen deshalb außerhalb von `public_html`. Geschützt bleiben `.well-known` (Zertifikate) und PHP-Einstellungsdateien.

### 7.3 GitHub Secrets und Variablen

In GitHub: *Settings -> Secrets and variables -> Actions*. Wir nutzen Repository-Secrets. Die funktionieren im kostenlosen GitHub-Plan sowohl bei öffentlichen als auch bei privaten Repositories (Environment-Secrets dagegen nur bei öffentlichen, belegt in der GitHub-Doku). Secrets sind auch in einem öffentlichen Repository nicht einsehbar.

**Sichtbarkeit des Repositorys:** `Gartenheld/Baumpflege-Webseite` ist derzeit **öffentlich**. Ich empfehle, es auf **privat** zu stellen (*Settings -> General -> Danger Zone -> Change repository visibility*). Grund: Im Repository liegen später auch Inhalte, die (noch) nicht auf der Website stehen, etwa unveröffentlichte Referenzen mit Kundenfotos und Ortsangaben, Bewertungsentwürfe und Platzhalter. Bei einem öffentlichen Repository kann sie jeder auf GitHub lesen.

| Name | Art | Inhalt |
|---|---|---|
| `HOSTINGER_SSH_KEY` | Secret | Inhalt der Datei `hostinger_deploy` (privater Schlüssel) |
| `HOSTINGER_KNOWN_HOSTS` | Secret | Inhalt von `known_hosts_hostinger` |
| `HOSTINGER_SSH_HOST` | Variable | Server-IP aus dem hPanel |
| `HOSTINGER_SSH_PORT` | Variable | SSH-Port aus dem hPanel (ohne Angabe nimmt der Workflow 65002) |
| `HOSTINGER_SSH_USER` | Variable | Benutzer, z. B. `u123456789` |
| `DEPLOY_PATH` | Variable | z. B. `/home/u123456789/domains/NEUE-DOMAIN.de/public_html/` |
| `DEPLOY_ENABLED` | Variable | `true`, sobald hochgeladen werden soll |
| `SITE_URL` | Variable | Adresse der Website, z. B. `https://NEUE-DOMAIN.de` (in der Vorschau die temporäre Adresse) |
| `NOINDEX` | Variable | `true` bis zur Liveschaltung (ohne Angabe gilt `true`), dann `false` |
| `PREVIEW_HTPASSWD_PATH` | Variable | Pfad zur Passwortdatei der Vorschau, außerhalb von `public_html`; leer = kein Passwortschutz |

Optional später: `HOSTINGER_API_TOKEN` (Secret), um nach dem Upload den Server-Cache automatisch zu leeren. Der Token hat weitreichende Konto-Rechte, deshalb nur, wenn der Cache wirklich stört. Sonst im hPanel von Hand leeren.

Kosten: Für private Repositories enthält der kostenlose GitHub-Plan 2.000 Actions-Minuten im Monat (belegt). Ein Durchlauf dauert wenige Minuten, das reicht gut.

### 7.4 Vorschau vor der Liveschaltung

Die Vorschau ist von Anfang an gesperrt, für Menschen per Passwort, für Suchmaschinen per noindex.

- **Solange die Domain offen ist:** Die Website läuft unter der temporären Hostinger-Adresse `*.hostingersite.com`. `SITE_URL` zeigt auf diese Adresse.
- **Sobald die Domain registriert ist:** Website auf der echten Domain anlegen und weiter mit Passwort und noindex betreiben. So entfällt später ein Umzug.
- **Sperre für Suchmaschinen** (automatisch bei `NOINDEX` = `true`): `<meta name="robots" content="noindex, nofollow">` auf jeder Seite, Header `X-Robots-Tag: noindex, nofollow`, `robots.txt` mit `Disallow: /`. Ob Hostinger die temporäre Adresse selbst sperrt, ist nicht belegt, deshalb sperren wir selbst.
- **Passwortschutz (Basic Auth):** Eine Passwortdatei außerhalb von `public_html` anlegen, z. B. `/home/u123456789/domains/NEUE-DOMAIN.de/.htpasswd-vorschau`. Inhalt erzeugen mit `printf 'vorschau:%s\n' "$(openssl passwd -apr1 'DEIN-PASSWORT')"` (lokal oder per SSH), Datei im Dateimanager hochladen, Pfad in `PREVIEW_HTPASSWD_PATH` eintragen. Der Workflow schreibt die Passwortregel dann in die `.htaccess` der Vorschau. Nach dem ersten Upload einmal testen, ob der Browser nach dem Passwort fragt.

**Liveschaltung:** `NOINDEX` auf `false`, `PREVIEW_HTPASSWD_PATH` leeren, `SITE_URL` prüfen, Workflow neu starten (*Actions -> Build und Deployment -> Run workflow*). Ein vergessenes `NOINDEX` ist der häufigste Fehler beim Start, deshalb steht es auf der Checkliste.

**Nach dem Start, bei Bedarf:** eine Subdomain `vorschau.NEUE-DOMAIN.de` mit eigenem Ordner, auf die ein Branch `vorschau` mit Passwort und noindex hochlädt. Dafür erweitern wir den Workflow, falls du größere Änderungen vorher ansehen willst.

### 7.5 Fallback: Git-Funktion im hPanel

Falls SSH nicht verfügbar ist oder die Verbindung aus GitHub blockiert wird:

1. GitHub Actions baut wie gehabt und legt das fertige Ergebnis (`dist/`) auf einem eigenen Branch `deploy` ab (z. B. mit `peaceiris/actions-gh-pages@v4`, dafür braucht der Workflow Schreibrechte `contents: write`).
2. Im hPanel: *Websites -> Manage -> Advanced -> Git*, mit GitHub verbinden, Branch `deploy`, Ordner `public_html`.
3. Automatisches Deployment einschalten. Ab dann holt Hostinger jeden neuen Stand selbst ab. Belegt in der Hostinger-API-Doku: Statische und PHP-Websites werden bei jedem Push auf den Branch sofort deployt, gebaut wird dabei nichts. In GitHub liegen bei diesem Weg keine Server-Zugangsdaten.

Nicht belegt und beim Einrichten zu testen: ob der Zielordner vorher leer sein muss und ob Dateien, die im Branch fehlen, auf dem Server gelöscht werden.

**Notfall:** Upload per FTPS (`SamKirkland/FTP-Deploy-Action` v4.4.0, kann nur FTP/FTPS, kein SFTP) oder ZIP-Upload im Dateimanager.

### 7.6 So änderst du Inhalte selbst (GitHub-Webeditor)

Die ausführliche Anleitung mit Bildschirmschritten kommt in Schritt 4 ins README. Das Prinzip:

```
Datei auf github.com öffnen (z. B. src/inhalte/leistungen/baumfaellung.md)
    -> Stift-Symbol klicken, Text ändern
    -> "Commit changes..." -> "Commit directly to the main branch"
    -> unter "Actions" läuft die Prüfung (gelber Punkt, dann grüner Haken)
    -> nach etwa 2 bis 4 Minuten ist die Änderung online
    -> roter Haken: nichts kaputt, die alte Version bleibt online.
       Die Fehlermeldung nennt Datei und Feld.
```

- **Foto tauschen:** im Zielordner *Add file -> Upload files*, Datei hineinziehen, committen, dann den Dateinamen in der `.md`-Datei eintragen.
- **Neue Referenz:** *Add file -> Create new file*, Name z. B. `src/inhalte/referenzen/2026-10-alfter-linde/index.md` (der Schrägstrich legt den Ordner an), Vorlage einfügen, Fotos in denselben Ordner laden, zum Schluss `veroeffentlichen: true`.
- **Neue Bewertung:** eine Datei in `src/inhalte/bewertungen/` kopieren und anpassen. Durchschnitt, Anzahl und Stand in `betrieb.ts` mit aktualisieren.
- **Fotos:** JPEG oder PNG, **kein HEIC** (die Bildverarbeitung kann iPhone-HEIC nicht lesen, getestet). Am iPhone unter Kamera -> Formate „Maximale Kompatibilität“ wählen. Lange Kante 2000 bis 3000 Pixel, möglichst unter 5 MB, Dateinamen klein, ohne Umlaute und Leerzeichen. Der Browser-Upload bei GitHub erlaubt höchstens 25 MB pro Datei.
- **Mehrere Dateien auf einmal:** im Repository die Taste „.“ drücken, dann öffnet sich der Editor github.dev.

Ein Redaktionssystem (CMS) brauchen wir zum Start nicht. Wenn dir die GitHub-Oberfläche nach einigen Wochen zu sperrig ist, kann Sveltia CMS dazukommen (Anmeldung per Zugriffstoken, kein eigener Anmeldeserver nötig).

---

## 8. Kontaktformular

### 8.1 Aufbau

- **Formular** nur auf `/kontakt/`. Startseite und Leistungsseiten verlinken mit „Anfrage mit Fotos senden“ dorthin, auf Wunsch mit vorausgewählter Leistung.
- **Felder:** Name (Pflicht), E-Mail, Telefon, Ort oder PLZ des Grundstücks, Anliegen (Leistung, optional), Nachricht (Pflicht), Fotos, Rückrufwunsch mit Zeitfenster (vormittags, nachmittags, egal). Pflicht ist E-Mail oder Telefon, bei Rückrufwunsch das Telefon. Am Formular stehen Erreichbarkeit und Antwortzeit aus `betrieb.ts` und ein Foto-Tipp (Gesamtansicht, Stamm, Zufahrt, möglichst ohne Personen).
- **Datenschutzhinweis** mit Link über dem Senden-Knopf, keine Einwilligungs-Checkbox. Den Text bestimmt der Generator.
- **Empfänger:** `public/anfrage/senden.php` mit Hilfsdatei `lib/anfrage.php` und PHPMailer 7.1.1 (drei Dateien, ohne Composer, Lizenz LGPL-2.1). Den Ordner `lib/` sperrt eine eigene `.htaccess`.
- **Zugangsdaten** in `anfrage-config.php` außerhalb von `public_html`, z. B. `/home/u123456789/domains/NEUE-DOMAIN.de/anfrage-config.php`: SMTP-Server, Postfach, Passwort, Empfänger, ein zufälliger Geheimschlüssel. Die Datei steht in `.gitignore` und kommt nie ins Repository. Daneben der Ordner `anfrage-daten/` für Rate-Limit und ein Fehlerprotokoll ohne Inhalte. Ob PHP dort lesen darf (`open_basedir`), testen wir einmal.
- **Nach dem Absenden:** Weiterleitung auf `/kontakt/danke/` mit nächsten Schritten, Antwortzeit, Telefon und WhatsApp. Keine automatische Eingangsbestätigung an Kunden: Jeder könnte eine fremde Adresse eintragen und das Formular als Spam-Schleuder missbrauchen, das schadet dem Ruf deines Postfachs. Deine persönliche Antwort ist die Bestätigung.

### 8.2 Spamschutz ohne Fremddienst

Prüfreihenfolge im Skript:

| Prüfung | Reaktion |
|---|---|
| Kein POST oder fremde Herkunft (`Origin`) | zurück zum Formular bzw. Fehlerseite |
| **Honeypot:** verstecktes Feld „Bitte dieses Feld leer lassen“, für Menschen unsichtbar, Bots füllen es aus | still verwerfen, Danke-Seite |
| **Zeitsperre:** signierter Zeitstempel (HMAC), Absenden frühestens nach 3 Sekunden, höchstens 24 Stunden | zu schnell: still verwerfen; abgelaufen: „Seite neu laden“ |
| Pflichtfelder, Formate, Längen | Fehlerseite mit Liste |
| Mehr als 2 Links oder Link im Namen | Fehlerseite mit Hinweis auf Telefon und WhatsApp |
| Fotos: Anzahl, Größe, echter Dateityp | Fehlerseite |
| **Rate-Limit:** 3 Anfragen in 10 Minuten und 10 am Tag je Anschluss, 50 am Tag insgesamt | Fehlerseite |

Jede Fehlerseite nennt Telefon und WhatsApp, damit ein fälschlich abgewiesener Kunde einen Ausweg hat. Das Rate-Limit speichert keine IP-Adresse, sondern einen täglich wechselnden Hash (bei IPv6 nur das Netzpräfix), gelöscht nach 24 Stunden. Kommt trotzdem Spam durch, ist die nächste Stufe ALTCHA (selbst gehostet, Open Source, braucht aber JavaScript).

**Zeitstempel auf einer statischen Seite:** Er muss bei jedem Aufruf neu entstehen. Dafür macht ein kleines Skript nach dem Build aus der Kontaktseite eine `index.php`, die nur den Zeitstempel einsetzt. Die `index.html` dort entfällt, sonst hätte sie laut `DirectoryIndex` Vorrang. Die Seite sendet dazu „nicht zwischenspeichern“-Header, damit kein Server-Cache den Zeitstempel einfriert. Nach der Liveschaltung prüfen wir das mit zwei Aufrufen hintereinander.

### 8.3 Foto-Upload

- `accept="image/*"`, mehrere Dateien, Kamera oder Galerie wählbar.
- Grenzen: **höchstens 8 Fotos, je 10 MB, zusammen 15 MB.** Als Mailanhang wird daraus gut 20 MB, das bleibt unter der üblichen Grenze von 25 MB für Anhänge (für Hostinger-Postfächer laut Recherche, Bitte prüfen mit einer Testmail).
- Erlaubt sind JPEG, PNG, WebP, HEIC und HEIF (anders als bei Fotos für die Website in 7.6, weil diese Fotos nur als Mailanhang weitergehen). Der Server prüft den echten Dateityp, nicht die Endung (getestet: eine als `.jpg` getarnte PHP-Datei wird abgewiesen).
- Mit JavaScript werden große Fotos schon im Browser auf höchstens 2560 Pixel verkleinert. Dabei fallen auch GPS-Daten und andere Metadaten weg. Ohne JavaScript gehen die Originale raus.
- Fotos werden **nicht auf dem Server gespeichert**, sie gehen nur als Anhang an dein Postfach. Anhänge heißen `foto-1.jpg` usw., der Dateiname des Kunden wird nie verwendet.

### 8.4 Versand per SMTP

- Versand über ein Hostinger-Postfach der neuen Domain per SMTP (`smtp.hostinger.com` existiert laut DNS-Abfrage; Port 465 mit SSL oder 587 mit STARTTLS laut Recherche, Werte im hPanel unter E-Mail ablesen). Nicht über PHP `mail()`: Das ist laut Hostinger stärker begrenzt und landet eher im Spam.
- **Absender ist immer dein eigenes Postfach**, die Adresse des Kunden steht nur in „Antworten an“. Ein Klick auf „Antworten“ schreibt also direkt dem Kunden.
- **Nie** mit einer Adresse `@gartenheldservice.com` versenden: Die alte Domain weist fremd versendete Mails ab (DMARC `p=reject`, eigene DNS-Abfrage).
- Mail nur als Text, UTF-8. Betreff z. B. „Anfrage über die Website: Baumfällung, Bornheim (Rückruf)“, damit du einen Rückrufwunsch schon in der Handy-Benachrichtigung siehst.
- DNS der neuen Domain: MX, SPF, DKIM und DMARC so eintragen, wie das hPanel sie unter E-Mail anzeigt (bei Hostinger-Nameservern meist automatisch). DMARC zuerst mit `p=none`, nach einigen Wochen ohne Auffälligkeiten strenger.

### 8.5 Keine Cookies, auch ohne JavaScript

- Das Skript startet keine Session und setzt kein Cookie (getestet: kein `Set-Cookie` auf `/kontakt/` und nach dem Absenden).
- **Ohne JavaScript** funktioniert alles: normaler Formularversand, Weiterleitung auf die Danke-Seite, bei Fehlern eine Fehlerseite im Design der Website. HTML-Prüfungen (`required`, `type="email"`) fangen die meisten Fehler vorher ab.
- **Mit JavaScript** zusätzlich: Fotos verkleinern, Senden-Knopf gegen Doppelklick, Telefon wird Pflichtfeld bei Rückrufwunsch.
- Barrierearm: sichtbare Beschriftung an jedem Feld, Fehlertexte am Feld, Autovervollständigung für Name, E-Mail, Telefon und PLZ.

### 8.6 Tests vor der Liveschaltung

1. Echte Anfragen vom iPhone, von einem Android-Handy und vom Rechner mit abgeschaltetem JavaScript.
2. In der eingegangenen Mail prüfen: SPF, DKIM und DMARC „pass“. Zusätzlich eine Testmail an ein Gmail-Konto, dort „Original anzeigen“.
3. „Antworten“ landet beim Kunden.
4. Zu große Fotos ergeben eine verständliche Meldung.
5. In den Browser-Entwicklertools sind keine Cookies gesetzt.
6. **Nach jedem Deployment eine kurze Testanfrage.** Das steht auch im README.

---

## 9. Datenschutz und Sicherheit

### 9.1 Kein Cookie-Banner: Begründung

Keine Rechtsberatung, sondern unsere Einschätzung nach dem Gesetzeswortlaut:

- Nach **§ 25 TDDDG** (bis Mai 2024 TTDSG) braucht eine Einwilligung, wer Informationen auf dem Gerät des Besuchers speichert oder dort ausliest. Ausgenommen ist, was für den gewünschten Dienst unbedingt erforderlich ist.
- Die Website setzt **keine Cookies**, nutzt keinen Browser-Speicher (localStorage o. ä.), **kein Tracking**, keine Analyse-Tools und **keine eingebetteten Fremdinhalte**. Damit gibt es nichts, wofür eine Einwilligung nötig wäre, also auch kein Banner.
- Die Informationspflichten nach DSGVO erfüllt die **Datenschutzerklärung**. Die brauchst du trotzdem.
- Das Impressum richtet sich nach **§ 5 DDG** (früher § 5 TMG).
- **Bedingung:** Das bleibt nur so, solange niemand später ein Analyse-Tool, eine eingebettete Karte, ein YouTube- oder Instagram-Video oder ein Bewertungs-Widget einbaut. Dieser Hinweis kommt ins README.

Nach der Liveschaltung prüfen wir in den Browser-Entwicklertools, dass auch Hosting oder Cache keine Cookies setzen.

### 9.2 Keine externen Ressourcen

| Bereich | Umsetzung |
|---|---|
| Schriften | als Datei auf dem eigenen Server, kein Google-Fonts-Dienst |
| Skripte und Styles | nur vom eigenen Server; die Content-Security-Policy (`default-src 'self'`) erzwingt das technisch |
| Karte Einsatzgebiet | eigene SVG-Karte mit Links auf die Ortsseiten, keine Google-Maps-Einbettung. Darunter ein normaler Link „Route in Google Maps öffnen“, Daten fließen erst beim Klick. Bei Kartengrundlage aus OpenStreetMap ist der Vermerk „© OpenStreetMap-Mitwirkende“ Pflicht. |
| Videos | selbst gehostet, kein YouTube, kein Instagram |
| Google-Bewertungen | statischer Text, eigene Stern-Grafik, normaler Link zum Profil, kein Widget |
| Social Media | nur Links mit eigenen Icons im Footer, keine Teilen-Knöpfe. Ein Profil ohne Link in `betrieb.ts` erscheint nicht. |
| WhatsApp | nur Link `https://wa.me/49...`, kein Chat-Widget |
| Telefon, E-Mail | `tel:`- und `mailto:`-Links |

### 9.3 Sicherheits-Header

Schon in `public/.htaccess`: `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy` und ein CSP-Header für `frame-ancestors`, `base-uri`, `form-action`, `object-src`. Die übrige Content-Security-Policy erzeugt Astro als `<meta>` mit Prüfsummen für jedes Skript und jeden Style. Die vollständige CSP senden wir bewusst nicht zusätzlich als Header, sonst würden die Inline-Skripte blockiert. `frame-ancestors` wirkt nur als Header, deshalb steht es dort (belegt in der MDN-Doku).

Zur Liveschaltung kommen dazu:

- `Strict-Transport-Security` (HSTS): erst mit einem Tag Laufzeit testen, nach einer Woche auf ein Jahr. Ohne `preload`.
- `Header unset X-Powered-By` (verrät die PHP-Version) und `Cross-Origin-Opener-Policy: same-origin`.
- `public/anfrage/.htaccess`: nur `senden.php` ist erreichbar. Test: `curl -I https://NEUE-DOMAIN.de/anfrage/lib/PHPMailer/PHPMailer.php` muss 403 liefern.

Hostinger nutzt nach unserer Recherche den Webserver LiteSpeed, der Apache-`.htaccess` versteht. Jede Regel testen wir nach dem ersten Upload mit `curl -I`.

### 9.4 Punkte für den Datenschutz-Generator

Auswählen bzw. beschreiben:

1. Verantwortlicher: Heinrich Happe, Anschrift und Kontakt wie im Impressum.
2. Hosting: Hostinger International Ltd. (laut Recherche, Zypern), Rechenzentrum in der EU, Vereinbarung zur Auftragsverarbeitung abgeschlossen.
3. Server-Logfiles (IP, Zeit, Adresse, Browser): Speicherdauer laut Auskunft von Hostinger.
4. SSL/TLS-Verschlüsselung.
5. Kontaktformular mit Datei-Upload: Felder Name, E-Mail, Telefon, Ort, Nachricht, Fotos, Rückrufwunsch. Versand per E-Mail, keine Speicherung auf dem Webserver. Fotos können Personen, Grundstücke oder Kennzeichen zeigen.
6. Spamschutz: Honeypot, Zeitprüfung, IP-Adresse nur als täglich wechselnder Hash (bei IPv6 gekürzt), nach 24 Stunden gelöscht. Kein reCAPTCHA, kein externer Dienst.
7. Kontakt per E-Mail und Telefon, Postfach bei Hostinger (oder deinem Mailanbieter).
8. WhatsApp: Kontakt über den Messenger von Meta, Übermittlung in Drittländer möglich. Auf der Website nur ein Link, bis zum Klick fließen keine Daten.
9. Links zu Social-Media-Profilen ohne Plugins. Falls du eigene Facebook- oder Instagram-Seiten betreibst: das Modul „Präsenz in sozialen Medien“.
10. Google-Bewertungen als statischer Text mit Link, keine Einbindung.
11. Lokal eingebundene Schriften und selbst gehostete Videos (optional erwähnen).
12. Ausdrücklich: keine Cookies, kein Tracking, keine Analyse-Tools.
13. Speicherdauer von Anfragen, die nicht zum Auftrag werden. Für Angebote und Geschäftsbriefe gelten gesetzliche Aufbewahrungsfristen.
14. Betroffenenrechte, Beschwerderecht bei der Landesbeauftragten für Datenschutz NRW (LDI NRW).

Nicht auswählen: Google Analytics, Google Fonts, Google Maps, YouTube, reCAPTCHA, Cookie-Consent-Tool, Pixel, Newsletter. Google Search Console braucht keinen Eintrag, sie läuft ohne Code auf der Website.

### 9.5 Hinweis zu Bewertungen

Wer Kundenbewertungen zeigt, muss nach **§ 5b Abs. 3 UWG** angeben, ob und wie er sicherstellt, dass sie von echten Kunden stammen. Fehlt der Hinweis, kann das als irreführend gelten. Vorschlag für den Text unter den Bewertungen: „Auszüge aus unserem Google-Unternehmensprofil, Stand MM/JJJJ. Wir prüfen nicht gesondert, ob die Verfasser Kunden waren.“ Die Durchschnittsbewertung muss dem echten Google-Wert zum genannten Stand entsprechen. Keine Rechtsberatung, im Zweifel fachkundig prüfen lassen.

### 9.6 Impressum und Datenschutzseite

- **Impressum** (`/impressum/`, nach § 5 DDG): Die Angaben kommen aus `betrieb.ts`: dein voller Name mit Betriebsname, Anschrift, Telefon, E-Mail und USt-IdNr. Bis zur Liveschaltung sind Kontakt und USt-IdNr. Platzhalter. Eine USt-IdNr. (oder Wirtschafts-Identifikationsnummer) steht nur drin, wenn du eine hast, ein Register nur, wenn der Betrieb eingetragen ist. Einen Hinweis zur Verbraucherschlichtung (§ 36 VSBG) brauchen Betriebe mit höchstens 10 Beschäftigten nach unserem Kenntnisstand nicht (Bitte prüfen).
- **Datenschutz** (`/datenschutz/`): Bis der Generator-Text da ist, steht in `src/inhalte/seiten/datenschutz.md` ein Platzhalter. Den Text aus dem Generator (Punkte in 9.4) fügen wir dort ein. Solange der Platzhalter drinsteht, bricht der Live-Build ab.
- Beide Seiten sind auf jeder Seite im Footer verlinkt.

---

## 10. Performance und Barrierearmut

**Grundsätze**

- **Mobile first:** Gestaltet und gebaut wird zuerst für das Handy, größere Bildschirme ergänzen das Layout. Alles funktioniert ab 320 Pixel Breite ohne seitliches Scrollen.
- **Semantisches HTML:** `header`, `nav`, `main`, `footer`, genau eine H1 je Seite, Überschriften ohne Sprünge, echte Listen, Links für Wege und Buttons für Aktionen, dazu ein Link „Zum Inhalt springen“.
- **Barrierearmut:** Ziel ist WCAG 2.2, Stufe AA: Textkontrast mindestens 4,5:1, sichtbarer Fokus, alles per Tastatur bedienbar, Klickflächen mindestens 24 x 24 Pixel (angestrebt 44 x 44).
- **Handy-Leiste** mit Anrufen und WhatsApp: fest am unteren Rand, nur HTML und CSS, ohne JavaScript. Sie ist von Anfang an da und hat am Seitenende eigenen Platz, damit sie nichts verdeckt und nichts springt.

### 10.1 Zielwerte

| Ebene | Ziel |
|---|---|
| Echte Nutzerdaten (75. Perzentil, Handy) | LCP höchstens 2,0 s, INP höchstens 100 ms, CLS höchstens 0,05. Googles Grenze für „gut“ liegt bei 2,5 s, 200 ms und 0,1. |
| Labortest (Lighthouse, Handy) | Performance mindestens 95, Barrierefreiheit 100, Best Practices mindestens 95, SEO 100 |
| Datenmenge je Seite (Erstaufruf Handy, ohne Video) | HTML höchstens 30 KB, CSS höchstens 20 KB, JavaScript 0 KB, nur Startseite (Video-Steuerung) und Kontakt (Fotos verkleinern) je höchstens 3 KB, Schriften höchstens 100 KB, Hero-Bild höchstens 120 KB, gesamt höchstens 400 KB |

Eine kleine lokale Website hat oft zu wenige Besucher für Googles Felddaten. Dann sind die Laborwerte der Maßstab.

### 10.2 Bilder

- Ausgabe als **AVIF mit WebP als Rückfall**, in mehreren Breiten, mit Breite und Höhe im HTML. Das Hero-Foto lädt mit Vorrang, alle anderen erst beim Scrollen.
- **Alt-Text ist Pflicht** (mindestens 10 Zeichen, sonst bricht der Build ab). Alt-Texte beschreiben, was zu sehen ist, z. B. „Rückschnitt einer Linde in einem Garten in Alfter“, ohne Keyword-Listen.
- Nur **echte eigene Fotos**, keine Stockfotos.

### 10.3 Schrift

Lokal eingebunden über die Fonts-Funktion von Astro: Datei im Repository, Preload, `font-display: swap` und automatisch angepasste Ersatzschrift gegen Layoutsprünge (getestet). Alle Kandidaten stehen unter der freien Lizenz OFL 1.1 und enthalten ä, ö, ü, ß, deutsche Anführungszeichen und das Eurozeichen. Die Auswahl treffen wir in Schritt 2 zusammen mit dem Logo.

| Paarung | Überschriften / Fließtext | Größe | Charakter |
|---|---|---|---|
| A | Source Serif 4 / Source Sans 3 | ca. 80 KB | ruhig, klassisch, eine Designfamilie, sehr gut lesbar |
| B | Fraunces (ruhige Variante) / Figtree | ca. 55 KB | warm, natürlich, eigenständig |
| C | Instrument Sans für alles | 30 bis 56 KB | modern, reduziert; schmale Schnitte helfen bei Logo und Fahrzeugbeschriftung |

Nur aufrechte Schnitte vorladen, Kursive im Design vermeiden.

### 10.4 Video

- **Startseite:** Das Hero-Foto ist immer das zuerst sichtbare Element (wichtig für LCP). Das Video liegt darüber und startet nur auf großen Bildschirmen, wenn der Besucher keine reduzierten Bewegungen eingestellt hat und keinen Datensparmodus nutzt. Auf dem Handy bleibt es beim Foto, das spart 1 bis 2,5 MB pro Aufruf.
- **Pause-Knopf** ist Pflicht: Bewegte Inhalte, die automatisch starten und länger als 5 Sekunden laufen, müssen sich anhalten lassen (WCAG 2.2.2, Stufe A).
- `muted playsinline loop`, keine Tonspur in der Datei. Formate: MP4 (H.264) als Pflicht, zusätzlich optional AV1 in WebM. Hero-Schleife 6 bis 10 Sekunden, 1280 x 720, höchstens 2,5 MB.
- **Clips (2 bis 3)** auf Unterseiten: 10 bis 20 Sekunden, 720p, je höchstens 3 MB, mit Bedienelementen, ohne Autoplay, Laden erst beim Klick.

### 10.5 Automatische Prüfungen in CI

Blockierend (im Deployment, schnell und eindeutig):

- `astro check`: Code und Inhalts-Pflichtfelder
- Build
- Linkprüfung: tote interne Links stoppen das Deployment
- Platzhalter-Wächter: Live-Build bricht ab, wenn `PLATZHALTER` vorkommt
- `php -l`: Syntax der PHP-Dateien
- Build-Cache für Bilder, damit Läufe schnell bleiben
- Längenprüfung für Title und Description, doppelte Titles

Nicht blockierend (eigener Workflow `qualitaet.yml`, bei jeder Änderung und wöchentlich):

- **Lighthouse CI** für 5 typische Seiten (Startseite, eine Leistung, ein Ort, Referenzen, Kontakt), je 3 Läufe
- **pa11y mit axe** über alle Seiten der Sitemap (Barriere-Test)

Ist dieser Workflow rot, bekommst du eine Mail, das Deployment läuft trotzdem. Messwerte auf GitHub schwanken, deshalb hier nur Warnungen.

Automatische Tests finden nur einen Teil der Barrieren. Vor der Liveschaltung prüfen wir zusätzlich von Hand: Bedienung nur mit Tastatur, sichtbarer Fokus, Zoom 200 und 400 Prozent, Screenreader (VoiceOver oder NVDA), Kontraste der gewählten Farben.

---

## 11. SEO-Technik

### 11.1 Strukturierte Daten (JSON-LD)

Ein Datenblock pro Seite, erzeugt aus `betrieb.ts`, damit Name, Anschrift und Telefon überall gleich sind.

| Seite | Typen |
|---|---|
| Alle Seiten | `HomeAndConstructionBusiness` (der Betrieb, mit Name, Slogan, Logo, Foto, Telefon, E-Mail, Anschrift, Koordinaten, Erreichbarkeit als `contactPoint`, die 9 Orte als `areaServed`, Leistungen als `knowsAbout`, Profil-Links als `sameAs`) und `WebSite` |
| Leistungsseiten | `Service` (Leistung, Beschreibung, Anbieter, Einsatzgebiet) und `BreadcrumbList` |
| Ortsseiten | `Service` „Baumpflege und Baumfällung in {Ort}“ mit nur diesem Ort und `BreadcrumbList` |
| FAQ | `FAQPage` und `BreadcrumbList` |
| Andere Unterseiten | `BreadcrumbList` |

Warum `HomeAndConstructionBusiness`: Der Typ ist ein Untertyp von `LocalBusiness` (geprüft in schema.org 30.1). Einen eigenen Typ für Baumpflege oder Landschaftsbau gibt es bei schema.org nicht (geprüft in Version 30.1). `ProfessionalService` ist dort als veraltet markiert. Wichtiger für die lokale Sichtbarkeit ist ohnehin dein Google-Unternehmensprofil.

**Bewusst weggelassen:**

| Was | Warum |
|---|---|
| Bewertungs-Sterne (`AggregateRating`, `Review`) | Google zeigt für Bewertungen, die ein Betrieb auf der eigenen Website über sich selbst auszeichnet, seit 2019 keine Sterne. Bewertungen von anderen Plattformen (hier Google) sollen ohnehin nicht übernommen und ausgezeichnet werden. Die Sterne in der Google-Suche kommen aus dem Unternehmensprofil. (Stand unseres Wissens, Bitte prüfen) |
| `priceRange` | Briefing: keine Preise |
| Öffnungszeiten als Ladenöffnung | Es gibt keinen Laden. Die Erreichbarkeit steht als `contactPoint`. |
| `FAQPage` auf Leistungsseiten | Dieselbe Frage soll nicht mehrfach ausgezeichnet werden. Nur auf `/faq/`. Google zeigt aufklappbare FAQ in der Suche seit 2023 nur noch für Behörden- und Gesundheitsseiten (Stand unseres Wissens). Das Markup schadet nicht, hat aber niedrige Priorität. |
| Seilklettertechnik | solange ausgeblendet, kein `Service` |

`Service` und `BreadcrumbList` erzeugen keine besonderen Suchtreffer, sie helfen Suchmaschinen beim Einordnen. Mehr versprechen wir davon nicht.

### 11.2 Sitemap und robots.txt

- **Sitemap:** automatisch aus allen gebauten Seiten, als `sitemap-index.xml` mit `sitemap-0.xml`. `/sitemap.xml` leitet per 301 dorthin, damit auch die übliche Adresse funktioniert. Nicht enthalten: 404, Danke-Seite, Fehlervorlage, ausgeblendete Seilklettertechnik. Keine Angaben zu Priorität oder Änderungshäufigkeit (ignoriert Google).
- **robots.txt (live):**
  ```
  User-agent: *
  Disallow: /anfrage/

  Sitemap: https://NEUE-DOMAIN.de/sitemap-index.xml
  ```
  Die Danke-Seite wird **nicht** per robots.txt gesperrt, sondern trägt `noindex`. Google kann ein noindex hinter einer Sperre nicht lesen.
- **robots.txt (Vorschau):** `Disallow: /`.

### 11.3 Canonical, Weiterleitungen, Open Graph

- **Canonical** auf jeder Seite: absolute Adresse, `https://`, ohne www, mit „/“ am Ende. Ist im Grundlayout schon so umgesetzt.
- **Eine Schreibweise:** `http://` und `www.` leiten per 301 auf `https://NEUE-DOMAIN.de/...`. Nach der Liveschaltung zählen wir mit `curl -I`, dass es höchstens zwei Sprünge sind. Sind es mehr, regeln wir alles in der `.htaccess`.
- **Open Graph** für die Vorschau beim Teilen per WhatsApp: `og:title`, `og:description`, `og:url`, `og:image` (JPEG 1200 x 630, möglichst unter 300 KB, mit Alt-Text), dazu `twitter:card` „summary_large_image“. Je Seite ein eigenes Bild, sonst ein Standardbild.
- `<html lang="de">` ist gesetzt, `hreflang` ist nicht nötig.

### 11.4 Title und Description

Faustregel aus der Praxis (keine feste Grenze von Google, gekürzt wird nach Breite): **Title 50 bis 60 Zeichen, Description 120 bis 155 Zeichen.** Leistung und Ort vorne, Trennzeichen „|“, keine Keyword-Ketten. Keine Aussagen, die Qualifikationen oder Fähigkeiten über das Briefing hinaus behaupten. Ein Build-Check meldet doppelte Titles und Längen außerhalb des Rahmens. Lange Leistungsnamen bekommen eine kürzere Fassung, z. B. „Heckenschnitt und Landschaftspflege in Bornheim | Happe“ (55 Zeichen).

| Seitentyp | Muster | Beispiel | Zeichen |
|---|---|---|---|
| Startseite | Leistung + Region \| Name | Baumpflege und Baumfällung zwischen Köln und Bonn \| Happe | 57 |
| Leistung | {Leistung} in Bornheim, Köln und Bonn \| Baumpflege Happe | Baumfällung in Bornheim, Köln und Bonn \| Baumpflege Happe | 57 |
| Leistung (langer Name) | {Leistung} in Bornheim, Köln und Bonn \| Happe | Wurzelstockentfernung in Bornheim, Köln und Bonn \| Happe | 56 |
| Ortsseite | Baumpflege und Baumfällung in {Ort} \| Baumpflege Happe | Baumpflege und Baumfällung in Bornheim \| Baumpflege Happe | 57 |
| Ortsseite | wie oben | Baumpflege und Baumfällung in Köln \| Baumpflege Happe | 53 |
| Einsatzgebiet | | Einsatzgebiet: Baumpflege zwischen Köln und Bonn \| Happe | 56 |
| Gewerbe | | Baumpflege für Hausverwaltungen und Gewerbe \| Happe | 51 |
| Referenzen | | Referenzen: Baumpflege und Baumfällung in der Region \| Happe | 60 |
| Über uns | | Über uns: Arbeitsweise und Qualifikation \| Baumpflege Happe | 59 |
| FAQ | | Fragen zu Fällgenehmigung, Schonzeit und Kosten \| Happe | 55 |
| Kontakt | | Anfrage mit Fotos und Kontakt \| Baumpflege Happe, Bornheim | 58 |

Descriptions nach dem Muster Leistung + Ort + Nutzen + Aufforderung:

| Seite | Beispiel | Zeichen |
|---|---|---|
| Startseite | Baumpflege und Baumfällung in Bornheim, Köln, Bonn und Umgebung: fachgerecht geplant, sauber ausgeführt, Aufräumen inklusive. Anfrage mit Fotos senden. | 151 |
| Leistung Baumfällung | Baumfällung in Bornheim, Köln und Bonn: sorgfältig geplant, sauber ausgeführt. Schnittgut wird vor Ort gehäckselt und abgefahren. Anfrage mit Fotos senden. | 155 |
| Ortsseite Bornheim | Baumpflege und Baumfällung in Bornheim und den Ortsteilen: Hinweise zur Fällgenehmigung, schriftliches Angebot, kurze Wege. Anfrage mit Fotos senden. | 149 |
| Ortsseite Köln | Baumpflege und Baumfällung in Köln: Hinweise zu Baumschutz und Fällgenehmigung, Anfahrt aus Bornheim, schriftliches Angebot. Anfrage mit Fotos senden. | 150 |

Die H1 nennt ebenfalls Leistung und Ort. Ortsseiten bekommen jeweils eigenen Text (Hinweis zur örtlichen Baumschutzsatzung mit Link zur Stadt, Anfahrt, später Referenzen aus dem Ort), keine Kopien mit ausgetauschtem Ortsnamen. Ob ein Ort eine Baumschutzsatzung hat, prüfen wir je Stadt und tragen das Prüfdatum ein.

---

## 12. Google Search Console einrichten

Zeitpunkt: Die **Bestätigung** geht, sobald die neue Domain registriert ist, auch vor der Liveschaltung. **Sitemap und Indexierung** erst nach der Liveschaltung mit `NOINDEX` = `false`. Nimm das Google-Konto des Betriebs, mit dem du auch das Unternehmensprofil verwaltest. Menüpfade nach unserem Wissensstand, Google ändert die Oberfläche gelegentlich.

1. **Property anlegen:** search.google.com/search-console öffnen, *Property hinzufügen*, links **Domain** wählen, `NEUE-DOMAIN.de` eingeben (ohne https und www). Eine Domain-Property umfasst alle Schreibweisen (http, https, mit und ohne www).
2. **Bestätigungscode kopieren:** Google zeigt einen TXT-Eintrag `google-site-verification=...`.
3. **TXT-Eintrag setzen** beim DNS-Anbieter, auf den die Nameserver der Domain zeigen:
   - Domain bei Hostinger mit Hostinger-Nameservern: im hPanel unter *Domains -> Domain verwalten -> DNS / Nameservers* einen Eintrag anlegen: Typ `TXT`, Name `@`, Wert aus der Search Console, TTL Standard.
   - Welches Nameserver-Paar gilt, zeigt das hPanel je Domain an (z. B. `ns1/ns2.dns-parking.com` oder `solar/lunar.dns-parking.com`). Nicht raten.
   - Liegt die Domain woanders, setzt du den Eintrag dort.
4. **Bestätigen** klicken. Oft klappt das nach Minuten, es kann bis zu einem Tag dauern. **Den TXT-Eintrag dauerhaft stehen lassen**, sonst verfällt die Bestätigung. Bei einem späteren Nameserver-Wechsel den Eintrag vorher übertragen.
5. **Nutzer hinzufügen** (optional): *Einstellungen -> Nutzer und Berechtigungen*. Inhaber bleibst du.
6. **Nach der Liveschaltung: Sitemap einreichen.** *Sitemaps*, `sitemap-index.xml` eingeben, *Senden*. Status „Erfolgreich“, die Zahl der Seiten muss passen.
7. **URL-Prüfung:** Startseiten-Adresse oben eingeben, *Live-URL testen*. Prüfen: „Indexierung zulässig“, kein noindex, richtiges Canonical, strukturierte Daten erkannt. Dann *Indexierung beantragen*, für Startseite und die wichtigsten Leistungsseiten. Den Rest findet Google über die Sitemap.
8. **Nach einigen Tagen: Bericht „Seiten“** unter Indexierung. Gut: Leistungs-, Orts- und Kernseiten unter „Indexiert“, Danke-Seite unter „Durch noindex ausgeschlossen“. Alarmzeichen: viele Seiten mit noindex (dann ist `NOINDEX` noch aktiv), „Duplikat“ bei Ortsseiten (Texte zu ähnlich), „Gefunden, zurzeit nicht indexiert“ bei Kernseiten.
9. **Optional Bing:** bing.com/webmasters, *Aus Google Search Console importieren*. Bing übernimmt Bestätigung und Sitemap.

Die alte Domain und die Adressänderung: siehe Abschnitt 13.

---

## 13. Alte Domain gartenheldservice.com

### 13.1 Befund

Eigene DNS-Abfrage vom 01.10.2026:

| Was | Wo |
|---|---|
| Nameserver und DNS-Zone | **STRATO** (`docks15.rzone.de`, `shades07.rzone.de`) |
| E-Mail (MX, DKIM, Autoconfig) | **STRATO** |
| DMARC | `p=reject`: Mails, die andere im Namen der Domain senden, werden abgewiesen |
| Webserver (mit und ohne www, verschiedene IPs, jeweils mit IPv6) | Netz von IONOS SE (gehört wie STRATO zu United Internet) |
| Google-Bestätigung | TXT `google-site-verification=...` vorhanden: Eine Search-Console-Property gibt es also vermutlich schon |
| TTL | 150 Sekunden: DNS-Änderungen greifen nach wenigen Minuten |

Du schreibst, die Domain liegt bei IONOS. Laut DNS liegen Nameserver und E-Mail bei STRATO, nur die Webserver-Adressen gehören zum Netz von IONOS. Bei welchem Anbieter die Domain registriert und die Website gebucht ist, lässt sich von außen nicht sicher sagen, weil beide zur selben Unternehmensgruppe gehören. Bitte in beiden Kundenkonten nachsehen (oder unter lookup.icann.org), bevor wir etwas umstellen. An der Empfehlung ändert das nichts, nur an den Menüpfaden.

Im Google-Index gefunden: `/`, `/kontakt/`, `/preise/`, `/dienstleistungen/`. Impressum und Datenschutz gibt es laut Footer, ihre Adressen sind nicht belegt.

### 13.2 Varianten

Die eingebaute Domain-Weiterleitung bei IONOS oder STRATO scheidet aus: Sie kennt nach unserer Recherche nur ein Ziel für die ganze Domain statt einer Zuordnung je Seite, und HTTPS funktioniert damit nur unter Bedingungen, die hier nicht erfüllt sind (Bitte prüfen, nicht an der Quelle belegbar). Wir brauchen einen Server mit gültigem Zertifikat für die alte Domain und einer `.htaccess` mit Einzelregeln.

| | A: alter Webspace bleibt | **B: Adresseinträge auf Hostinger** | C: Domain-Umzug zu Hostinger |
|---|---|---|---|
| Was passiert | Die alte Website wird gesichert und gelöscht, auf dem alten Webspace liegt nur noch die `.htaccess` | Beim DNS-Anbieter zeigen nur die A-Records von `@` und `www` auf Hostinger. Dort ist die alte Domain eine kleine eigene Website mit der `.htaccess`. | Domain wechselt mit Auth-Code zu Hostinger, DNS und Mail müssen vorher umziehen |
| Weiterleitung je Seite | ja | **ja** | ja |
| HTTPS | ja (bestehendes Zertifikat) | **ja (Hostinger-Zertifikat, nach Umstellung prüfen)** | ja |
| Risiko für E-Mail | keins | **keins (MX bleibt unverändert)** | hoch, Mailumzug nötig |
| Laufende Kosten | Hosting bei IONOS plus Domain | **nur Domain- und Mailvertrag beim bisherigen Anbieter** | Domain bei Hostinger plus Mail |
| Aufwand | mittel | **gering** | hoch |
| Alles bei einem Hoster | nein | **ja (Web)** | ja |

**Empfehlung: Variante B.** Ein Hoster, die Regeln liegen versioniert im Repository, das Zertifikat stellt Hostinger aus, die E-Mail bleibt unberührt, der alte Webspace ist kündbar. Ein Domain-Umzug (C) bringt für die Weiterleitungen nichts und ist höchstens später sinnvoll, wenn auf der alten Domain keine E-Mail mehr läuft. Variante A ist der Ausweg, falls du an der DNS nichts ändern willst.

### 13.3 Schritt für Schritt (Variante B)

**Vorbereitung, 1 bis 2 Wochen vor dem Start**

1. Im STRATO- und im IONOS-Kundenkonto klären: Wo liegt die Domain, welches Produkt hostet die alte Website, welche Postfächer gibt es, Laufzeiten und Kündigungsfristen.
2. Die DNS-Einträge der alten Domain als Screenshot sichern (A, AAAA, MX, TXT, `_dmarc`, DKIM, SRV, CNAME, alle Subdomains, besonders `www`).
3. Backup der alten Website ziehen, vor allem die Fotos (echte Arbeitsfotos sind eventuell für Referenzen nutzbar).
4. Die alte URL-Liste vervollständigen und die Weiterleitungen abschließen: Anleitung in [02-weiterleitungen.md](02-weiterleitungen.md).
5. Zugriff auf die Search-Console-Property der alten Domain und auf das Google-Unternehmensprofil sicherstellen.
6. Neue Mailadresse auf der neuen Domain einrichten und beim bisherigen Mailanbieter für jede noch genutzte Adresse `...@gartenheldservice.com` eine Weiterleitung auf die neue Adresse vorbereiten.

**Am Starttag (abends)**

7. Die neue Website läuft unter der neuen Domain mit SSL und ist getestet.
8. hPanel: *Websites -> Add website*, `gartenheldservice.com` als leere PHP/HTML-Website. Vorhandene Platzhalterdateien löschen, die Datei [`redirects/gartenheldservice.com/.htaccess`](../redirects/gartenheldservice.com/.htaccess) (mit eingesetzter neuer Domain, Erklärung in [02-weiterleitungen.md](02-weiterleitungen.md)) in deren `public_html` hochladen. Server-IP ablesen. Eventuell verlangt Hostinger vorher einen TXT-Eintrag als Eigentumsnachweis.
9. Beim DNS-Anbieter (laut Abfrage STRATO): A-Record für `@` **und** für `www` auf die Hostinger-IP. AAAA-Records für beide löschen (oder auf die Hostinger-IPv6, falls das hPanel eine anzeigt), sonst landen IPv6-Besucher weiter auf dem alten Server. **Nameserver, MX, TXT, DKIM, DMARC, SRV und Autoconfig nicht ändern.**
10. Nach einigen Minuten im hPanel den SSL-Status für `gartenheldservice.com` und `www.gartenheldservice.com` prüfen und die Installation bei Bedarf anstoßen. Bis das Zertifikat aktiv ist, kann `https://gartenheldservice.com` eine Warnung zeigen, deshalb abends umstellen. Für diese Website „Force HTTPS“ **nicht** einschalten: Die `.htaccess` leitet http und https in einem Schritt direkt zum Ziel.
11. Weiterleitungen testen (Anleitung in 02-weiterleitungen.md): jede Adresse mit http und https, mit und ohne www. Erwartet: genau ein 301 aufs Ziel.
12. Testmail an jede noch genutzte Adresse `...@gartenheldservice.com` schicken und prüfen, dass sie ankommt.

**Danach**

13. Search Console: Adressänderung (13.6).
14. Google-Unternehmensprofil umstellen (13.5).
15. Branchenverzeichnisse direkt auf neue Domain, neuen Namen und neue Mailadresse umstellen: Gelbe Seiten, Das Örtliche, Facebook, Instagram, weitere. Einheitliche Angaben zu Name, Anschrift und Telefon helfen der lokalen Sichtbarkeit.
16. Den alten Webspace erst kündigen, wenn Weiterleitungen und SSL laufen und das Backup vorliegt. Vorher prüfen, dass im Vertrag nicht noch Domain oder Postfächer stecken.

### 13.4 E-Mail und Dauer

- Die alte Mailadresse läuft weiter wie bisher. Sie leitet mindestens 12 bis 24 Monate an die neue Adresse weiter. Antworten schickst du nur noch von der neuen Adresse.
- Das Formular sendet nie mit Absender `@gartenheldservice.com` (wegen DMARC `p=reject`).
- **Weiterleitungen mindestens ein Jahr behalten, besser dauerhaft.** Google empfiehlt mindestens ein Jahr (Stand unseres Wissens). Die Domain **nie auslaufen lassen**: Ein Fremder könnte sie registrieren, Mails an die alte Adresse empfangen und die Einträge in Verzeichnissen ausnutzen. Automatische Verlängerung aktiv lassen.

### 13.5 Google-Unternehmensprofil

**Bitte prüfen:** Die Google-Hilfe war hier nicht abrufbar, die Angaben entsprechen unserem Wissensstand.

- **Website-Adresse** am Starttag auf die neue Domain ändern. Das ist unkritisch.
- **Name ändern:** Google erlaubt eine Umbenennung im bestehenden Profil nach unserem Kenntnisstand nur bei kleineren Änderungen. „Gartenheld“ zu „Baumpflege Happe“ ist eher ein Rebranding, das Google genauer prüft. Für dich spricht: dasselbe Einzelunternehmen, derselbe Inhaber, dieselbe Anschrift.
- **Vorgehen, um die Bewertungen zu behalten:**
  1. Zuerst Website, Beschreibung, Leistungen und Fotos anpassen.
  2. Eine Kategorie für Baumpflege ergänzen (genaue Bezeichnung in der Auswahlliste).
  3. Den Namen erst ändern, wenn „Baumpflege Happe“ in der echten Welt sichtbar ist: Fahrzeug, Arbeitskleidung, Rechnungen, Website. Mit einer erneuten Bestätigung rechnen, Nachweise bereithalten.
- **Kein zweites Profil parallel anlegen.** Das gilt als Duplikat. Lehnt Google die Umbenennung ab, bleibt nur ein neues Profil, und die alten Bewertungen bleiben beim alten.
- Den Bewertungslink für die Website übernehmen wir erst nach der Namensänderung.

### 13.6 Adressänderung in der Search Console

**Sinnvoll: ja.** Es ist ein echter Umzug desselben Betriebs, das Werkzeug kostet nichts und hilft Google, Suchtreffer wie „Gartenheld Bornheim“ schneller auf die neue Domain umzustellen. Rankings für Pflaster- oder Terrassenbegriffe gehen nicht mit über und sollen es auch nicht.

Voraussetzungen und Ablauf (Stand unseres Wissens, Bitte prüfen im Hilfeartikel „Tool zur Adressänderung“):

1. Alte und neue Domain sind beide im **selben Google-Konto** als Inhaber bestätigt. Für die alte Domain existiert schon ein TXT-Eintrag. Wir klären, in welchem Konto diese Property liegt (Frage 5).
2. Die 301-Weiterleitungen sind live, mindestens für die Startseite, besser für alle Seiten.
3. In der **alten** Property: *Einstellungen -> Adressänderung*, neue Property wählen, prüfen lassen, absenden. Nach unserem Kenntnisstand soll man das für alle Varianten der alten Domain tun, mit und ohne www (Bitte prüfen im Hilfeartikel). Eine Domain-Property deckt beide ab. Verlangt das Werkzeug einzelne Varianten, bestätigen wir sie zusätzlich.
4. In der neuen Property die Sitemap einreichen und beide Properties einige Wochen beobachten.
5. Den Google-TXT-Eintrag der alten Domain behalten (bei Variante B automatisch der Fall).

Nicht verwenden für http zu https, www zu ohne www oder einen reinen Hosterwechsel.

---

## 14. Fahrplan bis zur Liveschaltung

**Schritt 1: Technik und Deployment (dieses Dokument)**

- [ ] Du liest das Konzept und beantwortest die Fragen in Abschnitt 15.
- [ ] Hostinger-Tarif prüfen und buchen (Premium), Laufzeit festlegen, EU-Rechenzentrum.
- [ ] Repository auf privat stellen (Abschnitt 7.3).
- [ ] SSH, Deploy-Schlüssel, Secrets und Variablen einrichten. Erster Upload auf die temporäre Adresse mit Passwort und noindex.
- [ ] Datenschutz-Vereinbarung von Hostinger ablegen, Speicherdauer der Server-Logs erfragen.

**Schritt 2: Logo und Farben**

- [ ] Zwei bis drei Wortmarken als SVG, mit und ohne Kronensymbol.
- [ ] Zwei bis drei Farbwelten, geprüft auf Kontrast (Website) und Eignung für Fahrzeug und Kleidung.
- [ ] Schriftwahl aus den drei Paarungen (Abschnitt 10.3).
- [ ] Deine Auswahl.

**Schritt 3: Startseite als Entwurf**

- [ ] Grundlayout, Navigation, Footer, Handy-Leiste (Anrufen, WhatsApp).
- [ ] Startseite mit Hero (Foto, optional Video), Leistungsübersicht, Ablauf, Bewertungen, Einsatzgebiet, Kontakt.
- [ ] Freigabe durch dich auf der Vorschau.

**Schritt 4: Alle weiteren Seiten**

- [ ] Inhaltsarten mit Prüfregeln, Schalter Seilklettertechnik (SKT-A).
- [ ] Leistungs-, Orts-, Gewerbe-, Referenz-, Über-uns-, FAQ-, Kontakt-, Impressum- und Datenschutzseite.
- [ ] Formular mit PHP, Spamschutz, Foto-Upload; Postfächer, `anfrage-config.php`, PHP-Optionen im hPanel.
- [ ] Workflow ergänzen: Bild-Cache, Linkprüfung, Platzhalter-Wächter, Formular-Nachbearbeitung. Zweiter Workflow für Lighthouse und Barriere-Test.
- [ ] README mit Pflegeanleitung (Texte, Fotos, Referenzen, Bewertungen).
- [ ] Alte URL-Liste vervollständigen (02-weiterleitungen.md).

**Schritt 5: SEO-Feinschliff, Test und Liveschaltung**

- [ ] Strukturierte Daten, Titles, Descriptions, Open-Graph-Bilder, Längen- und Duplikat-Check.
- [ ] Alle `PLATZHALTER` ersetzt (Telefon, E-Mail, WhatsApp, Erreichbarkeit, Antwortzeit, USt-IdNr., Bewertungen, Datenschutztext aus dem Generator).
- [ ] Tests: Lighthouse, Barriere-Test, Handarbeit (Tastatur, Zoom, Screenreader), Formular von iPhone, Android und ohne JavaScript, keine Cookies.
- [ ] Domain registriert, SSL aktiv, Force HTTPS, www-Weiterleitung, HSTS zunächst kurz.
- [ ] `NOINDEX` = `false`, Passwortschutz aus, `SITE_URL` richtig. Danach Live-Seite prüfen: kein noindex, robots.txt richtig.
- [ ] Search Console einrichten, Sitemap einreichen, Startseite zur Indexierung.
- [ ] Alte Domain umstellen (Abschnitt 13.3), Weiterleitungen testen, Testmail.
- [ ] Adressänderung, Google-Unternehmensprofil, Branchenverzeichnisse.
- [ ] Nach 2 bis 4 Wochen: Search Console der alten und neuen Domain ansehen, fehlende alte Adressen nachtragen. HSTS auf ein Jahr.

---

## 15. Offene Punkte und Fragen an dich

Nach Wichtigkeit sortiert:

1. **Alte Domain:** Du schreibst IONOS, laut DNS liegen Nameserver und E-Mail von gartenheldservice.com bei STRATO, nur die Webserver im IONOS-Netz. Bei wem ist die Domain registriert, welches Produkt hostet die alte Website, und welche Adressen `...@gartenheldservice.com` nutzt du noch?
2. **Hostinger:** Hast du schon einen Vertrag, und wenn ja, welchen Tarif (bei Single fehlen SSH und eine zweite Website)? Wenn nein: Ist Premium für dich in Ordnung, und mit welcher Laufzeit?
3. **Neue Domain und E-Mail:** Welcher Domainname? Darf ich Registrierung und Postfächer bei Hostinger vorsehen (Domain laut Recherche im ersten Jahr gratis, Postfächer nach der Testphase kostenpflichtig), und an welche Adresse sollen die Anfragen gehen?
4. **GitHub:** Das Repository ist derzeit öffentlich. Bist du einverstanden, dass es privat wird (Abschnitt 7.3)? Umstellen kannst du es selbst mit einem Klick, ich habe dafür keinen Zugriff auf die Einstellungen.
5. **Google-Konten:** In welchem Google-Konto liegen die Search-Console-Property von gartenheldservice.com (eine Bestätigung existiert schon) und dein Unternehmensprofil, und hast du Zugriff auf beide?
6. **Neuer Name nach außen:** Ist „Baumpflege Happe“ zum Start schon auf Fahrzeug, Kleidung und Rechnungen sichtbar (wichtig für die Namensänderung im Google-Profil)? Werden „Garten Held“ bei Facebook und @gartenheld_ bei Instagram umbenannt oder neu angelegt? Erst dann verlinken wir sie im Footer.

---

## 16. Quellen

Stand aller Angaben: 01.10.2026. „Geprüft“ heißt an der Primärquelle oder durch eigenen Test bestätigt, „Recherche“ heißt aus Suchergebnissen, nicht an der Quelle überprüfbar.

**Technik (geprüft)**

- Astro 7.3.5 auf npm: https://www.npmjs.com/package/astro
- Astro-Changelogs (Fonts, CSP, Markdown, compressHTML): https://github.com/withastro/astro/blob/main/packages/astro/CHANGELOG.md, https://github.com/withastro/astro/blob/main/packages/astro/CHANGELOG-v6.md
- Astro Sitemap: https://github.com/withastro/astro/tree/main/packages/integrations/sitemap
- Node.js-Releaseplan: https://github.com/nodejs/Release/blob/main/schedule.json
- Eleventy / Build Awesome: https://github.com/11ty/eleventy
- Sveltia CMS: https://github.com/sveltia/sveltia-cms
- PHPMailer 7.1.1: https://github.com/PHPMailer/PHPMailer
- schema.org (Version 30.1): https://github.com/schemaorg/schemaorg, https://schema.org/HomeAndConstructionBusiness
- Web Vitals Grenzwerte: https://github.com/GoogleChrome/web-vitals
- Chromium LCP und Video: https://github.com/chromium/chromium/blob/main/docs/speed/metrics_changelog/2023_08_lcp.md
- WCAG 2.2.2 Pause, Stop, Hide: https://github.com/w3c/wcag/blob/main/guidelines/sc/20/pause-stop-hide.html
- WCAG 2.2 (Kontrast 1.4.3, Umbruch 1.4.10, Zielgröße 2.5.8): https://www.w3.org/TR/WCAG22/
- GitHub-Actions-Versionen (`actions/checkout` v7, `actions/setup-node` v7, `peaceiris/actions-gh-pages` v4, `SamKirkland/FTP-Deploy-Action` v4.4.0): Git-Tags der Repositories, abgefragt am 01.10.2026
- MDN zu CSP `frame-ancestors`: https://github.com/mdn/content/blob/main/files/en-us/web/http/reference/headers/content-security-policy/frame-ancestors/index.md
- Apache mod_rewrite: https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html

**GitHub (geprüft)**

- Environment-Secrets im Free-Plan: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- Grenzen für Dateien: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

**Hostinger**

- Git-Deployment (geprüft): https://github.com/hostinger/api-php-sdk/blob/main/docs/Api/HostingGitApi.md
- PHP-Optionen, Kappung (geprüft): https://github.com/hostinger/api-php-sdk/blob/main/docs/Api/HostingPHPApi.md
- SSL und Domain verbinden (geprüft): https://github.com/hostinger/api-php-sdk/blob/main/docs/Api/HostingSSLApi.md, https://github.com/hostinger/api-mcp-server/blob/main/skills/connect-domain/SKILL.md
- Cache (geprüft): https://github.com/hostinger/api-php-sdk/blob/main/docs/Api/HostingCacheApi.md
- Tarif-Limits seit 12/2025 (Recherche): https://www.hostinger.com/support/10717644-new-web-and-cloud-hosting-limits-at-hostinger/
- SSH aktivieren (Recherche): https://www.hostinger.com/support/1583645-how-to-enable-ssh-access-in-hostinger/
- PHP-Version (Recherche): https://www.hostinger.com/support/1575755-how-to-change-the-php-version-of-your-hostinger-hosting-plan/
- Mail-Testphase (Recherche): https://www.hostinger.com/support/how-the-hostinger-mail-trial-works/
- PHP mail() und SMTP (Recherche): https://www.hostinger.com/support/11393648-php-mail-limitation-explained-how-to-improve-email-delivery-with-smtp/
- Data Processing Addendum (Recherche): https://www.hostinger.com/legal/dpa
- Preise aus Testberichten (Recherche): https://www.stark.marketing/blog/hostinger-test/, https://www.hosttest.de/vergleich/hostinger-webhosting.html

**Alte Domain, IONOS, STRATO (Recherche, außer DNS)**

- Eigene DNS-Abfrage gartenheldservice.com (geprüft, 01.10.2026): NS `docks15/shades07.rzone.de`, MX `smtpin.rzone.de`, DMARC `p=reject`, TTL 150, A und AAAA für `@` und `www` im Netz von IONOS (Reverse-DNS `elastic-ssl.ui-r.com`)
- IONOS 301 per .htaccess: https://www.ionos.com/help/domains/forwarding-a-domain/manually-setting-up-a-301-redirect-using-htaccess/
- IONOS Domain-Weiterleitung: https://www.ionos.com/help/domains/forwarding-a-domain/forwarding-a-domain-to-a-different-domain/
- STRATO Domainumleitung: https://www.strato.de/faq/domains/alles-zur-domainumleitung/
- STRATO SSL bei Umleitung: https://www.strato.de/faq/domains/so-nutzen-sie-strato-ssl/
- STRATO A-Record: https://www.strato.de/faq/domains/welche-einstellungen-kann-ich-im-konfigurationsdialog-a-record-vornehmen/

**Google (Stand unseres Wissens, nicht an der Quelle abrufbar)**

- Website-Umzug mit URL-Änderungen: https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- Tool zur Adressänderung: https://support.google.com/webmasters/answer/9370220?hl=de
- FAQ-Rich-Results 2023: https://developers.google.com/search/blog/2023/08/howto-faq-changes
- Bewertungs-Snippets: https://developers.google.com/search/blog/2019/09/making-review-rich-results-more-helpful
- LocalBusiness-Markup: https://developers.google.com/search/docs/appearance/structured-data/local-business
- noindex: https://developers.google.com/search/docs/crawling-indexing/block-indexing
- Unternehmensprofil, Richtlinien: https://support.google.com/business/answer/3038177?hl=de

**Recht (Gesetzestext geprüft)**

- § 25 TDDDG: https://www.gesetze-im-internet.de/ttdsg/__25.html
- § 5 DDG: https://www.gesetze-im-internet.de/ddg/__5.html
- § 5b UWG: https://www.gesetze-im-internet.de/uwg_2004/__5b.html
- § 36 VSBG (nicht an der Quelle geprüft): https://www.gesetze-im-internet.de/vsbg/__36.html
