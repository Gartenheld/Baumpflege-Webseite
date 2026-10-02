# Fotos der Website

Hier liegen die eigenen Fotos. Jedes Foto hat einen festen Platz auf der Website.
Der Dateiname bestimmt den Platz, die Endung darf `.jpg`, `.jpeg`, `.png` oder `.webp` sein.

| Dateiname | Wo das Foto erscheint |
| --- | --- |
| `startseite.jpg` | Startseite, großes Foto oben |
| `ueber-uns.jpg` | Über uns, oben |
| `ueber-uns-ausstattung.jpg` | Über uns, neben Arbeitsweise und Ansprechpartner (Hubarbeitsbühne, Häcksler) |
| `gewerbe.jpg` | Gewerbe und Hausverwaltungen, oben |
| `leistung-baumpflege.jpg` | Leistung Baumpflege, oben und auf der Karte in der Übersicht |
| `leistung-baumfaellung.jpg` | Leistung Baumfällung, oben und auf der Karte in der Übersicht |
| `leistung-sturmschadenbeseitigung.jpg` | Leistung Sturmschadenbeseitigung |
| `leistung-wurzelstockentfernung.jpg` | Leistung Wurzelstockentfernung |
| `leistung-haeckselarbeiten.jpg` | Leistung Häckselarbeiten |
| `leistung-landschaftspflege-heckenschnitt.jpg` | Leistung Landschaftspflege und Heckenschnitt |
| `leistung-rollrasen.jpg` | Leistung Rollrasen |
| `leistung-seilklettertechnik.jpg` | Leistung Seilklettertechnik |

So geht es:

1. Auf github.com in diesen Ordner gehen, oben rechts **Add file** und **Upload files** wählen, Foto hineinziehen.
   Heißt die Datei anders, vorher am Computer umbenennen.
2. In [src/config/fotos.ts](../config/fotos.ts) beim selben Namen unter `alt` einen Satz eintragen, was zu sehen ist,
   zum Beispiel `alt: 'Heinrich Happe schneidet eine Hecke mit der Heckenschere'`.
3. **Commit changes** klicken. Nach wenigen Minuten ist das Foto online.

Tipps:

- Querformat, mindestens 2000 Pixel breit. Die Website verkleinert die Fotos selbst und entfernt dabei Standort- und Kameradaten.
- Ein Foto pro Datei höchstens 25 MB (Grenze von GitHub).
- iPhone-Fotos im Format HEIC vorher als JPG speichern (oder auf dem iPhone: Einstellungen, Kamera, Formate, „Maximale Kompatibilität“).
- Keine erkennbaren Personen ohne deren Einverständnis, keine Hausnummern und Autokennzeichen von Kunden.
- Foto austauschen: neue Datei mit gleichem Namen hochladen, die alte wird ersetzt. Foto entfernen: Datei löschen, dann erscheint wieder der Platzhalter.
