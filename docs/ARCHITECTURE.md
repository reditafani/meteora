# Meteora Events — Project architecture

## 1. Project architecture

| Layer | Choice | Why |
|---|---|---|
| Framework | **Astro 7, static output** | Pure HTML/CSS at build time, near-zero JS, deploys as plain files on Keliweb KeliPRO (no Node server). |
| Language | TypeScript (strict) | Typed content data and components. |
| Styling | Design tokens (CSS custom properties) + component-scoped CSS | No CSS framework dependency, no unused CSS, easy to theme. |
| Images | `astro:assets` + sharp | AVIF/WebP/JPEG srcsets, intrinsic sizes (no CLS), lazy loading. |
| Fonts | Self-hosted via Fontsource (Cormorant Garamond + Jost) | No Google Fonts request → better GDPR posture and performance. |
| Motion | CSS transitions, IntersectionObserver, CSS scroll-driven animations, cross-document View Transitions | No GSAP/Framer: ~2 KB of JS in total. Fully disabled under `prefers-reduced-motion`. |
| Forms | PHP 8 endpoint (`public/api/send.php`) + dependency-free SMTP client | Runs on any cPanel host. No SaaS, no Composer. |
| Analytics | Consent-gated loader (GA4 / GTM / Meta Pixel), Consent Mode v2 | Nothing non-essential loads before consent. |

```
├── astro.config.mjs        site URL, static output, trailing slashes
├── public/                 copied as-is into dist/
│   ├── .htaccess           HTTPS, canonical host, caching, security headers
│   ├── api/                send.php · mailer.php · config.sample.php · .htaccess
│   ├── images/og/          social sharing image
│   ├── videos/             compressed MP4/WebM (hero & stories)
│   └── favicon / icons / site.webmanifest
├── src/
│   ├── assets/images/      photography processed at build time
│   ├── components/         reusable UI + sections
│   ├── data/               CONTENT: bars, cocktails, events, destinations, services, craft, faq, testimonials, site
│   ├── i18n/               routes.ts (IT/EN URL map) · ui.ts (interface strings)
│   ├── layouts/            BaseLayout (SEO head, header, footer, consent, WhatsApp)
│   ├── lib/seo.ts          structured data builders
│   ├── pages/              thin route files (IT at root, EN under /en/), sitemap.xml, robots.txt
│   ├── scripts/            analytics, forms, reveal
│   ├── styles/             tokens.css · global.css · forms.css
│   └── views/              one view per page, shared by both languages (page copy lives here)
└── scripts/package-dist.mjs   zips dist/ for cPanel upload
```

## 2. Sitemap

| Page | Italian (default) | English |
|---|---|---|
| Home | `/` | `/en/` |
| Weddings | `/matrimoni/` | `/en/weddings/` |
| Destination Weddings | `/destination-wedding-italia/` | `/en/destination-weddings-italy/` |
| Bars | `/banchi-bar/` + `/banchi-bar/{slug}/` | `/en/bars/` + `/en/bars/{slug}/` |
| Cocktail Experience | `/cocktail-experience/` | `/en/cocktail-experience/` |
| Services | `/servizi/` | `/en/services/` |
| Corporate & Private | `/eventi-aziendali-privati/` | `/en/corporate-private-events/` |
| Planners & Venues (B2B) | `/wedding-planner-location/` | `/en/wedding-planners-venues/` |
| Events / Portfolio | `/eventi/` + `/eventi/{slug}/` | `/en/events/` + `/en/events/{slug}/` |
| About | `/chi-siamo/` | `/en/about/` |
| Why Meteora | `/perche-meteora/` | `/en/why-meteora/` |
| Contact / Quote | `/contatti/` | `/en/contact/` |
| Destination landing (data-driven) | `/bar-catering-matrimoni-toscana/` | `/en/wedding-bar-catering-tuscany/` |
| Thank you (noindex) | `/grazie/` | `/en/thank-you/` |
| Privacy / Cookie (noindex until final text) | `/privacy-policy/`, `/cookie-policy/` | `/en/privacy-policy/`, `/en/cookie-policy/` |

## 3. Design system

**Palette** (sampled from the brochure): cream `#F9F2E8` (background), deeper cream `#F1E8DA` (secondary), ink `#1C1614` (text), muted `#675D53`, logo gold `#B89E72` (accent — decorative/large type only), gold ink `#7A5F37` (small accent text, AA on cream), border `#DDD0BC`, warm black `#15110E` for cinematic sections.

**Typography**: Cormorant Garamond (display, echoes the logo's classical serif; italics used for accent phrases in gold) + Jost (geometric sans, echoes the brochure's spaced capitals). Micro labels are small uppercase with 0.24em tracking. Fluid `clamp()` scale: display → h1 → h2 → h3 → lead → body → micro.

**Principles**: square corners, hairline rules instead of boxes, generous negative space, asymmetric 12-column compositions, one arch motif (cocktail frame), photography dominant, CTAs as solid ink buttons or underlined text links.

**Memorable moments**: (1) cinematic hero; (2) Bar Collection index with crossfading stage; (3) cocktail families with arched crossfade frame; (4) dark "Ice is part of the cocktail" section; (5) Signature Tower cinematic composition; (6) "Not just an open bar" editorial mosaic.

## 4. Content structure

All editable content is in `src/data/*.ts` (collections) and at the top of each `src/views/*View.astro` (page copy, as `it ? '…' : '…'` pairs). Interface strings are in `src/i18n/ui.ts`. Nothing in the data invents facts beyond the brochure; placeholders are marked `TODO(client)`.

## 5. Component architecture

Header · MobileMenu · LanguageSwitcher · Logo · Hero (image + optional video) · PageHero · SectionHeading · EditorialSection · Img (responsive picture) · TrustBar · ExperienceMosaic · BarCollection · BarCard · CocktailFamilies · CocktailGallery · CocktailCard · IceSection · GlasswareSection · PersonalizationSection · TowerSection · ExperienceComparison · DestinationSection · PortfolioGrid · PortfolioStory · Testimonial · PartnerCTA · WhyGrid · LeadForm · PartnerForm · Field · FAQ · CTABand · InstagramStrip · WhatsAppButton (+ mobile CTA bar) · CookieConsent · Breadcrumbs · Footer · Icon.

## 6. SEO architecture

- Unique title/description per page and language; canonical URLs; `hreflang` it/en/x-default on every page and in the sitemap.
- Open Graph + Twitter cards (1200×630 image).
- JSON-LD: Organization + LocalBusiness (Montecatini Terme 51016, no invented street address), WebSite, BreadcrumbList, Service, FAQPage (only where FAQ is visible), ItemList (bars), Product (bar detail), ContactPage. No reviews/ratings.
- Semantic headings (one H1 per page), descriptive alt text, internal linking between weddings ↔ destination ↔ bars ↔ cocktails ↔ services ↔ contact.
- Local positioning: "Based in Tuscany, serving events throughout Italy". Destinations are content, not fake offices. Landing pages are only generated for destinations with real content (`landing` in `src/data/destinations.ts`).
- Draft portfolio entries are `noindex` and excluded from the sitemap until real event details are added.
