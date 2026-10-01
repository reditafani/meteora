"""
Builds languages/meteora.pot, it_IT.po and it_IT.mo from:
- strings-patterns.json (generated patterns, with msgctxt variants)
- MANUAL: strings in hand-written PHP (header, footer, menu, inc/*).
"""
import json
import os
import struct

ROOT = os.path.dirname(os.path.abspath(__file__))
LANG = os.path.join(ROOT, '..', 'meteora', 'languages')

MANUAL = {
    'About': 'Chi siamo', 'All rights reserved.': 'Tutti i diritti riservati.', 'Back to home': 'Torna alla home', 'Bars': 'Banchi bar',
    'Based in Tuscany, serving events throughout Italy and abroad.': 'Base in Toscana, operativi in tutta Italia e all’estero.',
    'Cocktail Experience': 'Cocktail Experience', 'Compact IT / EN switcher. Requires Polylang or WPML.': 'Selettore IT / EN compatto. Richiede Polylang o WPML.',
    'Complete page layouts with real content.': 'Layout di pagina completi con contenuti reali.', 'Contact': 'Contatti', 'Cookie Policy': 'Cookie Policy',
    'Cookie preferences': 'Preferenze cookie', 'Corporate': 'Aziende', 'Corporate & Private': 'Aziende & privati', 'Destination Weddings': 'Destination Weddings',
    'Editorial sections of the Meteora Events site.': 'Sezioni editoriali del sito Meteora Events.', 'Events': 'Eventi', 'Experience': 'Esperienza', 'Explore': 'Esplora',
    'Hello Meteora Events, I would like to request information about a bar catering service for my event.': 'Buongiorno Meteora Events, vorrei ricevere informazioni su un servizio di bar catering per il mio evento.',
    'Home': 'Home', 'IT / EN — activate Polylang or WPML': 'IT / EN — attiva Polylang o WPML', 'Language': 'Lingua', 'Language switcher (IT / EN)': 'Selettore lingua (IT / EN)',
    'Luxury Open Bar Catering & Hospitality Services': 'Luxury Open Bar Catering & Hospitality Services', 'Main navigation': 'Navigazione principale', 'Menu': 'Menu',
    'Meteora — Forms': 'Meteora — Moduli', 'Meteora — Full pages': 'Meteora — Pagine complete', 'Meteora — Sections': 'Meteora — Sezioni', 'More': 'Altro',
    'Nothing here yet. New event stories are on their way.': 'Ancora niente qui. Nuove storie di eventi sono in arrivo.',
    'Page not found. <em>Let’s get you back to the bar.</em>': 'Pagina non trovata. <em>Torniamo al bar.</em>', 'Partner area': 'Area partner', 'Partners': 'Partner',
    'Planners & venues': 'Wedding planner & location', 'Primary': 'Principale', 'Privacy Policy': 'Privacy Policy', 'Request a quote': 'Richiedi un preventivo',
    'Request partner pricing': 'Richiedi listino partner', 'Search': 'Cerca', 'Search the site': 'Cerca nel sito', 'Services': 'Servizi',
    'Tell us the date, the place and the number of guests: we will reply with a tailored proposal.': 'Raccontateci data, luogo e numero di ospiti: vi risponderemo con una proposta su misura.',
    'The Bar Collection': 'I banchi bar', 'The bar becomes <em>part of the event.</em>': 'Il bar diventa <em>parte dell’evento.</em>',
    'The page you are looking for does not exist or has moved.': 'La pagina che cercate non esiste o è stata spostata.', 'Tuscany · Italy': 'Toscana · Italia',
    'Weddings': 'Matrimoni', 'Why Meteora': 'Perché Meteora', 'Write to us': 'Scriveteci', 'More events': 'Altri eventi',
    'Message us on WhatsApp': 'Scrivici su WhatsApp',
    'Close': 'Chiudi',
    'You can edit the message before sending it.': 'Puoi modificare il messaggio prima di inviarlo.',
    'Open WhatsApp': 'Apri WhatsApp',
    'Your privacy': 'La tua privacy',
    'We use technical cookies that the site needs to work. With your consent we will also use analytics cookies to understand how to improve it. No non-essential cookie is set until you choose.': 'Usiamo cookie tecnici necessari al funzionamento del sito. Con il tuo consenso useremo anche cookie di analisi per capire come migliorare il sito. Nessun cookie non necessario viene attivato senza la tua scelta.',
    'Necessary': 'Necessari',
    'Required for the site to work and to remember your choices. Always active.': 'Indispensabili per il funzionamento del sito e per ricordare le tue preferenze. Sempre attivi.',
    'Analytics': 'Analisi',
    'Anonymous, aggregated statistics about how the site is used (e.g. Google Analytics).': 'Statistiche anonime e aggregate sull’uso del sito (es. Google Analytics).',
    'Marketing': 'Marketing',
    'Advertising campaign measurement (e.g. Meta Pixel).': 'Misurazione delle campagne pubblicitarie (es. Meta Pixel).',
    'Necessary only': 'Solo necessari',
    'Customise': 'Personalizza',
    'Save preferences': 'Salva preferenze',
    'Accept all': 'Accetta tutti',
}


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


