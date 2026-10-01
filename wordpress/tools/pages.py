"""
Page compositions (one function per page of the original site).
Each returns (blocks, meta) where meta holds SEO title/description per language.
"""
from __future__ import annotations

from blocks import B, Ctx, _cls, btn_link, btn_primary, button, buttons, eyebrow, group, h, img, p, section, ul
from sections import (DATA, LT, bar_card_body, bar_collection, bar_media, bar_section, cf7, cocktail_families,
                      cocktail_gallery, comparison_section, cta_band, cta_row, destinations, editorial, experience_mosaic,
                      faq, glassware, hero_dark, hero_home, ice_section, instagram_strip, ip, numbered_grid,
                      page_hero, partner_cta, personalisation, portfolio_query, services_list, sh, tower, trust_bar, why_grid)

Q = ('Request a quote', 'Richiedi un preventivo')


def quote_btn(c, track, cls=None, url=None):
    return btn_primary(c, c.T(*Q), url or c.L('contact'), track) if not cls else button(c, c.T(*Q), url or c.L('contact'), cls=f'{cls} meteora-track-{track}')


def quote_link(c, track, url=None):
    return btn_link(c, c.T(*Q), url or c.L('contact'), track)


# ===================================================================== HOME
def home(c: Ctx):
    moments = [('Aperitivo', 'Aperitivo'), ('Open bar', 'Open bar'), ('Cocktails', 'Cocktail'), ('Signature moments', 'Momenti signature'),
               ('Towers', 'Tower'), ('Customisation', 'Personalizzazione'), ('Service', 'Servizio')]
    blocks = [
        hero_home(c),
        trust_bar(c),
        experience_mosaic(c),
        section(c, [editorial(c, 'bars/pure-white-villa.webp', c.T('Pure White bar in the garden of a stone villa', 'Banco Pure White nel giardino di una villa in pietra'), [
            eyebrow(c, c.T('Weddings', 'Matrimoni')),
            h(c, 2, c.H('Your wedding. <em>Your bar experience.</em>', 'Il vostro matrimonio. <em>La vostra bar experience.</em>'), cls='animate-fade-up animate-delay-1'),
            p(c, c.T('From the garden aperitivo to the last toast after dinner, the bar accompanies every moment of the day — and stays in the photographs.',
                     'Dall’aperitivo in giardino all’ultimo brindisi dopo cena, il bar accompagna ogni momento della giornata — e resta nelle fotografie.'), cls='is-style-lead is-muted animate-fade-up animate-delay-2'),
            ul(c, [c.T(en, it) for en, it in moments], cls='is-style-list-inline animate-fade-up animate-delay-3'),
            cta_row(c, [btn_primary(c, c.T('Discover wedding services', 'Scopri i servizi per matrimoni'), c.L('weddings')), quote_link(c, 'weddings_quote')], cls='animate-fade-up animate-delay-4'),
        ], second='details/mint-coupes.webp', second_alt=c.T('Coupes with fresh mint and red berries on the bar', 'Coppe con menta fresca e frutti rossi sul banco'))], cls='mt-home-weddings', name='Weddings'),
        section(c, [group(c, [
            group(c, [
                eyebrow(c, 'Destination Weddings'),
                h(c, 2, c.H('Destination weddings <em>in Italy.</em>', 'Destination wedding <em>in Italia.</em>'), cls='animate-fade-up animate-delay-1'),
                p(c, c.T('Based in Tuscany, available throughout Italy. For couples who choose Italy, we are the bar partner who knows the villas, the timings and the people.',
                         'Base in Toscana, disponibili in tutta Italia. Per le coppie che scelgono l’Italia, siamo il partner bar che conosce le ville, i tempi e le persone.'), cls='is-style-lead is-muted animate-fade-up animate-delay-2'),
                buttons(c, [btn_primary(c, c.T('Destination weddings with Meteora', 'Destination wedding con Meteora'), c.L('destination'))]),
            ], cls='mt-split__intro'),
            destinations(c, compact=True),
        ], cls='mt-split mt-split--sticky')], cls='mt-home-dest', alt=True, name='Destination weddings'),
        bar_section(c),
        section(c, [
            sh(c, 'Cocktail Experience', c.H('Where cocktails <em>become part of the event.</em>', 'Dove il cocktail <em>diventa parte dell’evento.</em>'),
               c.T('A complete, balanced drink list, from the great classics to the Italian aperitivo, with variations on request and signatures created for you.',
                   'Una drink list completa ed equilibrata, dai grandi classici all’aperitivo italiano, con varianti su richiesta e signature create per voi.'), align='split'),
            cocktail_families(c),
        ], cls='mt-home-cocktails', alt=True, name='Cocktail experience'),
        ice_section(c, show_types=False),
        personalisation(c),
        tower(c),
        comparison_section(c, 'Open Bar', c.H('Two experiences, <em>one standard.</em>', 'Due esperienze, <em>uno stesso standard.</em>'),
                           c.T('Essential and Premium share the same service, staff and care. What changes is the label selection, the mixers and the presentation.',
                               'Essential e Premium condividono servizio, staff e cura. Cambiano la selezione delle etichette, i mixer e la presentazione.')),
        section(c, [
            sh(c, c.T('Events', 'Eventi'), c.H('Every event is <em>unique and unrepeatable.</em>', 'Ogni evento <em>è unico e irripetibile.</em>'),
               c.T('What we create remains in the images, and in the memories.', 'Ciò che realizziamo resta impresso nelle immagini e nei ricordi.'), align='split'),
            portfolio_query(c, 3),
            cta_row(c, [btn_primary(c, c.T('All events', 'Tutti gli eventi'), c.L('events')), quote_link(c, 'portfolio_quote')], cls='mt-section-cta'),
        ], cls='mt-portfolio', alt=True, name='Portfolio'),
        partner_cta(c),
        instagram_strip(c),
        cta_band(c, 'bars/golden-marble-night.webp', c.T('Golden bar lit up at night', 'Banco dorato illuminato di sera'), track='home_band'),
    ]
    meta = {'en': ('Meteora Events | Luxury Open Bar Catering in Tuscany & Italy', 'Luxury open bar catering for weddings, destination weddings, corporate and private events. Scenographic bars, cocktails, premium ice and professional glassware. Based in Tuscany, serving all of Italy.'),
            'it': ('Meteora Events | Open Bar Catering di lusso in Toscana e in Italia', 'Luxury open bar catering per matrimoni, destination wedding, eventi aziendali e privati. Banchi scenografici, cocktail, ghiaccio e bicchieri professionali. Base in Toscana, in tutta Italia.')}
    return blocks, meta


