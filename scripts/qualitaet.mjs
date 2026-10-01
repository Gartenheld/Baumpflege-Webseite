// Qualitätsprüfung mit Lighthouse (Handy-Profil), für den Workflow .github/workflows/qualitaet.yml.
// - 5 typische Seiten: Leistung, Barrierefreiheit, Best Practices und SEO
// - alle Seiten der Sitemap: Barrierefreiheit und SEO
// Erwartet die gebaute Website unter BASIS_URL (z. B. http://127.0.0.1:8080) und Lighthouse in node_modules
// (im Workflow: npm install --no-save lighthouse) oder unter LIGHTHOUSE_BIN.
// Schreibt eine Tabelle in die Zusammenfassung des Workflows und endet mit Fehler, wenn ein Wert unter der Grenze liegt.
import { execFileSync } from 'node:child_process';
import { readFileSync, appendFileSync, mkdtempSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const BASIS = process.env.BASIS_URL ?? 'http://127.0.0.1:8080';
const LIGHTHOUSE = process.env.LIGHTHOUSE_BIN ?? join('node_modules', '.bin', 'lighthouse');
const GRENZEN = { performance: 85, accessibility: 95, 'best-practices': 90, seo: 95 };
const TYPISCH = ['/', '/leistungen/baumfaellung/', '/einsatzgebiet/bornheim/', '/referenzen/', '/kontakt/'];

const sitemap = readFileSync('dist/sitemap-0.xml', 'utf8');
const alle = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => new URL(m[1]).pathname);
const ordner = mkdtempSync(join(tmpdir(), 'lighthouse-'));

function messen(pfad, kategorien) {
  const datei = join(ordner, pfad.replace(/\W+/g, '_') + '.json');
  execFileSync(
    LIGHTHOUSE,
    [
      BASIS + pfad,
      '--quiet',
      '--output=json',
      `--output-path=${datei}`,
      `--only-categories=${kategorien.join(',')}`,
      // Die Vorschau ist absichtlich auf noindex gestellt, das soll die SEO-Wertung nicht senken
      '--skip-audits=is-crawlable',
      '--chrome-flags=--headless=new --no-sandbox',
    ],
    { stdio: 'inherit' },
  );
  const r = JSON.parse(readFileSync(datei, 'utf8'));
  return Object.fromEntries(Object.values(r.categories).map((k) => [k.id, Math.round(k.score * 100)]));
}

const zeilen = [];
const fehler = [];
for (const pfad of alle) {
  const kategorien = TYPISCH.includes(pfad) ? Object.keys(GRENZEN) : ['accessibility', 'seo'];
  const werte = messen(pfad, kategorien);
  zeilen.push([pfad, ...Object.keys(GRENZEN).map((k) => werte[k] ?? '')]);
  for (const [k, w] of Object.entries(werte)) {
    if (w < GRENZEN[k]) fehler.push(`${pfad}: ${k} ${w} (Grenze ${GRENZEN[k]})`);
  }
  console.log(pfad, JSON.stringify(werte));
}

const tabelle = [
  '| Seite | Leistung | Barrierefreiheit | Best Practices | SEO |',
  '| --- | --- | --- | --- | --- |',
  ...zeilen.map((z) => `| ${z.join(' | ')} |`),
].join('\n');
if (process.env.GITHUB_STEP_SUMMARY) {
  appendFileSync(process.env.GITHUB_STEP_SUMMARY, `## Lighthouse (Handy)\n\n${tabelle}\n\n${fehler.length ? '**Unter der Grenze:**\n\n' + fehler.map((f) => `- ${f}`).join('\n') : 'Alle Werte über den Grenzen.'}\n`);
}
if (fehler.length) {
  for (const f of fehler) console.error(`::warning::${f}`);
  process.exit(1);
}
