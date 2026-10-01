import type { ImageMetadata } from 'astro';
import type { Localized } from '@/i18n/ui';
import compactCube from '@/assets/images/ice/compact-cube.jpg';
import hoshizaki from '@/assets/images/ice/hoshizaki.jpg';
import nugget from '@/assets/images/ice/nugget.jpg';
import cube5 from '@/assets/images/ice/cube-5cm.jpg';
import longDrink from '@/assets/images/ice/long-drink.jpg';
import sphere from '@/assets/images/ice/sphere.jpg';
import gWine from '@/assets/images/glassware/wine.jpg';
import gMartini from '@/assets/images/glassware/martini.jpg';
import gOld from '@/assets/images/glassware/old-fashioned.jpg';
import gLong from '@/assets/images/glassware/long-drink.jpg';
import gShot from '@/assets/images/glassware/shot.jpg';
import gHigh from '@/assets/images/glassware/highball.jpg';

/** Ice formats, from "Il nostro ghiaccio". Premium formats are confirmed during event planning. */
export const iceTypes: { name: Localized; note: Localized; image: ImageMetadata; premium?: boolean }[] = [
  {
    name: { it: 'Cubo compatto ad alta densità', en: 'High-density compact cube' },
    note: {
      it: 'Scioglimento lento, controllo della diluizione in long drink e cocktail strutturati.',
      en: 'Slow melting, controlled dilution in long drinks and structured cocktails.',
    },
    image: compactCube,
  },
  {
    name: { it: 'Ghiaccio Hoshizaki', en: 'Hoshizaki ice' },
    note: {
      it: 'Cubo compatto dalla resa estetica pulita; equilibrio e temperatura costante.',
      en: 'Compact cube with a clean look; balance and a constant temperature.',
    },
    image: hoshizaki,
  },
  {
    name: { it: 'Ghiaccio nugget', en: 'Nugget ice' },
    note: {
      it: 'Texture morbida e piacevole al sorso, per cocktail freschi e dinamici.',
      en: 'Soft texture, pleasant to sip — for fresh, lively cocktails.',
    },
    image: nugget,
  },
  {
    name: { it: 'Cubo 5 × 5 cm', en: '5 × 5 cm cube' },
    note: {
      it: 'Scioglimento molto lento, per Negroni, Old Fashioned e cocktail spirit-forward.',
      en: 'Very slow melting, for Negroni, Old Fashioned and spirit-forward cocktails.',
    },
    image: cube5,
    premium: true,
  },
  {
    name: { it: 'Cubo long drink 4 × 4 × 12 cm', en: 'Long drink cube 4 × 4 × 12 cm' },
    note: {
      it: 'Formato verticale per highball e long drink premium; rallenta la diluizione.',
      en: 'Vertical format for highballs and premium long drinks; slows dilution.',
    },
    image: longDrink,
    premium: true,
  },
  {
    name: { it: 'Sfera 50 mm', en: '50 mm sphere' },
    note: {
      it: 'Superficie di scioglimento ridotta e impatto estetico distintivo nel bicchiere.',
      en: 'Minimal melting surface and a distinctive look in the glass.',
    },
    image: sphere,
    premium: true,
  },
];

export const glassware: { name: Localized; use: Localized; image: ImageMetadata }[] = [
  { name: { it: 'Calice', en: 'Wine glass' }, use: { it: 'Spritz, bollicine, vino', en: 'Spritz, sparkling, wine' }, image: gWine },
  { name: { it: 'Coppa Martini', en: 'Martini coupe' }, use: { it: 'Martini, sour, cocktail serviti up', en: 'Martinis, sours, drinks served up' }, image: gMartini },
  { name: { it: 'Old Fashioned', en: 'Old Fashioned' }, use: { it: 'Spirit-forward su ghiaccio grande', en: 'Spirit-forward drinks over large ice' }, image: gOld },
  { name: { it: 'Long drink', en: 'Long drink' }, use: { it: 'Highball, tonic, Mojito', en: 'Highballs, tonics, Mojito' }, image: gLong },
  { name: { it: 'Cortina', en: 'Highball tumbler' }, use: { it: 'Drink corti e rinfrescanti', en: 'Short, refreshing serves' }, image: gHigh },
  { name: { it: 'Shot', en: 'Shot glass' }, use: { it: 'Shot e degustazioni', en: 'Shots and tastings' }, image: gShot },
];

