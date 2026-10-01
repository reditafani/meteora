import type { Localized } from '@/i18n/ui';

/**
 * Genuine FAQs, answered strictly from the brochure. Used on Weddings,
 * Destination and Contact pages (with FAQPage structured data).
 */
export interface FaqItem {
  q: Localized;
  a: Localized;
  topics: ('wedding' | 'destination' | 'general' | 'partner')[];
}

export const faq: FaqItem[] = [
  {
    q: { it: 'Come funziona il servizio di open bar?', en: 'How does the open bar service work?' },
    a: {
      it: 'Il nostro team si occupa interamente della gestione dell’open bar per tre ore, in modo professionale e autonomo, coordinandosi con il catering. Portiamo banco bar, bicchieri, prodotti, ghiaccio e staff.',
      en: 'Our team takes full responsibility for running the open bar for three hours, professionally and autonomously, in coordination with the catering. We bring the bar counter, glassware, products, ice and staff.',
    },
    topics: ['wedding', 'destination', 'general'],
  },
  {
    q: { it: 'Cosa è incluso?', en: 'What is included?' },
    a: {
      it: 'Prodotti e distillati del menu scelto, banco bar a scelta, drink list signature con eventuali personalizzazioni, staff professionale, gestione indipendente del servizio, bicchieri e allestimento di nostra proprietà. Tempo extra, staff aggiuntivo e moduli bar extra si possono aggiungere su richiesta.',
      en: 'Products and spirits from the chosen menu, a bar counter of your choice, our signature drink list with any customisation, professional staff, fully independent service management, and our own glassware and setup. Extra time, additional staff and extra bar modules can be added on request.',
    },
    topics: ['wedding', 'destination', 'general'],
  },
  {
    q: { it: 'Fin dove vi spostate?', en: 'How far do you travel?' },
    a: {
      it: 'La nostra sede è a Montecatini Terme, in Toscana. Lavoriamo in tutta Italia e realizziamo servizi anche fuori regione e all’estero. Gli eventuali costi di trasferta e logistica vengono concordati in fase di preventivo.',
      en: 'We are based in Montecatini Terme, Tuscany. We work throughout Italy and also deliver services outside the region and abroad. Any travel and logistics costs are agreed at the quoting stage.',
    },
    topics: ['destination', 'general', 'partner'],
  },
  {
    q: { it: 'Come vi coordinate con il catering?', en: 'How do you coordinate with the caterer?' },
    a: {
      it: 'Siamo completamente indipendenti: non dipendiamo da cucina, personale o attrezzature del catering. Questo permette al catering di chiudere il servizio cena con serenità, caricare il materiale e liberare il proprio staff senza attendere la fine del dopocena.',
      en: 'We are fully independent: we do not rely on the caterer’s kitchen, staff or equipment. This lets the caterer close dinner service calmly, load out and release their team without waiting for the after-party to end.',
    },
    topics: ['wedding', 'destination', 'partner'],
  },
  {
    q: { it: 'Come si sceglie il banco bar?', en: 'How do we choose the bar?' },
    a: {
      it: 'Ogni modello della collezione è disponibile in tre misure — Slim 1,5 m, Medium 3,5 m, Large 5,5 m — e si sceglie in base a stile dell’evento, location e numero di ospiti. Vi consigliamo noi in fase di preventivo.',
      en: 'Every model in the collection comes in three sizes — Slim 1.5 m, Medium 3.5 m, Large 5.5 m — chosen according to the style of the event, the venue and the guest count. We advise you during the quoting stage.',
    },
    topics: ['wedding', 'destination', 'general'],
  },
  {
    q: { it: 'Con quanto anticipo vanno richieste le personalizzazioni?', en: 'How early should customisations be requested?' },
    a: {
      it: 'Tovaglioli e frontali banco personalizzati richiedono 35 giorni di preavviso. Tutte le personalizzazioni vanno concordate in fase di ideazione dell’evento.',
      en: 'Custom napkins and custom bar fronts require 35 days’ notice. All customisations should be agreed during the event-planning phase.',
    },
    topics: ['wedding', 'destination'],
  },
  {
    q: { it: 'Offrite cocktail analcolici?', en: 'Do you offer alcohol-free cocktails?' },
    a: {
      it: 'Sì. La drink list dell’aperitivo include cocktail analcolici e succhi di frutta, e possiamo studiare alternative analcoliche anche per l’open bar.',
      en: 'Yes. The aperitivo drink list includes alcohol-free cocktails and fruit juices, and we can design alcohol-free options for the open bar too.',
    },
    topics: ['wedding', 'destination', 'general'],
  },
  {
    q: { it: 'Possiamo richiedere etichette o bicchieri specifici?', en: 'Can we request specific brands or glassware?' },
    a: {
      it: 'Sì. Siamo disponibili per richieste di altre etichette, ed è possibile noleggiare bicchieri specifici di qualsiasi linea o marca, compatibilmente con disponibilità e tempi di fornitura.',
      en: 'Yes. We welcome requests for other brands, and specific glassware of any line or brand can be rented, subject to availability and supply times.',
    },
    topics: ['wedding', 'destination', 'general'],
  },
];

export const faqFor = (topic: FaqItem['topics'][number]) => faq.filter((f) => f.topics.includes(topic));
