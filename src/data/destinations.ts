import type { Localized } from '@/i18n/ui';

/**
 * DESTINATIONS — scalable SEO architecture.
 *
 * Every destination appears on the Destination Weddings hub page.
 * A dedicated landing page is generated ONLY when `landing` is set — add it
 * when you have genuine local content (real events, venues you have worked at,
 * photos), to avoid thin duplicate pages.
 *
 * Never imply local offices: Meteora is based in Montecatini Terme and travels.
 */
export interface Destination {
  id: string;
  name: Localized;
  line: Localized;
  landing?: {
    slug: Localized;
    title: Localized;
    description: Localized;
    h1: Localized;
    intro: Localized<string[]>;
    sections: { h2: Localized; body: Localized<string[]> }[];
  };
}

export const destinations: Destination[] = [
  {
    id: 'tuscany',
    name: { it: 'Toscana', en: 'Tuscany' },
    line: {
      it: 'La nostra base. Ville, borghi e casali dove lavoriamo con la naturalezza di chi è di casa.',
      en: 'Our home base. Villas, hamlets and farmhouses where we work with the ease of locals.',
    },
    landing: {
      slug: { it: 'bar-catering-matrimoni-toscana', en: 'wedding-bar-catering-tuscany' },
      title: {
        it: 'Bar Catering per Matrimoni in Toscana | Meteora Events',
        en: 'Wedding Bar Catering in Tuscany | Meteora Events',
      },
      description: {
        it: 'Open bar e cocktail experience per matrimoni in Toscana. Banchi scenografici, bartender professionisti e servizio autonomo. Base a Montecatini Terme.',
        en: 'Open bar and cocktail experience for weddings in Tuscany. Scenographic bars, professional bartenders and fully independent service. Based in Montecatini Terme.',
      },
      h1: { it: 'Bar catering per matrimoni in Toscana', en: 'Wedding bar catering in Tuscany' },
      intro: {
        it: [
          'La Toscana è casa nostra. La sede di Meteora Events è a Montecatini Terme, a poca distanza da Firenze, Lucca, Pisa e dalla Versilia.',
          'Questa vicinanza è un vantaggio concreto: sopralluoghi più semplici, logistica più agile, e la conoscenza delle dinamiche di ville e location toscane.',
        ],
        en: [
          'Tuscany is home. Meteora Events is based in Montecatini Terme, a short drive from Florence, Lucca, Pisa and the Versilia coast.',
          'That proximity is a real advantage: simpler site visits, leaner logistics, and first-hand knowledge of how Tuscan villas and venues work.',
        ],
      },
      sections: [
        {
          h2: { it: 'Ville, casali e giardini', en: 'Villas, farmhouses and gardens' },
          body: {
            it: [
              'Molte location toscane sono dimore storiche: pietra antica, pavimenti delicati, giardini curati. Allestiamo e smontiamo con la massima cura di mura, pavimentazioni, arredi e verde, e lasciamo tutto pulito a fine servizio.',
              'Dietro al banco non vedrete contenitori termici o ceste di bicchieri: ogni rifornimento avviene a vassoio, lontano dagli occhi degli ospiti.',
            ],
            en: [
              'Many Tuscan venues are historic homes: old stone, delicate floors, manicured gardens. We set up and dismantle with the utmost care for walls, flooring, furniture and greenery, and leave everything clean after service.',
              'You will never see cool boxes or glass racks behind the bar: every restock is carried by tray, away from guests’ eyes.',
            ],
          },
        },
        {
          h2: { it: 'Dall’aperitivo in giardino al dopocena', en: 'From garden aperitivo to after-dinner' },
          body: {
            it: [
              'Il pacchetto Aperitivo + Open Bar copre un’ora e mezza di aperitivo e tre ore di open bar dopo cena, con un unico team. Se aperitivo e open bar sono nella stessa area, l’aperitivo si integra nel banco; altrimenti viene allestito su tavoli tovagliati.',
              'Operiamo in autonomia e in coordinamento con il catering, che può chiudere il servizio cena con serenità.',
            ],
            en: [
              'The Aperitivo + Open Bar package covers ninety minutes of aperitivo and three hours of after-dinner open bar, with one team throughout. If both take place in the same area, the aperitivo is integrated into the bar; otherwise it is set up on draped tables.',
              'We work independently and in step with the caterer, who can close dinner service calmly.',
            ],
          },
        },
        {
          h2: { it: 'Firenze, Chianti, Siena, Lucca, Pisa, Forte dei Marmi', en: 'Florence, Chianti, Siena, Lucca, Pisa, Forte dei Marmi' },
          body: {
            it: [
              'Da Montecatini Terme raggiungiamo tutte le principali aree del matrimonio in Toscana. Gli eventuali costi di trasferta e logistica vengono definiti in fase di preventivo, in modo trasparente.',
            ],
            en: [
              'From Montecatini Terme we reach every major wedding area in Tuscany. Any travel and logistics costs are agreed transparently at the quoting stage.',
            ],
          },
        },
      ],
    },
  },
  {
    id: 'florence',
    name: { it: 'Firenze', en: 'Florence' },
    line: {
      it: 'Palazzi storici, terrazze sui tetti e ville sulle colline fiorentine.',
      en: 'Historic palazzi, rooftop terraces and villas on the Florentine hills.',
    },
  },
  {
    id: 'chianti',
    name: { it: 'Chianti', en: 'Chianti' },
    line: { it: 'Tenute e casali tra le vigne, per ricevimenti all’aperto.', en: 'Wine estates and farmhouses among the vines, for open-air receptions.' },
  },
  {
    id: 'siena',
    name: { it: 'Siena', en: 'Siena' },
    line: { it: 'Borghi medievali e dimore di campagna in Val d’Orcia e dintorni.', en: 'Medieval hamlets and country estates around Siena and the Val d’Orcia.' },
  },
  {
    id: 'lucca',
    name: { it: 'Lucca', en: 'Lucca' },
    line: { it: 'Ville lucchesi e giardini storici, a pochi minuti dalla nostra sede.', en: 'Lucchese villas and historic gardens, minutes from our base.' },
  },
  {
    id: 'pisa',
    name: { it: 'Pisa', en: 'Pisa' },
    line: { it: 'Tra città d’arte, campagna e costa.', en: 'Between art city, countryside and coast.' },
  },
  {
    id: 'forte-dei-marmi',
    name: { it: 'Forte dei Marmi', en: 'Forte dei Marmi' },
    line: { it: 'Eventi sul mare in Versilia, dal tramonto a notte fonda.', en: 'Seaside events on the Versilia coast, from sunset until late.' },
  },
  {
    id: 'italy',
    name: { it: 'Tutta Italia e all’estero', en: 'All of Italy and abroad' },
    line: {
      it: 'Ci spostiamo in tutta Italia e realizziamo servizi anche fuori regione e all’estero.',
      en: 'We travel throughout Italy and also deliver services outside the region and abroad.',
    },
  },
];

export const landingDestinations = destinations.filter((d) => d.landing);
