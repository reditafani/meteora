"""
Section builders — one per component of the original Astro site.
Copy is taken verbatim from the original views (EN/IT pairs) and src/data (data.json).
"""
from __future__ import annotations

import json
import os

from blocks import (B, Ctx, _cls, btn_link, btn_primary, button, buttons, eyebrow, group, h,
                    html_block, img, p, section, ul)

DATA = json.load(open(os.path.join(os.path.dirname(__file__), 'data.json')))


def ip(src) -> str:
    """Original asset path -> theme WebP path (relative to assets/images/)."""
    s = src['src'] if isinstance(src, dict) else src
    s = s.split('assets/images/')[-1]
    return os.path.splitext(s)[0] + '.webp'


def LT(c: Ctx, loc: dict, html_ok=False) -> str:
    """Token from a localized {it, en} data value."""
    return c.T(loc['en'], loc['it'], html_ok)


def num(i: int) -> str:
    return f'{i + 1:02d}'


# ---------------------------------------------------------------- headings
def sh(c: Ctx, eye, title, lead=None, align='left', level=2, anchor=None, lead_cls='is-style-lead is-muted'):
    head = [eyebrow(c, eye)] if eye else []
    head.append(h(c, level, title, cls='mt-sh__title animate-fade-up animate-delay-1', anchor=anchor))
    inner = [group(c, head, cls='mt-sh__head')]
    if lead:
        inner.append(p(c, lead, cls=_cls(lead_cls, 'mt-sh__lead animate-fade-up animate-delay-2')))
    return group(c, inner, cls=f'mt-sh mt-sh--{align}')


def cta_row(c: Ctx, items, cls=None):
    return buttons(c, items, cls=_cls('mt-cta-row', cls))


