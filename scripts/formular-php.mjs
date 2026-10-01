// Läuft nach "astro build": Jede Seite mit der Marke __ANFRAGE_TOKEN__ wird zu einer index.php,
// damit der Server beim Aufruf einen frischen, signierten Zeitstempel einsetzt (Zeitsperre ohne Cookie).
// Die index.html dort wird entfernt, sonst hätte sie Vorrang.
import { readdir, readFile, writeFile, unlink } from 'node:fs/promises';
import { join } from 'node:path';

const DIST = 'dist';
const MARKE = '__ANFRAGE_TOKEN__';
const KOPF =
  "<?php require dirname(__DIR__) . '/anfrage/lib/anfrage.php';" +
  " header('Cache-Control: no-cache, private'); header('X-LiteSpeed-Cache-Control: no-cache'); ?>";

let anzahl = 0;
for (const datei of await readdir(DIST, { recursive: true })) {
  if (!datei.endsWith('index.html')) continue;
  const pfad = join(DIST, datei);
  const html = await readFile(pfad, 'utf8');
  if (!html.includes(MARKE)) continue;
  if (html.includes('<?')) throw new Error(`${pfad}: enthält "<?" und würde von PHP falsch gelesen.`);
  const tiefe = datei.split(/[\\/]/).length - 1;
  if (tiefe !== 1) throw new Error(`${pfad}: Formularseiten müssen eine Ebene tief liegen (z. B. /kontakt/).`);
  await writeFile(pfad.replace(/index\.html$/, 'index.php'), KOPF + html.replaceAll(MARKE, '<?= htmlspecialchars(anfrage_token(), ENT_QUOTES) ?>'));
  await unlink(pfad);
  anzahl++;
  console.log(`Formularseite als PHP: ${pfad.replace(/index\.html$/, 'index.php')}`);
}
if (anzahl === 0) throw new Error('Keine Formularseite gefunden (Marke __ANFRAGE_TOKEN__ fehlt).');
