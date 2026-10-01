/**
 * Consent-aware analytics & conversion tracking.
 *
 * - Nothing non-essential loads until the visitor opts in (GDPR / Garante Privacy).
 * - Google Consent Mode v2 defaults are set to "denied" before any tag loads.
 * - GA4, GTM and Meta Pixel are only injected if their IDs are configured (.env)
 *   AND the matching consent category is granted.
 * - Events are pushed to dataLayer; GA4/GTM pick them up once loaded.
 *
 * Event names: quote_request, partner_pricing_request, whatsapp_click,
 * email_click, phone_click, instagram_click, language_switch,
 * portfolio_interaction, cta_click.
 */
export type ConsentState = { necessary: true; analytics: boolean; marketing: boolean; ts: number; v: 1 };

const KEY = 'meteora_consent';

export function readConsent(): ConsentState | null {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as ConsentState;
    // Re-ask after 6 months, as recommended by the Italian DPA.
    if (Date.now() - parsed.ts > 1000 * 60 * 60 * 24 * 182) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function saveConsent(analytics: boolean, marketing: boolean): ConsentState {
  const state: ConsentState = { necessary: true, analytics, marketing, ts: Date.now(), v: 1 };
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    /* storage unavailable: consent applies to this page view only */
  }
  applyConsent(state);
  return state;
}

interface Ids {
  ga4: string;
  gtm: string;
  metaPixel: string;
}
let ids: Ids = { ga4: '', gtm: '', metaPixel: '' };
const loaded = { ga4: false, gtm: false, pixel: false };

function gtag(...args: unknown[]) {
  window.dataLayer = window.dataLayer || [];
  // eslint-disable-next-line prefer-rest-params
  window.dataLayer.push(arguments);
  void args;
}

function inject(src: string) {
  const s = document.createElement('script');
  s.async = true;
  s.src = src;
  document.head.appendChild(s);
}

export function initAnalytics(config: Ids) {
  ids = config;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || gtag;
  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    wait_for_update: 500,
  });
  const state = readConsent();
  if (state) applyConsent(state);
  window.meteoraTrack = track;
  bindDelegatedTracking();
}

function applyConsent(state: ConsentState) {
  window.gtag?.('consent', 'update', {
    analytics_storage: state.analytics ? 'granted' : 'denied',
    ad_storage: state.marketing ? 'granted' : 'denied',
    ad_user_data: state.marketing ? 'granted' : 'denied',
    ad_personalization: state.marketing ? 'granted' : 'denied',
  });

  if (state.analytics || state.marketing) {
    if (ids.gtm && !loaded.gtm) {
      loaded.gtm = true;
      window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
      inject(`https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(ids.gtm)}`);
    }
  }
  if (state.analytics && ids.ga4 && !loaded.ga4 && !ids.gtm) {
    loaded.ga4 = true;
    inject(`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(ids.ga4)}`);
    window.gtag?.('js', new Date());
    window.gtag?.('config', ids.ga4, { anonymize_ip: true });
  }
  if (state.marketing && ids.metaPixel && !loaded.pixel) {
    loaded.pixel = true;
    /* Meta Pixel base code (loaded only after marketing consent). */
    const f = window as unknown as Record<string, unknown>;
    const n = function (...args: unknown[]) {
      const self = n as unknown as { callMethod?: (...a: unknown[]) => void; queue: unknown[] };
      self.callMethod ? self.callMethod(...args) : self.queue.push(args);
    } as unknown as { queue: unknown[]; loaded: boolean; version: string; push: unknown };
    n.queue = [];
    n.loaded = true;
    n.version = '2.0';
    n.push = n;
    f.fbq = n;
    f._fbq = n;
    inject('https://connect.facebook.net/en_US/fbevents.js');
    window.fbq?.('init', ids.metaPixel);
    window.fbq?.('track', 'PageView');
  }
}

export function track(event: string, params: Record<string, unknown> = {}) {
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...params });
  if (loaded.ga4) window.gtag?.('event', event, params);
  if (loaded.pixel) {
    if (event === 'quote_request' || event === 'partner_pricing_request') window.fbq?.('track', 'Lead', { content_name: event });
    if (event === 'whatsapp_click' || event === 'phone_click' || event === 'email_click') window.fbq?.('track', 'Contact');
  }
}

function bindDelegatedTracking() {
  document.addEventListener(
    'click',
    (e) => {
      const target = (e.target as HTMLElement | null)?.closest<HTMLElement>('a, button');
      if (!target) return;
      let name = target.dataset.track;
      const href = target.getAttribute('href') || '';
      if (!name) {
        if (href.startsWith('mailto:')) name = 'email_click';
        else if (href.startsWith('tel:')) name = 'phone_click';
        else if (href.includes('wa.me/')) name = 'whatsapp_click';
        else if (href.includes('instagram.com')) name = 'instagram_click';
      }
      if (!name) return;
      track(name, {
        label: target.dataset.trackLabel || target.textContent?.trim().slice(0, 60),
        page_path: location.pathname,
        link_url: href || undefined,
      });
    },
    { capture: true },
  );
}
