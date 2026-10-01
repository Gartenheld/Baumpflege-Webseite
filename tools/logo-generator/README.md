# Logo-Generator

Erzeugt die Logo-Vorschläge als SVG mit in Pfade umgewandelter Schrift (Kerning über HarfBuzz) und die Zeichenflächen des Design-Canvas. Gehört nicht zum Website-Build.

Einrichtung (einmalig, in einem leeren Arbeitsordner):

```sh
python3 -m venv venv
./venv/bin/pip install fonttools brotli uharfbuzz
npm init -y
npm install @fontsource-variable/fraunces @fontsource-variable/source-serif-4 \
  @fontsource-variable/instrument-sans @fontsource-variable/figtree @fontsource-variable/source-sans-3
cp /pfad/zum/repo/tools/logo-generator/*.py /pfad/zum/repo/tools/logo-generator/ral.json .
```

Nutzung:

```python
from logos import VORSCHLAEGE, svg_doc
svg = svg_doc(VORSCHLAEGE[2]('quer'), '#1F3D2B', '#6F8A5E')
```

Varianten: `quer`, `stapel`, `wort`, `symbol`, jeweils auch mit `_kurz` (ohne Unterzeile). `gen_canvas.py` schreibt die Canvas-Dateien nach `canvas/project/`.

`ral.json` enthält die RAL-Classic-Farben aus dem npm-Paket `ral-colors` (MIT-Lizenz, Quelle: Wikipedia). Die Zuordnung zu RAL ist ein rechnerischer Richtwert.
