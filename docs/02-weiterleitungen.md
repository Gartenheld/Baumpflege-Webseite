# Weiterleitungen von gartenheldservice.com

Stand: 1. Oktober 2026. Gehört zu [01-technik-und-deployment.md](01-technik-und-deployment.md), Abschnitt 13.

Jede Adresse der alten Website leitet per **301** (dauerhaft umgezogen) auf die passende neue Seite. So landen Besucher, Links aus Branchenverzeichnissen und Google nicht auf einer Fehlerseite, und Google überträgt die Signale der alten Seiten auf die neuen.

> **Ziel: `https://baumpflege-happe.de`**
> Alle Weiterleitungen zeigen direkt auf die endgültige Schreibweise der neuen Domain: `https://` und **ohne www**. Dann kommt jede alte Adresse in einem einzigen Schritt an. Die fertige Datei liegt unter [`redirects/gartenheldservice.com/.htaccess`](../redirects/gartenheldservice.com/.htaccess).

---

## 1. Weiterleitungsliste

Alle Weiterleitungen gelten für jede Schreibweise der alten Domain: http und https, mit und ohne www, mit und ohne „/“ am Ende, Groß- und Kleinschreibung. Alte Parameter wie `?fbclid=...` oder `?page_id=12` werden dabei entfernt.

Spalte „Beleg“:

- **gefunden in Suche:** Die Seite steht im Google-Index (Websuche, Stand 01.10.2026).
- **Seite vorhanden, Pfad vermutet:** Die Seite gibt es laut Footer der alten Website, die genaue Adresse ist nicht belegt.
- **typischer WordPress-Pfad vermutet:** übliche Adresse, falls die alte Seite mit WordPress läuft. Das ist nicht belegt, spricht aber einiges dafür (Adressen mit „/“ am Ende).
- **Sicherheitsnetz:** Schlagwort-Regel für Adressen, die wir nicht kennen. Sie greift, wenn das Wort irgendwo in der alten Adresse steht.

### 1.1 Belegte und wahrscheinliche Seiten

| Alte URL | Neue URL | Beleg | Hinweis |
|---|---|---|---|
| `/` | `/` | gefunden in Suche | Startseite |
| `/kontakt/` | `/kontakt/` | gefunden in Suche | gleiches Thema |
| `/dienstleistungen/` | `/leistungen/` | gefunden in Suche | Sammelseite aller alten Leistungen, daher auf die Übersicht statt auf eine einzelne Leistung |
| `/preise/` | `/kosten/` | gefunden in Suche | Die Seite Kosten erklärt die Preisfaktoren ohne Preise zu nennen, die Leistungsseiten im Einzelnen. |
| `/impressum/` | `/impressum/` | Seite vorhanden, Pfad vermutet | Regel greift für jede Adresse mit „impressum“ |
| `/datenschutz/`, `/datenschutzerklaerung/`, `/privacy-policy/` | `/datenschutz/` | Seite vorhanden, Pfad vermutet | Regel greift für jede Adresse mit „datenschutz“, „privacy“, „dsgvo“ oder „cookie“ |
| `/index.php`, `/index.html` | `/` | typischer WordPress-Pfad vermutet | |

Sprungmarken wie `/dienstleistungen/#rollrasen` lassen sich nicht einzeln weiterleiten, weil der Teil nach `#` nie beim Server ankommt. Sie landen auf `/leistungen/`.

### 1.2 Vermutete Seiten über Schlagwörter (Sicherheitsnetz)

Die erste passende Regel gewinnt. Steht in einer Adresse eine Leistung und ein Ort (z. B. `/gartenpflege-bornheim/`), gewinnt die Leistung.

