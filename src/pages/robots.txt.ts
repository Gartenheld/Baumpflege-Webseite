// Erzeugt /robots.txt. In der Vorschau-Umgebung (PUBLIC_NOINDEX=true) wird alles gesperrt.
import type { APIRoute } from 'astro';
import { PUBLIC_NOINDEX } from 'astro:env/client';

export const GET: APIRoute = ({ site }) => {
  const sitemap = new URL('sitemap-index.xml', site).href;
  const body = PUBLIC_NOINDEX
    ? 'User-agent: *\nDisallow: /\n'
    : `User-agent: *\nDisallow: /kontakt/danke/\n\nSitemap: ${sitemap}\n`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
