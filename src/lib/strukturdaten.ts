// Strukturierte Daten (JSON-LD) für Suchmaschinen. Alle Angaben kommen aus src/config/betrieb.ts
// und den Inhalten, damit Name, Anschrift und Telefon überall gleich sind.
// Bewusst ohne Bewertungssterne, Preise und Öffnungszeiten (Begründung: docs/01, Abschnitt 11.1).
import type { CollectionEntry } from 'astro:content';
import { betrieb } from '../config/betrieb';

type Knoten = Record<string, unknown>;

export const betriebId = (site: URL) => new URL('/#betrieb', site).href;

const stadt = (name: string) => ({ '@type': 'City', name });

// Fachbegriffe, unter denen Kunden die Leistungen suchen (ergänzt die Leistungsnamen)
const FACHBEGRIFFE = [
  'Baumschnitt', 'Kronenpflege', 'Totholzentfernung', 'Kroneneinkürzung', 'Lichtraumprofilschnitt',
  'Problemfällung', 'Hubarbeitsbühne', 'Baumstumpf entfernen', 'Heckenschnitt',
];

/** Der Betrieb und die Website, auf jeder Seite. Leistungen als Name und Adresse der Leistungsseite. */
export function grunddaten(site: URL, leistungen: { name: string; url: string }[], orte: string[]): Knoten[] {
  const profile = Object.values(betrieb.profile).filter((p) => p !== '');
  return [
    {
      '@type': 'HomeAndConstructionBusiness',
      '@id': betriebId(site),
      name: betrieb.name,
      slogan: betrieb.claim,
      description: `${betrieb.unterzeile.replaceAll(' · ', ', ')}. ${betrieb.claim}.`,
      url: new URL('/', site).href,
      logo: { '@type': 'ImageObject', url: new URL('/logo.png', site).href, width: 600, height: 600 },
      image: new URL('/og-standard.jpg', site).href,
      telephone: betrieb.telefon.link,
      email: betrieb.email,
      address: {
        '@type': 'PostalAddress',
        streetAddress: betrieb.adresse.strasse,
        postalCode: betrieb.adresse.plz,
        addressLocality: betrieb.adresse.ort,
        addressRegion: 'Nordrhein-Westfalen',
        addressCountry: betrieb.adresse.land,
      },
      contactPoint: {
        '@type': 'ContactPoint',
        contactType: 'customer service',
        telephone: betrieb.telefon.link,
        email: betrieb.email,
        availableLanguage: 'de',
      },
      areaServed: orte.map(stadt),
      knowsAbout: [...leistungen.map((l) => l.name), ...FACHBEGRIFFE],
      hasOfferCatalog: {
        '@type': 'OfferCatalog',
        name: 'Leistungen',
        itemListElement: leistungen.map((l) => ({
          '@type': 'Offer',
          itemOffered: { '@type': 'Service', name: l.name, url: new URL(l.url, site).href },
        })),
      },
      ...(profile.length > 0 ? { sameAs: profile } : {}),
    },
    {
      '@type': 'WebSite',
      '@id': new URL('/#website', site).href,
      url: new URL('/', site).href,
      name: betrieb.name,
      inLanguage: 'de',
      publisher: { '@id': betriebId(site) },
    },
  ];
}

/** Eine Leistung, angeboten im ganzen Einsatzgebiet oder in einem Ort. */
export function dienstleistung(site: URL, url: string, name: string, art: string, beschreibung: string, orte: string[]): Knoten {
  return {
    '@type': 'Service',
    name,
    serviceType: art,
    description: beschreibung,
    url: new URL(url, site).href,
    provider: { '@id': betriebId(site) },
    areaServed: orte.map(stadt),
  };
}

/** Häufige Fragen mit Antworten (nur auf /faq/, damit keine Frage doppelt ausgezeichnet ist). */
export function fragenSeite(fragen: CollectionEntry<'faq'>[]): Knoten {
  return {
    '@type': 'FAQPage',
    mainEntity: fragen.map((f) => ({
      '@type': 'Question',
      name: f.data.frage,
      acceptedAnswer: { '@type': 'Answer', text: (f.rendered?.html ?? f.body ?? '').trim() },
    })),
  };
}

/** Brotkrumen als Liste vom Start bis zur aktuellen Seite. */
export function brotkrumen(site: URL, eintraege: { titel: string; url: string }[]): Knoten {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: eintraege.map((e, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: e.titel,
      item: new URL(e.url, site).href,
    })),
  };
}

/** JSON für ein script-Element, ohne dass Text wie "</script>" das Element beenden kann. */
export function alsJson(knoten: Knoten[]): string {
  return JSON.stringify({ '@context': 'https://schema.org', '@graph': knoten }).replace(/</g, '\\u003c');
}