# ---------------------------------------------------------------- heroes
def hero_home(c: Ctx):
    return B('core/cover', {
        'url': c.U('bars/golden-mirror-sunset.webp'),
        'id': c.media_ids.get('bars/golden-mirror-sunset.webp') if c.mode == 'wxr' else None,
        'alt': c.T('Golden Mirror bar at sunset on a terrace overlooking the hills', 'Banco bar Golden Mirror al tramonto su una terrazza affacciata sulle colline'),
        'dimRatio': 100, 'gradient': 'hero-shade', 'focalPoint': {'x': 0.5, 'y': 0.6},
        'minHeight': 100, 'minHeightUnit': 'svh', 'contentPosition': 'bottom left', 'isDark': True,
        'align': 'full', 'className': 'mt-hero animate-hero-settle', 'tagName': 'section',
        'layout': {'type': 'constrained', 'contentSize': '1440px'},
    }, [
        eyebrow(c, c.T('Weddings · Destination weddings · Corporate · Private', 'Matrimoni · Destination wedding · Aziende · Privati'), anim=False),
        h(c, 1, c.H('Luxury Open Bar Catering <em>&amp; Hospitality Services</em>'), cls='mt-hero__title'),
        p(c, c.T('Premium bar catering for weddings, destination weddings, corporate and private events. Based in Tuscany, throughout Italy.',
                 'Bar catering premium per matrimoni, destination wedding, eventi aziendali e privati. Base in Toscana, in tutta Italia.'), cls='is-style-lead mt-hero__lead'),
        cta_row(c, [
            button(c, c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact'), cls='is-style-button-light has-arrow meteora-track-hero_quote'),
            button(c, c.T('Explore the experience', "Scopri l'esperienza"), '#experience', cls='is-style-button-ghost-light meteora-track-hero_explore'),
        ]),
    ])


def hero_dark(c: Ctx, image, alt, eye, title, lead, cta_text, cta_url, track):
    return B('core/cover', {
        'url': c.U(image), 'id': c.media_ids.get(image) if c.mode == 'wxr' else None, 'alt': alt,
        'dimRatio': 100, 'gradient': 'hero-shade', 'minHeight': 88, 'minHeightUnit': 'svh',
        'contentPosition': 'bottom left', 'isDark': True, 'align': 'full', 'tagName': 'section',
        'className': 'mt-hero mt-hero--tall animate-hero-settle', 'layout': {'type': 'constrained', 'contentSize': '1440px'},
    }, [
        B('core/breadcrumbs', {'className': 'mt-crumbs'}),
        eyebrow(c, eye, anim=False),
        h(c, 1, title, cls='mt-hero__title mt-hero__title--page'),
        p(c, lead, cls='is-style-lead mt-hero__lead'),
        cta_row(c, [button(c, cta_text, cta_url, cls=f'is-style-button-light meteora-track-{track}')]),
    ])


def page_hero(c: Ctx, eye, title, lead=None, image=None, alt='', ctas=None, alt_bg=False, lead_extra=None):
    text = [B('core/breadcrumbs', {'className': 'mt-crumbs'})]
    if eye:
        text.append(eyebrow(c, eye))
    text.append(h(c, 1, title, cls='mt-phero__title animate-fade-up animate-delay-1'))
    if lead:
        text.append(p(c, lead, cls='is-style-lead is-muted mt-phero__lead animate-fade-up animate-delay-2'))
    for extra in (lead_extra or []):
        text.append(extra)
    if ctas:
        text.append(cta_row(c, ctas, cls='animate-fade-up animate-delay-3'))
    inner = [group(c, text, cls='mt-phero__text')]
    if image:
        inner.append(img(c, image, alt, cls='mt-phero__media animate-image-reveal', size='large'))
    return section(c, [group(c, inner, cls=_cls('mt-phero__grid', None if image else 'is-text-only'))],
                   cls='mt-phero', alt=alt_bg, pad_top='xl', name='Page hero')


# ---------------------------------------------------------------- trust
def trust_bar(c: Ctx):
    pts = DATA_TRUST
    return group(c, [
        group(c, [
            p(c, c.H('14<span>+</span>'), cls='mt-trust__num'),
            h(c, 2, c.T('14+ years of operational event experience', 'Oltre 14 anni di esperienza operativa negli eventi'), cls='is-style-micro mt-trust__label'),
        ], cls='mt-trust__figure animate-fade-up'),
        ul(c, [c.T(en, it) for en, it in pts], cls='mt-trust__list animate-fade-up animate-delay-2'),
    ], cls='mt-trust', tag='section', align='full', layout={'type': 'constrained', 'contentSize': '1440px'}, name='Trust bar')


DATA_TRUST = [
    ('Professional staff', 'Staff professionale'), ('Independent operation', 'Servizio indipendente'),
    ('Scenographic bars', 'Banchi scenografici'), ('Professional glassware', 'Bicchieri professionali'),
    ('Curated ice', 'Ghiaccio selezionato'), ('Cocktail experience', 'Cocktail experience'),
    ('Customisation', 'Personalizzazione'), ('Respect for venues', 'Rispetto delle location'),
    ('Discreet hospitality', 'Ospitalità discreta'), ('Italy-wide service', 'In tutta Italia'),
]


# ---------------------------------------------------------------- experience mosaic
def experience_mosaic(c: Ctx):
    items = [
        ('bars/golden-marble-night.webp', 'The bar', 'Il banco', 'Scenographic, modular, in three sizes.', 'Scenografico, modulare, in tre misure.', 'Golden bar on a chevron floor', 'Banco bar dorato su pavimento chevron'),
        ('cocktails/espresso-martini.webp', 'Cocktails', 'Cocktail', 'Classics made with method, bespoke signatures.', 'Classici eseguiti con metodo, signature su misura.', 'Espresso Martini', 'Espresso Martini'),
        ('team/bartender-strain.webp', 'Staff', 'Staff', 'Total black, discreet, professional.', 'Total black, discreto, professionale.', 'Bartender in black uniform straining a cocktail', 'Bartender in divisa nera che filtra un cocktail'),
        ('details/champagne-bowl.webp', 'Glassware', 'Bicchieri', 'The right glass for every drink.', 'Il vetro giusto per ogni drink.', 'Champagne bowl and back bar', 'Champagne bowl e bottigliera sul banco'),
        ('ice/cube-5cm.webp', 'Ice', 'Ghiaccio', 'An integral part of the cocktail.', 'Parte integrante del cocktail.', 'Clear 5×5 cm ice cube held in a hand', 'Cubo di ghiaccio trasparente 5×5 cm in mano'),
        ('details/mint-coupes.webp', 'Details', 'Dettagli', 'Fruit, botanicals, garnish.', 'Frutta, botaniche, garnish.', 'Coupes with fresh mint and red berries', 'Coppe con menta fresca e frutti rossi'),
        ('bars/terrace-panorama.webp', 'Logistics', 'Logistica', 'Independent from setup to load-out.', 'Autonomi dall’allestimento allo smontaggio.', 'Bar set up in front of a panoramic window', 'Banco allestito davanti a una vetrata panoramica'),
    ]
    tiles = []
    for i, (path, en, it, den, dit, aen, ait) in enumerate(items):
        tiles.append(group(c, [
            img(c, path, c.T(aen, ait), cls='mt-mosaic__media hover-zoom'),
            p(c, num(i), cls='is-style-micro mt-mosaic__n'),
            h(c, 3, c.T(en, it), cls='mt-mosaic__name'),
            p(c, c.T(den, dit), cls='mt-mosaic__d'),
        ], cls=f'mt-mosaic__item animate-fade-up animate-delay-{i % 3 + 1}'))
    return section(c, [
        sh(c, c.T('Meteora Experience'), c.H('Not just <em>an open bar.</em>', 'Non è solo <em>un open bar.</em>'),
           c.T('We design and run the entire beverage experience of your event: from the bar to the ice, from glassware to staff, from setup to the last drink. You think about your guests.',
               'Progettiamo e gestiamo l’intera esperienza beverage dell’evento: dal banco al ghiaccio, dai bicchieri allo staff, dall’allestimento all’ultimo drink. Voi pensate agli ospiti.'),
           align='split', anchor='experience-title'),
        group(c, tiles, cls='mt-mosaic'),
        cta_row(c, [
            button(c, c.T('Discover the cocktail experience', 'Scopri la cocktail experience'), c.L('cocktails'), cls='is-style-button-light'),
            btn_link(c, c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact'), 'experience_quote'),
        ], cls='mt-section-cta'),
    ], cls='mt-experience', dark=True, anchor='experience', name='Not just an open bar')


# ---------------------------------------------------------------- editorial
def editorial(c: Ctx, image, alt, content, second=None, second_alt='', reverse=False, ratio='landscape', caption=None):
    fig = [img(c, image, alt, cls='mt-ed__main animate-image-reveal animate-drift')]
    if second:
        fig.append(img(c, second, second_alt, cls='mt-ed__second animate-image-reveal animate-delay-2'))
    if caption:
        fig.append(p(c, caption, cls='mt-caption'))
    return group(c, [
        group(c, fig, cls='mt-ed__figure'),
        group(c, content, cls='mt-ed__text'),
    ], cls=_cls('mt-ed', f'mt-ed--{ratio}', 'mt-ed--reverse' if reverse else None, 'mt-ed--pair' if second else None))


# ---------------------------------------------------------------- destinations
def destinations(c: Ctx, compact=False):
    rows = []
    for i, d in enumerate(DATA['destinations']['destinations']):
        name = LT(c, d['name'])
        if d.get('landing'):
            name_p = p(c, f'<a href="{c.L("tuscany")}">' + name + '</a>', cls='mt-dest__name')
        else:
            name_p = p(c, name, cls='mt-dest__name')
        rows.append(group(c, [name_p, p(c, LT(c, d['line']), cls='mt-dest__line')],
                          cls=_cls('mt-dest__row animate-fade-up', 'has-link' if d.get('landing') else None), anchor=f'dest-{d["id"]}'))
    return group(c, rows, cls=_cls('mt-dest', 'mt-dest--compact' if compact else None))


# ---------------------------------------------------------------- bars
def bar_card_body(c: Ctx, bar, i, link=True):
    soon = bar['status'] == 'coming-soon'
    body = [p(c, f'<span class="mt-bar__num">{num(i)}</span>' + (('<span class="mt-bar__soon">' + c.T('Coming soon', 'In arrivo') + '</span>') if soon else ''), cls='is-style-micro mt-bar__n')]
    if not soon and link:
        body.append(h(c, 3, f'<a href="{c.L("bar-" + bar["slug"])}">{bar["name"]}</a>', cls='mt-bar__name'))
    else:
        body.append(h(c, 3, bar['name'], cls='mt-bar__name'))
    body += [
        p(c, LT(c, bar['mood']), cls='mt-bar__mood'),
        p(c, LT(c, bar['description']), cls='mt-bar__desc is-muted'),
        p(c, c.H('<span class="mt-bar__ideal-label">Ideal for</span> ' + ' · '.join(bar['idealFor']['en']),
                 '<span class="mt-bar__ideal-label">Ideale per</span> ' + ' · '.join(bar['idealFor']['it'])), cls='mt-bar__ideal'),
    ]
    return body


def bar_media(c: Ctx, bar):
    if bar['images']:
        im = bar['images'][0]
        return img(c, ip(im['src']), LT(c, im['alt']), cls='mt-bar__media hover-zoom')
    return group(c, [p(c, c.T('Coming soon', 'In arrivo'), cls='mt-swatch__label')],
                 cls='mt-bar__media mt-swatch', style={'color': {'background': bar['swatch']}})


def bar_collection(c: Ctx, cards_grid=False):
    rows = []
    for i, bar in enumerate(DATA['bars']['bars']):
        rows.append(group(c, [bar_media(c, bar), group(c, bar_card_body(c, bar, i), cls='mt-bar__body')],
                          cls=_cls('mt-bar', 'is-soon' if bar['status'] == 'coming-soon' else None, 'animate-fade-up' if cards_grid else None)))
    return group(c, rows, cls='mt-bars-grid' if cards_grid else 'mt-bc', name='Bar collection')


def bar_section(c: Ctx, eye=None, title=None, lead=None, ctas=True, pad_top=True):
    inner = [
        sh(c, eye or c.T('The Bar Collection', 'I nostri banchi'), title or c.H('The bar <em>collection.</em>', 'La collezione <em>dei banchi.</em>'),
           lead or c.T('Modular, scenographic bars, each in three sizes — Slim 1.5 m, Medium 3.5 m, Large 5.5 m. A collection that keeps growing.',
                       'Banchi modulari e scenografici, ciascuno in tre misure — Slim 1,5 m, Medium 3,5 m, Large 5,5 m. Una collezione in continuo ampliamento.'),
           align='split'),
        bar_collection(c),
    ]
    if ctas:
        inner.append(cta_row(c, [
            btn_primary(c, c.T('Explore the collection', 'Esplora la collezione'), c.L('bars')),
            btn_link(c, c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact'), 'bars_quote'),
        ], cls='mt-section-cta'))
    return section(c, inner, cls='mt-bars', pad_top=pad_top, name='The Bar Collection')


# ---------------------------------------------------------------- cocktails
FAMILY_LEAD = {'classics': 'old-fashioned', 'spritz': 'spritz', 'martini': 'espresso-martini', 'sour': 'sour', 'tropical': 'mojito', 'aperitivo': 'negroni'}


def cocktail_families(c: Ctx):
    rows = []
    cocktails = {k['slug']: k for k in DATA['cocktails']['cocktails']}
    for cat in DATA['cocktails']['cocktailCategories']:
        if cat['id'] == 'signature':
            image, alt = 'details/ice-stamp.webp', c.T('Ice cube pressed with initials', 'Cubo di ghiaccio con iniziali impresse')
            drink = ''
        else:
            k = cocktails[FAMILY_LEAD[cat['id']]]
            image, alt, drink = f'cocktails/{k["slug"]}.webp', c.T(k['name']), k['name']
        rows.append(group(c, [
            img(c, image, alt, cls='mt-cf__img'),
            p(c, f'<a href="{c.L("cocktails", cat["id"])}">' + c.T(cat['label']['en'], cat['label']['it']) + '</a>', cls='mt-cf__name'),
            p(c, LT(c, cat['blurb']), cls='mt-cf__blurb'),
        ] + ([p(c, drink, cls='is-style-micro mt-cf__drink')] if drink else []), cls='mt-cf__row'))
    return group(c, [group(c, [], cls='mt-cf__frame'), group(c, rows, cls='mt-cf__list')], cls='mt-cf', name='Cocktail families')


def cocktail_card(c: Ctx, k):
    cats = ' '.join('cat-' + x for x in k['categories'])
    inner = [img(c, f'cocktails/{k["slug"]}.webp', c.T(k['name']), cls='mt-cc__media hover-zoom'), h(c, 3, k['name'], cls='mt-cc__name')]
    if k.get('variants'):
        inner.append(p(c, k['variants'], cls='mt-cc__variants'))
    inner.append(group(c, [
        p(c, LT(c, k['profile']), cls='mt-cc__profile'),
        p(c, c.T(f'Alcohol level: {k["alcohol"]}/5', f'Grado alcolico: {k["alcohol"]}/5'), cls=f'mt-abv mt-abv--{k["alcohol"]}'),
    ], cls='mt-cc__meta'))
    return group(c, inner, cls=f'mt-cc {cats}')


def cocktail_gallery(c: Ctx):
    cats = DATA['cocktails']['cocktailCategories']
    items = [f'<a href="#all">' + c.T('All', 'Tutti') + '</a>']
    for cat in cats:
        if any(cat['id'] in k['categories'] for k in DATA['cocktails']['cocktails']):
            items.append(f'<a href="#{cat["id"]}">' + LT(c, cat['label']) + '</a>')
    return group(c, [
        ul(c, items, cls='mt-cg__filters'),
        group(c, [cocktail_card(c, k) for k in DATA['cocktails']['cocktails']], cls='mt-cg__grid'),
    ], cls='mt-cg', name='Cocktail list')


# ---------------------------------------------------------------- ice
ICE_PRINCIPLES = [
    ('Temperature', 'Temperatura', 'Ice does not only chill: it brings the drink to the right temperature and holds it there.', 'Il ghiaccio non serve solo a raffreddare: porta il drink alla temperatura giusta e ce lo tiene.'),
    ('Dilution', 'Diluizione', 'Too much ice flattens a cocktail; too little makes it aggressive.', 'Troppo ghiaccio appiattisce un cocktail, troppo poco lo rende aggressivo.'),
    ('Texture', 'Texture', 'The smaller the ice, the faster it chills. The larger and denser, the more dilution is controlled over time.', 'Più è piccolo, più raffredda in fretta. Più è grande e compatto, più la diluizione è controllata nel tempo.'),
    ('Presentation', 'Presentazione', 'A clear cube, a sphere, a tall long-drink spear: ice is seen, and it speaks.', 'Un cubo trasparente, una sfera, un long drink verticale: il ghiaccio si vede, e racconta.'),
    ('Precision', 'Precisione', 'Every cocktail has its own rules. Every cocktail begins with a precise choice.', 'Ogni cocktail ha le sue regole. Ogni cocktail nasce da una scelta precisa.'),
]


def ice_section(c: Ctx, show_types=True):
    principles = [group(c, [p(c, num(i), cls='is-style-micro'), h(c, 3, c.T(en, it)), p(c, c.T(den, dit), cls='is-muted')],
                        cls='mt-ice__principle animate-fade-up') for i, (en, it, den, dit) in enumerate(ICE_PRINCIPLES)]
    inner = [group(c, [
        img(c, 'ice/pour-coupe.webp', c.T('Crushed ice falling into a cocktail coupe', 'Ghiaccio tritato che cade in una coppa da cocktail'), cls='mt-ice__media animate-image-reveal animate-drift'),
        group(c, [
            eyebrow(c, c.T('The ice we use', 'Il nostro ghiaccio')),
            h(c, 2, c.H('Ice is <em>part of the cocktail.</em>', 'Il ghiaccio è <em>parte del cocktail.</em>'), cls='is-style-display mt-ice__title animate-fade-up animate-delay-1', anchor='ice-title'),
            group(c, principles, cls='mt-ice__principles'),
        ], cls='mt-ice__text'),
    ], cls='mt-ice__grid')]
    if show_types:
        types = [group(c, [img(c, ip(t['image']), LT(c, t['name']), cls='mt-ice__thumb'), h(c, 3, LT(c, t['name']), cls='mt-ice__name'), p(c, LT(c, t['note']), cls='is-muted')],
                       cls='mt-ice__type animate-fade-up') for t in DATA['craft']['iceTypes']]
        inner += [group(c, types, cls='mt-ice__rail'),
                  p(c, c.T('Availability of premium formats is confirmed during the event definition phase.', 'La disponibilità delle tipologie premium viene confermata in fase di definizione dell’evento.'), cls='is-style-micro is-muted mt-ice__note')]
    return section(c, inner, cls='mt-ice', dark=True, anchor='ice', name='Ice')


# ---------------------------------------------------------------- glassware
def glassware(c: Ctx):
    items = [group(c, [img(c, ip(g['image']), LT(c, g['name']), cls='mt-gl__tile'), h(c, 3, LT(c, g['name'])), p(c, LT(c, g['use']), cls='is-muted')],
                   cls='mt-gl__item animate-fade-up') for g in DATA['craft']['glassware']]
    return section(c, [
        group(c, [
            sh(c, c.T('Our glassware', 'I nostri bicchieri'), c.H('The right glass <em>for the right cocktail.</em>', 'Il bicchiere giusto <em>per il cocktail giusto.</em>'),
               c.T('Shape, thickness, opening and capacity are chosen for each cocktail: to manage temperature and dilution and to showcase its aromas. Professional HoReCa-grade glass, with lines that match the style of the setup.',
                   'Forma, spessore, apertura e capacità si scelgono in base al cocktail: per gestire la temperatura, la diluizione e valorizzare la componente aromatica. Vetro professionale, di livello HoReCa, con linee coerenti con lo stile dell’allestimento.'), anchor='glass-title'),
            img(c, 'glassware/crystal.webp', c.T('Cut-crystal tumblers lined up on the bar', 'Bicchieri in cristallo lavorato allineati sul banco'), cls='mt-gl__hero animate-image-reveal'),
        ], cls='mt-gl__top'),
        group(c, items, cls='mt-gl__grid'),
        p(c, c.T('On request, specific glassware of any line or brand can be rented, subject to availability and supply times.',
                 'Su richiesta è possibile noleggiare bicchieri specifici di qualsiasi linea o marca, compatibilmente con disponibilità e tempi di fornitura.'), cls='is-muted mt-gl__note'),
    ], cls='mt-gl', anchor='glassware', name='Glassware')


# ---------------------------------------------------------------- personalisation
def personalisation(c: Ctx):
    rows = []
    for cz in DATA['craft']['customizations']:
        inner = [h(c, 3, LT(c, cz['title'])), p(c, LT(c, cz['text']), cls='is-muted')]
        if cz.get('notice'):
            inner.append(p(c, LT(c, cz['notice']), cls='is-style-micro mt-pz__notice'))
        rows.append(group(c, inner, cls='mt-pz__row animate-fade-up'))
    return section(c, [group(c, [
        group(c, [
            img(c, 'details/ice-stamp.webp', c.T('Ice cube pressed with initials beside a brass stamp', 'Cubo di ghiaccio con iniziali impresse e stampo in ottone'), cls='mt-pz__img animate-image-reveal animate-drift'),
            p(c, c.T('Initials pressed into ice. The stamp is yours to keep.', 'Iniziali impresse sul ghiaccio. Lo stampo resta a voi, come ricordo.'), cls='mt-caption'),
        ], cls='mt-pz__media'),
        group(c, [
            eyebrow(c, c.T('Customisation', 'Personalizzazioni')),
            h(c, 2, c.H('Make it <em>yours.</em>', 'Rendetelo <em>vostro.</em>'), cls='animate-fade-up animate-delay-1', anchor='personalisation-title'),
            p(c, c.T('Bespoke details turn the bar service into an experience that reflects the couple, or the brand.',
                     'Dettagli studiati su misura trasformano il servizio bar in un’esperienza coerente con l’identità degli sposi o del brand.'), cls='is-style-lead is-muted mt-pz__lead animate-fade-up animate-delay-2'),
            group(c, rows, cls='mt-pz__list'),
            p(c, c.T('Customisations are agreed during the event-planning phase.', 'Le personalizzazioni vanno concordate in fase di ideazione dell’evento.'), cls='is-style-micro mt-pz__foot'),
            buttons(c, [btn_link(c, c.T('Let’s talk details', 'Parliamo dei dettagli'), c.L('contact'), 'personalisation')]),
        ], cls='mt-pz__text'),
    ], cls='mt-pz__grid')], cls='mt-pz', alt=True, anchor='personalisation', name='Make it yours')


# ---------------------------------------------------------------- tower
def tower(c: Ctx, cta=True, anchor='tower'):
    groups = []
    for g in DATA['services']['towers']:
        groups.append(group(c, [p(c, LT(c, g['group']), cls='is-style-micro mt-tw__group')] + [p(c, item, cls='mt-tw__item') for item in g['items']], cls='mt-tw__set animate-fade-up'))
    text = [
        p(c, c.T('Coupes or glasses arranged in a cascade and filled live by our staff or by the couple. For the toast, the cake cutting or opening the party: an elegant, captivating and highly photogenic moment.',
                 'Coppe o calici disposti a cascata, riempiti dal vivo dal nostro staff o dagli sposi. Per il brindisi, il taglio della torta o l’apertura della festa: un effetto elegante, coinvolgente e altamente fotografico.'), cls='is-style-lead animate-fade-up'),
        group(c, groups, cls='mt-tw__list'),
        p(c, c.T('Would you like a different tower? Just ask. Available alongside the bar service, or on its own on request.',
                 'Desiderate un altro tipo di tower? Chiedetecelo. Disponibile in abbinamento al servizio bar, o come servizio a sé su richiesta.'), cls='is-muted mt-tw__small'),
    ]
    if cta:
        text.append(cta_row(c, [
            button(c, c.T('Discover the Tower Experience', 'Scopri la Tower Experience'), c.L('services', 'tower'), cls='is-style-button-light'),
            btn_link(c, c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact'), 'tower_quote'),
        ]))
    return section(c, [
        eyebrow(c, 'Signature Tower Experience'),
        h(c, 2, c.H('A moment designed <em>to be remembered.</em>', 'Un momento pensato <em>per essere ricordato.</em>'), cls='is-style-display mt-tw__title animate-fade-up animate-delay-1'),
        group(c, [
            img(c, 'towers/couple-pour.webp', c.T('The couple pour sparkling wine over a coupe tower', 'Gli sposi versano bollicine su una tower di coppe'), cls='mt-tw__a animate-image-reveal'),
            img(c, 'towers/coupe-tower-sunset.webp', c.T('Coupe tower at sunset beneath blossoming trees', 'Tower di coppe al tramonto tra gli alberi in fiore'), cls='mt-tw__b animate-image-reveal animate-delay-2'),
            img(c, 'towers/espresso-martini-tower.webp', c.T('Espresso Martini Tower on a black table', 'Espresso Martini Tower su tavolo nero'), cls='mt-tw__c animate-image-reveal animate-delay-3'),
            group(c, text, cls='mt-tw__text'),
        ], cls='mt-tw__stage'),
    ], cls='mt-tw', dark=True, anchor=anchor, name='Signature Tower Experience')


# ---------------------------------------------------------------- comparison
def comparison(c: Ctx):
    cmp = DATA['services']['comparison']
    head = [{'content': ''}, {'content': c.H('<span>Open Bar</span> Essential <em>Experience</em>')}, {'content': c.H('<span>Open Bar</span> Premium <em>Experience</em>')}]
    body = [{'cells': [{'content': LT(c, r['label']), 'tag': 'td'}, {'content': LT(c, r['essential']), 'tag': 'td'}, {'content': LT(c, r['premium']), 'tag': 'td'}]} for r in cmp['rows']]
    for cell in head:
        cell['tag'] = 'th'
    return group(c, [
        B('core/table', {'head': [{'cells': head}], 'body': body, 'hasFixedLayout': False, 'className': 'mt-cmp__table',
                         'caption': c.T('Essential and Premium Experience compared', 'Confronto Essential e Premium Experience')}),
        p(c, LT(c, cmp['note']), cls='is-muted mt-cmp__note'),
        p(c, c.T('Both formulas include three hours of open bar, a bar of your choice, our signature drink list, professional staff and our own glassware. Extra time, additional staff and extra bar modules on request.',
                 'Entrambe le formule includono tre ore di open bar, banco a scelta, drink list signature, staff professionale e bicchieri di nostra proprietà. Tempo extra, staff e moduli bar aggiuntivi su richiesta.'), cls='is-muted mt-cmp__note'),
        buttons(c, [btn_primary(c, c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact'), 'comparison_quote', arrow=True)]),
    ], cls='mt-cmp', name='Essential vs Premium')


def comparison_section(c: Ctx, eye, title, lead=None, alt=False, pad_top=True):
    return section(c, [sh(c, eye, title, lead, align='split'), comparison(c)], cls='mt-compare', alt=alt, pad_top=pad_top, name='Essential vs Premium')


# ---------------------------------------------------------------- services
def services_list(c: Ctx):
    items = []
    for i, sv in enumerate(DATA['services']['services']):
        items.append(group(c, [
            img(c, ip(sv['image']), LT(c, sv['imageAlt']), cls='mt-svc__media animate-image-reveal'),
            group(c, [
                p(c, num(i) + ' · ' + LT(c, sv['kicker']), cls='is-style-micro mt-svc__kicker'),
                h(c, 2, LT(c, sv['name']), cls='mt-svc__title'),
                p(c, LT(c, sv['summary']), cls='is-style-lead is-muted'),
                ul(c, [c.T(en, it) for en, it in zip(sv['includes']['en'], sv['includes']['it'])], cls='is-style-list-ruled'),
                buttons(c, [button(c, c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact') + '?service=' + sv['formValue'], cls=f'is-style-button-outline-ink meteora-track-service_{sv["id"]}')]),
            ], cls='mt-svc__text'),
        ], cls=_cls('mt-svc__item', 'mt-svc__item--rev' if i % 2 else None), anchor=sv['id']))
    items.append(p(c, c.T('On request: extra time, additional bartenders and waiters, extra bar modules. At peak moments, support staff keep service fast and fluid. Services can also be delivered outside the region and abroad; any logistics costs are defined in the quote.',
                          'Su richiesta: tempo extra, bartender e camerieri aggiuntivi, moduli bar extra. Nei momenti di maggiore affluenza il personale di supporto rende il servizio più rapido e fluido. Servizi realizzabili anche fuori regione e all’estero; eventuali costi di logistica si definiscono nel preventivo.'), cls='is-muted mt-svc__note'))
    return section(c, [group(c, items, cls='mt-svc')], cls='mt-services', name='Service formulas')


# ---------------------------------------------------------------- portfolio
def portfolio_query(c: Ctx, per_page=3, cls='mt-pg'):
    return B('core/query', {'queryId': 7, 'query': {'perPage': per_page, 'pages': 0, 'offset': 0, 'postType': 'post', 'order': 'asc', 'orderBy': 'date', 'author': '', 'search': '', 'exclude': [], 'sticky': '', 'inherit': False},
                            'className': cls, 'layout': {'type': 'default'}}, [
        B('core/post-template', {'className': 'mt-pg__list', 'layout': {'type': 'default'}}, [
            B('core/post-featured-image', {'isLink': True, 'aspectRatio': '3/2', 'className': 'mt-pg__media hover-zoom'}),
            B('core/post-terms', {'term': 'post_tag', 'separator': ' — ', 'className': 'is-style-micro mt-pg__type'}),
            B('core/post-title', {'isLink': True, 'level': 3, 'className': 'mt-pg__title'}),
            B('core/post-excerpt', {'showMoreOnNewLine': False, 'excerptLength': 30, 'className': 'mt-pg__excerpt'}),
            B('core/read-more', {'content': c.T('Read the story', 'Leggi la storia'), 'className': 'mt-pg__cta'}),
        ]),
    ])


# ---------------------------------------------------------------- partner CTA
def partner_cta(c: Ctx):
    return section(c, [group(c, [
        img(c, 'venues/fresco-hall.webp', c.T('Long banquet table set in a frescoed hall', 'Tavolo imperiale apparecchiato in un salone affrescato'), cls='mt-pc__media animate-image-reveal'),
        group(c, [
            eyebrow(c, c.T('Wedding planners · Venues · Caterers', 'Wedding planner · Location · Catering')),
            h(c, 2, c.H('Your trusted <em>bar catering</em> partner.', 'Il vostro partner <em>di fiducia</em> per il bar.'), cls='animate-fade-up animate-delay-1'),
            p(c, c.T('We work alongside planners, venues and caterers with our own equipment, glassware and staff. Independent, clean, discreet — anywhere in Italy.',
                     'Lavoriamo al fianco di planner, location e catering con attrezzatura, bicchieri e staff propri. Autonomi, puliti, discreti — ovunque in Italia.'), cls='is-style-lead is-muted animate-fade-up animate-delay-2'),
            cta_row(c, [
                btn_primary(c, c.T('Request partner pricing', 'Richiedi listino partner'), c.L('partners', 'partner-form'), 'partner_band'),
                btn_link(c, c.T('How we work with partners', 'Come lavoriamo con i partner'), c.L('partners')),
            ], cls='animate-fade-up animate-delay-3'),
        ], cls='mt-pc__text'),
    ], cls='mt-pc__grid')], cls='mt-pc', name='Partner CTA')


# ---------------------------------------------------------------- numbered grid / why
def numbered_grid(c: Ctx, items, cols=4, cls=None, small=False, numbered=True):
    cells = [group(c, ([p(c, num(i), cls='is-style-micro mt-num__n')] if numbered else []) + [h(c, 3, t), p(c, d, cls='is-muted')], cls=f'mt-num__item animate-fade-up animate-delay-{i % 4 + 1}')
             for i, (t, d) in enumerate(items)]
    return group(c, cells, cls=_cls('mt-num', f'mt-num--{cols}', cls))


def why_grid(c: Ctx, limit=None):
    items = DATA['craft']['differentiators'][:limit] if limit else DATA['craft']['differentiators']
    return numbered_grid(c, [(LT(c, d['title']), LT(c, d['text'])) for d in items], cols=4, cls='mt-why')


# ---------------------------------------------------------------- FAQ
def faq(c: Ctx, topic='general', limit=None, eye='FAQ', title=None, alt=False, pad_top=True):
    items = [f for f in DATA['faq']['faq'] if topic in f['topics']]
    if limit:
        items = items[:limit]
    acc = B('core/accordion', {'className': 'mt-faq'}, [
        B('core/accordion-item', {}, [
            B('core/accordion-heading', {'title': LT(c, f['q'])}),
            B('core/accordion-panel', {}, [p(c, LT(c, f['a']))]),
        ]) for f in items])
    return section(c, [sh(c, eye, title or c.H('Frequently <em>asked.</em>', 'Domande <em>frequenti.</em>')), acc],
                   cls='mt-faq-section', alt=alt, pad_top=pad_top, width='62rem', name='FAQ')


# ---------------------------------------------------------------- instagram
def instagram_strip(c: Ctx, pad_top=True):
    imgs = [('towers/espresso-martini-tower.webp', 'Espresso Martini Tower'), ('bars/golden-mirror.webp', 'Golden Mirror'),
            ('details/mint-coupes.webp', 'Mint & berries'), ('bars/night-lounge.webp', 'Night bar'),
            ('towers/coupe-tower-sunset.webp', 'Coupe tower'), ('details/champagne-bowl.webp', 'Champagne bowl')]
    tiles = []
    for path, label in imgs:
        b = img(c, path, c.T(f'Meteora Events on Instagram — {label}', f'Meteora Events su Instagram — {label}'), cls='mt-ig__tile hover-zoom')
        b[1].update({'href': 'https://www.instagram.com/meteoraevents/', 'linkDestination': 'custom', 'linkTarget': '_blank', 'rel': 'noreferrer noopener'})
        tiles.append(b)
    return section(c, [
        group(c, [
            group(c, [eyebrow(c, 'Instagram'), h(c, 2, c.H('Behind the bar, <em>event after event.</em>', 'Dietro al banco, <em>evento dopo evento.</em>'), cls='mt-ig__title animate-fade-up')]),
            buttons(c, [btn_link(c, '@meteoraevents', 'https://www.instagram.com/meteoraevents/', 'instagram_strip')]),
        ], cls='mt-ig__head'),
        group(c, tiles, cls='mt-ig__grid'),
    ], cls='mt-ig', pad_top=pad_top, name='Instagram')


# ---------------------------------------------------------------- CTA band
def cta_band(c: Ctx, image, alt, title=None, lead=None, label=None, url=None, track='cta_band', secondary=None):
    items = [button(c, label or c.T('Request a quote', 'Richiedi un preventivo'), url or c.L('contact'), cls=f'is-style-button-light has-arrow meteora-track-{track}')]
    if secondary:
        items.append(secondary)
    return B('core/cover', {
        'url': c.U(image), 'id': c.media_ids.get(image) if c.mode == 'wxr' else None, 'alt': alt,
        'dimRatio': 100, 'gradient': 'band-shade', 'minHeight': 52, 'minHeightUnit': 'rem', 'isDark': True,
        'align': 'full', 'tagName': 'section', 'className': 'mt-band animate-drift', 'layout': {'type': 'constrained', 'contentSize': '1440px'},
    }, [
        h(c, 2, title or c.H('Picture the bar <em>at your event.</em>', 'Immaginate il bar <em>al vostro evento.</em>'), cls='mt-band__title animate-fade-up'),
        p(c, lead or c.T('Tell us the date, the place and the guests. We will reply with a tailored proposal.', 'Raccontateci data, luogo e ospiti. Vi risponderemo con una proposta su misura.'), cls='is-style-lead mt-band__lead animate-fade-up animate-delay-1'),
        cta_row(c, items, cls='animate-fade-up animate-delay-2'),
    ])


# ---------------------------------------------------------------- forms (Contact Form 7)
def cf7(c: Ctx, kind):
    titles = {'quote': ('Meteora — Request a quote', 'Meteora — Richiesta preventivo'), 'partner': ('Meteora — Partner pricing', 'Meteora — Listino partner')}[kind]
    return B('core/shortcode', {'text': '[contact-form-7 title="' + c.T(*titles) + f'" html_class="mt-form mt-form--{kind}"]'})
