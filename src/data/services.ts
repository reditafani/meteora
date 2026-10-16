import type { ImageMetadata } from 'astro';
import type { Localized } from '@/i18n/ui';
import goldenSunset from '@/assets/images/bars/back-bar-spirits.jpg';
import pureWhite from '@/assets/images/bars/bartender-coupe-pour.jpg';
import nightLounge from '@/assets/images/bars/night-lounge.jpg';
import coupleTower from '@/assets/images/towers/gold-coupe-tower.jpg';
import bartenderPour from '@/assets/images/team/bartender-pour.jpg';

/**
 * Service formulas from the brochure. PRICES ARE INTENTIONALLY NOT STORED HERE:
 * the public site never shows prices. Everything leads to a quote request.
 */
export interface Service {
  id: 'essential' | 'premium' | 'aperitivo' | 'tower' | 'bartender';
  name: Localized;
  kicker: Localized;
  summary: Localized;
  includes: Localized<string[]>;
  image: ImageMetadata;
  imageAlt: Localized;
  /** value used by the quote form "service" select */
  formValue: string;
}

export const services: Service[] = [
  {
    id: 'essential',
    name: { it: 'Open Bar — Essential Experience', en: 'Open Bar — Essential Experience' },
    kicker: { it: 'Open bar', en: 'Open bar' },
    summary: {
      it: `L'esperienza Meteora, completa: una selezione di cocktail e distillati, un banco della collezione e i nostri cristalli.`,
      en: 'Three hours of open bar run entirely by our team, independently and in step with the catering.',
    },
    includes: {
      it: [
        'Banco bar a scelta dalla nostra collezione',
        'Cocktail preparati al momento, curati fino all\'ultimo dettaglio',
        'Staff professionale dedicato',
        'Bicchieri in vetro, scelti per ogni drink',
        'Selezione di distillati e prodotti della linea Essential',
        'Un servizio completo e autonomo, dall\'inizio alla fine',
      ],
      en: [
        'Bar counter of your choice from our collection',
        'Cocktails prepared on the spot, crafted to the last detail',
        'Dedicated professional staff',
        'Glassware chosen for each drink',
        'Selection of spirits and products from the Essential line',
        'A fully autonomous service, from start to finish',
      ],
    },
    image: pureWhite,
    imageAlt: { it: 'Bartender che versa un cocktail in una coppa dal tin', en: 'Bartender pouring a cocktail into a coupe from a tin' },
    formValue: 'open-bar',
  },
  {
    id: 'premium',
    name: { it: 'Open Bar — Premium Experience', en: 'Open Bar — Premium Experience' },
    kicker: { it: 'Open bar', en: 'Open bar' },
    summary: {
      it: `Tutto l'Essential, con distillati premium dalla nostra selezione stagionale e mixer premium in bottiglie di vetro.`,
      en: 'The same standard of service, with a premium label selection and mixers served from glass bottles.',
    },
    includes: {
      it: [
        'Banco bar a scelta dalla nostra collezione',
        'Cocktail preparati al momento, curati fino all\'ultimo dettaglio',
        'Staff professionale dedicato',
        'Bicchieri in vetro, scelti per ogni drink',
        'Selezione di distillati e prodotti premium',
        'Un servizio completo e autonomo, dall\'inizio alla fine',
      ],
      en: [
        'Bar counter of your choice from our collection',
        'Cocktails prepared on the spot, crafted to the last detail',
        'Dedicated professional staff',
        'Glassware chosen for each drink',
        'Selection of premium spirits and products',
        'A fully autonomous service, from start to finish',
      ],
    },
    image: goldenSunset,
    imageAlt: { it: 'Bottigliera illuminata con distillati premium e calici pronti al servizio', en: 'Illuminated back bar with premium spirits and glassware ready for service' },
    formValue: 'open-bar',
  },
  {
    id: 'aperitivo',
    name: { it: 'Aperitivo + Open Bar', en: 'Aperitivo + Open Bar' },
    kicker: { it: 'Aperitivo + Open bar', en: 'Aperitivo + Open bar' },
    summary: {
      it: `La nostra formula combinata: aperitivo e open bar, per accompagnare tutta la serata, dal primo brindisi all'ultimo drink.`,
      en: 'A turnkey service, from the aperitivo to the after-dinner open bar. If both happen in the same area the aperitivo is integrated into the bar counter; otherwise it is set up on draped tables.',
    },
    includes: {
      it: [
        'Aperitivo con drink pensati per il momento',
        `Allestimento dell'aperitivo a vostra scelta`,
        'Open bar Essential o Premium, con tutti i suoi servizi',
        'Il banco bar che preferite, dalla nostra collezione',
        `Staff professionale dedicato all'aperitivo e all'open bar`,
      ],
      en: [
        'Aperitivo with drinks designed for the moment',
        'Aperitivo setup of your choice',
        'Essential or Premium open bar, with all its services',
        'Your preferred bar counter from our collection',
        'Professional staff dedicated to both the aperitivo and open bar',
      ],
    },
    image: nightLounge,
    imageAlt: { it: 'Banco bar serale con bottigliera e champagne bowl', en: 'Evening bar with back bar and champagne bowl' },
    formValue: 'aperitivo-open-bar',
  },
  {
    id: 'tower',
    name: { it: 'Signature Tower Experience', en: 'Signature Tower Experience' },
    kicker: { it: 'Un momento scenografico', en: 'A scenographic moment' },
    summary: {
      it: `Il momento che tutti fotografano: una torre di coppe riempita dal vivo con bollicine, Spritz o Espresso Martini. Per il brindisi, il taglio della torta o l'apertura della festa.`,
      en: 'Coupes or glasses arranged in a cascade and filled live by our staff or by the couple. For toasts, cake cutting or opening the party.',
    },
    includes: {
      it: ['Sparkling towers', 'Spritz tower', 'Espresso Martini tower'],
      en: ['Sparkling towers', 'Spritz tower', 'Espresso Martini tower'],
    },
    image: coupleTower,
    imageAlt: { it: 'Tower di coppe in cristallo con bordo dorato pronte per il brindisi', en: 'Gold-rimmed crystal coupe tower ready for the toast' },
    formValue: 'signature-tower',
  },
  {
    id: 'bartender',
    name: { it: 'Bartender Service', en: 'Bartender Service' },
    kicker: { it: 'Staff e metodo Meteora', en: 'Meteora staff and method' },
    summary: {
      it: `Il nostro metodo, anche senza il nostro bar. Per chi dispone già di banco, bicchieri, ghiaccio e attrezzatura, e cerca bartender qualificati con i nostri standard di servizio.`,
      en: 'For clients who already have products and equipment — bar counter, glassware, ice, tools — and need qualified staff working to our method.',
    },
    includes: {
      it: [
        'Bartender professionisti del nostro team',
        'Preparazione e servizio dei cocktail a regola d\'arte',
        'Allestimento e riordino della postazione',
        'Consulenza su drink list, prodotti, quantità e attrezzatura',
        'Staff di sala su richiesta',
      ],
      en: [
        'Professional bartenders from our team',
        'Cocktail preparation and service to the highest standard',
        'Setup and breakdown of the bar station',
        'Consultation on drink list, products, quantities and equipment',
        'Floor staff available on request',
      ],
    },
    image: bartenderPour,
    imageAlt: { it: 'Bartender che versa un cocktail in una coppa', en: 'Bartender pouring a cocktail into a coupe' },
    formValue: 'bartender-service',
  },
];

