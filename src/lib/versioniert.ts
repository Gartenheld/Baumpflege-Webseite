// Adresse einer Datei aus public/ mit Prüfsumme, z. B. "/favicon.ico?v=3f2a9c1d".
// Ändert sich die Datei (neues Logo), ändert sich die Adresse, und Browser laden sie neu statt der alten Kopie.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export function versioniert(datei: string): string {
  const inhalt = readFileSync(join(process.cwd(), 'public', datei));
  return `/${datei}?v=${createHash('sha256').update(inhalt).digest('hex').slice(0, 8)}`;
}
