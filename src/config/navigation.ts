// Hauptmenü und Links im Fuß. Reihenfolge hier ändern, dann überall gleich.
export const hauptmenue = [
  { titel: 'Leistungen', href: '/leistungen/' },
  { titel: 'Gewerbe', href: '/gewerbe-hausverwaltungen/' },
  { titel: 'Einsatzgebiet', href: '/einsatzgebiet/' },
  { titel: 'Referenzen', href: '/referenzen/' },
  { titel: 'Über uns', href: '/ueber-uns/' },
] as const;

export const fussmenue = [
  { titel: 'Gewerbe und Hausverwaltungen', href: '/gewerbe-hausverwaltungen/' },
  { titel: 'Einsatzgebiet', href: '/einsatzgebiet/' },
  { titel: 'Referenzen', href: '/referenzen/' },
  { titel: 'Über uns', href: '/ueber-uns/' },
  { titel: 'Häufige Fragen', href: '/faq/' },
  { titel: 'Kontakt und Anfrage', href: '/kontakt/' },
] as const;

export const rechtliches = [
  { titel: 'Impressum', href: '/impressum/' },
  { titel: 'Datenschutz', href: '/datenschutz/' },
] as const;
