// Hilfsfunktionen für Inhalte: welche Leistungen, Qualifikationen und Bewertungen sichtbar sind.
import { getCollection, getEntry } from 'astro:content';
import { PUBLIC_NOINDEX } from 'astro:env/client';

/** Bricht den Build ab, wenn eine Inhaltsart leer ist (z. B. Ordner versehentlich gelöscht). */
function nichtLeer<T>(liste: T[], ordner: string): T[] {
  if (liste.length === 0) throw new Error(`In src/inhalte/${ordner} wurde kein Eintrag gefunden.`);
  return liste;
}

/** Kennungen der Qualifikationen, die tatsächlich vorhanden sind. */
export async function vorhandeneQualifikationen() {
  const alle = await getCollection('qualifikationen', ({ data }) => data.vorhanden);
  return alle.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}

/** Qualifikationen, die ein Subunternehmer bei Bedarf stellt (vorhanden: false, partner: true). */
export async function partnerQualifikationen() {
  const alle = await getCollection('qualifikationen', ({ data }) => !data.vorhanden && data.partner);
  return alle.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}

/** Leistungen, deren benötigte Qualifikation vorhanden ist (z. B. Seilklettertechnik erst mit SKT-A). */
export async function sichtbareLeistungen() {
  const vorhanden = new Set((await vorhandeneQualifikationen()).map((q) => q.id));
  const alle = nichtLeer(await getCollection('leistungen', ({ data }) => !data.benoetigt || vorhanden.has(data.benoetigt)), 'leistungen');
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
  const alle = nichtLeer(await getCollection('orte'), 'orte');
  return alle.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}

export const leistungsUrl = (id: string) => `/leistungen/${id}/`;
export const ortUrl = (id: string) => `/einsatzgebiet/${id}/`;

/** Referenzen: live nur freigegebene, in der Vorschau auch Platzhalter. Optional nach Ort gefiltert. */
export async function sichtbareReferenzen(ort?: string) {
  const alle = (await getCollection('referenzen', ({ data }) => !ort || data.ort === ort)).sort((a, b) =>
    b.data.datum.localeCompare(a.data.datum),
  );
  const freigegeben = alle.filter((r) => r.data.veroeffentlichen);
  return { liste: freigegeben.length > 0 || !PUBLIC_NOINDEX ? freigegeben : alle, nurPlatzhalter: freigegeben.length === 0 };
}

const THEMEN = ['genehmigung', 'kosten', 'nachbarn', 'haftung', 'ablauf', 'leistung'] as const;
export const themenTitel: Record<(typeof THEMEN)[number], string> = {
  genehmigung: 'Fällgenehmigung und Schonzeit',
  kosten: 'Kosten und Abrechnung',
  nachbarn: 'Nachbarbäume und überhängende Äste',
  haftung: 'Haftung und Verkehrssicherungspflicht',
  ablauf: 'Anfrage und Ablauf',
  leistung: 'Zu unseren Leistungen',
};
const themaRang = (t: string) => THEMEN.indexOf(t as (typeof THEMEN)[number]);

/** Fragen, die auf einer Leistungsseite erscheinen: erst die zur Leistung, dann allgemeine Themen. */
export async function faqFuerLeistung(id: string) {
  const alle = await getCollection('faq', ({ data }) => data.leistungen.includes(id));
  return alle.sort(
    (a, b) =>
      Number(b.data.thema === 'leistung') - Number(a.data.thema === 'leistung') ||
      themaRang(a.data.thema) - themaRang(b.data.thema) ||
      a.data.reihenfolge - b.data.reihenfolge,
  );
}

/** Fragen für die FAQ-Seite, gruppiert nach Thema. */
export async function faqNachThema() {
  const alle = await getCollection('faq', ({ data }) => data.aufFaqSeite);
  return THEMEN.map((thema) => ({
    thema,
    titel: themenTitel[thema],
    fragen: alle.filter((f) => f.data.thema === thema).sort((a, b) => a.data.reihenfolge - b.data.reihenfolge),
  })).filter((g) => g.fragen.length > 0);
}

/** Fragen zu bestimmten Themen (z. B. Haftung auf der Gewerbe-Seite). */
export async function faqZuThemen(themen: string[]) {
  const alle = await getCollection('faq', ({ data }) => themen.includes(data.thema));
  return alle.sort((a, b) => themaRang(a.data.thema) - themaRang(b.data.thema) || a.data.reihenfolge - b.data.reihenfolge);
}

export async function seite(id: string) {
  const eintrag = await getEntry('seiten', id);
  if (!eintrag) throw new Error(`Seitentext src/inhalte/seiten/${id}.md fehlt.`);
  return eintrag;
}