| Schlagwörter in der alten Adresse (Beispiele) | Neue URL |
|---|---|
| gewerbe, hausverwaltung, firmenkunden, hausmeister, objektpflege, verkehrssicherung | `/gewerbe-hausverwaltungen/` |
| referenz, projekt, galerie, portfolio, vorher-nachher, bewertung, rezension | `/referenzen/` |
| ueber-uns, ueber-mich, about, team, unser-team, unternehmen, author | `/ueber-uns/` |
| kontakt, anfrage, anfordern, rueckruf, danke | `/kontakt/` (nicht auf `/kontakt/danke/`, die Seite ist noindex) |
| faq, fragen | `/faq/` |
| seilklettertechnik, seiltechnik | `/leistungen/baumpflege/`, solange die SKT-Seite ausgeblendet ist (Pflegehinweis in Abschnitt 4) |
| sturm, unwetter, notfall, notdienst | `/leistungen/sturmschadenbeseitigung/` |
| stubben, wurzel, stumpf | `/leistungen/wurzelstockentfernung/` |
| fällung, faellung, fällen, rodung | `/leistungen/baumfaellung/` |
| häcksel, haecksel, schredder | `/leistungen/haeckselarbeiten/` |
| hecke, strauch, sträucher, gehölz, formschnitt | `/leistungen/landschaftspflege-heckenschnitt/` |
| pflaster, terrasse, einfahrt, naturstein, zaun, mauer, rasen, vertikutieren, nachsaat | `/leistungen/` (wird nicht mehr angeboten, die Übersicht zeigt das neue Angebot) |
| baum, bäume, obst, krone, totholz | `/leistungen/baumpflege/` |
| garten, beet, unkraut, landschaft, laub, galabau | `/leistungen/landschaftspflege-heckenschnitt/` (Abschnitt kleine Gartenprojekte) |
| leistung, service, angebot | `/leistungen/` |
| beratung, besichtigung, termin | `/kontakt/` |
| preis, kosten, tarif | `/kosten/` |
| bornheim und Ortsteile (Brenig, Dersdorf, Hemmerich, Hersel, Kardorf, Merten, Roisdorf, Rösberg, Sechtem, Uedorf, Walberberg, Waldorf, Widdig) | `/einsatzgebiet/bornheim/` |
| alfter, gielsdorf, impekoven, oedekoven, volmershoven, heidgen, witterschlick | `/einsatzgebiet/alfter/` |
| bonn | `/einsatzgebiet/bonn/` |
| brühl, bruehl | `/einsatzgebiet/bruehl/` |
| köln, koeln, cologne | `/einsatzgebiet/koeln/` |
| wesseling | `/einsatzgebiet/wesseling/` |
| hürth, huerth | `/einsatzgebiet/huerth/` |
| erftstadt, lechenich, liblar | `/einsatzgebiet/erftstadt/` |
| weilerswist | `/einsatzgebiet/weilerswist/` |
| einsatzgebiet, standort, region, umgebung, heimerzheim, swisttal | `/einsatzgebiet/` |

### 1.3 WordPress-Technik und Sonderfälle

| Alte URL | Neue URL | Beleg |
|---|---|---|
| `/wp-content/uploads/...` (alte Bilder, PDFs) | `/` | typischer WordPress-Pfad vermutet |
| `/sitemap.xml`, `/wp-sitemap.xml`, `/sitemap_index.xml`, `/page-sitemap.xml` | `/sitemap-index.xml` | typischer WordPress-Pfad vermutet |
| `/feed/`, `/comments/feed/`, `/<seite>/feed/` | `/` | typischer WordPress-Pfad vermutet |
| `/?p=123`, `/?page_id=45`, `/?s=suchwort` | `/` (bekannte IDs als eigene Regel nachtragbar) | typischer WordPress-Pfad vermutet |
| `/category/...`, `/tag/...`, `/2025/05/`, `/page/2/` | mit Schlagwort die passende Seite, sonst `/` | typischer WordPress-Pfad vermutet |
| `/wp-admin/`, `/wp-login.php`, `/xmlrpc.php`, `/wp-json/`, `/wp-includes/`, `/wp-content/plugins/`, `/wp-content/themes/` | **410 Gone** (dauerhaft entfernt, betrifft fast nur Bots) | typischer WordPress-Pfad vermutet |
| alles andere | `/` | Auffangregel |

**Keine Weiterleitung** für `/.well-known/` (SSL-Zertifikat), `/googleXXXX.html` (Bestätigungsdatei der Search Console) und `/robots.txt`. Die alte Domain bekommt keine robots.txt, der Server antwortet dort mit 404. Das bedeutet „alles erlaubt“, und genau das brauchen wir: Google muss die Weiterleitungen crawlen dürfen. Die alte Domain nie per robots.txt sperren.