# ===================================================================== WEDDINGS
def weddings(c: Ctx):
    day = [
        (('Aperitivo', 'Aperitivo'), ('Spritz, Bellini, Mimosa, Prosecco and alcohol-free cocktails while you are busy with photographs. Integrated into the bar or served from draped tables.', 'Spritz, Bellini, Mimosa, Prosecco e cocktail analcolici, mentre gli sposi sono impegnati con le foto. Integrato nel banco o su tavoli tovagliati.')),
        (('Open bar', 'Open bar'), ('Three hours after dinner, with our signature drink list, the classics and variations on request.', 'Tre ore dopo cena, con la nostra drink list signature, i classici e le varianti su richiesta.')),
        (('Signature moments', 'Momenti signature'), ('The toast, the cake cutting, the start of the party: a cascading Tower turns a gesture into a scene.', 'Il brindisi, il taglio della torta, l’apertura della festa: una Tower a cascata trasforma un gesto in scenografia.')),
        (('Customisation', 'Personalizzazione'), ('Napkins and bar front with your names, initials pressed into ice, cocktails named after you.', 'Tovaglioli e frontale banco con i vostri nomi, iniziali impresse sul ghiaccio, cocktail che portano il vostro nome.')),
        (('Service', 'Servizio'), ('Discreet staff in total black. No crates in view, restocking by tray, the venue left spotless.', 'Staff in total black, discreto. Nessuna cassa a vista, rifornimenti a vassoio, location lasciata pulita.')),
    ]
    blocks = [
        page_hero(c, c.T('Weddings', 'Matrimoni'), c.H('Your wedding. <em>Your bar experience.</em>', 'Il vostro matrimonio. <em>La vostra bar experience.</em>'),
                  c.T('A bar that belongs to the most important day: designed around your style, run independently, made for your guests — and for the photographs.',
                      'Un bar che fa parte del giorno più importante: progettato sul vostro stile, gestito in autonomia, pensato per gli ospiti e per le fotografie.'),
                  'towers/couple-pour.webp', c.T('A couple pouring sparkling wine over a coupe tower', 'Sposi che versano le bollicine sulla tower di coppe'),
                  ctas=[quote_btn(c, 'weddings_hero_quote', url=c.L('contact') + '?type=wedding'), btn_link(c, c.T('Marrying in Italy from abroad?', 'Vi sposate in Italia dall’estero?'), c.L('destination'))]),
        section(c, [
            sh(c, c.T('Through the day', 'Durante la giornata'), c.H('Every moment <em>has its drink.</em>', 'Ogni momento <em>ha il suo drink.</em>'),
               c.T('We fit into the wedding timeline, in step with your planner, venue and caterer.', 'Ci integriamo nel programma del matrimonio, coordinandoci con planner, location e catering.'), align='split'),
            numbered_grid(c, [(c.T(*t), c.T(*d)) for t, d in day], cols=5),
        ], pad_top=False, name='Through the day'),
        section(c, [editorial(c, 'bars/pure-white-villa.webp', c.T('Pure White bar at a villa', 'Banco Pure White in villa'), [
            eyebrow(c, c.T('Our method', 'Il nostro metodo')),
            h(c, 2, c.H('One less thing <em>to worry about.</em>', 'Un pensiero <em>in meno.</em>'), cls='animate-fade-up'),
            p(c, c.T('We bring the bar, glassware, products, ice and staff. We set up, serve and dismantle completely independently, without weighing on the caterer or the venue.',
                     'Portiamo banco, bicchieri, prodotti, ghiaccio e staff. Allestiamo, serviamo e smontiamo in completa autonomia, senza pesare sul catering o sulla location.'), cls='is-muted animate-fade-up'),
            p(c, c.T('Behind the bar you will never see cool boxes or glass racks: every restock is carried by tray. In your photographs, only the bar remains.',
                     'Dietro al banco non vedrete contenitori termici o ceste di bicchieri: ogni rifornimento avviene a vassoio. Nelle vostre fotografie resterà solo il bar.'), cls='is-muted animate-fade-up'),
            buttons(c, [btn_link(c, c.T('Why Meteora', 'Perché Meteora'), c.L('why'))]),
        ], second='details/champagne-bowl.webp', second_alt=c.T('Champagne bowl on the bar', 'Champagne bowl sul banco'), reverse=True)], alt=True, name='Our method'),
        bar_section(c, title=c.H('Choose <em>your bar.</em>', 'Scegliete <em>il vostro banco.</em>'),
                    lead=c.T('Every model in three sizes, chosen for your style, venue and guest count.', 'Ogni modello in tre misure, da scegliere in base a stile, location e numero di ospiti.'), ctas=False),
        tower(c),
        personalisation(c),
        comparison_section(c, 'Open Bar', c.H('Essential <em>or Premium.</em>', 'Essential <em>o Premium.</em>')),
        section(c, [sh(c, c.T('Why Meteora', 'Perché Meteora'), c.H('What <em>you don’t see</em> makes the difference.', 'Ciò che <em>non si vede</em> fa la differenza.')), why_grid(c, 4)], alt=True, name='Why Meteora'),
        faq(c, 'wedding'),
        cta_band(c, 'bars/golden-mirror-sunset.webp', c.T('Golden Mirror bar at sunset', 'Banco Golden Mirror al tramonto'),
                 title=c.H('Tell us about <em>your day.</em>', 'Raccontateci <em>il vostro giorno.</em>'), url=c.L('contact') + '?type=wedding', track='weddings_band',
                 secondary=btn_link(c, 'Destination weddings', c.L('destination'))),
    ]
    meta = {'en': ('Wedding Bar Catering in Italy | Meteora Events', 'Open bar and cocktail experience for weddings in Italy: aperitivo, after-dinner open bar, Signature Towers, scenographic bars and personalisation. Based in Tuscany.'),
            'it': ('Bar Catering per Matrimoni in Toscana e in Italia | Meteora Events', 'Open bar e cocktail experience per matrimoni: aperitivo, open bar dopo cena, Signature Tower, banchi scenografici e personalizzazioni. Base in Toscana, in tutta Italia.')}
    return blocks, meta


# ===================================================================== DESTINATION
GUIDE = [
    (('How bar catering works', 'Come funziona il bar catering'), ('We take care of the entire bar service: we design the drink list, bring the bar counter, glassware, products and ice, and run the service with our own staff. Our standard open bar lasts three hours; the Aperitivo + Open Bar package adds ninety minutes of aperitivo before dinner.', 'Ci occupiamo dell’intera gestione del servizio bar: progettiamo la drink list, portiamo banco, bicchieri, prodotti e ghiaccio, e gestiamo il servizio con il nostro staff. L’open bar standard dura tre ore; il pacchetto Aperitivo + Open Bar aggiunge un’ora e mezza di aperitivo.')),
    (('What is included', 'Cosa è incluso'), ('Products and spirits from the chosen menu, a bar from the collection, our signature drink list with any customisation, professional staff, and our own glassware and setup. Extra time, additional staff and extra bar modules can be added on request.', 'Prodotti e distillati del menu scelto, banco a scelta dalla collezione, drink list signature con personalizzazioni, staff professionale, bicchieri e allestimento di nostra proprietà. Tempo extra, staff e moduli bar aggiuntivi si aggiungono su richiesta.')),
    (('Logistics and travel', 'Logistica e distanze'), ('We are based in Montecatini Terme, in the heart of Tuscany. We work throughout Italy and abroad; any travel and logistics costs are agreed transparently in your quote.', 'Siamo a Montecatini Terme, nel cuore della Toscana. Lavoriamo in tutta Italia e anche all’estero; gli eventuali costi di trasferta e logistica sono concordati in modo trasparente nel preventivo.')),
    (('Working with your caterer', 'Il coordinamento con il catering'), ('We are fully independent: we do not use the caterer’s kitchen, staff or equipment. Your caterer can close dinner service calmly while we carry the party forward.', 'Siamo completamente indipendenti: non usiamo cucina, staff o attrezzature del catering. Il catering può chiudere la cena con serenità mentre noi portiamo avanti la festa.')),
    (('Choosing your bar', 'La scelta del banco'), ('Golden Mirror, Silver Reflection and Pure White, each in three sizes (1.5 m, 3.5 m, 5.5 m). We help you choose based on your venue, style and guest count.', 'Golden Mirror, Silver Reflection e Pure White, ciascuno in tre misure (1,5 m, 3,5 m, 5,5 m). Vi aiutiamo a scegliere in base a location, stile e numero di ospiti.')),
    (('Personal touches', 'Personalizzazioni'), ('Napkins and a bar front with your names (35 days’ notice), engraved fruit and ice, a cocktail list created around you. All agreed during the planning phase.', 'Tovaglioli e frontale banco con i vostri nomi (35 giorni di preavviso), incisioni su frutta e ghiaccio, cocktail list creata su di voi. Si definiscono in fase di ideazione dell’evento.')),
    (('What to consider', 'Cosa considerare'), ('Guest count, length of the party, spaces for aperitivo and after-dinner, the venue’s setup times, preferred labels and alcohol-free options. The more you share, the more precise our proposal.', 'Numero di ospiti, durata della festa, spazi per aperitivo e dopocena, orari di montaggio della location, preferenze di etichette e bevande analcoliche. Più informazioni ci date, più precisa sarà la proposta.')),
]


