// Fotos der Website. Jeder Eintrag ist ein fester Platz auf einer Seite.
//
// So kommt ein Foto auf die Website:
// 1. Foto in den Ordner src/bilder hochladen. Der Dateiname ist der Name des Platzes,
//    die Endung darf .jpg, .jpeg, .png oder .webp sein, z. B. src/bilder/startseite.jpg.
// 2. Hier beim selben Platz unter alt einen kurzen Satz eintragen, was auf dem Foto zu sehen ist.
//    Ohne alt-Text bricht der Build mit einem Hinweis ab, die alte Version bleibt online.
// Solange kein Foto da ist, steht an der Stelle ein Platzhalter mit dem Text unter zeigt.
// Die Website verkleinert die Fotos selbst und entfernt dabei Standortdaten (GPS).

export const fotos: Record<string, { zeigt: string; alt: string }> = {
  startseite: {
    zeigt: 'großes eigenes Foto, zum Beispiel Baumkrone bei der Arbeit',
    alt: '',
  },
  'ueber-uns': {
    zeigt: 'bei der Arbeit, mit Ausrüstung',
    alt: '',
  },
  'ueber-uns-ausstattung': {
    zeigt: 'Arbeitsfoto mit Hubarbeitsbühne oder Häcksler',
    alt: '',
  },
  gewerbe: {
    zeigt: 'gepflegte Bäume an einer Wohnanlage',
    alt: '',
  },
  // Leistungsseiten: Foto oben auf der Seite und, bei Schwerpunkten, auf der Karte in der Übersicht
  'leistung-baumpflege': {
    zeigt: 'Baumpflege',
    alt: 'Baumpfleger mit Helm im Korb einer Hubarbeitsbühne an der Krone eines Laubbaums',
  },
  'leistung-baumfaellung': {
    zeigt: 'Baumfällung',
    alt: 'Arbeit mit der Motorsäge im Wald: Schutzhelm mit Visier und Gehörschutz, Sägespäne fliegen im Gegenlicht',
  },
  'leistung-sturmschadenbeseitigung': { zeigt: 'Sturmschadenbeseitigung', alt: '' },
  'leistung-wurzelstockentfernung': { zeigt: 'Wurzelstockentfernung', alt: '' },
  'leistung-haeckselarbeiten': { zeigt: 'Häckselarbeiten', alt: '' },
  'leistung-landschaftspflege-heckenschnitt': { zeigt: 'Landschaftspflege und Heckenschnitt', alt: '' },
  'leistung-seilklettertechnik': { zeigt: 'Seilklettertechnik', alt: '' },
};