### 1.4 Externe Einträge, die direkt umgestellt werden

Nicht nur auf die Weiterleitung verlassen. Nach dem Start direkt auf neue Domain, neuen Namen und neue Mailadresse ändern:

| Eintrag | Adresse (gefunden in Suche) |
|---|---|
| Gelbe Seiten | https://www.gelbeseiten.de/gsbiz/c52d7a57-133c-48b4-a812-3e626bec2982 |
| Das Örtliche | https://www.dasoertliche.de/Themen/Gartenheld-Heinrich-Happe-Bornheim-Merten-Schebenstr |
| Facebook „Garten Held“ | https://www.facebook.com/people/Garten-Held/61574093116578/ |
| Instagram @gartenheld_ | https://www.instagram.com/gartenheld_/ |
| Google-Unternehmensprofil | im Profil unter Website (siehe 01-technik-und-deployment.md, Abschnitt 13.5) |
| weitere (z. B. Bewertungsdienste) | beim Durchsehen ergänzen |

---

## 2. Liste vor der Liveschaltung vervollständigen

Über die Websuche ließen sich nur 4 Adressen der alten Website belegen. Die alte Website selbst war für uns nicht abrufbar. Ziel ist, jede echte alte Adresse zu kennen. Die Schlagwort-Regeln fangen vieles ab, echte Adressen bekommen aber eine eigene, genaue Regel.

1. **Sitemap der alten Website öffnen** (geht, solange sie noch läuft): `https://gartenheldservice.com/wp-sitemap.xml`, `https://gartenheldservice.com/sitemap_index.xml` und `https://gartenheldservice.com/sitemap.xml`. Dort stehen alle Seiten und Beiträge.
2. **WordPress-Verwaltung** (falls es WordPress ist): *Seiten -> Alle Seiten* und *Beiträge -> Alle Beiträge*, nur Veröffentlichtes zählt. Fährst du mit der Maus über einen Titel, zeigt der Browser unten die ID für `?page_id=`-Regeln. Unter *Einstellungen -> Permalinks* steht die Adressstruktur.
3. **Search Console der alten Domain** (eine Bestätigung existiert laut DNS schon):
   - *Indexierung -> Seiten -> Indexierte Seiten ansehen -> Exportieren*
   - *Leistung -> Suchergebnisse -> Tab „Seiten“ -> Exportieren* (bis 16 Monate, zeigt Seiten mit Klicks)
   - *Links -> Häufigste verlinkte Seiten -> Exportieren* (welche alten Seiten Links von außen haben)
4. **Crawl** mit Screaming Frog SEO Spider (kostenlose Version, für eine kleine Seite ausreichend): `https://gartenheldservice.com/` eingeben, starten, *Internal -> Filter HTML -> Export*.
5. **Wayback Machine:** `https://web.archive.org/web/*/gartenheldservice.com/*` zeigt auch früher vorhandene Adressen, die noch irgendwo verlinkt sein können.
6. **Alles in die Tabelle 1.1 übernehmen** und je Adresse das Ziel festlegen. Prüfen, ob eine Schlagwort-Regel schon das richtige Ziel liefert. Wenn nicht, eine genaue Regel in Abschnitt 4 der `.htaccess` ergänzen (nach den belegten Seiten, vor den Schlagwörtern):
   ```apache
   RewriteRule ^alter-pfad/?$ https://baumpflege-happe.de/neuer-pfad/? [R=301,L,NC]
   ```
   Für alte Kurzlinks mit ID, und zwar **über** der Startseiten-Regel `^(index\.(php|html?))?$`, sonst landet `/?p=123` vorher auf der Startseite:
   ```apache
   RewriteCond %{QUERY_STRING} (^|&)(p|page_id)=123(&|$)
   RewriteRule ^(index\.php)?$ https://baumpflege-happe.de/leistungen/? [R=301,L,NC]
   ```
7. **Backup** der alten Website ziehen (Dateien, Datenbank, Mediathek). Nach dem Umschalten ist sie nicht mehr erreichbar.

