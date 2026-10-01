// @ts-check
import { defineConfig } from 'astro/config';

// Canonical origin. Change PUBLIC_SITE_URL in .env if the canonical host changes
// (e.g. to https://www.meteoraevents.com) — every canonical, hreflang and sitemap URL follows it.
const SITE = process.env.PUBLIC_SITE_URL || 'https://meteoraevents.com';

export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'always',
  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
    assets: '_assets',
  },
  compressHTML: true,
  prefetch: { prefetchAll: false, defaultStrategy: 'hover' },
  image: {
    // Real event photography is processed at build time into AVIF/WebP srcsets.
    responsiveStyles: false,
  },
  devToolbar: { enabled: false },
});
