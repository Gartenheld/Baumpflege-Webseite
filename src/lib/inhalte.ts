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

/** Qualifikationen, die nicht selbst vorhanden sind, deren Leistung aber angeboten wird (beiBedarf: true). */
export async function qualifikationenBeiBedarf() {
  const alle = await getCollection('qualifikationen', ({ data }) => !data.vorhanden && data.beiBedarf);
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

const THEMEN = ['genehmigung', 'baum', 'kosten', 'nachbarn', 'haftung', 'ablauf', 'leistung'] as const;
export const themenTitel: Record<(typeof THEMEN)[number], string> = {
  genehmigung: 'Fällgenehmigung und Schonzeit',
  baum: 'Rund um Ihren Baum',
  kosten: 'Kosten und Abrechnung',
  nachbarn: 'Nachbarn, Grenzbäume und überhängende Äste',
  haftung: 'Haftung und Verkehrssicherungspflicht',
  ablauf: 'Anfrage und Ablauf',
  leistung: 'Zu unseren Leistungen',
};
const themaRang = (t: string) => THEMEN.indexOf(t as (typeof THEMEN)[number]);
type Thema = (typeof THEMEN)[number];

/** Kurze Namen der Themen für Verzeichnis und Sprungmarken auf der FAQ-Seite. */
export const themenKurz: Record<Thema, string> = {
  ablauf: 'Anfrage und Ablauf',
  kosten: 'Kosten',
  leistung: 'Leistungen',
  baum: 'Ihr Baum',
  genehmigung: 'Genehmigung und Schonzeit',
  nachbarn: 'Nachbarn',
  haftung: 'Haftung',
};

/** Ein Satz unter jeder Themenüberschrift auf der FAQ-Seite. */
export const themenEinleitung: Record<Thema, string> = {
  ablauf: 'Von der ersten Nachricht bis zum aufgeräumten Grundstück: So arbeiten wir mit Ihnen zusammen.',
  kosten: 'Worauf es beim Preis ankommt und was Ihr Angebot enthält.',
  leistung: 'Fragen zu den einzelnen Arbeiten, geordnet nach Leistung.',
  baum: 'Zustand, Schnitt und Pflege: Antworten rund um Ihren Baum.',
  genehmigung: 'Wann eine Genehmigung nötig ist und was in der Schonzeit gilt.',
  nachbarn: 'Was gilt, wenn ein Baum an der Grenze steht oder Äste hinüberragen.',
  haftung: 'Verkehrssicherungspflicht und Haftung für Eigentümer, Hausverwaltungen und Gewerbe.',
};

/** Reihenfolge der Themen auf der FAQ-Seite: erst Praktisches, dann Fachliches, dann Rechtliches. */
const SEITENTHEMEN: Thema[] = ['ablauf', 'kosten', 'leistung', 'baum', 'genehmigung', 'nachbarn', 'haftung'];

/**
 * Alle Fragen für die FAQ-Seite, nach Themen gegliedert. Die Fragen zu einzelnen Leistungen
 * (thema: leistung) stehen dort unter der jeweiligen Leistung, maßgeblich ist die erste in `leistungen`.
 */
export async function faqSeite() {
  const alle = await getCollection('faq', ({ data }) => data.aufFaqSeite);
  const leistungen = await sichtbareLeistungen();
  const nachReihenfolge = <T extends { data: { reihenfolge: number } }>(l: T[]) => l.sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
  return SEITENTHEMEN.map((thema) => {
    const fragen = nachReihenfolge(alle.filter((f) => f.data.thema === thema));
    const unter =
      thema === 'leistung'
        ? leistungen
            .map((l) => ({ id: l.id, titel: l.data.titel, fragen: fragen.filter((f) => f.data.leistungen[0] === l.id) }))
            .filter((u) => u.fragen.length > 0)
        : [];
    return {
      thema,
      titel: themenTitel[thema],
      kurz: themenKurz[thema],
      einleitung: themenEinleitung[thema],
      fragen: unter.length > 0 ? unter.flatMap((u) => u.fragen) : fragen,
      unter,
    };
  }).filter((g) => g.fragen.length > 0);
}

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

/** Fragen nach Thema gruppiert (z. B. für die Seite Kosten). */
export async function faqNachThema() {
  const alle = await getCollection('faq', ({ data }) => data.aufFaqSeite);
  return THEMEN.map((thema) => ({
    thema,
    titel: themenTitel[thema],
    fragen: alle.filter((f) => f.data.thema === thema).sort((a, b) => a.data.reihenfolge - b.data.reihenfolge),
  })).filter((g) => g.fragen.length > 0);
}

/** Fragen für die Seite Gewerbe und Hausverwaltungen: alle zur Haftung und die mit "gewerbe: true". */
export async function faqFuerGewerbe() {
  const alle = await getCollection('faq', ({ data }) => data.thema === 'haftung' || data.gewerbe);
  return alle.sort((a, b) => themaRang(a.data.thema) - themaRang(b.data.thema) || a.data.reihenfolge - b.data.reihenfolge);
}

export async function seite(id: string) {
  const eintrag = await getEntry('seiten', id);
  if (!eintrag) throw new Error(`Seitentext src/inhalte/seiten/${id}.md fehlt.`);
  return eintrag;
}
