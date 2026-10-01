import type { ImageMetadata } from 'astro';
import type { Localized } from '@/i18n/ui';
import goldenSunset from '@/assets/images/bars/golden-mirror-sunset.jpg';
import goldenMirror from '@/assets/images/bars/golden-mirror.jpg';
import pureWhite from '@/assets/images/bars/pure-white-villa.jpg';
import silver from '@/assets/images/bars/silver-reflection.jpg';
import terrace from '@/assets/images/bars/terrace-panorama.jpg';
import nightLounge from '@/assets/images/bars/night-lounge.jpg';
import marbleNight from '@/assets/images/bars/golden-marble-night.jpg';
import couplePour from '@/assets/images/towers/couple-pour.jpg';
import espressoTower from '@/assets/images/towers/espresso-martini-tower.jpg';
import coupeTower from '@/assets/images/towers/coupe-tower-sunset.jpg';

/**
 * EVENTS / PORTFOLIO — CMS-like structure.
 *
 * IMPORTANT (client): the entries below are built ONLY from photographs in the
 * brochure. Titles and stories describe what the images show; they do not
 * claim venues, dates, guest counts or client names.
 * Replace them with real event stories (with approval for any names) and set
 * `draft: false`. Draft entries are shown on the site but marked noindex and
 * excluded from the sitemap.
 *
 * Optional fields (location, guests, video) are hidden automatically when empty.
 */
export interface EventStory {
  slug: Localized;
  draft: boolean;
  title: Localized;
  type: Localized;
  /** e.g. { it: 'Chianti, Toscana', en: 'Chianti, Tuscany' } — only if approved */
  location?: Localized;
  /** Only if approved by the client */
  guests?: number;
  bar?: string;
  experience: Localized;
  excerpt: Localized;
  story: Localized<string[]>;
  cover: ImageMetadata;
  coverAlt: Localized;
  gallery: { src: ImageMetadata; alt: Localized }[];
  /** Path under /public, e.g. '/videos/events/slug.mp4' */
  video?: { mp4?: string; webm?: string; poster?: ImageMetadata };
  /** Links the story to the relevant service page */
  relatedService: 'weddings' | 'corporate' | 'destination' | 'bars' | 'cocktails';
}

