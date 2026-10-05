# Theme generator (developer tool — not needed to use the theme)

The section and page patterns in `../meteora/patterns/` are generated from the
original site's copy so that EN and IT stay identical to the source.

- `export-data.mjs` — exports `src/data/*.ts` of the Astro site to `data.json`.
- `blocks.py` — block builder with translation tokens; finalizes to translatable PHP (patterns) or plain text per language (WXR).
- `sections.py`, `pages.py` — one function per section/page of the original site.
- `canon.mjs` — serializes block specs inside a real WordPress editor (createBlock + serialize), so the markup is exactly what the editor saves; also round-trip validates.
- `build.py patterns <wp-url>` — writes the patterns; `build.py content <wp-url> <site-url>` — writes the page/post content JSON (used for the WXR).
- `i18n.py` — writes `languages/meteora.pot`, `it_IT.po`, `it_IT.mo`.
- `seed-local.php` — dev only: seeds a local WordPress with the content JSON.

Requires a running WordPress with the Meteora theme active and user admin/admin (local only).
