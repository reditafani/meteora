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
  weddings: { it: '/matrimoni/', en: '/en/weddings/' },
  destination: { it: '/destination-wedding-italia/', en: '/en/destination-weddings-italy/' },
  bars: { it: '/banchi-bar/', en: '/en/bars/' },
  cocktails: { it: '/cocktail-experience/', en: '/en/cocktail-experience/' },
  services: { it: '/servizi/', en: '/en/services/' },
  corporate: { it: '/eventi-aziendali-privati/', en: '/en/corporate-private-events/' },
  partners: { it: '/wedding-planner-location/', en: '/en/wedding-planners-venues/' },
  events: { it: '/eventi/', en: '/en/events/' },
  about: { it: '/chi-siamo/', en: '/en/about/' },
  why: { it: '/perche-meteora/', en: '/en/why-meteora/' },
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

/** Detail-page bases for data-driven collections. */
export const collectionBase = {
  bars: routes.bars,
  events: routes.events,
} as const;

export type Alternates = Record<Lang, string>;

export function alternatesFor(key: RouteKey): Alternates {
  return { ...routes[key] };
}
