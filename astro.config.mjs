// Astro-Konfiguration für die Website "Baumpflege Happe".
// Ergebnis ist eine rein statische Website im Ordner dist/, die per GitHub Actions zu Hostinger hochgeladen wird.
import { defineConfig, envField } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { satteri } from '@astrojs/markdown-satteri';

// Endgültige Adresse: https://baumpflege-happe.de (ohne www).
// In der Vorschau setzt GitHub Actions SITE_URL auf die temporäre Hostinger-Adresse
// (siehe docs/01-technik-und-deployment.md, Abschnitt 7).
const SITE_URL = process.env.SITE_URL || 'https://baumpflege-happe.de';

export default defineConfig({
  site: SITE_URL,
  // Jede Seite liegt als Ordner mit index.html vor, URLs enden immer mit "/".
  // Das passt zum Apache/LiteSpeed-Server bei Hostinger.
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  // Zwischenspeicher für optimierte Bilder außerhalb von node_modules, damit GitHub Actions ihn behalten kann.
  cacheDir: './.astro-cache',
  env: {
    schema: {
      // true für die Vorschau-Umgebung: Suchmaschinen werden ausgesperrt (robots.txt und noindex).
      PUBLIC_NOINDEX: envField.boolean({ context: 'client', access: 'public', default: false }),
    },
  },
  integrations: [
    sitemap({
      // Danke-Seite des Formulars gehört nicht in die Sitemap (sie trägt zusätzlich noindex).
      filter: (page) => !page.includes('/kontakt/danke/'),
    }),
  ],
  markdown: {
    // Keine Code-Hervorhebung nötig (verträgt sich nicht mit der Content-Security-Policy).
    syntaxHighlight: false,
    // Keine automatische Typografie: sonst würden aus "--" lange Gedankenstriche
    // und aus deutschen Anführungszeichen englische.
    processor: satteri({ features: { smartPunctuation: false } }),
  },
  security: {
    // Content-Security-Policy als <meta>-Element mit Hashes für Skripte und Styles.
    // Es werden keine fremden Server angesprochen: keine Google Fonts, keine CDNs, kein Tracking.
    csp: {
      directives: [
        "default-src 'self'",
        "img-src 'self' data:",
        "media-src 'self'",
        "font-src 'self'",
        "connect-src 'self'",
        "form-action 'self'",
        "base-uri 'self'",
        "object-src 'none'",
      ],
    },
  },
});
