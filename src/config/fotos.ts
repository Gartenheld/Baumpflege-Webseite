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
    zeigt: 'großes eigenes Foto, zum Beispiel Arbeit in einer Baumkrone',
    alt: '',
  },
  'ueber-uns': {
    zeigt: 'Monogramm von Baumpflege Happe (freigestellt, transparenter Hintergrund)',
    alt: 'Monogramm von Baumpflege Happe: ein H mit goldenen Blattlinien',
  },
  'ueber-uns-ausstattung': {
    zeigt: 'Arbeitsfoto mit Hubarbeitsbühne oder Häcksler',
    alt: '',
  },
  gewerbe: {
    zeigt: 'gepflegte Bäume, z. B. eine Allee oder Bäume an einer Wohnanlage',
    alt: 'Allee aus in Form geschnittenen Bäumen, ein breiter Kiesweg führt zwischen den grünen Baumwänden auf ein Schloss zu',
  },
  // Leistungsseiten: Foto oben auf der Seite und, bei Schwerpunkten, auf der Karte in der Übersicht
  'leistung-baumpflege': {
    zeigt: 'Baumpflege',
    alt: 'Baumpfleger mit Helm im Korb einer Hubarbeitsbühne an der Krone eines Laubbaums',
  },
  'leistung-baumfaellung': {
    zeigt: 'Baumfällung',
    alt: 'Baumkletterer am Seil trägt einen Stamm von oben Stück für Stück ab, Sägespäne fliegen durch die Luft',
  },
  'leistung-sturmschadenbeseitigung': {
    zeigt: 'Sturmschadenbeseitigung',
    alt: 'Vom Sturm entwurzelte Kiefer liegt mit aufgerissenem Wurzelballen auf einer Rasenfläche',
  },
  'leistung-wurzelstockentfernung': {
    zeigt: 'Wurzelstockentfernung',
    alt: 'Symbolbild, mit KI erstellt: Stubbenfräse auf Raupenketten fräst in einem Garten einen Baumstumpf aus dem Boden',
  },
  'leistung-haeckselarbeiten': {
    zeigt: 'Häckselarbeiten',
    alt: 'Symbolbild, mit KI erstellt: Häcksler mit Einzugstrichter und Auswurf, dahinter ein Kastenanhänger',
  },
  'leistung-landschaftspflege-heckenschnitt': {
    zeigt: 'Landschaftspflege und Heckenschnitt',
    alt: 'Mit KI bearbeitetes Foto: Baumpfleger mit Helm, Gehörschutz und Klettergurt in einem winterlichen Garten, daneben Schnittgut und Werkzeug',
  },
  'leistung-seilklettertechnik': {
    zeigt: 'Seilklettertechnik',
    alt: 'Baumkletterer mit Helm und Klettergurt hängt am Seil neben dem Stamm einer Kiefer',
  },
};
