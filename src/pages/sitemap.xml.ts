/**
 * XML sitemap with hreflang alternates, generated from the route map.
 * Noindex pages (thank-you, legal pages) are excluded.
 */
import type { APIRoute } from 'astro';
import { routes, type Lang, type RouteKey } from '@/i18n/routes';
import { site } from '@/data/site';

const EXCLUDE: RouteKey[] = ['thanks', 'privacy', 'cookies'];

export const GET: APIRoute = () => {
  const groups: Record<Lang, string>[] = [];
  (Object.keys(routes) as RouteKey[]).filter((k) => !EXCLUDE.includes(k)).forEach((k) => groups.push({ ...routes[k] }));

  const abs = (p: string) => `${site.url}${p}`;
  const today = new Date().toISOString().slice(0, 10);
  const urls = groups
    .flatMap((g) =>
      (Object.keys(g) as Lang[]).map(
        (lang) => `  <url>
    <loc>${abs(g[lang])}</loc>
    <lastmod>${today}</lastmod>
    <xhtml:link rel="alternate" hreflang="it" href="${abs(g.it)}"/>
    <xhtml:link rel="alternate" hreflang="en" href="${abs(g.en)}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="${abs(g.en)}"/>
  </url>`,
      ),
    )
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls}
</urlset>
`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
