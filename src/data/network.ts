import type { ImageMetadata } from 'astro';

export type ProfessionalType = 'wedding-planner' | 'location' | 'catering';

export type RegionKey = 'toscana' | 'centro-italia' | 'nord-italia' | 'sud-italia-isole';

export interface Professional {
  id: string;
  type: ProfessionalType;
  region: RegionKey;
  area: { it: string; en: string };
  name: string;
  tagline: { it: string; en: string };
  description: { it: string; en: string };
  tags?: string[];
  budget?: string;
  image?: ImageMetadata;
  imageAlt?: { it: string; en: string };
  instagram?: string;
  website?: string;
  featured?: boolean;
  languages?: string[];
  bookingLead?: { it: string; en: string };
  advice?: { it: string; en: string };
  locationDetails?: { capacity?: string; rooms?: string; ceremony?: string };
}

export const regionLabels: Record<RegionKey, { it: string; en: string }> = {
  'toscana':            { it: 'Toscana',            en: 'Tuscany'                  },
  'centro-italia':      { it: 'Centro Italia',       en: 'Central Italy'            },
  'nord-italia':        { it: 'Nord Italia',         en: 'Northern Italy'           },
  'sud-italia-isole':   { it: 'Sud Italia e Isole', en: 'Southern Italy & Islands' },
};

export const typeLabels: Record<ProfessionalType, { it: string; en: string }> = {
  'wedding-planner': { it: 'Wedding Planner', en: 'Wedding Planner' },
  'location':        { it: 'Location',        en: 'Venue'           },
  'catering':        { it: 'Catering',        en: 'Catering'        },
};

