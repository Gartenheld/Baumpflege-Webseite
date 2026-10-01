// Inhaltsarten der Website. Jede Datei in src/inhalte/ wird beim Bauen geprüft.
// Fehlt ein Pflichtfeld, bricht der Build mit Dateiname und Feld ab, die alte Version bleibt online.
// Dateien, die mit _ beginnen (Vorlagen), werden nie veröffentlicht.
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const leistungen = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/inhalte/leistungen' }),
  schema: z.object({
    titel: z.string().min(3),
    kurz: z.string().min(20).max(160, 'Der Kurztext soll höchstens 160 Zeichen haben.'),
    reihenfolge: z.number().int(),
    schwerpunkt: z.boolean().default(false),
    // Kennung einer Qualifikation (Dateiname in src/inhalte/qualifikationen), ohne die die Leistung nicht erscheint
    benoetigt: z.string().optional(),
  }),
});

const orte = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/inhalte/orte' }),
  schema: z.object({
    name: z.string(),
    reihenfolge: z.number().int(),
    // Lage für die Karte (WGS84, ungefähr Ortsmitte)
    breite: z.number().min(50).max(51.5),
    laenge: z.number().min(6).max(7.5),
  }),
});

const bewertungen = defineCollection({
  loader: glob({ pattern: '[^_]*.yaml', base: './src/inhalte/bewertungen' }),
  schema: z.object({
    name: z.string(),
    sterne: z.number().int().min(1).max(5),
    datum: z.string(),
    text: z.string().min(10),
    veroeffentlichen: z.boolean().default(false),
  }),
});

const qualifikationen = defineCollection({
  loader: glob({ pattern: '[^_]*.yaml', base: './src/inhalte/qualifikationen' }),
  schema: z.object({
    titel: z.string(),
    erklaerung: z.string().min(20),
    vorhanden: z.boolean(),
    reihenfolge: z.number().int(),
  }),
});

export const collections = { leistungen, orte, bewertungen, qualifikationen };
