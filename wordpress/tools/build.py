"""
Theme generator: writes /patterns/*.php (translatable) and languages/it_IT.po
from the section and page builders. Requires a running WordPress with the
theme active (for canon.mjs). Usage:

    python3 build.py patterns http://localhost:8890
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import pages as PG
import sections as S
from blocks import Ctx, finalize_pattern, group, section

ROOT = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(ROOT, '..', 'meteora')
SCRATCH = tempfile.gettempdir()


def tpl(fn):
    """Wrap a page function so it only returns blocks."""
    return lambda c: fn(c)[0]


# key: (title, description, categories, builder, extra header fields)
SECTION_PATTERNS = {
    'hero-home': ('Hero — cinematic home', 'Full-screen photo hero with headline, lead and two CTAs.', 'meteora-sections, banner', lambda c: [S.hero_home(c)]),
    'hero-page-dark': ('Hero — dark landing', 'Tall dark photo hero with breadcrumbs (Destination, Corporate).', 'meteora-sections, banner',
                       lambda c: [S.hero_dark(c, 'bars/silver-reflection.webp', c.T('Silver Reflection bar in a large hall', 'Banco Silver Reflection in una grande sala'), c.T('Corporate & private events', 'Eventi aziendali e privati'),
                                              c.H('Your brand, <em>served with style.</em>', 'Il vostro brand, <em>servito con stile.</em>'),
                                              c.T('Professionalism, customisation and discretion for corporate events, launches, activations and private parties.', 'Professionalità, personalizzazione e discrezione per eventi aziendali, lanci, activation e feste private.'),
                                              c.T('Request a quote', 'Richiedi un preventivo'), c.L('contact'), 'hero_quote')]),
    'page-hero': ('Page hero — editorial', 'Breadcrumbs, eyebrow, H1, lead, CTA and a tall photo.', 'meteora-sections, banner',
                  lambda c: [S.page_hero(c, c.T('Weddings', 'Matrimoni'), c.H('Your wedding. <em>Your bar experience.</em>', 'Il vostro matrimonio. <em>La vostra bar experience.</em>'),
                                         c.T('A bar that belongs to the most important day: designed around your style, run independently, made for your guests — and for the photographs.', 'Un bar che fa parte del giorno più importante: progettato sul vostro stile, gestito in autonomia, pensato per gli ospiti e per le fotografie.'),
                                         'towers/couple-pour.webp', c.T('A couple pouring sparkling wine over a coupe tower', 'Sposi che versano le bollicine sulla tower di coppe'),
                                         ctas=[PG.quote_btn(c, 'page_hero_quote')])]),
    'trust-bar': ('Trust — 14+ years', '14+ years of experience and key differentiators.', 'meteora-sections', lambda c: [S.trust_bar(c)]),
    'experience-mosaic': ('Not just an open bar', 'Dark editorial mosaic: bar, cocktails, staff, glassware, ice, details, logistics.', 'meteora-sections', lambda c: [S.experience_mosaic(c)]),
    'editorial-weddings': ('Editorial — image + text (weddings)', 'Asymmetric image pair with text and CTAs.', 'meteora-sections', lambda c: [PG.home(c)[0][3]]),
    'destinations': ('Destination weddings in Italy', 'Sticky intro with the list of destinations.', 'meteora-sections', lambda c: [PG.home(c)[0][4]]),
    'bar-collection': ('The Bar Collection', 'Interactive bar index with crossfading images (rail on mobile).', 'meteora-sections', lambda c: [S.bar_section(c)]),
    'bar-grid': ('Bar collection — cards', 'All bars as editorial cards.', 'meteora-sections', lambda c: [section(c, [S.bar_collection(c, cards_grid=True)])]),
    'cocktail-families': ('Cocktail families', 'Seven cocktail families with an arched crossfading frame.', 'meteora-sections', lambda c: [PG.home(c)[0][6]]),
    'cocktail-gallery': ('Cocktail list (filterable)', 'All cocktails with family filters. Duplicate a card to add a cocktail; add cat-<family> classes.', 'meteora-sections',
                         lambda c: [section(c, [S.cocktail_gallery(c)], anchor='list')]),
    'ice': ('Ice is part of the cocktail', 'Dark section: five principles and the ice formats.', 'meteora-sections', lambda c: [S.ice_section(c)]),
    'glassware': ('The right glass', 'Glassware grid.', 'meteora-sections', lambda c: [S.glassware(c)]),
    'personalisation': ('Make it yours', 'Personalisation options with the ice stamp image.', 'meteora-sections', lambda c: [S.personalisation(c)]),
    'tower': ('Signature Tower Experience', 'Cinematic tower section.', 'meteora-sections', lambda c: [S.tower(c)]),
    'comparison': ('Essential vs Premium', 'Refined comparison, no prices.', 'meteora-sections',
                   lambda c: [S.comparison_section(c, 'Open Bar', c.H('Two experiences, <em>one standard.</em>', 'Due esperienze, <em>uno stesso standard.</em>'))]),
    'services-list': ('Service formulas', 'All service formulas with includes and quote buttons.', 'meteora-sections', lambda c: [S.services_list(c)]),
    'portfolio': ('Portfolio — latest events', 'Asymmetric editorial grid of event stories (posts).', 'meteora-sections, query',
                  lambda c: [section(c, [S.portfolio_query(c, 3)], cls='mt-portfolio')]),
    'partner-cta': ('Partner CTA', 'B2B band for planners, venues and caterers.', 'meteora-sections, call-to-action', lambda c: [S.partner_cta(c)]),
    'why-grid': ('Why Meteora', 'The eight differentiators.', 'meteora-sections', lambda c: [section(c, [S.why_grid(c)])]),
    'faq': ('FAQ', 'Accordion with the genuine FAQs.', 'meteora-sections', lambda c: [S.faq(c, 'wedding')]),
    'instagram': ('Instagram strip', 'Six selected images linking to Instagram (no embed).', 'meteora-sections', lambda c: [S.instagram_strip(c)]),
    'cta-band': ('CTA band', 'Closing photo band with quote CTA.', 'meteora-sections, call-to-action',
                 lambda c: [S.cta_band(c, 'bars/golden-marble-night.webp', c.T('Golden bar lit up at night', 'Banco dorato illuminato di sera'))]),
    'cta-band-featured': ('CTA band — featured image', 'Closing band that uses the post’s featured image (event stories).', 'meteora-sections, call-to-action', lambda c: [_featured_band(c)]),
    'quote-form': ('Request a quote — form', 'Contact Form 7 quote form (falls back to email/WhatsApp if CF7 is inactive).', 'meteora-forms',
                   lambda c: [section(c, [S.cf7(c, 'quote')], width='62rem')]),
    'partner-form': ('Partner pricing — form', 'Contact Form 7 partner form.', 'meteora-forms', lambda c: [section(c, [S.cf7(c, 'partner')], width='62rem')]),
}

PAGE_PATTERNS = {
    'page-home': ('Page — Home', PG.home), 'page-weddings': ('Page — Weddings', PG.weddings),
    'page-destination': ('Page — Destination weddings', PG.destination), 'page-tuscany': ('Page — Wedding bar catering in Tuscany', PG.tuscany),
    'page-bars': ('Page — Bars', PG.bars),
    'page-bar-golden-mirror': ('Page — Bar: Golden Mirror', lambda c: PG.bar_detail(c, 'golden-mirror')),
    'page-bar-silver-reflection': ('Page — Bar: Silver Reflection', lambda c: PG.bar_detail(c, 'silver-reflection')),
    'page-bar-pure-white': ('Page — Bar: Pure White', lambda c: PG.bar_detail(c, 'pure-white')),
    'page-cocktails': ('Page — Cocktail Experience', PG.cocktails), 'page-services': ('Page — Services', PG.services),
    'page-corporate': ('Page — Corporate & private', PG.corporate), 'page-partners': ('Page — Planners & venues', PG.partners),
    'page-events': ('Page — Events', PG.events), 'page-about': ('Page — About', PG.about), 'page-why': ('Page — Why Meteora', PG.why),
    'page-contact': ('Page — Contact', PG.contact), 'page-thanks': ('Page — Thank you', PG.thanks),
    'page-privacy': ('Page — Privacy Policy', lambda c: PG.legal(c, 'privacy')), 'page-cookies': ('Page — Cookie Policy', lambda c: PG.legal(c, 'cookies')),
}


def _featured_band(c):
    band = S.cta_band(c, 'bars/golden-marble-night.webp', '', track='event_band')
    for k in ('url', 'alt', 'id'):
        band[1].pop(k, None)
    band[1]['useFeaturedImage'] = True
    c.urls.clear()
    return band


def canon(specs: dict, base: str) -> dict:
    inp = os.path.join(SCRATCH, 'meteora-specs.json')
    out = os.path.join(SCRATCH, 'meteora-canon.json')
    json.dump(specs, open(inp, 'w'), ensure_ascii=False)
    r = subprocess.run(['node', os.path.join(ROOT, 'canon.mjs'), base, inp, out], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stderr.write(r.stderr)
        raise SystemExit('canonical serialization failed')
    return json.load(open(out))


def header(slug, title, desc, cats, inserter=True, post_types=None, block_types=None, viewport=1440):
    lines = ['<?php', '/**', f' * Title: {title}', f' * Slug: meteora/{slug}', f' * Categories: {cats}', f' * Description: {desc}', f' * Viewport Width: {viewport}']
    if post_types:
        lines.append(f' * Post Types: {post_types}')
    if block_types:
        lines.append(f' * Block Types: {block_types}')
    if not inserter:
        lines.append(' * Inserter: no')
    lines += [' *', ' * Generated by wordpress/tools/build.py — edit the generator or edit the pattern in the Site Editor.', ' *', ' * @package Meteora', ' */', '', '?>']
    return '\n'.join(lines) + '\n'


def build_patterns(base: str):
    ctxs, specs, meta = {}, {}, {}
    for key, (title, desc, cats, fn) in SECTION_PATTERNS.items():
        c = Ctx('pattern')
        specs[key] = fn(c)
        ctxs[key] = c
        meta[key] = header(key, title, desc, cats)
    for key, (title, fn) in PAGE_PATTERNS.items():
        c = Ctx('pattern')
        specs[key] = fn(c)[0]
        ctxs[key] = c
        meta[key] = header(key, title, f'Complete “{title.split("— ")[1]}” page with real content.', 'meteora-pages', post_types='page', block_types='core/post-content')
    out = canon(specs, base)
    # gettext: identical English with different Italian gets a msgctxt so both stay exact.
    variants = {}
    for c in ctxs.values():
        for en, it, _ in c.texts:
            variants.setdefault(en, [])
            if it not in variants[en]:
                variants[en].append(it)
    entries = {}  # (ctx, en) -> it
    for key, c in ctxs.items():
        c.contexts = {}
        for i, (en, it, _) in enumerate(c.texts):
            n = variants[en].index(it)
            gctx = f'variant {n + 1}' if n else None
            if gctx:
                c.contexts[i] = gctx
            entries[(gctx, en)] = it
        php = meta[key] + finalize_pattern(c, out[key]) + '\n'
        open(os.path.join(THEME, 'patterns', f'{key}.php'), 'w').write(php)
    json.dump([[k[0], k[1], v] for k, v in entries.items()], open(os.path.join(ROOT, 'strings-patterns.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'wrote {len(out)} patterns, {len(entries)} translation entries')


if __name__ == '__main__' and sys.argv[1] == 'patterns':
    build_patterns(sys.argv[2])


# ============================================================ content (pages, posts, media)
from blocks import finalize_wxr  # noqa: E402

# key, builder, EN slug, IT slug, parent key, template, EN title, IT title
SITE_PAGES = [
    ('home', PG.home, 'home', 'home-it', None, '', 'Home', 'Home'),
    ('weddings', PG.weddings, 'weddings', 'matrimoni', None, 'page-no-title', 'Weddings', 'Matrimoni'),
    ('destination', PG.destination, 'destination-weddings-italy', 'destination-wedding-italia', None, 'page-landing', 'Destination Weddings', 'Destination Wedding'),
    ('tuscany', PG.tuscany, 'wedding-bar-catering-tuscany', 'bar-catering-matrimoni-toscana', None, 'page-no-title', 'Wedding bar catering in Tuscany', 'Bar catering per matrimoni in Toscana'),
    ('bars', PG.bars, 'bars', 'banchi-bar', None, 'page-no-title', 'Bars', 'Banchi bar'),
    ('bar-golden-mirror', lambda c: PG.bar_detail(c, 'golden-mirror'), 'golden-mirror', 'golden-mirror', 'bars', 'page-no-title', 'Golden Mirror', 'Golden Mirror'),
    ('bar-silver-reflection', lambda c: PG.bar_detail(c, 'silver-reflection'), 'silver-reflection', 'silver-reflection', 'bars', 'page-no-title', 'Silver Reflection', 'Silver Reflection'),
    ('bar-pure-white', lambda c: PG.bar_detail(c, 'pure-white'), 'pure-white', 'pure-white', 'bars', 'page-no-title', 'Pure White', 'Pure White'),
    ('cocktails', PG.cocktails, 'cocktail-experience', 'esperienza-cocktail', None, 'page-no-title', 'Cocktail Experience', 'Cocktail Experience'),
    ('services', PG.services, 'services', 'servizi', None, 'page-no-title', 'Services', 'Servizi'),
    ('corporate', PG.corporate, 'corporate-private-events', 'eventi-aziendali-privati', None, 'page-landing', 'Corporate & Private Events', 'Eventi aziendali e privati'),
    ('partners', PG.partners, 'wedding-planners-venues', 'wedding-planner-location', None, 'page-no-title', 'Wedding Planners & Venues', 'Wedding planner e location'),
    ('events', PG.events, 'events', 'eventi', None, 'page-no-title', 'Events', 'Eventi'),
    ('about', PG.about, 'about', 'chi-siamo', None, 'page-no-title', 'About', 'Chi siamo'),
    ('why', PG.why, 'why-meteora', 'perche-meteora', None, 'page-no-title', 'Why Meteora', 'Perché Meteora'),
    ('contact', PG.contact, 'contact', 'contatti', None, 'page-no-title', 'Contact', 'Contatti'),
    ('thanks', PG.thanks, 'thank-you', 'grazie', None, 'page-no-title', 'Thank you', 'Grazie'),
    ('privacy', lambda c: PG.legal(c, 'privacy'), 'privacy-policy', 'informativa-privacy', None, 'page-no-title', 'Privacy Policy', 'Privacy Policy'),
    ('cookies', lambda c: PG.legal(c, 'cookies'), 'cookie-policy', 'informativa-cookie', None, 'page-no-title', 'Cookie Policy', 'Cookie Policy'),
]
PAGE_ID = {'en': 101, 'it': 201}
POST_ID = {'en': 301, 'it': 401}


def asset_paths():
    base = os.path.join(THEME, 'assets', 'images')
    out = []
    for d, _, files in os.walk(base):
        for f in files:
            if f.endswith('.webp') and 'brand' not in d:
                out.append(os.path.relpath(os.path.join(d, f), base).replace(os.sep, '/'))
    return sorted(out)


def media_map():
    return {p: 1001 + i for i, p in enumerate(asset_paths())}


def page_paths():
    by_key = {p[0]: p for p in SITE_PAGES}
    res = {}
    for key, _, en, it, parent, *_ in SITE_PAGES:
        for lang, slug in (('en', en), ('it', it)):
            path = slug
            if parent:
                path = (by_key[parent][2] if lang == 'en' else by_key[parent][3]) + '/' + slug
            res[(key, lang)] = path
    return res


def make_resolver(base):
    paths = page_paths()

    def resolve(key, lang):
        prefix = base + ('/it' if lang == 'it' else '')
        if key == 'home':
            return prefix + '/'
        return f'{prefix}/{paths[(key, lang)]}/'
    return resolve


def build_content(base_canon: str, site: str):
    import blocks as BL
    BL.THEME_URL = site + '/wp-content/themes/meteora/'
    mm = media_map()
    specs, ctxs, metas = {}, {}, {}
    for key, fn, *_ in SITE_PAGES:
        c = Ctx('wxr', media_ids=mm)
        blocks_, meta = fn(c)
        specs['page:' + key], ctxs['page:' + key], metas['page:' + key] = blocks_, c, meta
    events = S.DATA['events']['events']
    for i, e in enumerate(events):
        c = Ctx('wxr', media_ids=mm)
        specs[f'post:{i}'], ctxs[f'post:{i}'] = PG.event_post(c, e), c
    out = canon(specs, base_canon)
    resolve = make_resolver(site)
    by_key = {p[0]: i for i, p in enumerate(SITE_PAGES)}
    result = {'site': site, 'attachments': [{'id': v, 'path': k, 'url': BL.THEME_URL + 'assets/images/' + k} for k, v in mm.items()], 'pages': [], 'posts': []}
    for idx, (key, fn, en, it, parent, template, ten, tit) in enumerate(SITE_PAGES):
        for lang, slug, title in (('en', en, ten), ('it', it, tit)):
            result['pages'].append({
                'id': PAGE_ID[lang] + idx, 'key': key, 'lang': lang, 'slug': slug, 'title': title, 'template': template,
                'parent': (PAGE_ID[lang] + by_key[parent]) if parent else 0, 'menu_order': idx,
                'translation_of': PAGE_ID['en'] + idx if lang == 'it' else None,
                'seo_title': metas['page:' + key][lang][0], 'seo_description': metas['page:' + key][lang][1],
                'content': finalize_wxr(ctxs['page:' + key], out['page:' + key], lang, resolve),
            })
    for i, e in enumerate(events):
        for lang in ('en', 'it'):
            cover = ip_path(e['cover'])
            result['posts'].append({
                'id': POST_ID[lang] + i, 'lang': lang, 'slug': e['slug'][lang], 'title': e['title'][lang], 'excerpt': e['excerpt'][lang],
                'tags': [e['type'][lang]], 'categories': ['events'] + (['placeholder'] if e['draft'] else []),
                'thumbnail': mm.get(cover), 'translation_of': POST_ID['en'] + i if lang == 'it' else None,
                'date': f'2026-09-{10 + i:02d} 10:00:00',
                'content': finalize_wxr(ctxs[f'post:{i}'], out[f'post:{i}'], lang, resolve),
            })
    path = os.path.join(SCRATCH, 'meteora-content.json')
    json.dump(result, open(path, 'w'), ensure_ascii=False, indent=1)
    print('content written to', path, len(result['pages']), 'pages', len(result['posts']), 'posts', len(result['attachments']), 'attachments')
    return path


def ip_path(src):
    return S.ip(src)


if __name__ == '__main__' and sys.argv[1] == 'content':
    build_content(sys.argv[2], sys.argv[3])


# ============================================================ WXR export
import cf7 as CF7  # noqa: E402
from xml.sax.saxutils import escape as xesc  # noqa: E402


def cdata(s: str) -> str:
    return '<![CDATA[' + (s or '').replace(']]>', ']]]]><![CDATA[>') + ']]>'


def build_wxr(content_path: str, out_path: str):
    d = json.load(open(content_path))
    site = d['site']
    now = '2026-06-01 09:00:00'
    cats = {('en', 'events'): ('events', 'Events'), ('en', 'placeholder'): ('placeholder', 'Placeholder story'),
            ('it', 'events'): ('eventi', 'Eventi'), ('it', 'placeholder'): ('placeholder-it', 'Storia segnaposto')}
    tags = sorted({(p['lang'], t) for p in d['posts'] for t in p['tags']})
    def slugify(s):
        import re
        import unicodedata
        s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
        return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

    # Polylang needs one term per language: IT tags whose slug equals an EN tag get a suffix.
    en_slugs = {slugify(t) for lang, t in tags if lang == 'en'}
    tag_slug = {(lang, t): slugify(t) + ('-it' if lang == 'it' and slugify(t) in en_slugs else '') for lang, t in tags}
    by_id = {p['id']: p for p in d['posts']}
    tag_group = {}
    for p in d['posts']:
        src = by_id[p['translation_of']] if p['translation_of'] else p
        for j, t in enumerate(p['tags']):
            tag_group[(p['lang'], t)] = 'post_tag:' + slugify(src['tags'][j])


    def meta(k, v):
        return f'\t\t<wp:postmeta>\n\t\t\t<wp:meta_key>{cdata(k)}</wp:meta_key>\n\t\t\t<wp:meta_value>{cdata(str(v))}</wp:meta_value>\n\t\t</wp:postmeta>\n'

    import datetime as _dt

    def item(pid, title, slug, ptype, content='', excerpt='', parent=0, order=0, date=None, metas=None, terms='', status='publish', extra='', link=''):
        # Distinct date per item: the WordPress Importer skips items whose title AND date already exist.
        if date is None:
            date = (_dt.datetime(2026, 6, 1, 8, 0, 0) + _dt.timedelta(minutes=pid)).strftime('%Y-%m-%d %H:%M:%S')
        out = ['\t<item>\n', f'\t\t<title>{cdata(title)}</title>\n', f'\t\t<link>{xesc(link or site + "/?p=" + str(pid))}</link>\n',
               '\t\t<dc:creator><![CDATA[admin]]></dc:creator>\n', f'\t\t<guid isPermaLink="false">{xesc(site)}/?p={pid}</guid>\n',
               '\t\t<description></description>\n', f'\t\t<content:encoded>{cdata(content)}</content:encoded>\n',
               f'\t\t<excerpt:encoded>{cdata(excerpt)}</excerpt:encoded>\n', f'\t\t<wp:post_id>{pid}</wp:post_id>\n',
               f'\t\t<wp:post_date>{cdata(date)}</wp:post_date>\n', f'\t\t<wp:post_date_gmt>{cdata(date)}</wp:post_date_gmt>\n',
               f'\t\t<wp:post_modified>{cdata(date)}</wp:post_modified>\n', f'\t\t<wp:post_modified_gmt>{cdata(date)}</wp:post_modified_gmt>\n',
               '\t\t<wp:comment_status><![CDATA[closed]]></wp:comment_status>\n', '\t\t<wp:ping_status><![CDATA[closed]]></wp:ping_status>\n',
               f'\t\t<wp:post_name>{cdata(slug)}</wp:post_name>\n', f'\t\t<wp:status>{cdata(status)}</wp:status>\n',
               f'\t\t<wp:post_parent>{parent}</wp:post_parent>\n', f'\t\t<wp:menu_order>{order}</wp:menu_order>\n',
               f'\t\t<wp:post_type>{cdata(ptype)}</wp:post_type>\n', '\t\t<wp:post_password><![CDATA[]]></wp:post_password>\n',
               '\t\t<wp:is_sticky>0</wp:is_sticky>\n', extra, terms]
        for k, v in (metas or {}).items():
            out.append(meta(k, v))
        out.append('\t</item>\n')
        return ''.join(out)

    parts = []
    head = f'''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Meteora Events — content export for the Meteora theme (WordPress eXtended RSS).
     Import with Tools → Import → WordPress after activating the theme
     (and, optionally, Polylang + Contact Form 7). Images are downloaded from the
     theme folder on {site}. -->
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
	<title>Meteora Events</title>
	<link>{xesc(site)}</link>
	<description>Luxury Open Bar Catering &amp; Hospitality Services</description>
	<language>en-US</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>{xesc(site)}</wp:base_site_url>
	<wp:base_blog_url>{xesc(site)}</wp:base_blog_url>
	<wp:author><wp:author_id>1</wp:author_id><wp:author_login><![CDATA[admin]]></wp:author_login><wp:author_email><![CDATA[info@meteoraevents.com]]></wp:author_email><wp:author_display_name><![CDATA[Meteora Events]]></wp:author_display_name><wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>
'''
    parts.append(head)
    def termmeta(lang, group):
        return (f'<wp:termmeta><wp:meta_key>{cdata("_meteora_lang")}</wp:meta_key><wp:meta_value>{cdata(lang)}</wp:meta_value></wp:termmeta>'
                f'<wp:termmeta><wp:meta_key>{cdata("_meteora_group")}</wp:meta_key><wp:meta_value>{cdata(group)}</wp:meta_value></wp:termmeta>')

    for i, ((lang, key), (slug, name)) in enumerate(sorted(cats.items())):
        parts.append(f'\t<wp:category><wp:term_id>{900 + i}</wp:term_id><wp:category_nicename>{cdata(slug)}</wp:category_nicename><wp:category_parent><![CDATA[]]></wp:category_parent><wp:cat_name>{cdata(name)}</wp:cat_name>{termmeta(lang, "category:" + key)}</wp:category>\n')
    for i, (lang, t) in enumerate(tags):
        parts.append(f'\t<wp:tag><wp:term_id>{950 + i}</wp:term_id><wp:tag_slug>{cdata(tag_slug[(lang, t)])}</wp:tag_slug><wp:tag_name>{cdata(t)}</wp:tag_name>{termmeta(lang, tag_group[(lang, t)])}</wp:tag>\n')

    for a in d['attachments']:
        folder, name = a['path'].rsplit('/', 1)
        title = folder.replace('-', ' ').title() + ' — ' + name.replace('.webp', '').replace('-', ' ').title()
        parts.append(item(a['id'], title, slugify(a['path'].replace('.webp', '')), 'attachment', status='inherit',
                          extra=f'\t\t<wp:attachment_url>{cdata(a["url"])}</wp:attachment_url>\n', link=a['url'],
                          metas={'_wp_attachment_image_alt': title}))

    for p in d['pages']:
        group = p['translation_of'] or p['id']
        metas = {'_wp_page_template': p['template'] or 'default', '_meteora_lang': p['lang'], '_meteora_group': group,
                 '_yoast_wpseo_title': p['seo_title'], '_yoast_wpseo_metadesc': p['seo_description'],
                 'rank_math_title': p['seo_title'], 'rank_math_description': p['seo_description']}
        parts.append(item(p['id'], p['title'], p['slug'], 'page', p['content'], p['seo_description'], p['parent'], p['menu_order'], metas=metas))

    en_post_slugs = {p['slug'] for p in d['posts'] if p['lang'] == 'en'}
    for p in d['posts']:
        group = p['translation_of'] or p['id']
        terms = ''
        for c in p['categories']:
            slug, name = cats[(p['lang'], c)]
            terms += f'\t\t<category domain="category" nicename="{xesc(slug)}">{cdata(name)}</category>\n'
        for t in p['tags']:
            terms += f'\t\t<category domain="post_tag" nicename="{xesc(tag_slug[(p["lang"], t)])}">{cdata(t)}</category>\n'
        metas = {'_meteora_lang': p['lang'], '_meteora_group': group, '_thumbnail_id': p['thumbnail']}
        date = p['date'][:-2] + ('01' if p['lang'] == 'it' else '00')
        # Polylang (free) cannot share a slug between languages: avoid WordPress's "-2".
        slug = p['slug'] + ('-it' if p['lang'] == 'it' and p['slug'] in en_post_slugs else '')
        parts.append(item(p['id'], p['title'], slug, 'post', p['content'], p['excerpt'], date=date, metas=metas, terms=terms))

    fid = 501
    for kind in ('quote', 'partner'):
        for lang in ('en', 'it'):
            f = CF7.FORMS[kind][lang]
            parts.append(item(fid, f['title'], slugify(f['title']), 'wpcf7_contact_form', f['form'], metas=CF7.form_meta(f, lang)))
            fid += 1

    parts.append('</channel>\n</rss>\n')
    open(out_path, 'w').write(''.join(parts))
    print('WXR written to', out_path, f'({os.path.getsize(out_path) // 1024} KB)')


if __name__ == '__main__' and sys.argv[1] == 'wxr':
    build_wxr(sys.argv[2], sys.argv[3])
