import type { APIRoute } from 'astro';
import { site } from '@/data/site';

export const GET: APIRoute = () =>
  new Response(
    `User-agent: *
Allow: /
Disallow: /api/
Disallow: /grazie/
Disallow: /en/thank-you/

Sitemap: ${site.url}/sitemap.xml
`,
    { headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
  );
