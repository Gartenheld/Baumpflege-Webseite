// Prüft die fertig gebaute Website in dist/, bevor sie hochgeladen wird:
// - jede Seite hat genau einen Title, eine Description, eine H1 und einen Canonical-Link
// - Titles und Descriptions sind nicht doppelt und nicht zu lang
// - interne Links und Bilder zeigen auf vorhandene Dateien, Sprungmarken (#…) auf vorhandene IDs
// - strukturierte Daten sind gültiges JSON, das Vorschaubild zum Teilen ist vorhanden
// - Live-Build (PUBLIC_NOINDEX=false): kein „Platzhalter“ und keine Platzhalter-Nummer mehr, Startseite indexierbar
// Lange Gedankenstriche werden nur als Hinweis gemeldet.
// Aufruf: node scripts/pruefe-seiten.mjs (läuft in "npm run build" automatisch mit)
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const DIST = 'dist';
const live = process.env.PUBLIC_NOINDEX === 'false';
const fehler = [];
const hinweise = [];

function dateien(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = join(dir, e.name);
    return e.isDirectory() ? dateien(p) : [p];
  });
}

// Pfad einer Seite, wie er im Browser erscheint: dist/leistungen/baumpflege/index.html -> /leistungen/baumpflege/
function urlVon(datei) {
  const r = '/' + relative(DIST, datei).split(sep).join('/');
  return r.replace(/index\.(html|php)$/, '');
}

const ent = (s) =>
  s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');

const alle = dateien(DIST);
const seiten = alle.filter((d) => /\.(html|php)$/.test(d) && !d.includes(`${sep}anfrage${sep}`));
const ids = new Map();
const inhalt = new Map();
for (const d of seiten) {
  const html = readFileSync(d, 'utf8');
  inhalt.set(d, html);
  ids.set(urlVon(d), new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
}

// Gibt es zu einem internen Pfad eine Datei?
function vorhanden(pfad) {
  const p = decodeURIComponent(pfad);
  const ziel = join(DIST, p);
  if (p.endsWith('/')) return existsSync(join(ziel, 'index.html')) || existsSync(join(ziel, 'index.php'));
  return existsSync(ziel) && statSync(ziel).isFile();
}

const titel = new Map();
const beschreibungen = new Map();

for (const [d, html] of inhalt) {
  const url = urlVon(d);
  const istFehlerseite = url === '/404.html' || url.startsWith('/kontakt/fehler/');
  const t = [...html.matchAll(/<title>([^<]*)<\/title>/g)].map((m) => ent(m[1]));
  const desc = [...html.matchAll(/<meta name="description" content="([^"]*)"/g)].map((m) => ent(m[1]));
  const h1 = (html.match(/<h1[\s>]/g) || []).length;

  if (t.length !== 1) fehler.push(`${url}: ${t.length} Title statt 1`);
  if (desc.length !== 1) fehler.push(`${url}: ${desc.length} Descriptions statt 1`);
  if (h1 !== 1) fehler.push(`${url}: ${h1} Überschriften H1 statt 1`);
  if (!/<link rel="canonical"/.test(html)) fehler.push(`${url}: Canonical-Link fehlt`);

  // Strukturierte Daten müssen gültiges JSON sein
  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try {
      JSON.parse(m[1]);
    } catch (e) {
      fehler.push(`${url}: strukturierte Daten sind kein gültiges JSON (${e.message})`);
    }
  }

  // Vorschaubild zum Teilen muss vorhanden sein
  const og = html.match(/<meta property="og:image" content="([^"]+)"/);
  if (!og) fehler.push(`${url}: Vorschaubild (og:image) fehlt`);
  else if (!vorhanden(new URL(ent(og[1])).pathname)) fehler.push(`${url}: Vorschaubild ${og[1]} fehlt`);

  // Live: Platzhalter-Nummern aus betrieb.ts und versehentliches noindex
  if (live && /0{8,}/.test(html)) fehler.push(`${url}: Telefon- oder WhatsApp-Nummer ist noch der Platzhalter (lauter Nullen)`);
  if (live && url === '/' && !/<meta name="robots" content="index, follow"/.test(html)) fehler.push('Startseite ist auf noindex gestellt');

  // Längen und Dubletten nur für Seiten, die in Suchmaschinen erscheinen sollen
  const zaehlt = !istFehlerseite && !url.startsWith('/kontakt/danke/');
  if (zaehlt && t[0]) {
    if (t[0].length > 65) hinweise.push(`${url}: Title hat ${t[0].length} Zeichen (empfohlen höchstens 65)`);
    if (titel.has(t[0])) fehler.push(`${url}: gleicher Title wie ${titel.get(t[0])}`);
    titel.set(t[0], url);
  }
  if (zaehlt && desc[0]) {
    if (desc[0].length > 165) hinweise.push(`${url}: Description hat ${desc[0].length} Zeichen (empfohlen höchstens 165)`);
    if (desc[0].length < 70) hinweise.push(`${url}: Description hat nur ${desc[0].length} Zeichen`);
    if (beschreibungen.has(desc[0])) fehler.push(`${url}: gleiche Description wie ${beschreibungen.get(desc[0])}`);
    beschreibungen.set(desc[0], url);
  }

  // Interne Links, Bilder, Skripte und Stile
  for (const m of html.matchAll(/\s(?:href|src|srcset)="([^"]+)"/g)) {
    for (const teil of m[1].split(',')) {
      const ref = ent(teil.trim().split(/\s+/)[0]);
      if (!ref.startsWith('/') || ref.startsWith('//')) continue;
      const [ohneHash, hash] = ref.split('#');
      const pfad = ohneHash.split('?')[0];
      if (pfad === '/anfrage/senden.php') continue;
      if (pfad && !vorhanden(pfad)) fehler.push(`${url}: Link auf ${ref} führt ins Leere`);
      else if (hash) {
        const zielIds = ids.get(pfad || url);
        if (zielIds && !zielIds.has(hash)) fehler.push(`${url}: Sprungmarke ${ref} gibt es nicht`);
      }
    }
  }
  for (const m of html.matchAll(/\shref="#([^"]+)"/g)) {
    if (!ids.get(url).has(m[1])) fehler.push(`${url}: Sprungmarke #${m[1]} gibt es nicht`);
  }

  // Sichtbarer Text ohne Skripte, Stile und SVG
  const text = html
    .replace(/<(script|style|svg)[\s\S]*?<\/\1>/g, ' ')
    .replace(/<[^>]+>/g, ' ');
  if (live && /Platzhalter/.test(html)) fehler.push(`${url}: enthält noch „Platzhalter“`);
  const strich = text.match(/.{0,30}[—–].{0,30}/);
  if (strich) hinweise.push(`${url}: langer Gedankenstrich in „${strich[0].trim()}“`);
}

// Platzhalter in Sitemap, Robots oder anderen Textdateien
if (live) {
  for (const d of alle.filter((d) => /\.(xml|txt|webmanifest)$/.test(d))) {
    if (/Platzhalter/.test(readFileSync(d, 'utf8'))) fehler.push(`${relative(DIST, d)}: enthält noch „Platzhalter“`);
  }
}

console.log(`Seitenprüfung: ${seiten.length} Seiten, ${live ? 'Live-Build' : 'Vorschau-Build'}`);
for (const h of hinweise) console.log(`  Hinweis: ${h}`);
if (fehler.length) {
  for (const f of fehler) console.error(`  Fehler: ${f}`);
  console.error(`Seitenprüfung fehlgeschlagen (${fehler.length} Fehler).`);
  process.exit(1);
}
console.log('Seitenprüfung bestanden.');