def destination(c: Ctx):
    blocks = [
        hero_dark(c, 'bars/pure-white-villa.webp', c.T('Pure White bar in a stone villa garden at sunset', 'Banco Pure White nel giardino di una villa in pietra al tramonto'),
                  c.T('Based in Tuscany · Throughout Italy', 'Base in Toscana · In tutta Italia'), c.H('Destination weddings <em>in Italy.</em>', 'Destination wedding <em>in Italia.</em>'),
                  c.T('For couples who travel from around the world to marry in Italy, we are your Italian bar partner: cocktails, service and scenography, with the peace of mind of a local team.',
                      'Per le coppie che arrivano da tutto il mondo per sposarsi in Italia, siamo il partner bar italiano: cocktail, servizio e scenografia, con la tranquillità di un team locale.'),
                  c.T(*Q), c.L('contact') + '?type=destination-wedding', 'destination_hero_quote'),
        section(c, [sh(c, c.T('Where we work', 'Dove lavoriamo'), c.H('Tuscany is home. <em>Italy is our range.</em>', 'La Toscana è casa. <em>L’Italia è il nostro raggio.</em>'),
                       c.T('Our base is in Montecatini Terme. From here we reach Tuscany’s great wedding destinations, travel throughout Italy and also deliver services abroad.',
                           'La nostra sede è a Montecatini Terme. Da qui raggiungiamo le grandi destinazioni del matrimonio in Toscana, ci spostiamo in tutta Italia e realizziamo servizi anche all’estero.'), align='split'),
                    destinations(c)], name='Where we work'),
        section(c, [editorial(c, 'bars/golden-mirror.webp', c.T('Golden Mirror bar on a terrace overlooking the hills', 'Banco Golden Mirror su terrazza con vista sulle colline'), [
            eyebrow(c, c.T('A local partner', 'Un partner locale')),
            h(c, 2, c.H('From afar, <em>in good hands.</em>', 'Da lontano, <em>in buone mani.</em>'), cls='animate-fade-up'),
            p(c, c.T('Planning a wedding in another country means trusting the people on the ground. We work independently alongside your wedding planner, venue and caterer, and we reply in English and Italian.',
                     'Organizzare un matrimonio in un altro Paese significa affidarsi. Lavoriamo in autonomia accanto al vostro wedding planner, alla location e al catering, e rispondiamo in italiano e in inglese.'), cls='is-muted animate-fade-up'),
            p(c, c.T('We know Italian villas, farmhouses and historic homes: we admire them and respect them, during setup and at the end of the night.',
                     'Conosciamo ville, casali e dimore storiche: le ammiriamo e le rispettiamo, in allestimento e a fine serata.'), cls='is-muted animate-fade-up'),
        ], second='towers/coupe-tower-sunset.webp', second_alt=c.T('Coupe tower at sunset', 'Tower di coppe al tramonto'))], alt=True, name='A local partner'),
        section(c, [
            sh(c, c.T('A guide for couples', 'Guida per le coppie'), c.H('Your wedding bar in Italy, <em>step by step.</em>', 'Il bar al vostro matrimonio in Italia, <em>passo per passo.</em>')),
            numbered_grid(c, [(c.T(*t), c.T(*d)) for t, d in GUIDE], cols=3),
            cta_row(c, [btn_link(c, c.T('The bars', 'I banchi'), c.L('bars')), btn_link(c, 'Cocktail Experience', c.L('cocktails')),
                        btn_link(c, c.T('Services', 'Servizi'), c.L('services')), btn_link(c, c.T('Weddings', 'Matrimoni'), c.L('weddings'))], cls='mt-section-cta mt-links'),
        ], name='Guide for couples'),
        faq(c, 'destination', alt=True),
        cta_band(c, 'venues/fresco-hall.webp', c.T('Long table set in a frescoed hall', 'Tavolo imperiale in un salone affrescato'),
                 title=c.H('Getting married in Italy? <em>Write to us.</em>', 'Vi sposate in Italia? <em>Scriveteci.</em>'), url=c.L('contact') + '?type=destination-wedding', track='destination_band'),
    ]
    meta = {'en': ('Destination Wedding Bar Catering in Tuscany & Italy | Meteora Events', 'Luxury bar catering for destination weddings in Italy. Based in Tuscany, serving Florence, Chianti, Siena, Lucca, Pisa, Forte dei Marmi, the rest of Italy and abroad.'),
            'it': ('Destination Wedding in Toscana e in Italia: Bar Catering | Meteora Events', 'Bar catering per destination wedding in Italia. Base in Toscana (Montecatini Terme), operativi a Firenze, Chianti, Siena, Lucca, Pisa, Forte dei Marmi, in tutta Italia e all’estero.')}
    return blocks, meta


# ===================================================================== TUSCANY LANDING
def tuscany(c: Ctx):
    d = next(x for x in DATA['destinations']['destinations'] if x.get('landing'))
    L = d['landing']
    prose = []
    for sec in L['sections']:
        prose.append(h(c, 2, LT(c, sec['h2'])))
        prose += [p(c, c.T(en, it)) for en, it in zip(sec['body']['en'], sec['body']['it'])]
    prose.append(p(c, f'<a href="{c.L("weddings")}">' + c.T('Wedding services', 'Servizi per matrimoni') + f'</a> · <a href="{c.L("destination")}">Destination weddings</a> · <a href="{c.L("cocktails")}">Cocktail Experience</a>'))
    intro = [p(c, c.T(en, it), cls='is-style-lead' if i == 0 else 'is-muted') for i, (en, it) in enumerate(zip(L['intro']['en'], L['intro']['it']))]
    blocks = [
        page_hero(c, c.T('Based in Tuscany · Throughout Italy', 'Base in Toscana · In tutta Italia'), LT(c, L['h1']), None, 'bars/pure-white-villa.webp',
                  c.T('Pure White bar at a villa at sunset', 'Banco Pure White in villa al tramonto'), ctas=[quote_btn(c, 'landing_tuscany_quote', url=c.L('contact') + '?type=wedding')], lead_extra=intro),
        section(c, [group(c, prose, cls='mt-prose', layout={'type': 'constrained', 'contentSize': '62rem'})], pad_top=False, name='Tuscany'),
        section(c, [sh(c, c.T('The Bar Collection', 'I nostri banchi'), c.H('The bar <em>for your venue.</em>', 'Il banco <em>per la vostra location.</em>')), bar_collection(c)], alt=True, name='Bars'),
        faq(c, 'destination'),
        cta_band(c, 'bars/golden-mirror-sunset.webp', c.T('Golden Mirror bar at sunset', 'Banco Golden Mirror al tramonto'), track='landing_tuscany_band'),
    ]
    meta = {'en': (L['title']['en'], L['description']['en']), 'it': (L['title']['it'], L['description']['it'])}
    return blocks, meta


