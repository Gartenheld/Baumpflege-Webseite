// Hilfsfunktionen für Inhalte: welche Leistungen, Qualifikationen und Bewertungen sichtbar sind.
import { getCollection } from 'astro:content';
import { PUBLIC_NOINDEX } from 'astro:env/client';

/** Kennungen der Qualifikationen, die tatsächlich vorhanden sind. */
export async function vorhandeneQualifikationen() {
  const alle = await getCollection('qualifikationen', ({ data }) => data.vorhanden);
  return alle.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}

/** Leistungen, deren benötigte Qualifikation vorhanden ist (z. B. Seilklettertechnik erst mit SKT-A). */
export async function sichtbareLeistungen() {
  const vorhanden = new Set((await vorhandeneQualifikationen()).map((q) => q.id));
  const alle = await getCollection('leistungen', ({ data }) => !data.benoetigt || vorhanden.has(data.benoetigt));
  return alle.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}

/**
 * Bewertungen für die Website: auf der Live-Seite nur freigegebene,
 * in der Vorschau zusätzlich die Platzhalter, damit man das Layout sieht.
 */
export async function sichtbareBewertungen() {
  const alle = await getCollection('bewertungen');
  const freigegeben = alle.filter((b) => b.data.veroeffentlichen);
  return { liste: freigegeben.length > 0 || !PUBLIC_NOINDEX ? freigegeben : alle, nurPlatzhalter: freigegeben.length === 0 };
}

export async function orteSortiert() {
  const alle = await getCollection('orte');
  return alle.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}

export const leistungsUrl = (id: string) => `/leistungen/${id}/`;
export const ortUrl = (id: string) => `/einsatzgebiet/${id}/`;
