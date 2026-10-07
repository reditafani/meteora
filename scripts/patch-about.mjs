import { readFileSync, writeFileSync } from 'fs';

let src = readFileSync('src/views/AboutView.astro', 'utf8');

// Normalise to LF so replacements work
src = src.replace(/\r\n/g, '\n');

// 1. Add Icon import
src = src.replace(
  "import SectionHeading from '@/components/SectionHeading.astro';",
  "import SectionHeading from '@/components/SectionHeading.astro';\nimport Icon from '@/components/Icon.astro';"
);

// 2. Data arrays before closing ---
const data = `
type IconName = 'ice' | 'user' | 'briefcase' | 'cocktail' | 'star' | 'snowflake';
const included: { icon: IconName; title: string; text: string }[] = it
  ? [
      { icon: 'ice',       title: 'Banco bar',                 text: 'Uno dei nostri banchi signature, nella misura scelta.' },
      { icon: 'user',      title: 'Staff preparato',           text: 'Barman professionisti formati da noi, inclusi nel prezzo.' },
      { icon: 'briefcase', title: 'Allestimento e smontaggio', text: "Montiamo prima degli ospiti, smontiamo dopo l'ultimo brindisi." },
      { icon: 'cocktail',  title: 'Bicchieri in vetro',        text: 'Cristalleria professionale.' },
      { icon: 'star',      title: 'Tutti gli ingredienti',     text: 'Distillati, mixer, frutta fresca, sciroppi e guarnizioni.' },
      { icon: 'snowflake', title: 'Ghiaccio',                  text: 'Ghiaccio artigianale, in quantita calcolata sui vostri ospiti.' },
    ]
  : [
      { icon: 'ice',       title: 'Bar counter',       text: 'One of our signature bars, in the size you choose.' },
      { icon: 'user',      title: 'Trained staff',     text: 'Professional bartenders trained by us, included in the price.' },
      { icon: 'briefcase', title: 'Setup & breakdown', text: 'We set up before your guests arrive, break down after the last toast.' },
      { icon: 'cocktail',  title: 'Crystal glassware', text: 'Professional glassware throughout.' },
      { icon: 'star',      title: 'All ingredients',   text: 'Spirits, mixers, fresh fruit, syrups and garnishes.' },
      { icon: 'snowflake', title: 'Ice',               text: 'Artisan ice, calculated for your guest count.' },
    ];

const steps: { title: string; text: string; cta?: boolean }[] = it
  ? [
      { title: 'Primo contatto',     text: 'Ascoltiamo la vostra richiesta e ci conosciamo.' },
      { title: 'Il vostro bar',      text: 'Scegliete il banco bar e la cocktail list.' },
      { title: 'La nostra proposta', text: "Tutto per iscritto: un contratto con ogni dettaglio di cio che e incluso.", cta: true },
      { title: 'Il grande giorno',   text: 'Allestimento, servizio e coordinamento in presenza.' },
      { title: 'Smontaggio',         text: "Lasciamo la location esattamente come l'abbiamo trovata." },
    ]
  : [
      { title: 'First contact', text: 'You tell us about your event and we get to know each other.' },
      { title: 'Your bar',      text: 'Choose your bar counter and cocktail list.' },
      { title: 'Our proposal',  text: 'Everything in writing: a contract detailing exactly what is included.', cta: true },
      { title: 'The big day',   text: 'Setup, service and on-site coordination.' },
      { title: 'Breakdown',     text: 'We leave the venue exactly as we found it.' },
    ];
`;

src = src.replace('---\n\n<BaseLayout', data + '\n---\n\n<BaseLayout');

writeFileSync('src/views/AboutView.astro', src, 'utf8');
console.log('done');
