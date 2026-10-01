import { site } from '@/data/site';
import type { Lang } from '@/i18n/routes';
import { routes } from '@/i18n/routes';
import type { FaqItem } from '@/data/faq';

export const abs = (path: string) => new URL(path, site.url + '/').toString();

const orgId = `${site.url}/#organization`;

/** Organization + LocalBusiness. Only facts from the brochure; no street address, no ratings. */
export function organizationSchema(lang: Lang) {
  return {
    '@context': 'https://schema.org',
    '@type': ['Organization', 'LocalBusiness'],
    '@id': orgId,
    name: site.name,
    slogan: site.tagline,
    url: abs(routes.home[lang]),
    logo: abs('/images/logo-meteora-events.png'),
    image: abs('/images/og/meteora-events.jpg'),
    email: site.email,
    telephone: site.phoneE164,
    address: {
      '@type': 'PostalAddress',
      addressLocality: site.address.locality,
      postalCode: site.address.postalCode,
      addressRegion: lang === 'it' ? site.address.region : site.address.regionEn,
      addressCountry: site.address.country,
    },
    areaServed: [
      { '@type': 'AdministrativeArea', name: lang === 'it' ? 'Toscana' : 'Tuscany' },
      { '@type': 'Country', name: lang === 'it' ? 'Italia' : 'Italy' },
    ],
    sameAs: [site.instagram.url],
    description:
      lang === 'it'
        ? 'Bar catering luxury per matrimoni, destination wedding, eventi aziendali e privati. Base a Montecatini Terme, in Toscana; operativi in tutta Italia e all’estero.'
        : 'Luxury bar catering for weddings, destination weddings, corporate and private events. Based in Montecatini Terme, Tuscany; serving events throughout Italy and abroad.',
    knowsLanguage: ['it', 'en'],
  };
}

export function websiteSchema(lang: Lang) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${site.url}/#website`,
    url: abs(routes.home[lang]),
    name: site.name,
    inLanguage: lang === 'it' ? 'it-IT' : 'en',
    publisher: { '@id': orgId },
  };
}

export function serviceSchema(opts: { name: string; description: string; url: string; serviceType: string; lang: Lang; area?: string[] }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Service',
    name: opts.name,
    serviceType: opts.serviceType,
    description: opts.description,
    url: abs(opts.url),
    provider: { '@id': orgId },
    areaServed: (opts.area ?? [opts.lang === 'it' ? 'Italia' : 'Italy']).map((name) => ({ '@type': 'Place', name })),
    inLanguage: opts.lang === 'it' ? 'it-IT' : 'en',
  };
}

export function faqSchema(items: FaqItem[], lang: Lang) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map((f) => ({
      '@type': 'Question',
      name: f.q[lang],
      acceptedAnswer: { '@type': 'Answer', text: f.a[lang] },
    })),
  };
}

export interface Crumb {
  name: string;
  href: string;
}

export function breadcrumbSchema(crumbs: Crumb[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((c, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: c.name,
      item: abs(c.href),
    })),
  };
}
