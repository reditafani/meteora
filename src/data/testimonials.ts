import type { Localized } from '@/i18n/ui';

/**
 * TESTIMONIALS — intentionally empty.
 * Add only authentic reviews, with the author's permission. The Testimonial
 * section renders nothing while this list is empty.
 *
 * Example:
 * { quote: { it: '…', en: '…' }, author: 'Name Surname', role: { it: 'Sposi, Chianti 2025', en: 'Couple, Chianti 2025' } }
 */
export interface Testimonial {
  quote: Localized;
  author: string;
  role?: Localized;
}

export const testimonials: Testimonial[] = [];
