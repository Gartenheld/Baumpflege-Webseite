// Social-Media-Profile aus src/config/betrieb.ts für Fußbereich und Kontaktseite.
// Ohne Adresse: in der Vorschau als Hinweis „Link folgt“, auf der Live-Seite ausgeblendet.
import { PUBLIC_NOINDEX } from 'astro:env/client';
import { betrieb } from '../config/betrieb';

export interface Profil {
  name: 'Instagram' | 'Facebook';
  icon: 'instagram' | 'facebook';
  href: string;
}

export function socialProfile(): Profil[] {
  const alle: Profil[] = [
    { name: 'Instagram', icon: 'instagram', href: betrieb.profile.instagram },
    { name: 'Facebook', icon: 'facebook', href: betrieb.profile.facebook },
  ];
  return alle.filter((p) => p.href !== '' || PUBLIC_NOINDEX);
}