export const events: EventStory[] = [
  {
    slug: { it: 'golden-hour-sulle-colline', en: 'golden-hour-in-the-hills' },
    draft: true,
    title: { it: 'Golden hour sulle colline', en: 'Golden hour in the hills' },
    type: { it: 'Ricevimento all’aperto', en: 'Outdoor reception' },
    bar: 'Golden Mirror',
    experience: { it: 'Open Bar', en: 'Open Bar' },
    excerpt: {
      it: 'Un banco oro specchiato che cattura l’ultima luce del giorno.',
      en: 'A mirrored-gold bar catching the last light of the day.',
    },
    story: {
      it: [
        'Una terrazza in cotto, le colline all’orizzonte e il sole che scende dietro la bottigliera.',
        'Il Golden Mirror riflette il paesaggio e diventa parte della scena: il bar è il punto verso cui gli ospiti si muovono naturalmente al calare della sera.',
      ],
      en: [
        'A terracotta terrace, hills on the horizon and the sun setting behind the back bar.',
        'The Golden Mirror reflects the landscape and becomes part of the scene: the bar is where guests naturally gather as evening falls.',
      ],
    },
    cover: goldenSunset,
    coverAlt: { it: 'Banco Golden Mirror su terrazza al tramonto', en: 'Golden Mirror bar on a terrace at sunset' },
    gallery: [
      { src: goldenMirror, alt: { it: 'Vista frontale del Golden Mirror', en: 'Front view of the Golden Mirror' } },
    ],
    relatedService: 'weddings',
  },
  {
    slug: { it: 'villa-in-pietra-pure-white', en: 'stone-villa-pure-white' },
    draft: true,
    title: { it: 'Pure White in villa', en: 'Pure White at the villa' },
    type: { it: 'Ricevimento in villa', en: 'Villa reception' },
    bar: 'Pure White',
    experience: { it: 'Open Bar', en: 'Open Bar' },
    excerpt: {
      it: 'Bianco a spina di pesce davanti alla pietra antica di una villa.',
      en: 'Herringbone white against the old stone of a villa.',
    },
    story: {
      it: [
        'Il prato, le finestre ad arco, la luce radente del tardo pomeriggio.',
        'Il Pure White dialoga con l’architettura senza sovrastarla: pulito, luminoso, pronto per il servizio.',
      ],
      en: [
        'The lawn, the arched windows, the low light of late afternoon.',
        'Pure White converses with the architecture without overpowering it: clean, luminous, ready for service.',
      ],
    },
    cover: pureWhite,
    coverAlt: { it: 'Banco Pure White nel giardino di una villa in pietra', en: 'Pure White bar in a stone villa garden' },
    gallery: [],
    relatedService: 'destination',
  },
  {
    slug: { it: 'vista-panoramica-dal-giorno-alla-notte', en: 'panoramic-view-day-to-night' },
    draft: true,
    title: { it: 'Dal giorno alla notte, sopra la città', en: 'Day to night, above the city' },
    type: { it: 'Evento privato', en: 'Private event' },
    bar: 'Golden Mirror · Pure White',
    experience: { it: 'Aperitivo + Open Bar', en: 'Aperitivo + Open Bar' },
    excerpt: {
      it: 'Vetrate panoramiche, rami scenografici e un bar che cambia con la luce.',
      en: 'Panoramic windows, sculptural branches and a bar that changes with the light.',
    },
    story: {
      it: [
        'Di giorno la vista entra dalle vetrate e il bar resta leggero, quasi sospeso.',
        'Di sera le luci si abbassano, la champagne bowl si accende di riflessi e il banco diventa il centro della festa.',
      ],
      en: [
        'By day the view pours in through the windows and the bar feels light, almost suspended.',
        'By night the lights dim, the champagne bowl catches every reflection and the bar becomes the heart of the party.',
      ],
    },
    cover: nightLounge,
    coverAlt: { it: 'Banco bar serale davanti a vetrate panoramiche', en: 'Evening bar in front of panoramic windows' },
    gallery: [
      { src: terrace, alt: { it: 'Banco bar di giorno davanti a una vetrata panoramica', en: 'Bar by day in front of a panoramic window' } },
      { src: marbleNight, alt: { it: 'Banco dorato su pavimento chevron', en: 'Golden bar on a chevron floor' } },
    ],
    relatedService: 'weddings',
  },
  {
    slug: { it: 'gala-silver-reflection', en: 'silver-reflection-gala' },
    draft: true,
    title: { it: 'Una sala, mille riflessi', en: 'One hall, a thousand reflections' },
    type: { it: 'Cena di gala', en: 'Gala dinner' },
    bar: 'Silver Reflection',
    experience: { it: 'Open Bar', en: 'Open Bar' },
    excerpt: {
      it: 'Un grande spazio industriale, tavoli imperiali e un bar al centro della sala.',
      en: 'A vast industrial space, long tables and a bar at the centre of the room.',
    },
    story: {
      it: [
        'In una sala di grandi dimensioni il bar deve essere visibile da ogni tavolo.',
        'Il Silver Reflection raccoglie le luci della sala e le restituisce: moderno, preciso, perfetto per il linguaggio corporate.',
      ],
      en: [
        'In a room this size, the bar has to be visible from every table.',
        'Silver Reflection gathers the room’s lighting and gives it back: modern, precise, right for a corporate setting.',
      ],
    },
    cover: silver,
    coverAlt: { it: 'Banco Silver Reflection in una grande sala per cena di gala', en: 'Silver Reflection bar in a large gala hall' },
    gallery: [],
    relatedService: 'corporate',
  },
  {
    slug: { it: 'signature-tower-moments', en: 'signature-tower-moments' },
    draft: true,
    title: { it: 'Il momento della tower', en: 'The tower moment' },
    type: { it: 'Signature Tower Experience', en: 'Signature Tower Experience' },
    experience: { it: 'Sparkling & Espresso Martini Tower', en: 'Sparkling & Espresso Martini Tower' },
    excerpt: {
      it: 'Bollicine a cascata, un brindisi che diventa fotografia.',
      en: 'Cascading bubbles — a toast that becomes a photograph.',
    },
    story: {
      it: [
        'Una piramide di coppe, versata dagli sposi o dal nostro staff, al tramonto o in piena notte.',
        'Una Sparkling Tower per il brindisi, una Espresso Martini Tower per accendere la festa.',
      ],
      en: [
        'A pyramid of coupes, poured by the couple or by our staff, at sunset or deep into the night.',
        'A Sparkling Tower for the toast, an Espresso Martini Tower to start the party.',
      ],
    },
    cover: couplePour,
    coverAlt: { it: 'Sposi che versano bollicine sulla tower di coppe', en: 'Couple pouring sparkling wine over a coupe tower' },
    gallery: [
      { src: coupeTower, alt: { it: 'Tower di coppe al tramonto', en: 'Coupe tower at sunset' } },
      { src: espressoTower, alt: { it: 'Espresso Martini Tower', en: 'Espresso Martini Tower' } },
    ],
    relatedService: 'weddings',
  },
];