# ===================================================================== BARS
def bars(c: Ctx):
    sizes = DATA['bars']['barSizes']
    size_list = group(c, [group(c, [p(c, z['name'], cls='is-style-micro'), p(c, c.T(z['lengthEn'], z['length']), cls='mt-sizes__v')]) for z in sizes], cls='mt-sizes')
    blocks = [
        page_hero(c, c.T('The Bar Collection', 'I nostri banchi'), c.H('The bar, <em>as scenography.</em>', 'Il bar, <em>come scenografia.</em>'),
                  c.T('Modular, professional, scenographic bars, chosen to match the character of your event. A collection that keeps growing.',
                      'Banchi bar modulari, professionali e scenografici, scelti in base al carattere dell’evento. Una collezione in continuo ampliamento.'),
                  'details/champagne-bowl.webp', c.T('Champagne bowl on a golden marble bar', 'Champagne bowl su banco in marmo dorato'), lead_extra=[size_list]),
        section(c, [
            sh(c, c.T('Collection', 'Collezione'), c.H('Six characters, <em>three sizes.</em>', 'Sei caratteri, <em>tre misure.</em>')),
            bar_collection(c, cards_grid=True),
            p(c, c.T('Every bar comes in Slim (1.5 m), Medium (3.5 m) and Large (5.5 m), and can run in continuous extension. Extra bar modules on request.',
                     'Ogni banco è disponibile in versione Slim (1,5 m), Medium (3,5 m) e Large (5,5 m), anche in estensione continua. Moduli bar aggiuntivi su richiesta.'), cls='is-muted mt-bars__note'),
        ], pad_top=False, name='Collection'),
        cta_band(c, 'bars/golden-marble-night.webp', c.T('Golden bar at night', 'Banco dorato di sera'), title=c.H('Which bar <em>for your event?</em>', 'Quale banco <em>per il vostro evento?</em>'),
                 lead=c.T('We recommend the model and size for your venue, style and guest count.', 'Vi consigliamo modello e misura in base a location, stile e numero di ospiti.'), track='bars_band'),
    ]
    meta = {'en': ('Luxury Mobile Bar Setups for Weddings & Events | Meteora Events', 'The Meteora Events bar collection: Golden Mirror, Silver Reflection, Pure White and new models coming soon. Modular, in three sizes, for weddings and events in Italy.'),
            'it': ('Banchi Bar Scenografici per Eventi e Matrimoni | Meteora Events', 'La collezione di banchi bar Meteora Events: Golden Mirror, Silver Reflection, Pure White e nuovi modelli in arrivo. Modulari, in tre misure, per matrimoni ed eventi.')}
    return blocks, meta


def bar_detail(c: Ctx, slug):
    bars_all = DATA['bars']['bars']
    bar = next(b for b in bars_all if b['slug'] == slug)
    sizes = DATA['bars']['barSizes']
    others = [b for b in bars_all if b['status'] == 'available' and b['slug'] != slug]
    text = [
        B('core/breadcrumbs', {'className': 'mt-crumbs'}),
        eyebrow(c, c.T('The collection', 'La collezione')),
        h(c, 1, bar['name'], cls='mt-bd__title'),
        p(c, LT(c, bar['mood']), cls='mt-bd__mood'),
        p(c, LT(c, bar['description']), cls='is-style-lead is-muted'),
        group(c, [
            group(c, [p(c, c.T('Ideal for', 'Ideale per'), cls='is-style-micro'), ul(c, [c.T(en, it) for en, it in zip(bar['idealFor']['en'], bar['idealFor']['it'])])]),
            group(c, [p(c, c.T('Sizes', 'Misure'), cls='is-style-micro'), ul(c, [z['name'] + ' · ' + c.T(z['lengthEn'], z['length']) for z in sizes])]),
        ], cls='mt-bd__facts'),
        cta_row(c, [quote_btn(c, f'bar_{slug}_quote'), btn_link(c, c.T('Back to collection', 'Torna alla collezione'), c.L('bars'))]),
    ]
    media = [img(c, ip(im['src']), LT(c, im['alt']), cls=f'mt-bd__img animate-image-reveal animate-delay-{i + 1}') for i, im in enumerate(bar['images'])]
    blocks = [
        section(c, [group(c, [group(c, text, cls='mt-bd__text'), group(c, media, cls='mt-bd__media')], cls='mt-bd')], cls='mt-bar-detail', pad_top='xl', name=bar['name']),
        section(c, [h(c, 2, c.T('More from the collection', 'Altri banchi della collezione'), cls='mt-bd__others-title'),
                    group(c, [group(c, [bar_media(c, b), group(c, bar_card_body(c, b, bars_all.index(b)), cls='mt-bar__body')], cls='mt-bar') for b in others], cls='mt-bars-grid')],
                alt=True, name='More bars'),
        cta_band(c, 'bars/terrace-panorama.webp', c.T('Bar in front of a panoramic window', 'Banco bar davanti a una vetrata panoramica'), track=f'bar_{slug}_band'),
    ]
    desc = {lang: bar['mood'][lang] + ' ' + bar['description'][lang] for lang in ('en', 'it')}
    meta = {'en': (f'{bar["name"]} Bar for Weddings & Events | Meteora Events', desc['en']),
            'it': (f'Banco bar {bar["name"]} per eventi e matrimoni | Meteora Events', desc['it'])}
    return blocks, meta


# ===================================================================== COCKTAILS
def cocktails(c: Ctx):
    sig = next(x for x in DATA['cocktails']['cocktailCategories'] if x['id'] == 'signature')
    blocks = [
        page_hero(c, 'Cocktail Experience', c.H('Designed to be experienced. <em>Designed to be remembered.</em>', 'Progettato per essere vissuto. <em>Pensato per essere ricordato.</em>'),
                  c.T('A complete, balanced selection. The way our service is built lets us prepare further classics and variations on request, depending on the ingredients available on site.',
                      'Una selezione completa ed equilibrata. La struttura del nostro servizio permette di preparare altri classici e varianti su richiesta, in base agli ingredienti disponibili.'),
                  'team/bartender-pour.webp', c.T('Bartender pouring a red cocktail into a coupe', 'Bartender che versa un cocktail rosso in una coppa'),
                  ctas=[btn_primary(c, c.T('The drink list', 'La drink list'), '#list'), btn_link(c, c.T('The ice', 'Il ghiaccio'), '#ice'), btn_link(c, c.T('Glassware', 'I bicchieri'), '#glassware')]),
        section(c, [
            sh(c, c.T('Our cocktail list', 'La nostra cocktail list'), c.H('The classics, <em>made with method.</em>', 'I classici, <em>fatti con metodo.</em>'),
               c.T('Aromatic profile and alcohol level (1 to 5) for every drink. Presentation, ice and garnish may vary depending on the chosen offer.',
                   'Profilo aromatico e grado alcolico (da 1 a 5) di ogni drink. Estetica, ghiaccio e garnish possono variare in base all’offerta scelta.'), align='split'),
            cocktail_gallery(c),
        ], anchor='list', pad_top=False, name='Cocktail list'),
        section(c, [editorial(c, 'details/ice-stamp.webp', c.T('Ice cube pressed with initials', 'Cubo di ghiaccio con iniziali impresse'), [
            eyebrow(c, LT(c, sig['label'])),
            h(c, 2, c.H('A cocktail <em>with your name on it.</em>', 'Un cocktail <em>con il vostro nome.</em>'), cls='animate-fade-up'),
            p(c, LT(c, sig['blurb']), cls='is-style-lead is-muted animate-fade-up'),
            p(c, c.T('A bespoke cocktail list takes shape during event planning: we start from your story, the flavours you love or your brand colours, and turn them into drinks.',
                     'La cocktail list su misura si costruisce in fase di ideazione dell’evento: partiamo dalla vostra storia, dai sapori che amate o dai colori del brand, e la trasformiamo in drink.'), cls='is-muted animate-fade-up'),
            buttons(c, [quote_link(c, 'signature_quote')]),
        ], second='team/bartender-strain.webp', second_alt=c.T('Bartender straining a cocktail', 'Bartender che filtra un cocktail'), ratio='portrait')], alt=True, anchor='signature', name='Signature'),
        ice_section(c),
        glassware(c),
        tower(c),
        cta_band(c, 'bars/night-lounge.webp', c.T('Evening bar', 'Banco bar serale'), track='cocktails_band'),
    ]
    meta = {'en': ('Cocktail Experience for Weddings & Events | Meteora Events', 'Cocktail catering in Tuscany and across Italy: classics, spritz, martinis, sours, Italian aperitivo and bespoke signatures. Curated ice and professional glassware.'),
            'it': ('Cocktail Experience per Eventi e Matrimoni | Meteora Events', 'Cocktail catering in Toscana e in Italia: classici, spritz, martini, sour, aperitivo italiano e signature su misura. Ghiaccio selezionato e bicchieri professionali.')}
    return blocks, meta


