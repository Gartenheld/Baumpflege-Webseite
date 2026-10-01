// Zentrale Betriebsdaten. Jede Angabe steht nur hier und wird überall auf der Website verwendet.
// Ändern: nur den Text zwischen den Anführungszeichen anpassen, Anführungszeichen und Kommas stehen lassen.
// Alles mit "PLATZHALTER" muss vor der Liveschaltung ersetzt werden.

export const betrieb = {
  name: 'Baumpflege Happe',
  unterzeile: 'Baumpflege · Baumfällung · Landschaftspflege',
  claim: 'Ihr Baumspezialist zwischen Köln und Bonn',
  inhaber: 'Heinrich Happe',
  rechtsform: 'Einzelunternehmen',

  adresse: {
    strasse: 'Schebenstraße 6',
    plz: '53332',
    ort: 'Bornheim',
    land: 'DE',
  },

  telefon: {
    // So wird die Nummer angezeigt:
    anzeige: 'PLATZHALTER Telefon',
    // So wird sie gewählt (international, ohne Leerzeichen), z. B. +4922221234567:
    link: '+490000000000',
  },
  whatsapp: {
    // Nummer international ohne + und ohne Leerzeichen, z. B. 491701234567:
    nummer: '490000000000',
    vorbelegterText: 'Guten Tag, ich habe eine Anfrage zu einem Baum:',
  },
  email: 'PLATZHALTER@example.com',

  // Erreichbarkeit für Telefon und Rückrufe:
  erreichbarkeit: 'PLATZHALTER Erreichbarkeitszeiten, z. B. Mo bis Fr 8 bis 17 Uhr',
  // Antwortzeit auf Anfragen (wird im Ablauf und am Formular genannt):
  antwortzeit: 'PLATZHALTER innerhalb von zwei Werktagen',

  ustId: 'PLATZHALTER USt-IdNr.',

  // Links zu den Profilen (leer lassen, wenn es das Profil nicht gibt):
  profile: {
    google: '',
    instagram: '',
    facebook: '',
  },
} as const;

// Schalter für Bereiche, die vorbereitet, aber noch nicht sichtbar sind.
export const schalter = {
  // Erst auf true setzen, wenn der Nachweis SKT-A vorliegt.
  // Bei false wird die Seite Seilklettertechnik nicht gebaut, nicht verlinkt und nicht in die Sitemap aufgenommen.
  seilklettertechnik: false,
} as const;
