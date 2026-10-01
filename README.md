# Website Baumpflege Happe

Statische Website, gebaut mit [Astro](https://astro.build). Bei jeder Änderung auf `main` baut GitHub Actions die Seite und lädt sie zu Hostinger hoch. Das Kontaktformular läuft über ein kleines PHP-Skript auf dem Hostinger-Server.

Konzept und Hintergründe:

- [docs/01-technik-und-deployment.md](docs/01-technik-und-deployment.md): Technik, Hosting, Deployment, Formular, Datenschutz, SEO, Search Console, alte Domain
- [docs/02-weiterleitungen.md](docs/02-weiterleitungen.md): Weiterleitungen von gartenheldservice.com
- [docs/03-logo-und-farben.md](docs/03-logo-und-farben.md): Logo-Vorschläge und Farbwelten zur Auswahl (Schritt 2)
- [redirects/gartenheldservice.com/.htaccess](redirects/gartenheldservice.com/.htaccess): fertige Weiterleitungsdatei für die alte Domain (wird von Hand hochgeladen, nicht über das Deployment)

## Inhalte selbst ändern

Die ausführliche Anleitung für Texte, Fotos, Referenzen und Bewertungen folgt, sobald die Seiten gebaut sind (Schritt 4). Das Prinzip:

1. Datei im Repository auf github.com öffnen, auf den Stift klicken, ändern.
2. Unten "Commit changes" klicken.
3. Nach etwa 2 bis 4 Minuten ist die Änderung online. Den Fortschritt siehst du unter "Actions".

Zentrale Betriebsdaten (Telefon, E-Mail, WhatsApp, Erreichbarkeit, Antwortzeit, USt-IdNr., Profil-Links) stehen in einer einzigen Datei: [src/config/betrieb.ts](src/config/betrieb.ts). Alles mit `PLATZHALTER` muss vor der Liveschaltung ersetzt werden.

## Für Entwickler

Voraussetzung: Node.js 22.12 oder neuer (empfohlen 24).

```sh
npm ci          # Abhängigkeiten installieren
npm run dev     # lokale Vorschau unter http://localhost:4321
npm run build   # fertige Website nach dist/
npm run preview # gebaute Website lokal ansehen
```

Umgebungsvariablen beim Build:

| Variable | Bedeutung |
| --- | --- |
| `SITE_URL` | Adresse der Website. Ohne Angabe gilt `https://baumpflege-happe.de`. In der Vorschau die temporäre Hostinger-Adresse. |
| `PUBLIC_NOINDEX` | `true` sperrt Suchmaschinen aus (Vorschau). Zur Liveschaltung auf `false`. |

Deployment: [.github/workflows/deploy.yml](.github/workflows/deploy.yml). Benötigte Secrets und Variablen stehen im Konzept unter "Deployment".