# ===================================================================== SERVICES
def services(c: Ctx):
    idx = [btn_link(c, LT(c, {'en': sv['name']['en'].replace('Open Bar — ', ''), 'it': sv['name']['it'].replace('Open Bar — ', '')}), '#' + sv['id']) for sv in DATA['services']['services']]
    blocks = [
        page_hero(c, c.T('Services', 'Servizi'), c.H('From aperitivo <em>to the last drink.</em>', 'Dall’aperitivo <em>all’ultimo drink.</em>'),
                  c.T('Complete, independent formulas coordinated with your caterer — or simply our staff and our method. Every proposal is built to measure.',
                      'Formule complete e autonome, coordinate con il catering, oppure solo il nostro staff e il nostro metodo. Ogni proposta è costruita su misura.'),
                  'bars/golden-marble-night.webp', c.T('Golden bar on a chevron floor', 'Banco dorato su pavimento chevron'), ctas=idx),
        services_list(c),
        comparison_section(c, 'Open Bar', c.H('Essential <em>and Premium,</em> compared.', 'Essential <em>e Premium,</em> a confronto.'), alt=True),
        tower(c, cta=False, anchor='tower-detail'),
        faq(c, 'general'),
        cta_band(c, 'bars/golden-mirror.webp', c.T('Golden Mirror bar', 'Banco Golden Mirror'), track='services_band'),
    ]
    meta = {'en': ('Open Bar & Bar Catering Services | Meteora Events', 'Essential and Premium Open Bar, Aperitivo + Open Bar, Signature Tower Experience and bartender-only service. Tailored quotes for weddings and events across Italy.'),
            'it': ('Servizi di Open Bar e Bar Catering | Meteora Events', 'Open Bar Essential e Premium, Aperitivo + Open Bar, Signature Tower Experience e servizio solo barman. Preventivi su misura per matrimoni ed eventi in tutta Italia.')}
    return blocks, meta


# ===================================================================== CORPORATE
def corporate(c: Ctx):
    formats = [('Corporate events', 'Eventi aziendali'), ('Brand activations', 'Brand activation'), ('Product launches', 'Lanci prodotto'),
               ('Private parties', 'Feste private'), ('Company celebrations', 'Celebrazioni aziendali'), ('Gala dinners', 'Cene di gala')]
    pillars = [
        (('Branding', 'Branding'), ('Your logo on the bar front, custom napkins, your logo pressed into ice.', 'Frontale banco con il vostro logo, tovaglioli personalizzati, logo impresso sul ghiaccio.')),
        (('Branded uniforms', 'Divise brandizzate'), ('Company or event logo on shirts, waistcoats and ties with screen-printed patches. To be agreed well in advance.', 'Logo dell’azienda o dell’evento su camicia, gilet e cravatta, con patch serigrafate. Da concordare con adeguato anticipo.')),
        (('Brand cocktails', 'Cocktail di brand'), ('A drink list created and named after your brand identity.', 'Una drink list creata e nominata sull’identità del brand.')),
        (('Discretion', 'Discrezione'), ('Staff trained to respect guests’ privacy, including high-profile guests.', 'Staff formato a non invadere la privacy degli ospiti, anche di quelli più noti.')),
        (('Reliability', 'Affidabilità'), ('Independent service, restocking by tray, nothing out of place at the bar.', 'Servizio autonomo, rifornimenti a vassoio, nessun elemento fuori posto al banco.')),
        (('Visual consistency', 'Coerenza visiva'), ('Bar, glassware, uniforms and garnish speak the same language as your event.', 'Banco, bicchieri, divise e garnish parlano lo stesso linguaggio dell’evento.')),
    ]
    CQ = ('Request a corporate quote', 'Richiedi un preventivo aziendale')
    blocks = [
        hero_dark(c, 'bars/silver-reflection.webp', c.T('Silver Reflection bar in a large hall for an evening event', 'Banco Silver Reflection in una grande sala per evento serale'),
                  c.T('Corporate & private events', 'Eventi aziendali e privati'), c.H('Your brand, <em>served with style.</em>', 'Il vostro brand, <em>servito con stile.</em>'),
                  c.T('Professionalism, customisation and discretion for corporate events, launches, activations and private parties.',
                      'Professionalità, personalizzazione e discrezione per eventi aziendali, lanci, activation e feste private.'),
                  c.T(*CQ), c.L('contact') + '?type=corporate', 'corporate_hero_quote'),
        section(c, [sh(c, c.T('Formats', 'Formati'), c.H('Every format, <em>the same standard.</em>', 'Ogni formato, <em>lo stesso standard.</em>'),
                       c.T('From a product launch to a private villa party: the bar becomes a meeting point and part of your visual identity.',
                           'Dal lancio di prodotto alla festa privata in villa: il bar diventa un punto di incontro e un elemento dell’identità visiva.'), align='split'),
                    ul(c, [c.T(en, it) for en, it in formats], cls='mt-formats animate-fade-up')], name='Formats'),
        section(c, [
            group(c, [
                img(c, 'team/bartender-strain.webp', c.T('Bartender in total black straining a cocktail', 'Bartender in total black che filtra un cocktail'), cls='mt-pillars__img animate-image-reveal'),
                group(c, [
                    eyebrow(c, c.T('For companies', 'Per le aziende')),
                    h(c, 2, c.H('Visible <em>professionalism.</em> Invisible <em>discretion.</em>', 'Professionalità <em>visibile.</em> Discrezione <em>invisibile.</em>'), cls='animate-fade-up'),
                    p(c, c.T('Our standard uniform is total black: no showy logos, nothing to distract. When you need it, we brand it with your identity.',
                             'La divisa standard è total black: nessun logo vistoso, nessun elemento che distragga. Quando serve, la personalizziamo con il vostro brand.'), cls='is-style-lead is-muted animate-fade-up'),
                ]),
            ], cls='mt-split mt-split--end'),
            numbered_grid(c, [(c.T(*t), c.T(*d)) for t, d in pillars], cols=3),
        ], dark=True, name='For companies'),
        section(c, [editorial(c, 'bars/terrace-panorama.webp', c.T('Bar set in front of a panoramic window', 'Banco bar davanti a una vetrata panoramica'), [
            eyebrow(c, c.T('Private events', 'Eventi privati')),
            h(c, 2, c.H('A party, <em>as you imagine it.</em>', 'Una festa, <em>come la immaginate.</em>'), cls='animate-fade-up'),
            p(c, c.T('Birthdays, anniversaries, villa dinners, receptions: a full open bar or simply our bartender, with the same care we bring to large events.',
                     'Compleanni, anniversari, cene in villa, ricevimenti: open bar completo o solo il nostro barman, con la stessa cura dei grandi eventi.'), cls='is-muted animate-fade-up'),
            buttons(c, [btn_link(c, c.T('Bartender-only service', 'Servizio solo barman'), c.L('services', 'bartender'))]),
        ], second='cocktails/espresso-martini.webp', second_alt='Espresso Martini', reverse=True)], name='Private events'),
        section(c, [group(c, [
            img(c, 'details/shaker.webp', c.T('Steel shaker and bar tools', 'Shaker e strumenti da bar in acciaio'), cls='mt-quote__img animate-image-reveal'),
            p(c, c.H('Protecting the image and reputation of our partners <em>is one of our highest priorities.</em>', 'Proteggere l’immagine dei nostri collaboratori <em>è una delle nostre priorità.</em>'), cls='mt-quote__text animate-fade-up'),
        ], cls='mt-quote')], alt=True, name='Discretion'),
        cta_band(c, 'bars/golden-marble-night.webp', c.T('Golden bar lit up at night', 'Banco dorato illuminato di sera'), title=c.H('Let’s talk about <em>your event.</em>', 'Parliamo <em>del vostro evento.</em>'),
                 label=c.T(*CQ), url=c.L('contact') + '?type=corporate', track='corporate_band'),
    ]
    meta = {'en': ('Corporate & Private Event Bar Catering in Italy | Meteora Events', 'Open bar for corporate events, product launches, brand activations, private parties and celebrations. Branded bars and uniforms, bespoke cocktail lists, complete discretion.'),
            'it': ('Bar Catering per Eventi Aziendali e Privati in Italia | Meteora Events', 'Open bar per eventi aziendali, lanci prodotto, brand activation, feste private e celebrazioni. Banchi e divise brandizzati, cocktail list su misura, massima discrezione.')}
    return blocks, meta


