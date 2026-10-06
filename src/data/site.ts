/**
 * Company facts. Everything here comes from the Meteora Events brochure.
 * Do not add street addresses, VAT numbers or legal names until the client supplies them.
 */
export const site = {
  name: 'Meteora Events',
  tagline: 'Luxury Open Bar Catering & Hospitality Services',
  url: (import.meta.env.PUBLIC_SITE_URL || 'https://meteoraevents.com').replace(/\/$/, ''),
  email: 'info@meteoraevents.com',
  phoneDisplay: '+39 328 064 2479',
  phoneE164: '+393280642479',
  whatsapp: import.meta.env.PUBLIC_WHATSAPP_NUMBER || '393280642479',
  instagram: {
    handle: '@meteoraevents',
    url: 'https://www.instagram.com/meteoraevents/',
  },
  address: {
    street: 'Via Nofretti 21',
    locality: 'Montecatini Terme',
    postalCode: '51016',
    province: 'PT',
    region: 'Toscana',
    regionEn: 'Tuscany',
    country: 'IT',
  },
  yearsExperience: 14,
  formEndpoint: import.meta.env.PUBLIC_FORM_ENDPOINT || '/api/send.php',
  analytics: {
    ga4: import.meta.env.PUBLIC_GA4_ID || '',
    gtm: import.meta.env.PUBLIC_GTM_ID || '',
    metaPixel: import.meta.env.PUBLIC_META_PIXEL_ID || '',
  },
  /**
   * TODO(client): legal entity details for the footer and legal pages
   * (ragione sociale, P.IVA, sede legale). Leave empty until supplied.
   */
  legal: {
    companyName: 'Meteora Events',
    vatNumber: '02132520475',
    registeredOffice: 'Via Nofretti 21, Montecatini Terme (PT)',
  },
} as const;

export function whatsappLink(message: string): string {
  return `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(message)}`;
}