def main():
    entries = {}
    for ctx, en, it in json.load(open(os.path.join(ROOT, 'strings-patterns.json'))):
        entries[(ctx, en)] = it
    for en, it in MANUAL.items():
        entries.setdefault((None, en), it)
    os.makedirs(LANG, exist_ok=True)
    head = ('msgid ""\nmsgstr ""\n"Project-Id-Version: Meteora 1.0.0\\n"\n"Language: {lang}\\n"\n"MIME-Version: 1.0\\n"\n'
            '"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n"X-Domain: meteora\\n"\n\n')
    pot, po = [head.format(lang='')], [head.format(lang='it_IT')]
    for (ctx, en), it in sorted(entries.items(), key=lambda kv: (kv[0][1], kv[0][0] or '')):
        c = f'msgctxt "{esc(ctx)}"\n' if ctx else ''
        pot.append(f'{c}msgid "{esc(en)}"\nmsgstr ""\n\n')
        po.append(f'{c}msgid "{esc(en)}"\nmsgstr "{esc(it)}"\n\n')
    open(os.path.join(LANG, 'meteora.pot'), 'w').write(''.join(pot))
    open(os.path.join(LANG, 'it_IT.po'), 'w').write(''.join(po))
    # .mo (GNU gettext binary format)
    meta = 'Project-Id-Version: Meteora 1.0.0\nLanguage: it_IT\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\nPlural-Forms: nplurals=2; plural=(n != 1);\n'
    items = [('', meta)] + [((f'{ctx}\x04{en}' if ctx else en), it) for (ctx, en), it in entries.items() if it]
    items.sort(key=lambda kv: kv[0].encode('utf-8'))
    ids = b''.join(k.encode() + b'\0' for k, _ in items)
    strs = b''.join(v.encode() + b'\0' for _, v in items)
    n = len(items)
    o_ids, o_strs = 28, 28 + n * 8
    data_start = 28 + n * 16
    id_table, str_table, off = [], [], data_start
    for k, _ in items:
        b = k.encode(); id_table.append((len(b), off)); off += len(b) + 1
    for _, v in items:
        b = v.encode(); str_table.append((len(b), off)); off += len(b) + 1
    out = struct.pack('<7I', 0x950412de, 0, n, o_ids, o_strs, 0, 0)
    out += b''.join(struct.pack('<2I', *x) for x in id_table) + b''.join(struct.pack('<2I', *x) for x in str_table) + ids + strs
    open(os.path.join(LANG, 'it_IT.mo'), 'wb').write(out)
    print(f'{len(entries)} entries → meteora.pot, it_IT.po, it_IT.mo')


if __name__ == '__main__':
    main()