# ===================================================================== PARTNERS
def partners(c: Ctx):
    audiences = [
        (('Wedding planners', 'Wedding planner'), ('A supplier who works independently, keeps to the timeline and makes you look good in front of your clients.', 'Un fornitore che lavora in autonomia, rispetta i tempi e fa bella figura con i vostri clienti.')),
        (('Venues', 'Location'), ('Utmost care for walls, floors, furniture and gardens. We leave everything clean after service.', 'Massima cura di mura, pavimenti, arredi e verde. Lasciamo tutto pulito a fine servizio.')),
        (('Caterers', 'Catering'), ('Close dinner service calmly, load out and release your team: the after-party is ours.', 'Chiudete la cena con serenità, caricate il materiale e liberate il vostro staff: il dopocena è nostro.')),
        (('Event professionals', 'Professionisti eventi'), ('A reliable beverage partner for productions, agencies and organisers.', 'Un partner beverage affidabile per produzioni, agenzie e organizzatori.')),
    ]
    benefits = [('Reliable, independent operation', 'Operatività indipendente e affidabile'), ('Professional, discreet staff', 'Staff professionale e discreto'),
                ('Our own equipment and glassware', 'Attrezzatura e bicchieri propri'), ('Organised logistics', 'Logistica organizzata'), ('Care for the venue', 'Cura della location'),
                ('A visually clean service, no crates in view', 'Servizio visivamente pulito, nessuna cassa a vista'), ('Coordination with catering', 'Coordinamento con il catering'),
                ('Available throughout Italy', 'Operativi in tutta Italia')]
    PP = ('Request partner pricing', 'Richiedi listino partner')
    blocks = [
        page_hero(c, c.T('For planners, venues and caterers', 'Per wedding planner, location e catering'), c.H('Your trusted <em>bar catering</em> partner.', 'Il vostro partner <em>di fiducia</em> per il bar.'),
                  c.T('We work alongside wedding planners, venues, caterers and event professionals. Your event stays yours: we take care of the bar, quietly and precisely.',
                      'Lavoriamo al fianco di wedding planner, location, catering e professionisti degli eventi. Il vostro evento resta vostro: noi ci occupiamo del bar, in silenzio e con precisione.'),
                  'venues/fresco-hall.webp', c.T('Long table in a frescoed hall', 'Tavolo imperiale in un salone affrescato'), ctas=[btn_primary(c, c.T(*PP), '#partner-form', 'partner_hero')]),
        section(c, [sh(c, c.T('Who we work with', 'Con chi lavoriamo'), c.H('One goal: <em>a flawless event.</em>', 'Un solo obiettivo: <em>la buona riuscita dell’evento.</em>')),
                    numbered_grid(c, [(c.T(*t), c.T(*d)) for t, d in audiences], cols=4)], pad_top=False, name='Who we work with'),
        section(c, [group(c, [
            group(c, [eyebrow(c, c.T('Why partners choose us', 'Perché i partner ci scelgono')), h(c, 2, c.H('One less thing <em>to worry about.</em>', 'Un pensiero <em>in meno.</em>'), cls='animate-fade-up'),
                      img(c, 'details/champagne-bowl.webp', c.T('Champagne bowl on the bar', 'Champagne bowl sul banco'), cls='mt-ben__img animate-image-reveal')], cls='mt-split__intro'),
            ul(c, [c.T(en, it) for en, it in benefits], cls='mt-ben__list', ordered=True),
        ], cls='mt-split mt-split--sticky')], dark=True, name='Benefits'),
        section(c, [group(c, [
            group(c, [eyebrow(c, c.T('Partner area', 'Area partner'), anim=False), h(c, 2, c.H('Request <em>partner pricing.</em>', 'Richiedete il <em>listino partner.</em>'), anchor='partner-form-title'),
                      p(c, c.T('Our price list for planners, venues and professionals is not public. Fill in the form and we will send you our dedicated terms and rates.',
                               'Il listino riservato a planner, location e professionisti non è pubblico. Compilate il modulo: vi invieremo condizioni e tariffe dedicate.'), cls='is-muted')], cls='mt-split__intro'),
            group(c, [cf7(c, 'partner')], cls='mt-form-wrap'),
        ], cls='mt-split mt-split--sticky')], alt=True, anchor='partner-form', name='Partner form'),
        faq(c, 'partner'),
    ]
    meta = {'en': ('Bar Catering Partner for Wedding Planners & Venues | Meteora Events', 'A bar catering partner for wedding planners, venues, caterers and event professionals. Own staff, equipment and glassware, fully independent service across Italy. Request partner pricing.'),
            'it': ('Partner Bar Catering per Wedding Planner e Location | Meteora Events', 'Bar catering partner per wedding planner, location, catering e professionisti eventi. Staff, attrezzatura e bicchieri propri, servizio autonomo in tutta Italia. Richiedi il listino partner.')}
    return blocks, meta


# ===================================================================== EVENTS
def events(c: Ctx):
    blocks = [
        page_hero(c, c.T('Events', 'Eventi'), c.H('What we create <em>stays in the images.</em>', 'Ciò che realizziamo <em>resta nelle immagini.</em>'),
                  c.T('Every event is unique and unrepeatable. A selection of setups, places and moments.', 'Ogni evento è unico e irripetibile. Una selezione di allestimenti, luoghi e momenti.')),
        section(c, [portfolio_query(c, 12)], cls='mt-portfolio', pad_top=False, name='Portfolio'),
        instagram_strip(c),
        cta_band(c, 'towers/couple-pour.webp', c.T('Couple pouring sparkling wine over the tower', 'Sposi che versano bollicine sulla tower'), title=c.H('The next one <em>could be yours.</em>', 'Il prossimo <em>potrebbe essere il vostro.</em>'), track='events_band'),
    ]
    meta = {'en': ('Events & Portfolio: Weddings, Galas and Parties | Meteora Events', 'A selection of Meteora Events setups and moments: scenographic bars at villas, on panoramic terraces and in grand halls, Signature Towers and open bars.'),
            'it': ('Eventi e Portfolio: Matrimoni, Gala e Feste | Meteora Events', 'Una selezione di allestimenti e momenti Meteora Events: banchi scenografici in villa, su terrazze panoramiche e in grandi sale, Signature Tower e open bar.')}
    return blocks, meta


