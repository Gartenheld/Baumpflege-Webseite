# Logo-Generator

Erzeugt die Logo-Vorschläge als SVG mit in Pfade umgewandelter Schrift (Kerning über HarfBuzz) und die Zeichenflächen des Design-Canvas. Gehört nicht zum Website-Build.

Einrichtung (einmalig, in einem leeren Arbeitsordner):

```sh
python3 -m venv venv
./venv/bin/pip install fonttools brotli uharfbuzz skia-python pillow   # skia-python braucht libEGL (apt: libegl1)
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

Endfassungen des gewählten Logos (Logo 1, Tanne und Kupfer) nach `brand/logo/`: `python brand_export.py`, danach `node brand_render.mjs` (PNG und PDF über Playwright). `final_symbol.py` und `outline.py` rechnen das ausgesparte Astwerk der Krone in eine einzige Fläche um (ohne Masken, geeignet für Plotter und Stick).

`ral.json` enthält die RAL-Classic-Farben aus dem npm-Paket `ral-colors` (MIT-Lizenz, Quelle: Wikipedia). Die Zuordnung zu RAL ist ein rechnerischer Richtwert.
