"""
Block-spec builder with i18n tokens.

Every user-facing string goes through T(en, it). Specs are serialized by the
real WordPress editor (canon.mjs), then tokens are replaced either by
translatable PHP (theme patterns) or by plain text in a given language (WXR).
"""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass, field

SITE = 'https://meteoraevents.com'
THEME_URL = SITE + '/wp-content/themes/meteora/'


@dataclass
class Ctx:
    mode: str  # 'pattern' | 'wxr'
    texts: list = field(default_factory=list)   # (en, it, is_html)
    urls: list = field(default_factory=list)    # theme-relative asset paths
    links: list = field(default_factory=list)   # (key, hash)
    media_ids: dict = field(default_factory=dict)  # asset path -> attachment id (wxr)

    # ---- tokens ----
    def T(self, en: str, it: str | None = None, html_ok: bool = False) -> str:
        self.texts.append((en, it if it is not None else en, html_ok))
        return f'⟦T{len(self.texts) - 1}⟧'

    def H(self, en: str, it: str | None = None) -> str:
        """Text that contains inline HTML (<em>, <br>, <a>)."""
        return self.T(en, it, True)

    def U(self, path: str) -> str:
        self.urls.append(path)
        return f'⟦U{len(self.urls) - 1}⟧'

    def L(self, key: str, hash_: str = '') -> str:
        self.links.append((key, hash_))
        return f'⟦L{len(self.links) - 1}⟧'


def B(name: str, attrs: dict | None = None, inner: list | None = None) -> list:
    return [name, {k: v for k, v in (attrs or {}).items() if v is not None}, inner or []]


def _cls(*parts) -> str | None:
    c = ' '.join(p for p in parts if p)
    return c or None


