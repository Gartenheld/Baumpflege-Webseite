// Hintergrundvideos aus src/videos. Ein Video besteht aus:
//   <name>.mp4        Hauptdatei (H.264, Full HD), Pflicht
//   <name>-klein.mp4  kleinere Fassung für Handys (optional), dazu optional <name>-klein.webm
//   <name>.webm       platzsparende Fassung für moderne Browser (optional)
//   <name>.jpg        Standbild, solange das Video lädt oder wenn es angehalten ist (optional)
import type { ImageMetadata } from 'astro';

const dateien = import.meta.glob<string>('../videos/*.{mp4,webm}', { query: '?url', import: 'default', eager: true });
const standbilder = import.meta.glob<{ default: ImageMetadata }>('../videos/*.{jpg,jpeg,png,webp}', { eager: true });

const name = (pfad: string) => pfad.split('/').pop()!.toLowerCase();

export interface Video {
  mp4: string;
  klein?: string;
  kleinWebm?: string;
  webm?: string;
  standbild?: ImageMetadata;
}

export function video(platz: string): Video | undefined {
  const datei = (endung: string) => Object.entries(dateien).find(([p]) => name(p) === `${platz}${endung}`)?.[1];
  const mp4 = datei('.mp4');
  if (!mp4) return undefined;
  const standbild = Object.entries(standbilder).find(([p]) => name(p).replace(/\.[^.]+$/, '') === platz)?.[1].default;
  return { mp4, klein: datei('-klein.mp4'), kleinWebm: datei('-klein.webm'), webm: datei('.webm'), standbild };
}
