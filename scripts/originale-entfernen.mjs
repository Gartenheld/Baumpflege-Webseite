// Entfernt nach dem Build die unverkleinerten Originalfotos aus dist/_astro.
// Astro legt sie neben den verkleinerten Fassungen ab, obwohl keine Seite sie verwendet.
// Die Originale können Standortdaten (GPS) und Kameradaten enthalten und sollen nicht online stehen.
// Gelöscht wird nur, was in keiner HTML-, PHP-, CSS-, JS- oder XML-Datei vorkommt.
import { readFileSync, readdirSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';

const DIST = 'dist';

function dateien(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = join(dir, e.name);
    return e.isDirectory() ? dateien(p) : [p];
  });
}

const alle = dateien(DIST);
const texte = alle
  .filter((d) => /\.(html|php|css|js|mjs|xml|json|webmanifest)$/.test(d))
  .map((d) => readFileSync(d, 'utf8'))
  .join('\n');

let entfernt = 0;
for (const d of dateien(join(DIST, '_astro'))) {
  const name = d.split(/[\\/]/).pop();
  if (!/\.(jpe?g|png|webp|avif|gif|tiff?|heic|heif)$/i.test(name)) continue;
  if (texte.includes(name)) continue;
  unlinkSync(d);
  entfernt++;
}
console.log(`Originalfotos entfernt: ${entfernt}`);