def _clean(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


# ---------- block shortcuts ----------
def group(c: Ctx, inner, cls=None, tag=None, layout=None, align=None, anchor=None, style=None, name=None, **extra):
    a = _clean({'tagName': tag, 'align': align, 'anchor': anchor, 'className': cls, 'style': style,
                'layout': layout or {'type': 'default'}, 'metadata': {'name': name} if name else None})
    a.update(extra)
    return B('core/group', a, inner)


def section(c: Ctx, inner, cls='', dark=False, alt=False, anchor=None, pad=True, pad_top=True, name=None, width='1440px'):
    style_cls = 'is-style-section-dark' if dark else ('is-style-section-alt' if alt else None)
    style = None
    if pad:
        top = {True: 'var:preset|spacing|section', False: '0'}.get(pad_top, f'var:preset|spacing|{pad_top}')
        style = {'spacing': {'padding': {'top': top, 'bottom': 'var:preset|spacing|section'}}}
    return group(c, inner, cls=_cls('mt-section', cls, style_cls), tag='section', align='full', anchor=anchor,
                 layout={'type': 'constrained', 'contentSize': width}, style=style, name=name)


def p(c: Ctx, content, cls=None, align=None, **extra):
    a = _clean({'content': content, 'className': cls, 'align': align})
    a.update(extra)
    return B('core/paragraph', a)


def eyebrow(c: Ctx, content, anim=True, extra_cls=None):
    return p(c, content, cls=_cls('is-style-eyebrow', 'animate-fade-up' if anim else None, extra_cls))


def h(c: Ctx, level, content, cls=None, anchor=None, align=None):
    a = _clean({'level': level if level != 2 else None, 'content': content, 'className': cls, 'anchor': anchor, 'textAlign': align})
    return B('core/heading', a)


def img(c: Ctx, path, alt, ratio=None, cls=None, size='large', scale='cover', focal=None, caption=None):
    a = {'url': c.U(path), 'alt': alt, 'sizeSlug': size, 'linkDestination': 'none'}
    if c.mode == 'wxr' and path in c.media_ids:
        a['id'] = c.media_ids[path]
    if ratio:
        a['aspectRatio'] = ratio
        a['scale'] = scale
    if cls:
        a['className'] = cls
    if caption:
        a['caption'] = caption
    return B('core/image', a)


def buttons(c: Ctx, items, cls=None, layout=None):
    return B('core/buttons', _clean({'className': cls, 'layout': layout}), items)


def button(c: Ctx, text, url, cls=None, width=None, target=None):
    a = _clean({'text': text, 'url': url, 'className': cls, 'width': width, 'linkTarget': target,
                'rel': 'noreferrer noopener' if target else None})
    return B('core/button', a)


def btn_primary(c, text, url, track=None, arrow=False):
    return button(c, text, url, cls=_cls('has-arrow' if arrow else None, f'meteora-track-{track}' if track else None))


def btn_link(c, text, url, track=None):
    return button(c, text, url, cls=_cls('is-style-button-text-link', f'meteora-track-{track}' if track else None))


def ul(c: Ctx, items, cls=None, ordered=False):
    a = _clean({'className': cls, 'ordered': True if ordered else None})
    return B('core/list', a, [B('core/list-item', {'content': it}) for it in items])


def html_block(c: Ctx, content):
    return B('core/html', {'content': content})


def spacer(c: Ctx, height='var:preset|spacing|l'):
    return B('core/spacer', {'height': height})


# ---------- finalization ----------
TOKEN = re.compile(r'⟦([TUL])(\d+)⟧')


def _context(s: str, pos: int) -> str:
    """'json' inside a block comment, 'attr' inside an HTML tag, else 'text'."""
    last_c_open = s.rfind('<!--', 0, pos)
    last_c_close = s.rfind('-->', 0, pos)
    if last_c_open > last_c_close:
        return 'json'
    last_lt = s.rfind('<', 0, pos)
    last_gt = s.rfind('>', 0, pos)
    return 'attr' if last_lt > last_gt else 'text'


def php_str(s: str) -> str:
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def wp_json_inner(s: str) -> str:
    """Escape a string the way WordPress serializes block comment attributes."""
    out = json.dumps(s, ensure_ascii=False)[1:-1]
    return (out.replace('--', '\\u002d\\u002d').replace('<', '\\u003c').replace('>', '\\u003e')
               .replace('&', '\\u0026').replace('\\"', '\\u0022'))


def finalize_pattern(c: Ctx, markup: str) -> str:
    def rep(m):
        kind, idx = m.group(1), int(m.group(2))
        ctx = _context(markup, m.start())
        if kind == 'T':
            en, it, is_html = c.texts[idx]
            gctx = c.contexts.get(idx) if hasattr(c, 'contexts') else None
            if gctx:
                cx = php_str(gctx)
                if ctx in ('json', 'attr'):
                    return f'<?php echo esc_attr_x( {php_str(en)}, {cx}, \'meteora\' ); ?>'
                if is_html:
                    return f'<?php echo wp_kses_post( _x( {php_str(en)}, {cx}, \'meteora\' ) ); ?>'
                return f'<?php echo esc_html_x( {php_str(en)}, {cx}, \'meteora\' ); ?>'
            if ctx in ('json', 'attr'):
                return f'<?php echo esc_attr__( {php_str(en)}, \'meteora\' ); ?>'
            if is_html:
                return f'<?php echo wp_kses_post( __( {php_str(en)}, \'meteora\' ) ); ?>'
            return f'<?php echo esc_html__( {php_str(en)}, \'meteora\' ); ?>'
        if kind == 'U':
            return f'<?php echo esc_url( meteora_asset( {php_str("assets/images/" + c.urls[idx])} ) ); ?>'
        key, hash_ = c.links[idx]
        args = php_str(key) + (', ' + php_str(hash_) if hash_ else '')
        return f'<?php echo esc_url( meteora_page_url( {args} ) ); ?>'
    return TOKEN.sub(rep, markup)


def finalize_wxr(c: Ctx, markup: str, lang: str, link_resolver) -> str:
    def rep(m):
        kind, idx = m.group(1), int(m.group(2))
        ctx = _context(markup, m.start())
        if kind == 'T':
            en, it, is_html = c.texts[idx]
            s = it if lang == 'it' else en
            if ctx == 'json':
                return wp_json_inner(s)
            if ctx == 'attr':
                return html.escape(s, quote=True)
            return s if is_html else html.escape(s, quote=False)
        if kind == 'U':
            url = THEME_URL + 'assets/images/' + c.urls[idx]
            return wp_json_inner(url) if ctx == 'json' else url
        key, hash_ = c.links[idx]
        url = link_resolver(key, lang) + (('#' + hash_) if hash_ else '')
        return wp_json_inner(url) if ctx == 'json' else html.escape(url, quote=True)
    return TOKEN.sub(rep, markup)