export const professionals: Professional[] = [
  /* ── Wedding Planners ── */
  {
    id: 'wp-001',
    type: 'wedding-planner',
    region: 'toscana',
    area: { it: 'Toscana', en: 'Tuscany' },
    name: 'Studio Fiori Weddings',
    tagline: { it: 'Matrimoni italiani e destination wedding.', en: 'Italian weddings and destination weddings.' },
    description: { it: 'Organizzazione completa per coppie italiane e internazionali, con profonda conoscenza del territorio toscano e delle sue ville storiche.', en: 'Full-service planning for Italian and international couples, with deep knowledge of Tuscany and its historic villas.' },
    tags: ['Destination wedding', 'Ville storiche'],
    budget: '€€€',
    featured: true,
    languages: ['IT', 'EN', 'FR'],
    bookingLead: { it: '12 mesi prima', en: '12 months ahead' },
    advice: { it: 'Contattatela almeno 12 mesi prima: per maggio e settembre le date migliori vanno via presto.', en: 'Contact them at least 12 months ahead: the best May and September dates go fast.' },
  },
  {
    id: 'wp-002',
    type: 'wedding-planner',
    region: 'nord-italia',
    area: { it: 'Milano', en: 'Milan' },
    name: 'Bianchi & Rossi Weddings',
    tagline: { it: 'Relazione, eleganza, ogni dettaglio al suo posto.', en: 'Relationship, elegance, every detail in its place.' },
    description: { it: 'Studio milanese specializzato in matrimoni di lusso per coppie internazionali. Coordinamento completo con rete di fornitori selezionati.', en: 'Milan-based studio specialised in luxury weddings for international couples. Full coordination with a curated supplier network.' },
    tags: ['Luxury', 'Grandi eventi'],
    budget: '€€€€',
    languages: ['IT', 'EN', 'DE'],
    bookingLead: { it: '14 mesi prima', en: '14 months ahead' },
    advice: { it: 'Perfetta per coppie internazionali che vogliono un referente unico: gestisce tutto, dagli hotel ai transfer.', en: 'Perfect for international couples wanting a single point of contact: they handle everything, from hotels to transfers.' },
  },
  {
    id: 'wp-003',
    type: 'wedding-planner',
    region: 'centro-italia',
    area: { it: 'Roma', en: 'Rome' },
    name: 'Atelier del Giorno',
    tagline: { it: 'Il design al servizio del vostro giorno.', en: 'Design in service of your day.' },
    description: { it: 'Wedding design e coordinamento per eventi raffinati tra Roma e il Lazio. Specializzate in elopement e piccoli matrimoni con grande cura estetica.', en: 'Wedding design and coordination for refined events in Rome and Lazio. Specialised in elopements and small weddings with great aesthetic care.' },
    tags: ['Elopement', 'Matrimoni intimi'],
    budget: '€€',
    languages: ['IT', 'EN'],
    bookingLead: { it: '6–8 mesi prima', en: '6–8 months ahead' },
    advice: { it: 'Ideale per chi vuole un matrimonio curato e intimo. Ottimo rapporto qualità-prezzo nella fascia media.', en: 'Ideal for couples who want a carefully curated, intimate wedding. Excellent value in the mid-range bracket.' },
  },
  {
    id: 'wp-004',
    type: 'wedding-planner',
    region: 'toscana',
    area: { it: 'Firenze', en: 'Florence' },
    name: 'Verde Wedding Studio',
    tagline: { it: 'Spontanei, precisi, appassionati.', en: 'Spontaneous, precise, passionate.' },
    description: { it: 'Organizzazione completa e matrimoni elopement in Toscana, con vocazione per i dettagli artigianali e la scenografia naturale dei borghi.', en: 'Full planning and elopement weddings in Tuscany, with a focus on artisan details and the natural scenography of Tuscan villages.' },
    tags: ['Destination wedding', 'Matrimoni in campagna'],
    budget: '€€',
    languages: ['IT', 'EN'],
    bookingLead: { it: '8–10 mesi prima', en: '8–10 months ahead' },
    advice: { it: 'Conoscono la Toscana palmo a palmo: affidatevi a loro per i borghi meno noti, spesso più belli e meno costosi.', en: 'They know Tuscany inside out: trust them for the lesser-known villages, often more beautiful and less expensive.' },
  },
  {
    id: 'wp-005',
    type: 'wedding-planner',
    region: 'nord-italia',
    area: { it: 'Milano / Roma', en: 'Milan / Rome' },
    name: 'Luxury Events Italia',
    tagline: { it: 'Standard internazionale, cuore italiano.', en: 'International standards, Italian heart.' },
    description: { it: 'Luxury wedding planning per ospiti internazionali che scelgono l\'Italia. Esperienze su misura, coordinamento dal Nord al Sud.', en: 'Luxury wedding planning for international guests choosing Italy. Tailored experiences, coordination from North to South.' },
    tags: ['Luxury', 'Lago di Como'],
    budget: '€€€€',
    languages: ['IT', 'EN', 'DE', 'FR'],
    bookingLead: { it: '18 mesi prima', en: '18 months ahead' },
    advice: { it: 'La scelta giusta quando gli ospiti arrivano da più paesi: gestiscono ogni aspetto logistico con standard internazionali.', en: 'The right choice when guests arrive from multiple countries: they handle every logistical aspect to international standards.' },
  },
  {
    id: 'wp-006',
    type: 'wedding-planner',
    region: 'sud-italia-isole',
    area: { it: 'Puglia / Sicilia', en: 'Puglia / Sicily' },
    name: 'Esperia Events',
    tagline: { it: 'Il Sud Italia come non lo avete mai visto.', en: 'Southern Italy as you\'ve never seen it.' },
    description: { it: 'Specializzate in matrimoni in Puglia, Sicilia e Calabria. Reti locali solide, conoscenza profonda delle tradizioni e dei luoghi più esclusivi del meridione.', en: 'Specialised in weddings in Puglia, Sicily and Calabria. Strong local networks and deep knowledge of the South\'s most exclusive venues.' },
    tags: ['Tradizioni del Sud', 'Matrimoni sul mare'],
    budget: '€€€',
    languages: ['IT', 'EN'],
    bookingLead: { it: '10–12 mesi prima', en: '10–12 months ahead' },
    advice: { it: 'Indispensabili se scegliete il Sud Italia: la loro rete locale apre porte che non esistono online.', en: "Indispensable if you choose Southern Italy: their local network opens doors that don't exist online." },
  },
  /* ── Locations ── */
  {
    id: 'loc-001',
    type: 'location',
    region: 'toscana',
    area: { it: 'Siena', en: 'Siena' },
    name: 'Villa Belvedere',
    tagline: { it: 'Panorama sulla Val d\'Orcia.', en: 'Views over the Val d\'Orcia.' },
    description: { it: 'Villa storica toscana con giardino all\'italiana, interni affrescati e capienza fino a 200 ospiti. Disponibile per esclusiva.', en: 'Historic Tuscan villa with Italian garden, frescoed interiors and capacity for up to 200 guests. Available for exclusive hire.' },
    tags: ['Toscana', 'Interno & Esterno'],
    budget: '€€€',
    featured: true,
    bookingLead: { it: '12–18 mesi prima', en: '12–18 months ahead' },
    advice: { it: "Prenotate in anticipo per giugno e settembre: la vista sulla Val d'Orcia è insuperabile e le date si esauriscono presto.", en: "Book well in advance for June and September: the Val d'Orcia view is unbeatable and dates sell out early." },
    locationDetails: { capacity: 'Fino a 200', rooms: '40 camere', ceremony: 'Civile e simbolica' },
  },
  {
    id: 'loc-002',
    type: 'location',
    region: 'centro-italia',
    area: { it: 'Perugia', en: 'Perugia' },
    name: 'Castello di Corte',
    tagline: { it: 'Pietra, storia, bellezza.', en: 'Stone, history, beauty.' },
    description: { it: 'Castello medievale in Umbria con torre panoramica, cantina storica e giardini romantici. Fino a 150 ospiti.', en: 'Medieval castle in Umbria with panoramic tower, historic wine cellar and romantic gardens. Up to 150 guests.' },
    tags: ['Umbria', 'Storico'],
    budget: '€€€',
    bookingLead: { it: '10–12 mesi prima', en: '10–12 months ahead' },
    advice: { it: 'La cantina storica è lo spazio più suggestivo per il ricevimento serale quando il castello si illumina.', en: 'The historic wine cellar is the most evocative space for the evening reception when the castle is lit up.' },
    locationDetails: { capacity: 'Fino a 150', rooms: '15 camere', ceremony: 'Simbolica' },
  },
  {
    id: 'loc-003',
    type: 'location',
    region: 'nord-italia',
    area: { it: 'Treviso', en: 'Treviso' },
    name: 'Tenuta dei Fiori',
    tagline: { it: 'Colline venete, vigneti, silenzio.', en: 'Venetian hills, vineyards, silence.' },
    description: { it: 'Agriturismo di lusso tra i vigneti del Prosecco. Atmosfera autentica, vocazione gastronomica e location fotografica per eccellenza.', en: 'Luxury farm stay among Prosecco vineyards. Authentic atmosphere, culinary vocation and a naturally photogenic setting.' },
    tags: ['Veneto', 'Rustico'],
    budget: '€€',
    bookingLead: { it: '8–10 mesi prima', en: '8–10 months ahead' },
    advice: { it: 'La primavera è la stagione ideale: i vigneti in fiore e le temperature miti rendono tutto naturalmente scenografico.', en: 'Spring is the ideal season: flowering vineyards and mild temperatures make everything naturally scenic.' },
    locationDetails: { capacity: 'Fino a 100', rooms: '20 camere', ceremony: 'Solo simbolica' },
  },
  {
    id: 'loc-004',
    type: 'location',
    region: 'centro-italia',
    area: { it: 'Viterbo', en: 'Viterbo' },
    name: 'Borgo San Leone',
    tagline: { it: 'Un intero borgo medievale per voi.', en: 'An entire medieval hamlet, all yours.' },
    description: { it: 'Borgo esclusivo nel Lazio disponibile in affitto privato. Fino a 80 ospiti in pernottamento, capienza eventi fino a 250.', en: 'Exclusive hamlet in Lazio available for private hire. Up to 80 overnight guests, event capacity up to 250.' },
    tags: ['Lazio', 'Esclusivo'],
    budget: '€€€€',
    bookingLead: { it: '14–18 mesi prima', en: '14–18 months ahead' },
    advice: { it: "L'esclusiva del borgo vale ogni euro: nessun ospite estraneo, nessuna sovrapposizione, solo voi.", en: 'The exclusive hire of the hamlet is worth every euro: no other guests, no overlap, just you.' },
    locationDetails: { capacity: 'Fino a 250', rooms: '80 camere', ceremony: 'Civile e simbolica' },
  },
  {
    id: 'loc-005',
    type: 'location',
    region: 'centro-italia',
    area: { it: 'Roma', en: 'Rome' },
    name: 'Palazzo Rinascimento',
    tagline: { it: 'Il cuore storico di Roma.', en: 'The historic heart of Rome.' },
    description: { it: 'Palazzo del XVI secolo con salone affrescato e terrazza panoramica sui tetti di Roma. Ideale per eventi di classe fino a 100 ospiti.', en: '16th-century palazzo with frescoed hall and panoramic rooftop terrace over Rome. Ideal for elegant events up to 100 guests.' },
    tags: ['Lazio', 'Urbano'],
    budget: '€€€€',
    bookingLead: { it: '12 mesi prima', en: '12 months ahead' },
    advice: { it: 'Le autorizzazioni per gli eventi in centro storico richiedono tempo: affidate la pratica al palazzo, hanno già tutto strutturato.', en: 'Permits for events in the historic centre take time: let the palazzo handle the paperwork, they have everything in place.' },
    locationDetails: { capacity: 'Fino a 100', rooms: 'Nessuna', ceremony: 'Civile' },
  },
  {
    id: 'loc-006',
    type: 'location',
    region: 'sud-italia-isole',
    area: { it: 'Costa Smeralda', en: 'Costa Smeralda' },
    name: 'Villa Marina',
    tagline: { it: 'Il mare sardo a perdita d\'occhio.', en: 'The Sardinian sea as far as the eye can see.' },
    description: { it: 'Villa privata affacciata sul Mediterraneo in Costa Smeralda. Spiaggia privata, giardino botanico, piscina infinity.', en: 'Private villa overlooking the Mediterranean in Costa Smeralda. Private beach, botanical garden, infinity pool.' },
    tags: ['Sardegna', 'Sul mare'],
    budget: '€€€€',
    bookingLead: { it: '18 mesi prima', en: '18 months ahead' },
    advice: { it: "Se volete privacy assoluta evitate agosto: luglio o settembre garantiscono la stessa bellezza con meno affollamento.", en: 'For total privacy avoid August: July or September offer the same beauty with far fewer visitors.' },
    locationDetails: { capacity: 'Fino a 80', rooms: '12 suite', ceremony: 'Solo simbolica' },
  },
  /* ── Catering ── */
  {
    id: 'cat-001',
    type: 'catering',
    region: 'toscana',
    area: { it: 'Firenze', en: 'Florence' },
    name: 'Sapori & Colori Catering',
    tagline: { it: 'Cucina italiana contemporanea.', en: 'Contemporary Italian cuisine.' },
    description: { it: 'Catering che lavora con i migliori produttori locali toscani. Personalizzazione completa del menu: il cibo sarà sempre parte indimenticabile della festa.', en: 'Catering that works with Tuscany\'s best local producers. Full menu customisation so the food becomes an unforgettable part of the celebration.' },
    tags: ['Toscana', 'Km zero'],
    budget: '€€€',
    featured: true,
    languages: ['IT', 'EN'],
    bookingLead: { it: '8 mesi prima', en: '8 months ahead' },
    advice: { it: 'Chiedete il menu di degustazione prima di confermare: ogni piatto racconta il territorio.', en: 'Ask for the tasting menu before confirming: each dish tells a story of the land.' },
  },
  {
    id: 'cat-002',
    type: 'catering',
    region: 'nord-italia',
    area: { it: 'Milano', en: 'Milan' },
    name: 'Alto Gusto Banqueting',
    tagline: { it: 'Servizio impeccabile dal buffet alla cena di gala.', en: 'Impeccable service from buffet to gala dinner.' },
    description: { it: 'Banqueting di lusso per grandi eventi. Esperienza consolidata con matrimoni internazionali e banchetti aziendali su tutta la penisola.', en: 'Luxury banqueting for large events. Established experience with international weddings and corporate banquets across Italy.' },
    tags: ['Nazionale', 'Luxury'],
    budget: '€€€€',
    languages: ['IT', 'EN', 'DE'],
    bookingLead: { it: '10 mesi prima', en: '10 months ahead' },
    advice: { it: 'La loro forza sono i grandi numeri: da 150 ospiti in su il servizio diventa impeccabile.', en: 'Their strength is large numbers: from 150 guests upward the service becomes impeccable.' },
  },
  {
    id: 'cat-003',
    type: 'catering',
    region: 'centro-italia',
    area: { it: 'Roma', en: 'Rome' },
    name: 'Chef Privato Roma',
    tagline: { it: 'La cucina del territorio portata al matrimonio.', en: 'Local cuisine brought to the wedding.' },
    description: { it: 'Chef privato con esperienza nei migliori ristoranti romani. Cucina del territorio e piatti della tradizione italiana rivisitati con tecnica moderna.', en: 'Private chef with experience in Rome\'s finest restaurants. Local cuisine and Italian tradition revisited with modern technique.' },
    tags: ['Lazio', 'Chef privato'],
    budget: '€€',
    languages: ['IT', 'EN'],
    bookingLead: { it: '6 mesi prima', en: '6 months ahead' },
    advice: { it: 'Perfetto per eventi fino a 80 ospiti: il servizio è molto personalizzato e lo chef è presente per tutto il ricevimento.', en: 'Perfect for events up to 80 guests: highly personalised service with the chef present throughout the reception.' },
  },
  {
    id: 'cat-004',
    type: 'catering',
    region: 'toscana',
    area: { it: 'Siena', en: 'Siena' },
    name: 'Gourmet Toscana',
    tagline: { it: 'L\'eccellenza del territorio in ogni piatto.', en: 'The best of the territory in every dish.' },
    description: { it: 'Catering gourmet specializzato in matrimoni toscani. Prodotti biologici, vini locali selezionati, presentazione curata in ogni minimo dettaglio.', en: 'Gourmet catering specialised in Tuscan weddings. Organic products, selected local wines, carefully crafted presentation.' },
    tags: ['Toscana', 'Gourmet'],
    budget: '€€€',
    languages: ['IT', 'EN'],
    bookingLead: { it: '8–10 mesi prima', en: '8–10 months ahead' },
    advice: { it: "L'abbinamento vino-piatto è il loro punto di forza: lasciateli guidare nella selezione delle etichette locali.", en: 'Wine-to-dish pairing is their strength: let them guide the selection of local labels.' },
  },
  {
    id: 'cat-005',
    type: 'catering',
    region: 'nord-italia',
    area: { it: 'Milano', en: 'Milan' },
    name: 'Food Design Studio',
    tagline: { it: 'L\'estetica del cibo come linguaggio visivo.', en: 'Food aesthetics as visual language.' },
    description: { it: 'Catering creativo con forte identità visiva. Piatti progettati per essere fotografati, pensati per essere gustati. Ideale per coppie con una visione estetica precisa.', en: 'Creative catering with a strong visual identity. Dishes designed to be photographed, made to be enjoyed. Ideal for couples with a precise aesthetic vision.' },
    tags: ['Nazionale', 'Creativo'],
    budget: '€€€',
    languages: ['IT', 'EN'],
    bookingLead: { it: '10 mesi prima', en: '10 months ahead' },
    advice: { it: "Contattateli con un moodboard del matrimonio: il cibo diventa parte dello stile visivo dell'evento.", en: "Contact them with a wedding moodboard: the food becomes part of the event's visual style." },
  },
  {
    id: 'cat-006',
    type: 'catering',
    region: 'toscana',
    area: { it: 'Arezzo', en: 'Arezzo' },
    name: 'Pasticceria del Borgo',
    tagline: { it: 'La torta nuziale come opera d\'arte.', en: 'The wedding cake as a work of art.' },
    description: { it: 'Pasticceria artigianale con specializzazione in torte nuziali su commissione e dessert table per matrimoni. Ogni creazione è unica e irripetibile.', en: 'Artisan pastry specialised in bespoke wedding cakes and dessert tables. Every creation is unique and unrepeatable.' },
    tags: ['Toscana', 'Pasticceria'],
    budget: '€€',
    languages: ['IT', 'EN', 'FR'],
    bookingLead: { it: '6 mesi prima', en: '6 months ahead' },
    advice: { it: 'Prenotate la torta almeno 6 mesi prima e fissate un appuntamento per la degustazione: ogni torta è su misura.', en: 'Book the cake at least 6 months ahead and schedule a tasting: every cake is bespoke and requires multiple trials.' },
  },
];

export function professionalsOfType(type: ProfessionalType): Professional[] {
  return professionals.filter(p => p.type === type);
}

export function byRegion(type: ProfessionalType): Array<{ region: RegionKey; items: Professional[] }> {
  const order: RegionKey[] = ['toscana', 'centro-italia', 'nord-italia', 'sud-italia-isole'];
  return order
    .map(region => ({ region, items: professionals.filter(p => p.type === type && p.region === region) }))
    .filter(g => g.items.length > 0);
}
