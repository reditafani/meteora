# Meteora Events — website

**Luxury Open Bar Catering & Hospitality Services** · meteoraevents.com

A static, bilingual (Italian default + English) website built with Astro. It is designed to run on **Keliweb KeliPRO** (cPanel, Apache, PHP) with no Node.js server: you build on your computer, then upload the `dist/` folder.

- Architecture, sitemap, design system, SEO: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Public prices are **never** shown. Every page leads to **Request a quote**, and planners and venues get a separate **Request partner pricing** form.

---

## Contents

1. [Install](#1-install)
2. [Run locally](#2-run-locally)
3. [Build](#3-build)
4. [Deploy to Keliweb KeliPRO (cPanel)](#4-deploy-to-keliweb-kelipro-cpanel)
5. [Contact form (PHP / SMTP)](#5-contact-form-php--smtp)
6. [Domain, HTTPS, www / non-www, redirects](#6-domain-https-www--non-www-redirects)
7. [Editing text](#7-editing-text)
8. [Images](#8-images)
9. [Videos](#9-videos)
10. [Adding cocktails](#10-adding-cocktails)
11. [Adding bars](#11-adding-bars)
12. [Adding events (portfolio)](#12-adding-events-portfolio)
13. [Adding destinations](#13-adding-destinations)
14. [Testimonials](#14-testimonials)
15. [WhatsApp, email, Instagram](#15-whatsapp-email-instagram)
16. [Analytics, cookie consent, conversion tracking](#16-analytics-cookie-consent-conversion-tracking)
17. [Environment variables](#17-environment-variables)
18. [Before go-live checklist](#18-before-go-live-checklist)

---

## 1. Install

Requirements: **Node.js 20.3+** (22 LTS recommended) and npm.

```bash
npm install
cp .env.example .env      # then edit values if needed
```

## 2. Run locally

```bash
npm run dev               # http://localhost:4321
```

The PHP form endpoint does not run under `astro dev`. To test forms locally, run `npm run build`, then `php -S localhost:8080 -t dist`, and open http://localhost:8080.

## 3. Build

```bash
npm run build             # type-check + build into dist/
npm run build:fast        # build without type-check
npm run preview           # preview dist/ (no PHP)
npm run package           # build + create meteora-events-dist.zip for cPanel
```

The first build takes about a minute because every photograph is converted to AVIF/WebP/JPEG at several sizes. Later builds reuse the cache.

## 4. Deploy to Keliweb KeliPRO (cPanel)

No SSH is required.

1. **Build locally:** `npm run package`. This creates `meteora-events-dist.zip` with the contents of `dist/`, including the hidden `.htaccess` files.
2. **Log in to cPanel** (from the Keliweb client area) and open **File Manager → `public_html`**.
3. **Back up** the current site: select everything, then *Compress* and download.
4. Delete the old site files. Do **not** delete `api/config.php` if it already exists.
5. **Upload** `meteora-events-dist.zip` into `public_html`, right-click it and choose **Extract**, then delete the zip.
   - In File Manager → *Settings*, tick **Show Hidden Files** and check that `public_html/.htaccess` and `public_html/api/.htaccess` are there.
   - On Windows, `Compress-Archive` may skip hidden files. If `.htaccess` is missing, upload `dist/.htaccess` and `dist/api/.htaccess` by hand.
6. **Configure the form** (once): see [§5](#5-contact-form-php--smtp).
7. Check that PHP is **8.1 or newer**: cPanel → *Select PHP Version* / *MultiPHP Manager*.
8. Open the site, submit a test quote and a test partner request, and check both inboxes.

Updating later means repeating steps 1, 4 and 5. Your `api/config.php` is never inside the zip, so it is not overwritten.

## 5. Contact form (PHP / SMTP)

Files: `public/api/send.php` (endpoint), `mailer.php` (dependency-free SMTP / `mail()` transport), `config.sample.php`.

1. In cPanel → **Email Accounts**, create a mailbox for sending, e.g. `noreply@meteoraevents.com`.
2. In File Manager, copy `public_html/api/config.sample.php` to **`public_html/api/config.php`** and edit:
   - `recipient`: where requests arrive (default `info@meteoraevents.com`).
   - `partner_recipient`: optional separate inbox for partner pricing requests.
   - `from_email` / `smtp_user` / `smtp_pass`: the mailbox from step 1.
   - `smtp_host`: usually `mail.meteoraevents.com`. Check cPanel → Email Accounts → *Connect Devices*.
   - `smtp_port` / `smtp_secure`: `465` + `ssl` (default) or `587` + `tls`.
   - `transport`: keep `smtp` (better deliverability). `mail` uses PHP `mail()`.
   - `send_autoreply`: sends a short, generic confirmation to the person who wrote.
   - `allowed_hosts`: add `www.meteoraevents.com` if you use www.
3. In cPanel → **Email Deliverability**, make sure SPF and DKIM are valid for the domain.

Built-in protections: honeypot field, minimum fill time, per-IP rate limit (5 per 10 minutes), origin check, header-injection-safe output, and server-side validation that mirrors the client-side validation. With JavaScript the confirmation appears inline. Without JavaScript, the visitor is redirected to `/grazie/` or `/en/thank-you/`.

Conversion events `quote_request` and `partner_pricing_request` fire only after the server confirms the email was sent.

## 6. Domain, HTTPS, www / non-www, redirects

- **SSL:** cPanel → **SSL/TLS Status** → *Run AutoSSL* (free Let's Encrypt / Sectigo certificate on Keliweb). Include both `meteoraevents.com` and `www.meteoraevents.com`.
- **HTTPS** is forced by `public/.htaccess`.
- **Canonical host:** the site uses **non-www** (`https://meteoraevents.com`) and `.htaccess` redirects `www` to it. To use **www** instead:
  1. Set `PUBLIC_SITE_URL=https://www.meteoraevents.com` in `.env` and rebuild.
  2. In `public/.htaccess`, replace the www → non-www block with:
     ```apache
     RewriteCond %{HTTP_HOST} !^www\. [NC]
     RewriteRule ^ https://www.%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
     ```
- **Old URLs:** add 301 redirects in `public/.htaccess` (section 4) for any URLs indexed from the previous site, e.g. `RewriteRule ^contact/?$ /contatti/ [L,R=301]`.
- **DNS:** if the domain is registered elsewhere, point the A record (or nameservers) to the Keliweb server shown in your hosting welcome email.
- After launch, submit `https://meteoraevents.com/sitemap.xml` in **Google Search Console** and **Bing Webmaster Tools**.

## 7. Editing text

| What | Where |
|---|---|
| Page copy (headlines, paragraphs) | top and body of `src/views/<Page>View.astro`. Each sentence appears as an Italian/English pair: `it ? 'Italiano' : 'English'` |
| SEO titles and meta descriptions | the `meta` object at the top of each view |
| Buttons, form labels, cookie banner, menu | `src/i18n/ui.ts` |
| URLs (IT/EN slugs) | `src/i18n/routes.ts` |
| Company facts (email, phone, Instagram, address, years) | `src/data/site.ts` |
| Services, Essential vs Premium, towers | `src/data/services.ts` |
| Ice, glassware, personalisation, differentiators | `src/data/craft.ts` |
| FAQ | `src/data/faq.ts` |
| Legal company details (footer, privacy) | `site.legal` in `src/data/site.ts` |

After any edit: `npm run build`, then upload.

## 8. Images

Photographs live in **`src/assets/images/`**, not in `public/`, so the build can optimise them into responsive AVIF/WebP/JPEG with width/height and lazy loading. See `src/assets/images/README.md` for the folder map.

- **Replace an image:** overwrite the file with the same name. No code change is needed.
- **Recommended source files:** JPG, sRGB, longest side 2400–3000 px, unedited by social apps.
- **Current images** were cropped from the PDF brochure. Replace them with the photographer's originals. Some brochure shots (studio cocktail photos, bartender close-ups) may be stock: check the rights.
- **Logo:** `src/assets/images/brand/` holds PNGs extracted from the brochure. Replace them with the original vector logo when available.
- **Social image:** `public/images/og/meteora-events.jpg` (1200 × 630).
- **Alt text** lives next to each image in the data file or view. Always describe what the photo shows.

## 9. Videos

Put compressed files in **`public/videos/`**.

- **Hero video:** in `src/views/HomeView.astro`, add a `video` prop to `<Hero>`:
  ```astro
  <Hero image={hero} video={{ mp4: '/videos/hero-1080.mp4', webm: '/videos/hero-1080.webm' }} … >
  ```
  The poster image always shows first. Video plays only on screens of 768 px and up, never with *reduced motion* or *Save-Data*, and is fetched only after the page has loaded.
- **Event stories:** set `video: { mp4: '/videos/events/slug.mp4', poster: someImport }` on an event in `src/data/events.ts`.
- **Encoding:** 1080p (or 1280 px wide for the hero), H.264 MP4 at about 4–6 Mbps plus WebM (VP9/AV1), 10–20 s loop, **no audio track**, ideally under 8 MB. For example: `ffmpeg -i in.mov -vf scale=1920:-2 -an -c:v libx264 -crf 24 -preset slow -movflags +faststart hero-1080.mp4`.

## 10. Adding cocktails

1. Add a photo `src/assets/images/cocktails/<slug>.jpg` (4:3, drink centred on a neutral background).
2. Add an entry in `src/data/cocktails.ts`:
   ```ts
   { slug: 'paper-plane', name: 'Paper Plane', categories: ['sour'], profile: P('Agrumato, amaricante', 'Citrusy, bittersweet'), alcohol: 3 },
   ```
   - `categories`: any of `classics`, `signature`, `spritz`, `martini`, `sour`, `tropical`, `aperitivo`.
   - Optional: `variants`, and `featured: true` to show it in the homepage selection.
   - The image is matched to the slug automatically. Recipes are intentionally not published.

## 11. Adding bars

1. Add photos to `src/assets/images/bars/`.
2. In `src/data/bars.ts`, import them and add an entry (or update one of the "coming soon" bars). Set `status: 'available'` and add `images`. A detail page `/banchi-bar/<slug>/` and `/en/bars/<slug>/` is created automatically, and the bar appears in every Bar Collection.
3. Green Harmony, Country Classic and Black Essence are currently **coming soon**, without photos. The brochure's "Summer 2026" date has passed, so no date is shown. Add photos and set `status: 'available'` when ready.

## 12. Adding events (portfolio)

Edit `src/data/events.ts`. Each event supports: localised `slug`, `title`, `type`, `location`, `guests` (only if approved), `bar`, `experience`, `excerpt`, `story` paragraphs, `cover`, `gallery`, `video`, `relatedService`, and `draft`.

> **Important:** the five current entries were built only from the brochure photographs. They describe what the photos show and do not name venues, clients, dates or guest counts. They are marked `draft: true`, which keeps them visible on the site but `noindex` and out of the sitemap. Replace them with real event stories (with the clients' approval for any names) and set `draft: false`.

## 13. Adding destinations

`src/data/destinations.ts`:

- Every destination appears on the Destination Weddings page.
- A dedicated landing page is generated **only** for destinations with a `landing` block. Tuscany has one: `/bar-catering-matrimoni-toscana/` and `/en/wedding-bar-catering-tuscany/`.
- Add a `landing` (localised slug, title, description, H1, intro, sections) only when you have genuine local content, such as real events, venues you have worked at, or photos. This avoids thin duplicate pages, which hurt SEO.
- Never imply local offices. Meteora is based in Montecatini Terme and travels.

Suggested future slugs: `wedding-bar-catering-florence`, `wedding-bar-catering-chianti`, `wedding-bar-catering-siena`, `wedding-bar-catering-lucca`, `wedding-bar-catering-forte-dei-marmi`, `destination-wedding-bar-catering-italy` (with Italian equivalents such as `bar-catering-matrimoni-firenze`).

## 14. Testimonials

`src/data/testimonials.ts` is intentionally empty, and the section renders nothing until you add entries. Add **only authentic** reviews, with permission. No review or rating schema is generated.

## 15. WhatsApp, email, Instagram

- **WhatsApp number:** `PUBLIC_WHATSAPP_NUMBER` in `.env`, as digits only with the country code (default `393280642479`, from the brochure).
- **Pre-filled message:** `whatsappMessage` in `src/i18n/ui.ts`, per language. Visitors can edit it in the WhatsApp panel before sending.
- **Email / phone / Instagram:** `src/data/site.ts`.
- **Instagram:** the site uses a lightweight strip of selected images that link to the profile, with no embedded feed, third-party script or tracking. Change the images in `src/components/InstagramStrip.astro`.

## 16. Analytics, cookie consent, conversion tracking

No tracking is active by default. To enable it, set the IDs in `.env` and rebuild:

```
PUBLIC_GA4_ID=G-XXXXXXX        # Google Analytics 4 (direct)
PUBLIC_GTM_ID=GTM-XXXXXXX      # or Google Tag Manager (if set, GA4 should be configured inside GTM)
PUBLIC_META_PIXEL_ID=          # optional; adds a "Marketing" category to the banner
```

- The cookie banner (necessary / analytics / marketing) blocks every non-essential script until the visitor consents. Google **Consent Mode v2** defaults to `denied`. Consent is stored for 6 months, and visitors can reopen it from the footer ("Cookie preferences").
- **Events** are pushed to `dataLayer` (and to GA4 / Meta when loaded and consented):

| Event | When |
|---|---|
| `quote_request` | quote form sent successfully (Meta: `Lead`) |
| `partner_pricing_request` | partner form sent successfully (Meta: `Lead`) |
| `whatsapp_click` | any WhatsApp link (Meta: `Contact`) |
| `email_click` | any `mailto:` link |
| `phone_click` | any `tel:` link |
| `instagram_click` | any Instagram link |
| `language_switch` | IT/EN switch |
| `portfolio_interaction` | opening an event story |
| `cta_click` | quote/CTA buttons (`label` says which one) |

In GA4, mark `quote_request` and `partner_pricing_request` as **key events**. With GTM, create Custom Event triggers with the same names.

- Update `src/views/LegalView.astro` with your final Privacy and Cookie Policy texts. They are currently drafts marked `noindex`. Once final, remove `noindex` there and the legal routes from `EXCLUDE` in `src/pages/sitemap.xml.ts` if you want them indexed.

## 17. Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `PUBLIC_SITE_URL` | `https://meteoraevents.com` | canonical origin for canonicals, hreflang, sitemap, OG |
| `PUBLIC_WHATSAPP_NUMBER` | `393280642479` | WhatsApp links |
| `PUBLIC_FORM_ENDPOINT` | `/api/send.php` | form action |
| `PUBLIC_GA4_ID` / `PUBLIC_GTM_ID` / `PUBLIC_META_PIXEL_ID` | empty | analytics, consent-gated |

These values are baked in at **build time**, so rebuild after changing them. SMTP credentials are **not** environment variables. They live only on the server in `public_html/api/config.php`.

## 18. Before go-live checklist

- [ ] Replace brochure crops with original photography; confirm rights on any stock image.
- [ ] Replace the logo PNGs with the vector logo.
- [ ] Final Privacy / Cookie Policy text and legal company details (`site.legal`).
- [ ] Real portfolio stories (`draft: false`), approved testimonials (optional).
- [ ] `api/config.php` created and a test submission received for both forms.
- [ ] AutoSSL active; `www` → non-www redirect verified.
- [ ] 301 redirects from old URLs added.
- [ ] Analytics IDs set (optional), consent banner tested.
- [ ] Sitemap submitted to Search Console; Google Business Profile updated with the same name, phone and Montecatini Terme location.
