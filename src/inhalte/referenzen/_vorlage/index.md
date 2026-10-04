---
# Vorlage für eine neue Referenz. Ordner, die mit _ beginnen, werden nie veröffentlicht.
#
# So legen Sie eine Referenz an:
# 1. Neue Datei anlegen: src/inhalte/referenzen/JJJJ-MM-ort-baumart/index.md,
#    zum Beispiel src/inhalte/referenzen/2026-10-alfter-linde/index.md (der Schrägstrich legt den Ordner an).
# 2. Den Inhalt dieser Vorlage hineinkopieren und alle Angaben in eckigen Klammern ersetzen.
#    Solange irgendwo „Platzhalter“ steht, geht die Website nicht live.
# 3. Fotos in denselben Ordner laden und die Bildzeilen unten aktivieren (das # am Zeilenanfang entfernen).
# 4. Erst wenn alles stimmt und der Eigentümer mit der Veröffentlichung einverstanden ist:
#    veroeffentlichen: true
#
# Kurzer Titel mit Arbeit, Baumart und Ort, zum Beispiel "Fällung einer Fichte in Bornheim-Merten":
titel: "[Platzhalter: Fällung einer Fichte in Bornheim-Merten]"
# Ort als Dateiname aus src/inhalte/orte: bornheim, alfter, bonn, bruehl, koeln, wesseling, huerth, erftstadt, weilerswist.
# Dann erscheint die Referenz auch auf der passenden Ortsseite. Für andere Orte freier Text, zum Beispiel "Meckenheim".
ort: bornheim
# Eine oder mehrere Leistungen (Dateinamen aus src/inhalte/leistungen): baumpflege, baumfaellung,
# sturmschadenbeseitigung, wurzelstockentfernung, haeckselarbeiten, landschaftspflege-heckenschnitt, seilklettertechnik
leistungen: [baumfaellung]
baumart: "[Platzhalter: Fichte]"
# Ein Satz, was zu tun war, zum Beispiel "Fällung einer abgestorbenen Fichte dicht am Wohnhaus":
aufgabe: "[Platzhalter: Ein Satz zur Aufgabe]"
# Jahr und Monat der Arbeit als JJJJ-MM, zum Beispiel "2026-09":
datum: "2026-09"
#
# Fotos (optional): im selben Ordner ablegen, Dateiname genau wie in der Zeile.
# Der Alt-Text beschreibt in mindestens 10 Zeichen, was auf dem Foto zu sehen ist.
# Fotos ohne Personen, Hausnummern und Autokennzeichen auswählen.
# vorher: ./vorher.jpg
# vorherAlt: "Hohe Fichte dicht am Wohnhaus vor der Fällung"
# nachher: ./nachher.jpg
# nachherAlt: "Aufgeräumter Garten nach der Fällung der Fichte"
#
# false = nur in der Vorschau sichtbar, true = auf der Live-Seite sichtbar:
veroeffentlichen: false
---
[Platzhalter: Zwei bis drei Sätze zum Projekt, zum Beispiel Ausgangslage, Vorgehen und Ergebnis.]