Zwei Zuordnungen kannst du gern anders entscheiden, sag dann Bescheid: Alte Pflaster-, Terrassen- und Rasenseiten zeigen auf die Leistungsübersicht (Rollrasen wird seit 3. Oktober 2026 nicht mehr angeboten).

---

## 3. Wohin die Datei kommt

Empfohlen ist Variante B (Begründung in 01-technik-und-deployment.md, Abschnitt 13):

- Bei Hostinger eine eigene kleine Website `gartenheldservice.com` anlegen (leere PHP/HTML-Website), Platzhalterdateien löschen, nur diese `.htaccess` in deren `public_html` legen.
- Im STRATO-Kundenkonto nur die A-Records von `@` und `www` auf die Hostinger-IP setzen, AAAA-Records entfernen (beide Namen haben laut DNS-Abfrage vom 01.10.2026 einen). MX, TXT, DKIM, DMARC und alles andere bleibt. Die Domain liegt bei STRATO (von dir bestätigt). Menüpfad nach unserer Recherche (Bitte prüfen): *Domains -> Domainverwaltung -> Zahnrad an der Domain -> DNS -> A-Record verwalten*.
- SSL-Zertifikat für beide Namen (mit und ohne www) im hPanel prüfen. Ohne gültiges Zertifikat zeigt der Browser bei `https://gartenheldservice.com/...` eine Warnung, bevor die Weiterleitung greift.
- „Force HTTPS“ für diese Website **nicht** einschalten, sonst gibt es zwei Sprünge statt einem.
- Eine Kopie der Datei legen wir im Repository unter `redirects/gartenheldservice.com/.htaccess` ab. Sie wird nicht automatisch hochgeladen, weil sie zu einer anderen Website gehört.

Bei Variante A (alter Webspace bleibt) kommt dieselbe Datei nach Backup und Löschen der alten Website per FTP oder Dateimanager ins Hauptverzeichnis des alten Webspace. Voraussetzung: Der alte Tarif erlaubt eigene `.htaccess`-Dateien und hat ein SSL-Zertifikat für beide Namen (bitte im Kundenkonto prüfen).

---

## 4. Fertige .htaccess für die alte Domain

Getestet am 01.10.2026 auf Apache 2.4.58 mit 134 Test-Adressen (Weiterleitungsziele, 410 für WordPress-Technik, Ausnahmen, Umlaute, Groß- und Kleinschreibung, fremde Domains werden nicht umgeleitet). Alle Ziele gibt es in der URL-Struktur (01-technik-und-deployment.md, Abschnitt 3). Hostinger nutzt nach unserer Recherche LiteSpeed, das Apache-Regeln versteht (Bitte prüfen). Der Test auf dem echten Server steht deshalb noch aus (Abschnitt 5).