/** Personalisation options, from "Personalizzazioni" and "Le divise". */
export const customizations: { title: Localized; text: Localized; notice?: Localized }[] = [
  {
    title: { it: 'Tovaglioli personalizzati', en: 'Custom napkins' },
    text: { it: 'Con i nomi degli sposi o il logo aziendale.', en: 'With the couple’s names or a company logo.' },
    notice: { it: '35 giorni di preavviso', en: '35 days’ notice' },
  },
  {
    title: { it: 'Frontale banco personalizzato', en: 'Custom bar front' },
    text: {
      it: 'Nomi o logo sul banco: il bar diventa elemento scenografico e punto focale.',
      en: 'Names or logo on the counter: the bar becomes a branded focal point.',
    },
    notice: { it: '35 giorni di preavviso', en: '35 days’ notice' },
  },
  {
    title: { it: 'Incisione su frutta', en: 'Fruit engraving' },
    text: { it: 'Nomi o logo incisi sulla frutta decorativa. Un dettaglio che sorprende.', en: 'Names or logo etched on decorative fruit. A detail that surprises.' },
  },
  {
    title: { it: 'Incisione su ghiaccio', en: 'Ice engraving' },
    text: {
      it: 'Logo o nomi impressi sul cubone di ghiaccio. A fine evento lo stampo vi viene regalato come ricordo.',
      en: 'Logo or names pressed into large ice cubes. At the end of the event the stamp is yours to keep.',
    },
  },
  {
    title: { it: 'Cocktail list su misura', en: 'Bespoke cocktail list' },
    text: {
      it: 'Drink creati e nominati sulla personalità degli sposi o sull’identità del brand.',
      en: 'Drinks created and named after the couple’s personality or the brand identity.',
    },
  },
  {
    title: { it: 'Divise brandizzate', en: 'Branded uniforms' },
    text: {
      it: 'Per eventi aziendali: logo su camicia, gilet e cravatta con patch serigrafate.',
      en: 'For corporate events: logo on shirt, waistcoat and tie with screen-printed patches.',
    },
  },
];

/** Differentiators, from "Perché noi". Keep strictly to what the brochure states. */
export const differentiators: { title: Localized; text: Localized }[] = [
  {
    title: { it: 'Bartender qualificati', en: 'Qualified bartenders' },
    text: { it: 'Professionali, affidabili, seri. Total black, nessun logo vistoso.', en: 'Professional and reliable. Total black, no showy logos.' },
  },
  {
    title: { it: 'Pulizia visiva', en: 'A clean visual service' },
    text: {
      it: 'Al banco nessun contenitore termico, cassa o cesta di bicchieri a vista. Ogni rifornimento avviene a vassoio, con discrezione.',
      en: 'No cool boxes, storage crates or glass racks in view. All restocking is done discreetly, by tray.',
    },
  },
  {
    title: { it: 'Rispetto per ville e location', en: 'Respect for villas and venues' },
    text: {
      it: 'Massima cura di mura, pavimenti, arredi e verde, in allestimento e a fine servizio. Lasciamo tutto pulito.',
      en: 'Utmost care for walls, floors, furniture and gardens during setup and after service. We leave everything clean.',
    },
  },
  {
    title: { it: 'Un pensiero in meno', en: 'One less thing to worry about' },
    text: {
      it: 'Operiamo in completa autonomia, in armonia con gli altri fornitori.',
      en: 'We operate completely independently, in harmony with every other supplier.',
    },
  },
  {
    title: { it: 'Massima discrezione', en: 'Complete discretion' },
    text: {
      it: 'Con ogni ospite, anche con personaggi noti. Proteggere l’immagine dei nostri collaboratori è una priorità.',
      en: 'With every guest, including high-profile ones. Protecting our partners’ reputation is a priority.',
    },
  },
  {
    title: { it: 'Qualità del drink', en: 'Drink quality' },
    text: {
      it: 'Qualità gustativa, estetica nelle decorazioni, controllo rigoroso delle temperature.',
      en: 'Taste, aesthetic garnish and rigorous temperature control.',
    },
  },
  {
    title: { it: 'Supporto al catering', en: 'Support for the catering team' },
    text: {
      it: 'Il catering può chiudere la cena con serenità, caricare il materiale e liberare lo staff senza attendere la fine del dopocena.',
      en: 'The caterer can close dinner service calmly, load out and release their staff without waiting for the after-party to end.',
    },
  },
  {
    title: { it: 'Vicinanza', en: 'Close by' },
    text: {
      it: 'Sede a Montecatini Terme, punto di forza per i catering in Toscana. Ci muoviamo in tutta Italia.',
      en: 'Based in Montecatini Terme — a strategic advantage across Tuscany. We travel throughout Italy.',
    },
  },
];
