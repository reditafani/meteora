/**
 * Central route map. Every static page has an English (default, root) and an
 * Italian (/it/) URL. Navigation, the language switcher, hreflang tags and the
 * sitemap are all generated from this single table.
 */
export type Lang = 'it' | 'en';
export const LANGS: Lang[] = ['it', 'en']; // display order of the language switcher (IT / EN)
export const DEFAULT_LANG: Lang = 'en';

export const routes = {
  home: { it: '/it/', en: '/' },
  bars: { it: '/it/banchi-bar/', en: '/bars/' },
  services: { it: '/it/servizi/', en: '/services/' },
  partners: { it: '/it/wedding-planner-location/', en: '/wedding-planners-venues/' },
  about: { it: '/it/chi-siamo/', en: '/about/' },
  ice: { it: '/it/noleggio-ghiaccio/', en: '/ice-rental/' },
  contact: { it: '/it/contatti/', en: '/contact/' },
  thanks: { it: '/it/grazie/', en: '/thank-you/' },
  privacy: { it: '/it/privacy-policy/', en: '/privacy-policy/' },
  cookies: { it: '/it/cookie-policy/', en: '/cookie-policy/' },
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