# ===================================================================== ABOUT
def about(c: Ctx):
    values = [(('Experience', 'Esperienza'), ('More than 14 years of operational experience in events: weddings, corporate and private.', 'Oltre 14 anni di esperienza operativa nel settore eventi: matrimoni, corporate ed eventi privati.')),
              (('Method', 'Metodo'), ('Every service follows a precise method, from setup to load-out.', 'Ogni servizio segue un metodo preciso, dall’allestimento allo smontaggio.')),
              (('Visual culture', 'Cultura visiva'), ('Great attention to the aesthetic and visual side of every setup.', 'Grande attenzione all’aspetto estetico e visivo dell’allestimento.')),
              (('Hospitality', 'Ospitalità'), ('Professionalism and discretion, with every guest.', 'Professionalità e discrezione, con ogni ospite.'))]
    blocks = [
        page_hero(c, c.T('About', 'Chi siamo'), c.H('Beverage expertise. <em>Flawless execution.</em>', 'Esperienza beverage. <em>Esecuzione impeccabile.</em>'),
                  c.T('Meteora Events is the partner specialised in managing beverage services for high-level events. We grew out of more than 14 years of operational experience in events.',
                      'Meteora Events è il partner specializzato nella gestione del servizio beverage per eventi di alto livello. Nasciamo da oltre 14 anni di esperienza operativa negli eventi.'),
                  'team/bartender-strain.webp', c.T('Bartender in a black waistcoat straining a cocktail', 'Bartender in gilet nero che filtra un cocktail')),
        section(c, [editorial(c, 'bars/terrace-panorama.webp', c.T('Bar in front of a panoramic window', 'Banco bar davanti a una vetrata panoramica'), [
            eyebrow(c, c.T('Our story', 'La nostra storia')),
            h(c, 2, c.H('We don’t simply offer <em>a bar service.</em>', 'Non offriamo semplicemente <em>un servizio bar.</em>'), cls='animate-fade-up'),
            p(c, c.T('We bring professionalism, method and scenographic experience, with great attention to the aesthetic and visual side of the setup. We know the dynamics of weddings, corporate and private events inside out, because we have lived them for years.',
                     'Portiamo professionalità, metodo ed esperienza scenografica, con grande attenzione all’aspetto estetico e visivo dell’allestimento. Conosciamo a fondo le dinamiche di matrimoni, eventi corporate e privati, perché le viviamo da anni dall’interno.'), cls='is-muted animate-fade-up'),
            p(c, c.T('Every event is unique and unrepeatable, and what is created remains in the images and in the memories. That is why we aim for excellence, in service and in visual impact.',
                     'Ogni evento è unico e irripetibile, e ciò che viene realizzato resta impresso nelle immagini e nei ricordi. Per questo puntiamo all’eccellenza, nel servizio e nell’impatto visivo.'), cls='is-style-lead animate-fade-up'),
            p(c, c.T('We create bar services and cocktail experiences for private clients, companies and event professionals, from our base in Montecatini Terme, Tuscany.',
                     'Realizziamo servizi bar e cocktail experience per privati, aziende e professionisti del settore, dalla nostra sede di Montecatini Terme, in Toscana.'), cls='is-muted animate-fade-up'),
        ], second='details/mint-coupes.webp', second_alt=c.T('Coupes with mint and red berries', 'Coppe con menta e frutti rossi'))], pad_top=False, name='Our story'),
        section(c, [sh(c, c.T('How we work', 'Come lavoriamo'), c.H('Four words, <em>every time.</em>', 'Quattro parole, <em>ogni volta.</em>')),
                    numbered_grid(c, [(c.T(*t), c.T(*d)) for t, d in values], cols=4, cls='mt-values')], alt=True, name='How we work'),
        section(c, [sh(c, c.T('Why Meteora', 'Perché Meteora'), c.H('The details <em>that set us apart.</em>', 'I dettagli <em>che ci distinguono.</em>')),
                    why_grid(c, 4), buttons(c, [btn_link(c, c.T('All the reasons', 'Tutti i motivi'), c.L('why'))], cls='mt-section-cta')], name='Why Meteora'),
        cta_band(c, 'bars/golden-mirror-sunset.webp', c.T('Golden Mirror bar at sunset', 'Banco Golden Mirror al tramonto'), track='about_band'),
    ]
    meta = {'en': ('About Us: 14+ Years of Event Experience | Meteora Events', 'Meteora Events is the partner specialised in beverage service management for high-level events. 14+ years of operational experience, based in Montecatini Terme, Tuscany.'),
            'it': ('Chi Siamo: oltre 14 anni di eventi | Meteora Events', 'Meteora Events è il partner specializzato nella gestione del servizio beverage per eventi di alto livello. Oltre 14 anni di esperienza operativa, base a Montecatini Terme.')}
    return blocks, meta


# ===================================================================== WHY
def why(c: Ctx):
    blocks = [
        page_hero(c, c.T('Why Meteora', 'Perché Meteora'), c.H('You don’t hire us to serve drinks. <em>You hire us because the bar becomes part of the event.</em>',
                                                               'Non vi affidate a noi per servire drink. <em>Vi affidate a noi perché il bar diventi parte dell’evento.</em>'),
                  None, 'bars/golden-marble-night.webp', c.T('Golden bar on a chevron floor', 'Banco dorato su pavimento chevron')),
        section(c, [why_grid(c)], pad_top=False, name='The reasons'),
        section(c, [editorial(c, 'bars/pure-white-villa.webp', c.T('Pure White bar in a garden, nothing out of place', 'Banco Pure White in giardino, senza nulla a vista'), [
            eyebrow(c, c.T('A clean service', 'Pulizia di servizio')),
            h(c, 2, c.H('Hygienically impeccable. <em>Visually refined.</em>', 'Igienicamente impeccabile. <em>Visivamente raffinato.</em>'), cls='animate-fade-up'),
            p(c, c.T('Guests who approach the bar during service will never see cool boxes, storage crates or glass racks. Every restock of supplies, ice and glassware is carried discreetly by tray.',
                     'Chi si avvicina al banco durante il servizio non vedrà contenitori termici, casse o ceste di bicchieri. Ogni rifornimento di scorte, ghiaccio e bicchieri avviene a vassoio, con discrezione.'), cls='is-muted animate-fade-up'),
        ], second='team/bartender-strain.webp', second_alt=c.T('Bartender at work', 'Bartender al lavoro'))], alt=True, name='A clean service'),
        ice_section(c, show_types=False),
        partner_cta(c),
        cta_band(c, 'bars/silver-reflection.webp', c.T('Silver Reflection bar', 'Banco Silver Reflection'), track='why_band'),
    ]
    meta = {'en': ('Why Choose Meteora Events | High-End Bar Catering', 'Qualified bartenders, a visually clean service, respect for venues, independence, discretion and temperature control. Here is why clients choose Meteora Events.'),
            'it': ('Perché scegliere Meteora Events | Bar Catering di livello', 'Bartender qualificati, servizio visivamente pulito, rispetto delle location, autonomia, discrezione e controllo delle temperature. Ecco perché scegliere Meteora Events.')}
    return blocks, meta


# ===================================================================== CONTACT
def contact(c: Ctx):
    links = ul(c, [
        '<a href="mailto:info@meteoraevents.com">info@meteoraevents.com</a>',
        '<a href="https://wa.me/393280642479" target="_blank" rel="noreferrer noopener">WhatsApp</a>',
        '<a href="tel:+393280642479">+39 328 064 2479</a>',
        '<a href="https://www.instagram.com/meteoraevents/" target="_blank" rel="noreferrer noopener">@meteoraevents</a>',
        c.T('Montecatini Terme (PT), Tuscany — serving all of Italy', 'Montecatini Terme (PT), Toscana — operativi in tutta Italia'),
    ], cls='mt-ct__links')
    blocks = [
        section(c, [group(c, [
            group(c, [
                B('core/breadcrumbs', {'className': 'mt-crumbs'}),
                eyebrow(c, c.T('Contact', 'Contatti'), anim=False),
                h(c, 1, c.H('Request <em>your quote.</em>', 'Richiedete <em>il vostro preventivo.</em>'), cls='mt-ct__title'),
                p(c, c.T('Tell us about your event and we will reply with a proposal built around it. The more you share, the more precise it will be.',
                         'Raccontateci il vostro evento: vi risponderemo con una proposta costruita su misura. Più dettagli ci date, più precisa sarà.'), cls='is-style-lead is-muted'),
                links,
                img(c, 'bars/golden-mirror-sunset.webp', c.T('Golden Mirror bar at sunset', 'Banco Golden Mirror al tramonto'), cls='mt-ct__img'),
                p(c, c.T('Are you a wedding planner, venue or caterer?', 'Siete un wedding planner, una location o un catering?'), cls='is-muted mt-ct__partner'),
                buttons(c, [btn_link(c, c.T('Request partner pricing', 'Richiedi listino partner'), c.L('partners', 'partner-form'))]),
            ], cls='mt-ct__side'),
            group(c, [cf7(c, 'quote')], cls='mt-form-wrap mt-ct__form'),
        ], cls='mt-ct')], cls='mt-contact', pad_top='xl', name='Contact'),
        faq(c, 'general', limit=4, title=c.H('Before <em>you write.</em>', 'Prima di <em>scriverci.</em>'), alt=True),
    ]
    meta = {'en': ('Request a Quote | Meteora Events', 'Request a quote for bar catering at your wedding or event in Italy. We reply with a tailored proposal. Email info@meteoraevents.com, WhatsApp or phone.'),
            'it': ('Richiedi un Preventivo | Meteora Events', 'Richiedi un preventivo per il bar catering del tuo matrimonio o evento. Rispondiamo con una proposta su misura. Email info@meteoraevents.com, WhatsApp e telefono.')}
    return blocks, meta


