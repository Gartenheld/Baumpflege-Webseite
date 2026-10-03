# Videos der Website

Hier liegt das Hintergrundvideo der Startseite. Es läuft stumm in Schleife hinter der Überschrift,
leicht abgedunkelt, mit Pause-Knopf. Ohne Video zeigt die Startseite das Foto `src/bilder/startseite.jpg`
oder, wenn auch das fehlt, einen ruhigen dunkelgrünen Hintergrund.

| Datei | Inhalt |
| --- | --- |
| `startseite.mp4` | Hauptdatei, H.264, 1920 x 1080, ohne Ton (Pflicht) |
| `startseite.webm` | gleiche Szene als VP9, kleiner (optional) |
| `startseite-klein.mp4`, `startseite-klein.webm` | 1280 x 720 für Handys (optional) |
| `startseite.jpg` | Standbild aus dem Video, erscheint während des Ladens (optional) |

Am einfachsten: das Rohvideo (gern direkt vom Handy oder von Pexels/Pixabay) an Claude geben.
Claude schneidet es auf 10 bis 20 Sekunden, entfernt den Ton und erzeugt alle Fassungen.
Ziel: jede Datei unter 3 MB, damit die Seite auch mobil schnell bleibt.

Ruhige Motive wirken am professionellsten: Blick in eine Baumkrone, Licht durch Blätter, Arbeit in der Krone
aus der Ferne. Keine Namen oder Logos anderer Baumpflegebetriebe im Bild.

Aktuell (Test seit 3. Oktober 2026): Motorsäge in Zeitlupe beim Durchtrennen eines Stammes, mit fliegenden
Spänen (Pexels, frei nutzbar). 11 Sekunden ab Sekunde 0,5 verwendet, als Schleife von gut 10 Sekunden mit weicher
Überblendung. Größen: 2,5 MB (MP4), 2,0 MB (WebM), Handy rund 1,3 MB.
Vorher: Drohnenflug über Baumkronen, liegt in der Git-Historie (Commit „Startseite: wieder das Hintergrundvideo
mit dem Drohnenflug über Baumkronen“).
