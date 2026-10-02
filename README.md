# Website Baumpflege Happe

Statische Website, gebaut mit [Astro](https://astro.build). Bei jeder Änderung auf `main` baut GitHub Actions die Seite und lädt sie zu Hostinger hoch. Das Kontaktformular läuft über ein kleines PHP-Skript auf dem Hostinger-Server.

Konzept und Hintergründe:

- [docs/01-technik-und-deployment.md](docs/01-technik-und-deployment.md): Technik, Hosting, Deployment, Formular, Datenschutz, SEO, Search Console, alte Domain
- [docs/02-weiterleitungen.md](docs/02-weiterleitungen.md): Weiterleitungen von gartenheldservice.com
- [docs/03-logo-und-farben.md](docs/03-logo-und-farben.md): Logo-Vorschläge und Farbwelten (Schritt 2)
- [docs/04-liveschaltung.md](docs/04-liveschaltung.md): Checkliste für die Liveschaltung (Schritt 5)
- [brand/README.md](brand/README.md): gewähltes Logo und Farben, Endfassungen für Druck, Folie und Stick
- [redirects/gartenheldservice.com/.htaccess](redirects/gartenheldservice.com/.htaccess): fertige Weiterleitungsdatei für die alte Domain (wird von Hand hochgeladen, nicht über das Deployment)

## Inhalte selbst ändern

Alle Texte, Fotos, Referenzen und Bewertungen änderst du direkt auf github.com. Du brauchst dafür kein Programm.

### So läuft eine Änderung

1. Datei im Repository öffnen, oben rechts auf den **Stift** klicken und ändern.
2. **Commit changes...** klicken, „Commit directly to the main branch“ lassen, bestätigen.
3. Unter **Actions** startet die Prüfung: gelber Punkt, dann grüner Haken. Nach etwa 2 bis 4 Minuten ist die Änderung online.
4. **Roter Haken?** Dann ist nichts kaputt, die alte Version bleibt online. Auf den roten Lauf klicken: Die Meldung nennt Datei und Feld, zum Beispiel „Die Beschreibung soll höchstens 165 Zeichen haben“. Korrigieren, erneut speichern.

Mehrere Dateien auf einmal bearbeiten: im Repository die Taste „.“ drücken, dann öffnet sich der Editor github.dev.

### Wo steht was?

| Was | Datei oder Ordner |
| --- | --- |
| Telefon, E-Mail, WhatsApp, Erreichbarkeit, Antwortzeit, USt-IdNr., Bewertungsdurchschnitt, Profil-Links | [src/config/betrieb.ts](src/config/betrieb.ts) |
| Fotos der Seiten | Ordner [src/bilder](src/bilder) (Anleitung dort), alt-Texte in [src/config/fotos.ts](src/config/fotos.ts) |
| Leistungsseiten | [src/inhalte/leistungen](src/inhalte/leistungen), eine Datei pro Leistung |
| Ortsseiten | [src/inhalte/orte](src/inhalte/orte), eine Datei pro Ort |
| Häufige Fragen | [src/inhalte/faq](src/inhalte/faq), eine Datei pro Frage |
| Referenzen | [src/inhalte/referenzen](src/inhalte/referenzen), ein Ordner pro Projekt |
| Google-Bewertungen | [src/inhalte/bewertungen](src/inhalte/bewertungen), eine Datei pro Bewertung |
| Qualifikationen (AS Baum I, AS Baum II, SKT-A, SKT-B) | [src/inhalte/qualifikationen](src/inhalte/qualifikationen) |
| Texte von Über uns, Gewerbe, Einsatzgebiet, Referenzen, FAQ, Kontakt, Leistungsübersicht | [src/inhalte/seiten](src/inhalte/seiten) |
| Datenschutzerklärung | [src/inhalte/seiten/datenschutz.md](src/inhalte/seiten/datenschutz.md) |
| Impressum (Angaben kommen aus `betrieb.ts`, dazu der Satz zur Verbraucherschlichtung) | [src/pages/impressum.astro](src/pages/impressum.astro) |
| Menü | [src/config/navigation.ts](src/config/navigation.ts) |

### Texte ändern

Jede Inhaltsdatei hat oben einen Kopf zwischen zwei Zeilen `---`. Dort stehen feste Felder wie `seitentitel`, `beschreibung` oder `h1`. Darunter folgt der Fließtext.

- Im Kopf nur den Text **zwischen den Anführungszeichen** ändern. Anführungszeichen, Doppelpunkte und Einrückungen stehen lassen.
- `seitentitel` (höchstens 65 Zeichen) und `beschreibung` (80 bis 165 Zeichen) sieht man in den Google-Ergebnissen. Leistung und Ort sollten darin vorkommen. Jede Seite braucht eigene Texte, doppelte Titel lässt die Prüfung nicht durch.
- Im Fließtext: `## Überschrift`, eine Leerzeile zwischen Absätzen, `- ` am Zeilenanfang für eine Aufzählung, `**fett**`, Links als `[Text](/kontakt/)`.
- Schreibregeln der Website: Kunden mit „Sie“ ansprechen, keine Gendersternchen oder Doppelnennungen, keine langen Gedankenstriche (die Prüfung meldet sie als Hinweis), keine Preise, keine Zusagen, die der Betrieb nicht einhalten kann.

### Fotos

Fotos haben feste Plätze, zum Beispiel `startseite.jpg` oder `leistung-baumfaellung.jpg`. Foto mit genau diesem Namen in den Ordner [src/bilder](src/bilder) hochladen und in [src/config/fotos.ts](src/config/fotos.ts) einen alt-Text eintragen. Die Liste aller Plätze und die Schritte stehen in [src/bilder/README.md](src/bilder/README.md). Die Website verkleinert die Fotos selbst, liefert AVIF und WebP aus und entfernt Standort- und Kameradaten.

### Neue Referenz

1. **Add file** und **Create new file** wählen, als Namen zum Beispiel `src/inhalte/referenzen/2026-10-alfter-linde/index.md` eingeben (die Schrägstriche legen die Ordner an).
2. Den Inhalt von [src/inhalte/referenzen/_vorlage/index.md](src/inhalte/referenzen/_vorlage/index.md) hineinkopieren und alle Angaben in eckigen Klammern ersetzen.
3. Vorher- und Nachher-Foto in denselben Ordner hochladen und die Bildzeilen in der Datei aktivieren (das `#` am Zeilenanfang entfernen).
4. Erst wenn der Kunde mit der Veröffentlichung einverstanden ist: `veroeffentlichen: true`.

Die Referenz erscheint auf der Referenzseite und, wenn `ort` einer der neun Orte ist, auch auf der Ortsseite. Die drei Platzhalter-Referenzen (`platzhalter-1` bis `-3`) sind nur in der Vorschau sichtbar. Sobald echte Referenzen da sind, kannst du die Platzhalter-Ordner löschen.

### Google-Bewertungen

1. Eine Datei in [src/inhalte/bewertungen](src/inhalte/bewertungen) kopieren, zum Beispiel als `2026-10-erika-m.yaml`.
2. Name gekürzt (Vorname und Anfangsbuchstabe), Sterne, Monat und Text aus dem Google-Profil übernehmen, `veroeffentlichen: true` setzen.
3. In [src/config/betrieb.ts](src/config/betrieb.ts) Durchschnitt, Anzahl und Stand anpassen.

Es werden nur echte Bewertungen wörtlich (gern gekürzt) übernommen, keine erfundenen oder umgeschriebenen. Die Platzhalter-Dateien `platzhalter-1` bis `-3` danach löschen.

### Häufige Fragen

Eine vorhandene Datei in [src/inhalte/faq](src/inhalte/faq) kopieren und anpassen:

- `frage` endet mit einem Fragezeichen.
- `thema`: `genehmigung`, `kosten`, `nachbarn`, `haftung`, `ablauf` oder `leistung` (Fragen zu einer einzelnen Leistung).
- `leistungen`: auf welchen Leistungsseiten die Frage zusätzlich erscheint, zum Beispiel `[baumfaellung, baumpflege]`.
- `aufFaqSeite: false` zeigt eine Frage nur auf den Leistungsseiten.
- `reihenfolge`: kleinere Zahl steht weiter oben.

Rechtliche Themen bitte allgemein halten und auf die zuständige Stelle verweisen, keine Rechtsberatung.

### Qualifikationen

Jede Qualifikation ist eine Datei in [src/inhalte/qualifikationen](src/inhalte/qualifikationen) mit Titel, einem Satz Erklärung und `vorhanden`.

- **AS Baum I, AS Baum II, SKT-A:** `vorhanden: true`. Mit SKT-A erscheint die Seite Seilklettertechnik in der Leistungsübersicht, im Fußbereich und in der Sitemap.
- **SKT-B:** `vorhanden: false` und `partner: true`. Die Website zeigt SKT-B mit dem Hinweis „über Subunternehmer“. Die Texte zu Seilklettertechnik und Fällung auf engem Raum sagen, dass Arbeiten mit der Motorsäge im Baum ein Subunternehmer mit SKT-B übernimmt.
- **SKT-B selbst bestanden:** in `skt-b.yaml` `vorhanden: true` und `partner: false` setzen und mir Bescheid geben, dann passen wir die Texte an.
- **Neue Qualifikation:** eine Datei kopieren und anpassen. Nur Qualifikationen eintragen, die nachweisbar vorliegen.

### Instagram und Facebook

In [src/config/betrieb.ts](src/config/betrieb.ts) unter `profile` die komplette Adresse eintragen, zum Beispiel `instagram: 'https://www.instagram.com/baumpflege.happe/'`. Dann erscheinen die Links mit Symbol im Fußbereich jeder Seite (unter „Folgen Sie uns“) und auf der Kontaktseite, außerdem in den Daten für Google. Solange ein Feld leer ist, steht in der Vorschau „Link folgt“, auf der Live-Seite erscheint an der Stelle nichts.

### Nach jeder Änderung am Formular oder am Server

Eine kurze Testanfrage über [/kontakt/](https://baumpflege-happe.de/kontakt/) senden und prüfen, ob die Mail ankommt. Die Zugangsdaten für den Mailversand stehen nur auf dem Server in `anfrage-config.php` außerhalb von `public_html` (Vorlage: [server/anfrage-config.beispiel.php](server/anfrage-config.beispiel.php)), nie im Repository.

## Für Entwickler

Voraussetzung: Node.js 22.12 oder neuer (empfohlen 24).

```sh
npm ci          # Abhängigkeiten installieren
npm run dev     # lokale Vorschau unter http://localhost:4321
npm run build   # fertige Website nach dist/, danach Seitenprüfung (Links, Titles, Platzhalter)
npm run preview # gebaute Website lokal ansehen
```

Umgebungsvariablen beim Build:

| Variable | Bedeutung |
| --- | --- |
| `SITE_URL` | Adresse der Website. Ohne Angabe gilt `https://baumpflege-happe.de`. In der Vorschau die temporäre Hostinger-Adresse. |
| `PUBLIC_NOINDEX` | `true` sperrt Suchmaschinen aus (Vorschau, gilt auch ohne Angabe). Zur Liveschaltung auf `false`. Nur dann prüft der Build, dass kein Platzhalter mehr übrig ist. |

Deployment: [.github/workflows/deploy.yml](.github/workflows/deploy.yml). Benötigte Secrets und Variablen stehen im Konzept unter "Deployment".
