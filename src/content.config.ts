// Inhaltsarten der Website. Jede Datei in src/inhalte/ wird beim Bauen geprüft.
// Fehlt ein Pflichtfeld, bricht der Build mit Dateiname und Feld ab, die alte Version bleibt online.
// Dateien, die mit _ beginnen (Vorlagen), werden nie veröffentlicht.
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Title und Description für Suchmaschinen: Längen als Faustregel (Google kürzt nach Breite).
const seitentitel = z.string().min(20).max(65, 'Der Seitentitel soll höchstens 65 Zeichen haben.');
const beschreibung = z.string().min(80).max(165, 'Die Beschreibung soll höchstens 165 Zeichen haben.');
const karte = z.object({ titel: z.string(), text: z.string() });

const leistungen = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/inhalte/leistungen' }),
  schema: ({ image }) =>
    z.object({
      titel: z.string().min(3),
      kurz: z.string().min(20).max(160, 'Der Kurztext soll höchstens 160 Zeichen haben.'),
      reihenfolge: z.number().int(),
      schwerpunkt: z.boolean().default(false),
      // Kennung einer Qualifikation (Dateiname in src/inhalte/qualifikationen), ohne die die Leistung nicht erscheint
      benoetigt: z.string().optional(),
      seitentitel,
      beschreibung,
      h1: z.string(),
      einleitung: z.string(),
      // Nutzen für den Kunden, 3 oder 4 Punkte
      vorteile: z.array(karte).min(3).max(4),
      // Abschnitt „Was kostet …?“: Preisfaktoren ohne Zahlen
      kosten: z.object({
        frage: z.string().endsWith('?'),
        einleitung: z.string(),
        faktoren: z.array(karte).min(3),
      }),
      bild: image().optional(),
      bildAlt: z.string().min(10).optional(),
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
    seitentitel,
    beschreibung,
    h1: z.string(),
    einleitung: z.string(),
    ortsteile: z.array(z.string()).default([]),
    // Luftlinie vom Betrieb, gerundet
    entfernungKm: z.number().optional(),
    baumschutz: z.object({
      // satzung = Baumschutzsatzung bekannt, keine = keine Satzung, unklar = noch nicht geprüft
      status: z.enum(['satzung', 'keine', 'unklar']),
      stelle: z.string(),
      link: z.string().url(),
      // Datum der letzten Prüfung (JJJJ-MM-TT), leer = noch nicht geprüft
      geprueft: z.string().nullable().default(null),
    }),
  }),
});

const faq = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/inhalte/faq' }),
  schema: z.object({
    frage: z.string().endsWith('?', 'Eine Frage endet mit einem Fragezeichen.'),
    thema: z.enum(['genehmigung', 'kosten', 'nachbarn', 'haftung', 'ablauf', 'leistung']),
    // Auf welchen Leistungsseiten die Frage zusätzlich erscheint (Dateinamen aus src/inhalte/leistungen)
    leistungen: z.array(z.string()).default([]),
    aufFaqSeite: z.boolean().default(true),
    reihenfolge: z.number().int().default(50),
  }),
});

const referenzen = defineCollection({
  loader: glob({ pattern: '[^_]*/index.md', base: './src/inhalte/referenzen' }),
  schema: ({ image }) =>
    z.object({
      titel: z.string(),
      // Ort als Dateiname aus src/inhalte/orte (z. B. bornheim) oder als freier Text
      ort: z.string(),
      leistungen: z.array(z.string()).min(1),
      baumart: z.string(),
      aufgabe: z.string(),
      datum: z.string().regex(/^\d{4}-\d{2}$/, 'Datum als JJJJ-MM, z. B. 2026-09'),
      vorher: image().optional(),
      vorherAlt: z.string().min(10).optional(),
      nachher: image().optional(),
      nachherAlt: z.string().min(10).optional(),
      veroeffentlichen: z.boolean().default(false),
    }),
});

const seiten = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './src/inhalte/seiten' }),
  schema: z.object({
    seitentitel,
    beschreibung,
    kicker: z.string().optional(),
    h1: z.string(),
    einleitung: z.string(),
    karten: z.array(karte).default([]),
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

export const collections = { leistungen, orte, faq, referenzen, seiten, bewertungen, qualifikationen };
