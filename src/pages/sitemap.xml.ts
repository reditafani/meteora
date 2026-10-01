/**
 * XML sitemap with hreflang alternates, generated from the route map and the
 * data collections. Noindex pages (drafts, legal drafts, thank-you) are excluded.
 */
import type { APIRoute } from 'astro';
import { routes, type Lang, type RouteKey } from '@/i18n/routes';
import { availableBars } from '@/data/bars';
import { events } from '@/data/events';
import { landingDestinations } from '@/data/destinations';
import { site } from '@/data/site';

const EXCLUDE: RouteKey[] = ['thanks', 'privacy', 'cookies'];

export const GET: APIRoute = () => {
  const groups: Record<Lang, string>[] = [];
  (Object.keys(routes) as RouteKey[]).filter((k) => !EXCLUDE.includes(k)).forEach((k) => groups.push({ ...routes[k] }));
  availableBars.forEach((b) => groups.push({ it: `${routes.bars.it}${b.slug}/`, en: `${routes.bars.en}${b.slug}/` }));
  events.filter((e) => !e.draft).forEach((e) => groups.push({ it: `${routes.events.it}${e.slug.it}/`, en: `${routes.events.en}${e.slug.en}/` }));
  landingDestinations.forEach((d) => groups.push({ it: `/${d.landing!.slug.it}/`, en: `/en/${d.landing!.slug.en}/` }));

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
    <xhtml:link rel="alternate" hreflang="x-default" href="${abs(g.it)}"/>
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
