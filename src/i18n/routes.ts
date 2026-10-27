/**
 * Central route map. Every static page has an Italian (default, root) and an
 * English (/en/) URL. Navigation, the language switcher, hreflang tags and the
 * sitemap are all generated from this single table.
 */
export type Lang = 'it' | 'en';
export const LANGS: Lang[] = ['it', 'en'];
export const DEFAULT_LANG: Lang = 'it';

export const routes = {
  home: { it: '/', en: '/en/' },
  bars: { it: '/banchi-bar/', en: '/en/bars/' },
  services: { it: '/servizi/', en: '/en/services/' },
  partners: { it: '/wedding-planner-location/', en: '/en/wedding-planners-venues/' },
  about: { it: '/chi-siamo/', en: '/en/about/' },
  ice: { it: '/noleggio-ghiaccio/', en: '/en/ice-rental/' },
  contact: { it: '/contatti/', en: '/en/contact/' },
  thanks: { it: '/grazie/', en: '/en/thank-you/' },
  privacy: { it: '/privacy-policy/', en: '/en/privacy-policy/' },
  cookies: { it: '/cookie-policy/', en: '/en/cookie-policy/' },
} as const satisfies Record<string, Record<Lang, string>>;

export type RouteKey = keyof typeof routes;

/** Localised path for a static route, optionally with a hash. */
export function url(key: RouteKey, lang: Lang, hash?: string): string {
  return routes[key][lang] + (hash ? `#${hash}` : '');
}

export type Alternates = Record<Lang, string>;

export function alternatesFor(key: RouteKey): Alternates {
  return { ...routes[key] };
}