```apache
# =====================================================================
# 301-Weiterleitungen gartenheldservice.com -> neue Website Baumpflege Happe
# Stand: 2026-10-01
#
# Diese Datei gehört in das Hauptverzeichnis (public_html) der ALTEN Domain
# gartenheldservice.com, empfohlen: eigene kleine Website bei Hostinger.
# Sie gehört NICHT in die neue Website.
#
# Ziel ist die neue Domain in ihrer endgültigen Schreibweise:
# https://baumpflege-happe.de (https, ohne www). Erst hochladen, wenn die neue
# Website unter dieser Adresse live ist.
#
# Gilt für alle Schreibweisen: http und https, mit und ohne www, mit und ohne
# Schrägstrich am Ende, Groß- und Kleinschreibung. Jede alte Adresse kommt in
# einem einzigen Schritt am Ziel an. Deshalb für diese Website im hPanel
# "Force HTTPS" NICHT einschalten (sonst zwei Sprünge statt einem).
# Voraussetzung: Beide Hostnamen (mit und ohne www) zeigen auf diesen Server und
# haben ein gültiges SSL-Zertifikat, sonst scheitert https:// vor der Weiterleitung.
#
# Reihenfolge (die erste passende Regel gewinnt):
#   0 nur alte Domain   1 Ausnahmen   2 WordPress-Technik   3 Medien, Sitemaps, Feeds
#   4 belegte Seiten    5 Rechtliches 6 Seitentypen         7 Leistungen
#   8 Kosten            9 Orte        10 WordPress-Archive   11 Catch-all
#
# Das "?" am Ende jedes Ziels entfernt alte Parameter (z. B. ?page_id=12, ?fbclid=...).
# Umlaute in alten Adressen: ".{1,2}", "(ae|..)" und "(o|oe|..)" stehen für ä/ae/a, ö/oe/o usw.
# Getestet am 2026-10-01 auf Apache 2.4.58 mit 134 Test-Adressen.
# =====================================================================

RewriteEngine On

# --- 0. Nur für die alte Domain -----------------------------------------------
# Schutz, falls die Datei in einem Ordner liegt, den auch eine andere Domain nutzt.
RewriteCond %{HTTP_HOST} !^(www\.)?gartenheldservice\.com\.?(:\d+)?$ [NC]
RewriteRule ^ - [L]

# --- 1. Ausnahmen: diese Adressen NICHT weiterleiten -------------------------
# SSL-Zertifikat (Let's Encrypt), Bestätigungsdatei der Google Search Console, robots.txt
RewriteRule ^\.well-known/ - [L]
RewriteRule ^google[0-9a-f]+\.html$ - [L,NC]
RewriteRule ^robots\.txt$ - [L,NC]

# --- 2. WordPress-Technik: 410 "dauerhaft entfernt" (betrifft fast nur Bots) --
# Achtung: Sperrt auch den Zugang zu einer noch laufenden alten WordPress-Installation.
RewriteRule ^(wp-admin|wp-includes|wp-json)(/|$) - [G,NC]
RewriteRule ^(wp-login|xmlrpc|wp-cron|wp-config|wp-signup|wp-trackback)\.php$ - [G,NC]
RewriteRule ^(readme\.html|license\.txt)$ - [G,NC]
RewriteRule ^wp-content/(plugins|themes|cache|languages|upgrade)/ - [G,NC]

# --- 3. Medien, Sitemaps, Feeds -----------------------------------------------
# Alte Bilder und PDFs aus der Mediathek -> Startseite
RewriteRule ^wp-content/ https://baumpflege-happe.de/? [R=301,L,NC]
# Alte Sitemaps (WordPress, Yoast, Rank Math, andere) -> neue Sitemap
RewriteRule ^(wp-sitemap|sitemap|sitemap_index|[^/]*-sitemap)[^/]*\.(xml|xsl|xml\.gz)$ https://baumpflege-happe.de/sitemap-index.xml? [R=301,L,NC]
# RSS-Feeds (/feed/, /comments/feed/, /seite/feed/) -> Startseite
RewriteRule (^|/)(feed|rss|rss2|atom|rdf)(/.*)?$ https://baumpflege-happe.de/? [R=301,L,NC]

# --- 4. Belegte Seiten (per Suchmaschine nachgewiesen, Stand 2026-10-01) ------
# Alte Kurzlinks mit ID (?p=, ?page_id=) müssen VOR der Startseiten-Regel direkt darunter stehen.
# IDs in WordPress ablesen und eintragen, Beispiel:
# RewriteCond %{QUERY_STRING} (^|&)(p|page_id)=123(&|$)
# RewriteRule ^(index\.php)?$ https://baumpflege-happe.de/leistungen/? [R=301,L,NC]
RewriteRule ^(index\.(php|html?))?$ https://baumpflege-happe.de/? [R=301,L,NC]
RewriteRule ^kontakt/?$ https://baumpflege-happe.de/kontakt/? [R=301,L,NC]
RewriteRule ^dienstleistungen/?$ https://baumpflege-happe.de/leistungen/? [R=301,L,NC]
RewriteRule ^preise/?$ https://baumpflege-happe.de/kosten/? [R=301,L,NC]
# Hier weitere exakt bekannte alte Adressen eintragen (vor den Schlagwort-Regeln), Muster:
# RewriteRule ^alter-pfad/?$ https://baumpflege-happe.de/neuer-pfad/? [R=301,L,NC]

# --- 5. Rechtliches (Seiten laut Footer vorhanden, genaue Adresse vermutet) ---
RewriteRule (impressum|imprint|legal-notice) https://baumpflege-happe.de/impressum/? [R=301,L,NC]
RewriteRule (datenschutz|privacy|dsgvo|cookie) https://baumpflege-happe.de/datenschutz/? [R=301,L,NC]

# --- 6. Seitentypen (vermutet) -------------------------------------------------
RewriteRule (gewerbe|hausverwaltung|firmenkunden|unternehmenskunden|wohnungswirtschaft|hausmeister|objektpflege|verkehrssicherung) https://baumpflege-happe.de/gewerbe-hausverwaltungen/? [R=301,L,NC]
RewriteRule (referenz|projekt|galerie|gallery|portfolio|vorher-nachher|bewertung|rezension|kundenstimme|testimonial) https://baumpflege-happe.de/referenzen/? [R=301,L,NC]
RewriteRule (ber-uns|ber-mich|about|unser-team|(^|/)(team|unternehmen|wir|philosophie)(/|$)) https://baumpflege-happe.de/ueber-uns/? [R=301,L,NC]
RewriteRule (^|/)author/ https://baumpflege-happe.de/ueber-uns/? [R=301,L,NC]
# Kontakt vor FAQ, weil "anfragen" sonst als "fragen" erkannt würde
RewriteRule (kontakt|contact|anfrage|anfordern|r.{1,2}ckruf|danke|thank-you) https://baumpflege-happe.de/kontakt/? [R=301,L,NC]
RewriteRule (faq|fragen) https://baumpflege-happe.de/faq/? [R=301,L,NC]

# --- 7. Leistungen (vermutet, Schlagwörter im alten Pfad) ---------------------
# Seilklettertechnik: solange die Seite ausgeblendet ist -> Baumpflege.
# Wenn /leistungen/seilklettertechnik/ online ist: Ziel der nächsten Regel entsprechend ändern.
RewriteRule (seilklett|klettertechnik|seiltechnik) https://baumpflege-happe.de/leistungen/baumpflege/? [R=301,L,NC]
RewriteRule (sturm|unwetter|notfall|notdienst) https://baumpflege-happe.de/leistungen/sturmschadenbeseitigung/? [R=301,L,NC]
RewriteRule (stubben|wurzel|stumpf) https://baumpflege-happe.de/leistungen/wurzelstockentfernung/? [R=301,L,NC]
RewriteRule (f.{1,2}llung|f.{1,2}llen|felling|rodung) https://baumpflege-happe.de/leistungen/baumfaellung/? [R=301,L,NC]
RewriteRule (h.{1,2}cksel|schredder) https://baumpflege-happe.de/leistungen/haeckselarbeiten/? [R=301,L,NC]
RewriteRule (hecke|strauch|str.{1,2}ucher|geh.{1,2}lz|formschnitt) https://baumpflege-happe.de/leistungen/landschaftspflege-heckenschnitt/? [R=301,L,NC]
# Nicht mehr angeboten -> Leistungsübersicht
RewriteRule (pflaster|terrass|einfahrt|naturstein|zaun|mauer|rasen|vertikutier|nachsaat) https://baumpflege-happe.de/leistungen/? [R=301,L,NC]
RewriteRule (baum|b(ae|..)ume|obst|krone|totholz) https://baumpflege-happe.de/leistungen/baumpflege/? [R=301,L,NC]
RewriteRule (garten|beet|unkraut|landschaft|gr.{1,2}npflege|(^|[-_/])laub|galabau) https://baumpflege-happe.de/leistungen/landschaftspflege-heckenschnitt/? [R=301,L,NC]
RewriteRule (leistung|service|angebot) https://baumpflege-happe.de/leistungen/? [R=301,L,NC]

# Beratung und Besichtigung ohne Leistungsbezug -> Kontakt
RewriteRule (beratung|besichtigung|termin) https://baumpflege-happe.de/kontakt/? [R=301,L,NC]

# --- 8. Kosten (nach den Leistungen, damit z. B. "baumfaellung-kosten" zur Leistung führt)
RewriteRule (preis|kosten|tarif) https://baumpflege-happe.de/kosten/? [R=301,L,NC]

# --- 9. Orte (vermutet) ---------------------------------------------------------
RewriteRule (bornheim|brenig|dersdorf|merten|roisdorf|sechtem|hersel|walberberg|waldorf|kardorf|hemmerich|r.{1,2}sberg|widdig|uedorf) https://baumpflege-happe.de/einsatzgebiet/bornheim/? [R=301,L,NC]
RewriteRule (alfter|witterschlick|oedekoven|impekoven|gielsdorf|volmershoven|heidgen) https://baumpflege-happe.de/einsatzgebiet/alfter/? [R=301,L,NC]
RewriteRule (bonn) https://baumpflege-happe.de/einsatzgebiet/bonn/? [R=301,L,NC]
RewriteRule (br.{1,2}hl) https://baumpflege-happe.de/einsatzgebiet/bruehl/? [R=301,L,NC]
RewriteRule (k(o|oe|..)ln|cologne) https://baumpflege-happe.de/einsatzgebiet/koeln/? [R=301,L,NC]
RewriteRule (wesseling) https://baumpflege-happe.de/einsatzgebiet/wesseling/? [R=301,L,NC]
RewriteRule (h.{1,2}rth) https://baumpflege-happe.de/einsatzgebiet/huerth/? [R=301,L,NC]
RewriteRule (erftstadt|lechenich|liblar) https://baumpflege-happe.de/einsatzgebiet/erftstadt/? [R=301,L,NC]
RewriteRule (weilerswist) https://baumpflege-happe.de/einsatzgebiet/weilerswist/? [R=301,L,NC]
RewriteRule (einsatzgebiet|standort|region|umgebung|heimerzheim|swisttal) https://baumpflege-happe.de/einsatzgebiet/? [R=301,L,NC]

# --- 10. WordPress-Archive ohne Schlagwort (Kategorien, Schlagwörter, Datum, Seiten) ->
#         Startseite (übernimmt die Catch-all-Regel)

# --- 11. Catch-all: alles Unbekannte -> Startseite -----------------------------
RewriteRule ^ https://baumpflege-happe.de/? [R=301,L]
```

