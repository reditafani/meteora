=== Meteora ===
Contributors: meteoraevents
Requires at least: 7.0
Tested up to: 7.1
Requires PHP: 8.2
Stable tag: 1.0.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Block theme (Full Site Editing) for Meteora Events — Luxury Open Bar Catering & Hospitality Services.

== Description ==

Meteora is the native block theme of meteoraevents.com: editorial layouts, cinematic
heroes, scenographic bar collection, cocktail gallery, comparison table, FAQ and lead
forms. Everything is built with core blocks — no page builder and no required plugin.

* theme.json (schema v3): palette, fluid typography, spacing scale and block styles.
* Every section is a pattern (Patterns → Meteora — Sections) and every page has a
  full-page pattern (Meteora — Pages).
* Scroll animations controllable from the editor: add the CSS classes
  `animate-fade-up`, `animate-image-reveal`, `animate-delay-1` … `animate-delay-4`,
  `animate-drift` (Advanced → Additional CSS class). They respect
  `prefers-reduced-motion`.
* Self-hosted fonts (Cormorant Garamond, Jost), WebP images, deferred vanilla JS loaded
  only on the pages that use it.
* Translation-ready (text domain `meteora`, Italian included), compatible with
  Polylang and WPML; language switcher in header, menu and footer.
* JSON-LD LocalBusiness + Service (area served: Tuscany, Italy); defers to Yoast SEO or
  Rank Math when one of them is active.
* Instagram strip with the latest posts of @meteoraevents through the free
  "Smash Balloon Social Photo Feed" plugin (curated images as fallback).
* Optional Contact Form 7 integration for the quote and partner forms (an email /
  WhatsApp fallback is shown when the plugin is not active).

== Installation ==

1. Appearance → Themes → Add New → Upload Theme, choose meteora.zip, Activate.
2. Optional plugins: Polylang (bilingual EN/IT site), Contact Form 7 (forms),
   WordPress Importer (to import meteora-content.xml).
3. Tools → Import → WordPress → meteora-content.xml. The theme then sets the static
   front page and links the EN/IT translations automatically.

See GUIDA.md (Italian) shipped with the package for the full guide.

== Frequently Asked Questions ==

= How do I change texts? =
Pages are made of normal blocks: edit them in Pages. Header, footer and mobile menu
are template parts (Appearance → Editor → Patterns → Template parts).

= How do I change colours and fonts? =
Appearance → Editor → Styles. The palette and font sizes come from theme.json.

= How do I enable analytics? =
Add to wp-config.php, for example: define( 'METEORA_GA4_ID', 'G-XXXXXXX' );
Tags only load after the visitor accepts analytics cookies (Consent Mode v2).

== Changelog ==

= 1.0.0 =
* Initial release: conversion of the Meteora Events site into a block theme.

== Copyright ==

Meteora WordPress Theme, Copyright 2026 Meteora Events.
Meteora is distributed under the terms of the GNU GPL v2 or later.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

== Resources ==

* Cormorant Garamond — Copyright 2015 The Cormorant Project Authors.
  License: SIL Open Font License 1.1 (assets/fonts/OFL-cormorant-garamond.txt).
  Source: https://github.com/CatharsisFonts/Cormorant
* Jost — Copyright 2020 The Jost Project Authors.
  License: SIL Open Font License 1.1 (assets/fonts/OFL-jost.txt).
  Source: https://github.com/indestructible-type/Jost
* Photographs and logos in assets/images/ — Copyright Meteora Events, all rights
  reserved. They are not covered by the GPL and may only be used on meteoraevents.com.
* screenshot.png — Copyright Meteora Events (theme screenshot of the home page).
