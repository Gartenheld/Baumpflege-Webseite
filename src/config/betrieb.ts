// Zentrale Betriebsdaten. Jede Angabe steht nur hier und wird überall auf der Website verwendet.
// Ändern: nur den Text zwischen den Anführungszeichen anpassen, Anführungszeichen und Kommas stehen lassen.
// Alles mit "Platzhalter" muss vor der Liveschaltung ersetzt werden.

export const betrieb = {
  name: 'Baumpflege Happe',
  unterzeile: 'Baumpflege · Baumfällung · Landschaftspflege',
  claim: 'Ihr Baumspezialist zwischen Köln und Bonn',
  inhaber: 'Heinrich Happe',
  rechtsform: 'Einzelunternehmen',
  domain: 'baumpflege-happe.de',

  adresse: {
    strasse: 'Schebenstraße 6',
    plz: '53332',
    ort: 'Bornheim',
    land: 'DE',
  },

  telefon: {
    // So wird die Nummer angezeigt:
    anzeige: '[Platzhalter Telefon]',
    // So wird sie gewählt (international, ohne Leerzeichen), z. B. +4922221234567:
    link: '+490000000000',
  },
  whatsapp: {
    // Nummer international ohne + und ohne Leerzeichen, z. B. 491701234567:
    nummer: '490000000000',
    vorbelegterText: 'Guten Tag, ich habe eine Anfrage zu einem Baum:',
  },
  email: '[Platzhalter]@baumpflege-happe.de',

  // Erreichbarkeit für Telefon und Rückrufe:
  erreichbarkeit: '[Platzhalter: Mo bis Fr 8 bis 17 Uhr]',
  // Antwortzeit auf Anfragen (wird im Ablauf und am Formular genannt):
  antwortzeit: '[Platzhalter: innerhalb von zwei Werktagen]',

  ustId: '[Platzhalter USt-IdNr.]',

  // Google-Bewertungen (Werte aus dem Google-Unternehmensprofil übernehmen):
  bewertungen: {
    durchschnitt: '[Platzhalter: 4,9]',
    anzahl: '[Platzhalter: Anzahl]',
    stand: '[Platzhalter: Monat Jahr]',
  },

  // Links zu den Profilen (leer lassen, wenn es das Profil nicht gibt):
  profile: {
    google: '',
    instagram: '',
    facebook: '',
  },
} as const;

export const telefonLink = `tel:${betrieb.telefon.link}`;
export const whatsappLink = `https://wa.me/${betrieb.whatsapp.nummer}?text=${encodeURIComponent(betrieb.whatsapp.vorbelegterText)}`;
export const mailLink = `mailto:${betrieb.email}`;

// Die Seite Seilklettertechnik erscheint erst, wenn in src/inhalte/qualifikationen/skt-a.yaml
// "vorhanden: true" steht (siehe src/lib/inhalte.ts).