Pflege:

- **Seilklettertechnik:** Sobald `/leistungen/seilklettertechnik/` online ist, in der Regel unter „Seilklettertechnik“ das Ziel von `/leistungen/baumpflege/` auf `/leistungen/seilklettertechnik/` ändern und die Datei neu hochladen.
- **Neu gefundene alte Adressen** als genaue Regel in Abschnitt 4 der Datei eintragen.

---

## 5. Test nach dem Umschalten

Jede Adresse aus der Liste in vier Varianten prüfen: http und https, mit und ohne www. Erwartet wird **genau ein** 301 direkt auf `https://baumpflege-happe.de/...`, keine Kette, kein 302, danach Status 200.

Im Terminal:

```sh
curl -sI http://gartenheldservice.com/preise/ | grep -iE "^(HTTP|location)"
curl -sIL -o /dev/null -w '%{num_redirects} %{http_code} %{url_effective}\n' https://www.gartenheldservice.com/dienstleistungen/
```

Erwartet: `301` mit `location: https://baumpflege-happe.de/kosten/` bzw. `1 200 https://baumpflege-happe.de/leistungen/`.

Ohne Terminal: Online-Statuscode-Prüfer (z. B. httpstatus.io) oder Screaming Frog im Listenmodus (*Mode -> List*, Adressen einfügen, Spalte „Redirect URL“).

Stichproben:

| Adresse | Erwartet |
|---|---|
| `/wp-login.php` | 410 |
| `/robots.txt` | keine Weiterleitung (404, solange dort keine Datei liegt) |
| `/.well-known/acme-challenge/test` | keine Weiterleitung |
| `/Kontakt` (ohne „/“, groß geschrieben) | 301 auf `/kontakt/` |
| `/kontakt/?utm_source=gbp` | 301 auf `/kontakt/` ohne Parameter |

2 bis 4 Wochen später in der Search Console der alten Domain unter *Indexierung -> Seiten* die Gründe „Nicht gefunden (404)“ und „Seite mit Weiterleitung“ ansehen und unbekannte Adressen nachtragen.

**Dauer:** Die Weiterleitungen mindestens ein Jahr aktiv lassen, besser dauerhaft. Dafür die Domain gartenheldservice.com behalten und nie auslaufen lassen.