export const towers = [
  {
    group: { it: 'Sparkling Towers', en: 'Sparkling Towers' },
    items: ['Classic Celebration Tower — Prosecco', 'Italian Elegance Tower — Franciacorta', 'Golden Cascade — Champagne'],
  },
  { group: { it: 'Spritz Towers', en: 'Spritz Towers' }, items: ['Aperol / Campari Spritz Tower', 'Hugo Spritz Tower'] },
  { group: { it: 'Espresso Martini Tower', en: 'Espresso Martini Tower' }, items: ['Espresso Martini Tower'] },
];

/** Essential vs Premium — described qualitatively, never with prices. */
export const comparison = {
  rows: [
    {
      label: { it: 'Distillati', en: 'Spirits' },
      essential: {
        it: 'Etichette affidabili di grandi case internazionali, scelte per equilibrio e costanza.',
        en: 'Reliable labels from established international houses, chosen for balance and consistency.',
      },
      premium: {
        it: `Etichette premium, ad esempio Grey Goose, Belvedere, Hendrick's, Tanqueray No. Ten, Patrón, Diplomático.`,
        en: `Premium labels such as Grey Goose, Belvedere, Hendrick's, Tanqueray No. Ten, Patrón and Diplomático.`,
      },
    },
    {
      label: { it: 'Mixer e soft drink', en: 'Mixers and soft drinks' },
      essential: {
        it: 'Toniche, soda e soft drink in formato professionale da servizio.',
        en: 'Tonics, soda and soft drinks in professional service formats.',
      },
      premium: {
        it: 'Toniche Fever-Tree, soft drink e acqua San Pellegrino, tutto in vetro.',
        en: 'Fever-Tree tonics, soft drinks and San Pellegrino water, all in glass.',
      },
    },
    {
      label: { it: 'Presentazione', en: 'Presentation' },
      essential: {
        it: 'Banco a scelta, bicchieri professionali, frutta fresca e disidratata, botaniche e spezie.',
        en: 'Bar of your choice, professional glassware, fresh and dehydrated fruit, botanicals and spices.',
      },
      premium: {
        it: `Tutto l'Essential, con bottiglie in vetro a vista che elevano la presentazione del banco.`,
        en: 'Everything in Essential, with glass bottles on display that elevate the look of the bar.',
      },
    },
    {
      label: { it: 'Esperienza', en: 'Experience' },
      essential: {
        it: 'Un open bar completo e curato, gestito in piena autonomia.',
        en: 'A complete, polished open bar, managed with full autonomy.',
      },
      premium: {
        it: 'Per chi desidera che ogni drink parli la lingua delle grandi etichette.',
        en: 'For hosts who want every drink to speak the language of the great labels.',
      },
    },
  ],
  note: {
    it: 'Le etichette possono variare in base alla disponibilità, con referenze equivalenti o superiori, sempre comunicate in anticipo. Siamo disponibili per richieste di altre etichette.',
    en: 'Labels may vary with availability, replaced by equivalent or superior references and always communicated in advance. Requests for other brands are welcome.',
  },
};
