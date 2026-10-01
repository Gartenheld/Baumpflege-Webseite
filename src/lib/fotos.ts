// Findet zu einem Foto-Platz (src/config/fotos.ts) die passende Datei in src/bilder.
import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import type { ImageMetadata } from 'astro';
import { fotos } from '../config/fotos';

// Dateien, die die Website nicht verarbeiten kann, mit klarem Hinweis melden statt still zu übergehen
for (const datei of readdirSync(join(process.cwd(), 'src/bilder'))) {
  if (/\.(heic|heif)$/i.test(datei)) {
    throw new Error(`Foto src/bilder/${datei}: HEIC-Fotos (iPhone) bitte als JPG speichern und erneut hochladen.`);
  }
}

const dateien = import.meta.glob<{ default: ImageMetadata }>('../bilder/*.{jpg,jpeg,png,webp,JPG,JPEG,PNG,WEBP}', {
  eager: true,
});

const nachName = new Map<string, ImageMetadata>();
for (const [pfad, modul] of Object.entries(dateien)) {
  const name = pfad.split('/').pop()!.replace(/\.[^.]+$/, '').toLowerCase();
  if (!fotos[name]) {
    throw new Error(
      `Foto src/bilder/${pfad.split('/').pop()}: Zu diesem Namen gibt es keinen Platz. Erlaubte Namen stehen in src/config/fotos.ts.`,
    );
  }
  nachName.set(name, modul.default);
}

export function foto(name: string): { bild?: ImageMetadata; alt: string; zeigt: string } {
  const eintrag = fotos[name];
  if (!eintrag) throw new Error(`Foto-Platz "${name}" fehlt in src/config/fotos.ts.`);
  const bild = nachName.get(name);
  if (bild && eintrag.alt.trim().length < 10) {
    throw new Error(`Foto "${name}": Bitte in src/config/fotos.ts unter alt kurz beschreiben, was auf dem Foto zu sehen ist.`);
  }
  return { bild, alt: eintrag.alt, zeigt: eintrag.zeigt };
}