# ===================================================================== THANKS
def thanks(c: Ctx):
    blocks = [section(c, [group(c, [
        eyebrow(c, c.T('Request received', 'Richiesta ricevuta'), anim=False),
        h(c, 1, c.H('Thank you. <em>Your event is in good hands.</em>', 'Grazie. <em>Il vostro evento è in buone mani.</em>')),
        p(c, c.T('We will reply as soon as possible with a tailored proposal.', 'Vi risponderemo al più presto con una proposta su misura.'), cls='is-style-lead is-muted'),
        cta_row(c, [btn_primary(c, c.T('Back to home', 'Torna alla home'), c.L('home')), btn_link(c, c.T('See our events', 'Guarda gli eventi'), c.L('events'))]),
    ], cls='mt-ty')], width='62rem', name='Thank you')]
    meta = {'en': ('Thank you | Meteora Events', 'Request received.'), 'it': ('Grazie | Meteora Events', 'Richiesta ricevuta.')}
    return blocks, meta


# ===================================================================== LEGAL
def legal(c: Ctx, kind):
    if kind == 'privacy':
        title = ('Privacy Policy', 'Privacy Policy')
        body = [
            (('Data controller', 'Titolare del trattamento'), ('[COMPANY NAME — to be supplied], Montecatini Terme (PT), Italy. Email: info@meteoraevents.com.', '[RAGIONE SOCIALE — da inserire], Montecatini Terme (PT). Email: info@meteoraevents.com.')),
            (('Data we process', 'Dati trattati'), ('Data you provide through our contact forms (name, surname, email, phone, event details, company details where relevant) and technical browsing data.', 'Dati forniti volontariamente tramite i moduli di contatto (nome, cognome, email, telefono, dettagli dell’evento, eventuali dati aziendali) e dati di navigazione tecnici.')),
            (('Purposes and legal basis', 'Finalità e base giuridica'), ('Replying to information and quote requests (pre-contractual measures, Art. 6.1.b GDPR). Website usage statistics only with your consent (Art. 6.1.a GDPR).', 'Rispondere alle richieste di informazioni e preventivo (misure precontrattuali, art. 6.1.b GDPR). Statistiche di utilizzo del sito solo previo consenso (art. 6.1.a GDPR).')),
            (('Retention', 'Conservazione'), ('[To be defined by the data controller.]', '[Da definire a cura del titolare.]')),
            (('Recipients', 'Destinatari'), ('Hosting and email provider and, only if enabled with consent, analytics providers. [To be completed.]', 'Fornitore di hosting ed email e, solo se attivati con consenso, fornitori di servizi di analisi. [Da completare.]')),
            (('Your rights', 'Diritti dell’interessato'), ('Access, rectification, erasure, restriction, objection, portability, and the right to lodge a complaint with the Italian Data Protection Authority (Garante), by writing to info@meteoraevents.com.', 'Accesso, rettifica, cancellazione, limitazione, opposizione, portabilità e reclamo al Garante per la protezione dei dati personali, scrivendo a info@meteoraevents.com.')),
        ]
    else:
        title = ('Cookie Policy', 'Cookie Policy')
        body = [
            (('What cookies are', 'Cosa sono i cookie'), ('Small text files the site stores on your device to work or to gather information about how it is used.', 'Piccoli file di testo che il sito salva sul dispositivo per funzionare o per raccogliere informazioni sull’utilizzo.')),
            (('Technical cookies (always active)', 'Cookie tecnici (sempre attivi)'), ('The site stores your cookie preferences in the browser (localStorage, key meteora_consent). No consent is required.', 'Il sito salva nel browser (localStorage, chiave meteora_consent) le preferenze sui cookie. Non richiede consenso.')),
            (('Analytics and marketing cookies (consent only)', 'Cookie di analisi e marketing (solo con consenso)'), ('If configured, Google Analytics 4 / Google Tag Manager and possibly Meta Pixel are loaded only after your explicit consent. [Detailed list to be completed.]', 'Se configurati dal titolare, Google Analytics 4 / Google Tag Manager ed eventualmente Meta Pixel vengono caricati solo dopo il consenso esplicito. [Elenco dettagliato da completare.]')),
            (('Managing your preferences', 'Gestire le preferenze'), ('You can change your choices at any time from the “Cookie preferences” link in the footer.', 'Puoi modificare le tue scelte in qualsiasi momento dal link “Preferenze cookie” nel footer.')),
        ]
    prose = [p(c, c.T('Draft — final legal text to be supplied by the client', 'Bozza — testo legale definitivo da inserire a cura del cliente'), cls='is-style-micro mt-legal__draft')]
    for (hen, hit), (ben, bit) in body:
        prose += [h(c, 2, c.T(hen, hit)), p(c, c.T(ben, bit))]
    blocks = [section(c, [B('core/breadcrumbs', {'className': 'mt-crumbs'}), h(c, 1, c.T(*title), cls='mt-legal__title'), group(c, prose, cls='mt-prose')], width='62rem', cls='mt-legal', pad_top='xl', name=title[0])]
    meta = {'en': (f'{title[0]} | Meteora Events', title[0]), 'it': (f'{title[1]} | Meteora Events', title[1])}
    return blocks, meta


# ===================================================================== EVENT POSTS (content of each story)
def event_post(c: Ctx, e):
    facts = [(('Event type', 'Tipologia'), LT(c, e['type']))]
    if e.get('location'):
        facts.append((('Location', 'Luogo'), LT(c, e['location'])))
    if e.get('bar'):
        facts.append((('Bar', 'Banco bar'), e['bar']))
    facts.append((('Experience', 'Esperienza'), LT(c, e['experience'])))
    story = [p(c, c.T(en, it), cls='is-style-lead' if i == 0 else None) for i, (en, it) in enumerate(zip(e['story']['en'], e['story']['it']))]
    gallery = [img(c, ip(g['src']), LT(c, g['alt']), cls='mt-ps__gimg animate-image-reveal') for g in e['gallery']]
    inner = [group(c, [
        group(c, [group(c, [p(c, c.T(*k), cls='is-style-micro'), p(c, v, cls='mt-ps__fact')]) for k, v in facts], cls='mt-ps__facts'),
        group(c, story, cls='mt-ps__story'),
    ], cls='mt-ps')]
    if gallery:
        inner.append(group(c, gallery, cls='mt-ps__gallery'))
    labels = {'weddings': ('Weddings', 'Matrimoni'), 'corporate': ('Corporate & private events', 'Eventi aziendali e privati'),
              'destination': ('Destination weddings', 'Destination weddings'), 'bars': ('The bars', 'I banchi'), 'cocktails': ('Cocktail Experience', 'Cocktail Experience')}
    rel = e['relatedService']
    inner.append(cta_row(c, [quote_btn(c, 'event_story_quote'), btn_link(c, c.T(*labels[rel]), c.L(rel)),
                             btn_link(c, c.T('Back to events', 'Torna agli eventi'), c.L('events'))], cls='mt-ps__links'))
    return inner
