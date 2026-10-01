# Logo und Farben: Baumpflege Happe

Gewählt am 1. Oktober 2026: **Logo 1 (klassisch) mit Symbol, Farbwelt C „Tanne und Kupfer“.**

## Farben

| Name | Verwendung | HEX | RGB | RAL-Richtwert |
|---|---|---|---|---|
| Tanne | Hauptfarbe: Schriftzug, Symbol, Überschriften, dunkle Flächen | `#173F3C` | 23 63 60 | nahe RAL 6004 Blaugrün |
| Kupfer | Akzent: Unterzeile, Hauptbutton, Sterne | `#A65A2E` | 166 90 46 | nahe RAL 8023 Orangebraun |
| Sand | Grund der Website, helles Logo auf Tanne | `#F3EEE6` | 243 238 230 | nahe RAL 9001 Cremeweiß |
| Kupfer hell | Unterzeile auf dunklem Grund | `#DE9A68` | 222 154 104 |  |
| Nebel | Flächen, Bild-Platzhalter | `#DCE6E2` | 220 230 226 |  |

RAL-Angaben sind rechnerische Richtwerte. Folierer, Sticker und Druckerei stimmen die Farben mit ihrem Farbfächer ab und legen CMYK- oder Garnfarben fest.

## Welche Datei wofür

Alle Dateien liegen in `logo/`. Der Name sagt Variante und Farbe: `baumpflege-happe_<variante>_<farbe>`.

| Variante | Wofür |
|---|---|
| `quer` | Standard mit Unterzeile: Fahrzeug, Briefbogen, Angebote, große Flächen |
| `quer-kurz` | ohne Unterzeile: Website-Kopf, Brustlogo, kleine Anzeigen |
| `stapel` | gestapelt mit Unterzeile: Jackenrücken, Schilder, quadratische Flächen |
| `stapel-kurz` | gestapelt ohne Unterzeile |
| `wort`, `wort-kurz` | nur Schriftzug, wenn kein Platz für das Symbol ist |
| `symbol` | nur Krone: Kappe, Stempel, Social-Media-Profilbild, Fahrzeugtür |
| `symbol-klein` | vereinfachte Krone für sehr kleine Größen (Favicon, App-Symbol, Stick unter 25 mm) |

| Farbe | Wofür |
|---|---|
| `farbig` | Tanne und Kupfer auf hellem Grund (Standard) |
| `tanne` | einfarbig Tanne, z. B. einfarbige Folie |
| `schwarz` | einfarbig Schwarz: Stempel, Gravur, Schwarz-Weiß-Druck |
| `weiss` | einfarbig Weiß auf dunklem Grund oder Foto |
| `negativ` | Sand und helles Kupfer auf Tanne (Arbeitskleidung, dunkle Flächen) |

Formate: `svg/` für Website, Folierung und Plotter (Schrift in Pfade umgewandelt, Symbol als eine Fläche ohne Masken), `pdf/` als Vektor für Druckerei und Sticker, `png/` mit transparentem Hintergrund für Office und Social Media.

## Schutzzone

Rund um das Logo bleibt ein freier Rand in der Höhe des Großbuchstabens „H“ aus „Happe“ (etwa ein Viertel der Logohöhe bei der Variante `quer`). Dort stehen keine Texte, Kanten oder Bildelemente.

## Mindestgrößen

| Variante | Druck, Folie | Bildschirm | Grund |
|---|---|---|---|
| `quer` mit Unterzeile | ab 64 mm Breite | ab 380 px Breite | Unterzeile muss lesbar bleiben |
| `quer-kurz` | ab 22 mm Breite | ab 100 px Breite | Schriftzug muss lesbar bleiben |
| `symbol` | ab 10 mm Höhe | ab 48 px | feines Astwerk |
| `symbol-klein` | ab 5 mm Höhe | ab 16 px | Favicon |

Stick: Unterzeile nur auf großen Flächen (Jackenrücken, ab etwa 120 mm Logobreite). Für die Brust die Kurzfassung mit etwa 80 bis 100 mm Breite. Feine Äste der Krone erst ab etwa 25 mm Symbolhöhe, darunter `symbol-klein`. Der Sticker stimmt die Umsetzung vorher ab.

## Nicht erlaubt

- Logo verzerren, drehen, mit Schatten oder Verlauf versehen
- andere Farben als die oben genannten
- Schriftzug in einer anderen Schrift nachsetzen
- Symbol und Schriftzug neu anordnen (dafür gibt es die Varianten)

## Schriften

Logo: Source Serif 4 (Schriftzug) und Source Sans 3 (Unterzeile), beide unter der SIL Open Font License 1.1, gewerblich frei nutzbar. Website: dieselben Schriften, lokal eingebunden (`src/assets/fonts/`). Für Drucksachen können sie kostenlos installiert werden (Google Fonts oder Adobe Fonts).

Erzeugt mit `tools/logo-generator/`.
