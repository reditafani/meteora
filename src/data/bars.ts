import type { ImageMetadata } from 'astro';
import type { Localized } from '@/i18n/ui';
import goldenMirror from '@/assets/images/bars/golden-mirror.jpg';
import goldenMirrorSunset from '@/assets/images/bars/golden-mirror-sunset.jpg';
import silverReflection from '@/assets/images/bars/silver-reflection.jpg';
import pureWhiteVilla from '@/assets/images/bars/pure-white-villa.jpg';

/**
 * THE BAR COLLECTION
 * Names, descriptions and sizes come from the brochure ("I nostri banchi").
 * To add a bar: add an image to src/assets/images/bars/, import it above and
 * append an entry. Set `status: 'available'` to publish its detail page.
 */
export interface Bar {
  slug: string;
  name: string;
  status: 'available' | 'coming-soon';
  /** Tone used for the typographic panel when no photograph exists yet. */
  swatch: string;
  images: { src: ImageMetadata; alt: Localized }[];
  mood: Localized;
  description: Localized;
  idealFor: Localized<string[]>;
}

export const barSizes = [
  { name: 'Slim', length: '1,5 m', lengthEn: '1.5 m' },
  { name: 'Medium', length: '3,5 m', lengthEn: '3.5 m' },
  { name: 'Large', length: '5,5 m', lengthEn: '5.5 m' },
];

export const bars: Bar[] = [
  {
    slug: 'golden-mirror',
    name: 'Golden Mirror',
    status: 'available',
    swatch: '#b89e72',
    images: [
      {
        src: goldenMirrorSunset,
        alt: {
          it: 'Banco bar Golden Mirror al tramonto su una terrazza affacciata sulle colline',
          en: 'Golden Mirror bar at sunset on a terrace overlooking the hills',
        },
      },
      {
        src: goldenMirror,
        alt: {
          it: 'Dettaglio frontale del banco Golden Mirror con bottigliera completa e vetri pronti',
          en: 'Front view of the Golden Mirror bar with a full back bar and glassware ready',
        },
      },
    ],
    mood: { it: 'Impatto scenico, carattere deciso.', en: 'Scenic impact, strong character.' },
    description: {
      it: 'La superficie oro specchiato riflette luci e atmosfera e trasforma il bar nel punto focale dell’evento.',
      en: 'Its mirrored gold surface reflects light and atmosphere, turning the bar into the focal point of the event.',
    },
    idealFor: {
      it: ['Ricevimenti glamour', 'Party esclusivi', 'Contesti ad alto effetto visivo'],
      en: ['Glamorous receptions', 'Exclusive parties', 'Settings built for visual impact'],
    },
  },
  {
    slug: 'silver-reflection',
    name: 'Silver Reflection',
    status: 'available',
    swatch: '#9a9a98',
    images: [
      {
        src: silverReflection,
        alt: {
          it: 'Banco bar Silver Reflection in una grande sala allestita per una cena di gala',
          en: 'Silver Reflection bar in a large hall set for a gala dinner',
        },
      },
    ],
    mood: { it: 'Moderno, brillante, sofisticato.', en: 'Modern, brilliant, sophisticated.' },
    description: {
      it: 'L’argento specchiato dona un’eleganza contemporanea e valorizza l’illuminazione dell’ambiente.',
      en: 'Mirrored silver brings contemporary elegance and makes the most of the ambient lighting.',
    },
    idealFor: {
      it: ['Eventi corporate', 'Wedding chic', 'Allestimenti minimal di design'],
      en: ['Corporate events', 'Chic weddings', 'Minimalist design setups'],
    },
  },
  {
    slug: 'pure-white',
    name: 'Pure White',
    status: 'available',
    swatch: '#ece6dc',
    images: [
      {
        src: pureWhiteVilla,
        alt: {
          it: 'Banco bar Pure White nel giardino di una villa in pietra al tramonto',
          en: 'Pure White bar in the garden of a stone villa at sunset',
        },
      },
    ],
    mood: { it: 'Eleganza luminosa, texture raffinata.', en: 'Luminous elegance, refined texture.' },
    description: {
      it: 'Il bianco lucido con disegno a spina di pesce crea movimento e profondità, con un’estetica pulita e contemporanea.',
      en: 'Glossy white with a herringbone pattern creates movement and depth while keeping a clean, contemporary look.',
    },
    idealFor: {
      it: ['Matrimoni eleganti', 'Eventi luxury minimal', 'Ambientazioni sofisticate'],
      en: ['Elegant weddings', 'Minimalist luxury events', 'Sophisticated settings'],
    },
  },
  {
    slug: 'green-harmony',
    name: 'Green Harmony',
    status: 'coming-soon',
    swatch: '#a9b49a',
    images: [],
    mood: { it: 'Freschezza naturale.', en: 'Natural freshness.' },
    description: {
      it: 'Fresco, luminoso, contemporaneo. La finitura verde chiaro aggiunge un tocco botanico ed elegante.',
      en: 'Fresh, luminous, contemporary. The light-green finish adds an elegant botanical touch.',
    },
    idealFor: {
      it: ['Garden party', 'Matrimoni moderni', 'Eventi eco-chic'],
      en: ['Garden parties', 'Modern weddings', 'Eco-chic events'],
    },
  },
  {
    slug: 'country-classic',
    name: 'Country Classic',
    status: 'coming-soon',
    swatch: '#8a6a4c',
    images: [],
    mood: { it: 'Caldo, naturale, accogliente.', en: 'Warm, natural, cosy.' },
    description: {
      it: 'Il legno a venatura naturale crea un’atmosfera country-chic autentica.',
      en: 'Exposed-grain wood creates an authentic country-chic atmosphere.',
    },
    idealFor: {
      it: ['Eventi all’aperto', 'Matrimoni in stile boho'],
      en: ['Outdoor events', 'Boho-style weddings'],
    },
  },
  {
    slug: 'black-essence',
    name: 'Black Essence',
    status: 'coming-soon',
    swatch: '#1c1614',
    images: [],
    mood: { it: 'Nero laccato, puro e sofisticato.', en: 'Lacquered black, pure and sophisticated.' },
    description: {
      it: 'Un carattere deciso e contemporaneo che fa del bar un elemento scenografico di grande impatto.',
      en: 'A bold, contemporary character that makes the bar a scenographic element of great impact.',
    },
    idealFor: {
      it: ['Eventi luxury', 'Serate di gala', 'Party esclusivi', 'Matrimoni moderni minimal'],
      en: ['Luxury events', 'Gala nights', 'Exclusive parties', 'Modern minimalist weddings'],
    },
  },
];

export const availableBars = bars.filter((b) => b.status === 'available');
