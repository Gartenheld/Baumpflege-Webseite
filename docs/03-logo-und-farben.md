# Logo und Farben

Schritt 2 von 5. Stand: 1. Oktober 2026.

Zur Auswahl auf dem Design-Canvas: https://claude.ai/artifact/KMmaJdHmugUFEsR9kLNWWn (privat, nur für dich sichtbar, solange du ihn nicht teilst). Dort lassen sich in den drei Anwendungen (Website, Pritschenwagen, Arbeitskleidung) Logo und Farbwelt per Klick umschalten.

Logo und Farbwelt sind frei kombinierbar. Jedes Logo gibt es mit und ohne Symbol und als Kurzfassung ohne Unterzeile für kleine Größen (Kopfzeile, Brustlogo).

## Logo-Vorschläge

| Nr. | Charakter | Schrift (Logo / Website) | Symbol |
|---|---|---|---|
| 1 | Klassisch: „Baumpflege“ und „Happe“ zweizeilig, Unterzeile in Versalien | Source Serif 4 und Source Sans 3 | Runde Krone als Fläche, Astwerk ausgespart, Stamm darunter |
| 2 | Natürlich und warm: „Baumpflege Happe“ einzeilig, Unterzeile darunter | Fraunces und Figtree | Blatt, dessen Mittelrippe zum Stamm wird (Linienzeichnung, zweifarbig) |
| 3 | Modern und reduziert: „BAUMPFLEGE HAPPE“ in Versalien, Unterzeile auf gleiche Breite gesetzt | Instrument Sans | Jahresringe eines Stammquerschnitts mit Trockenriss |

Alle Schriften stehen unter der SIL Open Font License 1.1: kostenlos, auch gewerblich, für Logo, Website, Fahrzeug und Druck. Im Logo ist die Schrift in Pfade umgewandelt. Folierer, Sticker und Druckerei brauchen die Schriftdatei deshalb nicht.

Dateien (vorläufig in Farbwelt A): [`docs/design/logo-vorschlaege/`](design/logo-vorschlaege/), je Vorschlag `quer`, `quer-kurz`, `stapel`, `wort` und `symbol`. Erzeugt mit [`tools/logo-generator/`](../tools/logo-generator/).

## Farbwelten

RAL-Angaben sind die rechnerisch nächstliegenden RAL-Classic-Farben (Farbabstand ΔE 2000 in Klammern). Sie sind Richtwerte. Folierer und Textildrucker stimmen die Farbe mit ihrem Farbfächer ab, für Drucksachen legt die Druckerei die CMYK-Werte fest.

### A: Waldgrün und Leinen

| Rolle | Name | HEX | RGB | RAL-Richtwert |
|---|---|---|---|---|
| Hauptfarbe | Waldgrün | `#1F3D2B` | 31 61 43 | nahe RAL 6005 Moosgrün (4,8) |
| Akzent | Salbei | `#6F8A5E` | 111 138 94 | nahe RAL 6011 Resedagrün (3,1) |
| Grund | Leinen | `#F5F1E8` | 245 241 232 | nahe RAL 9001 Cremeweiß (2,9) |
| Hervorhebung | Ocker | `#B07A2A` | 176 122 42 | nahe RAL 1011 Braunbeige (6,2) |
| Schrift | Fast Schwarz | `#1A1F1B` | 26 31 27 | für Texte |

Kontraste: Schrift auf Grund 14,8 : 1, weiße Schrift auf Button 11,9 : 1, Akzent auf Grund 3,4 : 1 (nur für Symbole, Linien und große Schrift), helles Logo auf Hauptfarbe 6,8 : 1.

Fahrzeug: Weißes Fahrzeug, Schrift und Symbol in Waldgrün, Unterzeile in Salbei. Kleidung: Waldgrün, Logo in Leinen und hellem Salbei.

### B: Anthrazit und Moos

| Rolle | Name | HEX | RGB | RAL-Richtwert |
|---|---|---|---|---|
| Hauptfarbe | Anthrazit | `#2B2F2D` | 43 47 45 | nahe RAL 7021 Schwarzgrau (3,0) |
| Akzent | Moos | `#5E7D32` | 94 125 50 | nahe RAL 6025 Farngrün (5,0) |
| Grund | Kalkweiß | `#F6F6F2` | 246 246 242 | nahe RAL 9003 Signalweiß (1,9) |
| Fläche | Hellmoos | `#E3E8D8` | 227 232 216 | nahe RAL 9002 Grauweiß (3,8) |
| Schrift | Fast Schwarz | `#1E211F` | 30 33 31 | für Texte |

Kontraste: Schrift auf Grund 15,0 : 1, weiße Schrift auf Button 4,7 : 1, Akzent auf Grund 4,4 : 1 (nur für Symbole, Linien und große Schrift), helles Logo auf Hauptfarbe 6,6 : 1.

Fahrzeug: Weißes Fahrzeug, Schrift in Anthrazit, Symbol und Unterzeile in Moos. Kleidung: Anthrazit, Logo in Kalkweiß und hellem Moos.

### C: Tanne und Kupfer

| Rolle | Name | HEX | RGB | RAL-Richtwert |
|---|---|---|---|---|
| Hauptfarbe | Tanne | `#173F3C` | 23 63 60 | nahe RAL 6004 Blaugrün (2,5) |
| Akzent | Kupfer | `#A65A2E` | 166 90 46 | nahe RAL 8023 Orangebraun (1,7) |
| Grund | Sand | `#F3EEE6` | 243 238 230 | nahe RAL 9001 Cremeweiß (3,4) |
| Fläche | Nebelgrün | `#DCE6E2` | 220 230 226 | nahe RAL 9002 Grauweiß (4,6) |
| Schrift | Fast Schwarz | `#1A2120` | 26 33 32 | für Texte |

Kontraste: Schrift auf Grund 14,2 : 1, weiße Schrift auf Button 5,1 : 1, Akzent auf Grund 4,4 : 1 (nur für Symbole, Linien und große Schrift), helles Logo auf Hauptfarbe 4,9 : 1.

Fahrzeug: Weißes Fahrzeug, Schrift in Tanne, Symbol und Unterzeile in Kupfer. Kleidung: Tanne, Logo in Sand und hellem Kupfer.

## Was nach deiner Auswahl passiert

1. Feinschliff am gewählten Logo: Abstände, Strichstärken für kleine Größen und Stick, Schutzzone und Mindestgröße.
2. Endfassungen: SVG für Website und Folierung, PDF für Druckerei und Sticker, PNG für Social Media und Office, Favicon und App-Symbol.
3. Farben und Schriften als feste Werte ins Website-Projekt übernehmen (CSS-Variablen, lokal eingebundene Schriften).
4. Schritt 3: Startseite als Entwurf zur Freigabe.
