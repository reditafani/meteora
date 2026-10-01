import type { ImageMetadata } from 'astro';
import type { Localized } from '@/i18n/ui';
import goldenSunset from '@/assets/images/bars/golden-mirror-sunset.jpg';
import pureWhite from '@/assets/images/bars/pure-white-villa.jpg';
import nightLounge from '@/assets/images/bars/night-lounge.jpg';
import coupleTower from '@/assets/images/towers/couple-pour.jpg';
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
    kicker: { it: 'Open bar · 3 ore', en: 'Open bar · 3 hours' },
    summary: {
      it: 'Tre ore di open bar gestite interamente dal nostro team, in modo autonomo e coordinato con il catering.',
      en: 'Three hours of open bar run entirely by our team, independently and in step with the catering.',
    },
    includes: {
      it: [
        'Prodotti e distillati inclusi dal menu scelto',
        'Banco bar a scelta dalla collezione',
        'Drink list signature, con eventuali personalizzazioni',
        'Staff professionale',
        'Gestione del servizio completamente indipendente',
        'Bicchieri e allestimento bar di nostra proprietà',
      ],
      en: [
        'All products and spirits from the selected menu',
        'A bar counter of your choice from the collection',
        'Our signature drink list, with any requested customisation',
        'Professional staff',
        'Fully independent service management',
        'Our own glassware and bar setup',
      ],
    },
    image: pureWhite,
    imageAlt: { it: 'Banco Pure White allestito per un open bar in villa', en: 'Pure White bar set for an open bar at a villa' },
    formValue: 'open-bar',
  },
  {
    id: 'premium',
    name: { it: 'Open Bar — Premium Experience', en: 'Open Bar — Premium Experience' },
    kicker: { it: 'Open bar · 3 ore', en: 'Open bar · 3 hours' },
    summary: {
      it: 'La stessa cura del servizio, con una selezione di etichette premium e mixer serviti in vetro.',
      en: 'The same standard of service, with a premium label selection and mixers served from glass bottles.',
    },
    includes: {
      it: [
        'Distillati premium dalla nostra selezione stagionale',
        'Toniche e soft drink premium in vetro',
        'Banco bar a scelta dalla collezione',
        'Drink list signature, con eventuali personalizzazioni',
        'Staff professionale e bicchieri di nostra proprietà',
      ],
      en: [
        'Premium spirits from our seasonal selection',
        'Premium tonics and soft drinks in glass bottles',
        'A bar counter of your choice from the collection',
        'Our signature drink list, with any requested customisation',
        'Professional staff and our own glassware',
      ],
    },
    image: goldenSunset,
    imageAlt: { it: 'Banco Golden Mirror al tramonto', en: 'Golden Mirror bar at sunset' },
    formValue: 'open-bar',
  },
  {
    id: 'aperitivo',
    name: { it: 'Aperitivo + Open Bar', en: 'Aperitivo + Open Bar' },
    kicker: { it: '1h30 aperitivo + 3h open bar', en: '1h30 aperitivo + 3h open bar' },
    summary: {
      it: 'Un servizio chiavi in mano, dall’aperitivo all’open bar dopo cena. Se le aree coincidono l’aperitivo si integra nel banco bar; altrimenti viene allestito su tavoli tovagliati.',
      en: 'A turnkey service, from the aperitivo to the after-dinner open bar. If both happen in the same area the aperitivo is integrated into the bar counter; otherwise it is set up on draped tables.',
    },
    includes: {
      it: [
        'Aperol, Campari, Limoncello, Passion Fruit e Hugo Spritz',
        'Bellini, Mimosa, Prosecco',
        'Cocktail analcolici e succhi di frutta',
        'Continuità di servizio e staff dall’aperitivo al dopocena',
      ],
      en: [
        'Aperol, Campari, Limoncello, Passion Fruit and Hugo Spritz',
        'Bellini, Mimosa, Prosecco',
        'Alcohol-free cocktails and fruit juices',
        'One team and seamless service from aperitivo to after-dinner',
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
      it: 'Coppe o calici disposti a cascata e riempiti dal vivo dal nostro staff o dagli sposi. Per brindisi, taglio torta o apertura della festa.',
      en: 'Coupes or glasses arranged in a cascade and filled live by our staff or by the couple. For toasts, cake cutting or opening the party.',
    },
    includes: {
      it: ['Una coppa o un drink a persona', 'Ingredienti', 'Allestimento e attrezzatura', 'Personale qualificato di assistenza'],
      en: ['One coupe or drink per person', 'Ingredients', 'Setup and equipment', 'Qualified assistance staff'],
    },
    image: coupleTower,
    imageAlt: { it: 'Sposi che versano le bollicine su una tower di coppe', en: 'A couple pouring sparkling wine over a coupe tower' },
    formValue: 'signature-tower',
  },
  {
    id: 'bartender',
    name: { it: 'Servizio solo barman', en: 'Bartender-only service' },
    kicker: { it: 'Staff e metodo Meteora', en: 'Meteora staff and method' },
    summary: {
      it: 'Per chi dispone già di prodotti e attrezzature — banco, bicchieri, ghiaccio, utensileria — e cerca personale qualificato con il nostro metodo di lavoro.',
      en: 'For clients who already have products and equipment — bar counter, glassware, ice, tools — and need qualified staff working to our method.',
    },
    includes: {
      it: [
        'Preparazione e servizio secondo standard professionali di mixology',
        'Possibile integrazione con un cameriere',
        'Ideale per eventi privati, aziendali, di piccole dimensioni e rinfreschi',
      ],
      en: [
        'Preparation and service to professional mixology standards',
        'Can be combined with a waiter for order handling',
        'Designed for private, corporate and smaller events and receptions',
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
        it: 'Etichette premium, ad esempio Grey Goose, Belvedere, Hendrick’s, Tanqueray No. Ten, Patrón, Diplomático.',
        en: 'Premium labels such as Grey Goose, Belvedere, Hendrick’s, Tanqueray No. Ten, Patrón and Diplomático.',
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
        it: 'Tutto l’Essential, con bottiglie in vetro a vista che elevano la presentazione del banco.',
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
