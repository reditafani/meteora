/**
 * Meteora UI: WhatsApp panel, cookie consent, consent-aware analytics and conversion tracking.
 * Nothing non-essential loads before consent (Google Consent Mode v2 defaults to "denied").
 *
 * Events: quote_request, partner_pricing_request, whatsapp_click, email_click, phone_click,
 * instagram_click, language_switch, portfolio_interaction, cta_click.
 */
( function () {
	var cfg = window.meteoraUI || {};
	var KEY = 'meteora_consent';
	var loaded = { gtm: false, ga4: false, pixel: false };

	/* ---------------- WhatsApp ---------------- */
	var panel = document.querySelector( '[data-wa-panel]' );
	var msg = document.querySelector( '[data-wa-message]' );
	var send = document.querySelector( '[data-wa-send]' );
	var toggles = document.querySelectorAll( '[data-wa-toggle]' );
	function setOpen( open ) {
		if ( ! panel ) {
			return;
		}
		panel.hidden = ! open;
		toggles.forEach( function ( b ) {
			b.setAttribute( 'aria-expanded', String( open ) );
		} );
		if ( open && msg ) {
			msg.focus();
		}
	}
	toggles.forEach( function ( b ) {
		b.addEventListener( 'click', function () {
			setOpen( panel ? panel.hidden : false );
		} );
	} );
	var closeBtn = document.querySelector( '[data-wa-close]' );
	if ( closeBtn ) {
		closeBtn.addEventListener( 'click', function () {
			setOpen( false );
			if ( toggles[ 0 ] ) {
				toggles[ 0 ].focus();
			}
		} );
	}
	if ( panel ) {
		panel.addEventListener( 'keydown', function ( e ) {
			if ( 'Escape' === e.key ) {
				setOpen( false );
			}
		} );
	}
	if ( msg && send && cfg.wa ) {
		msg.addEventListener( 'input', function () {
			send.href = 'https://wa.me/' + cfg.wa + '?text=' + encodeURIComponent( msg.value );
		} );
	}

	/* ---------------- Consent & analytics ---------------- */
	window.dataLayer = window.dataLayer || [];
	function gtag() {
		window.dataLayer.push( arguments );
	}
	window.gtag = window.gtag || gtag;
	window.gtag( 'consent', 'default', {
		ad_storage: 'denied',
		ad_user_data: 'denied',
		ad_personalization: 'denied',
		analytics_storage: 'denied',
		wait_for_update: 500,
	} );

	function readConsent() {
		try {
			var raw = window.localStorage.getItem( KEY );
			if ( ! raw ) {
				return null;
			}
			var s = JSON.parse( raw );
			// Ask again after 6 months, as recommended by the Italian DPA.
			return Date.now() - s.ts > 1000 * 60 * 60 * 24 * 182 ? null : s;
		} catch ( e ) {
			return null;
		}
	}
	function inject( src ) {
		var s = document.createElement( 'script' );
		s.async = true;
		s.src = src;
		document.head.appendChild( s );
	}
	function applyConsent( s ) {
		window.gtag( 'consent', 'update', {
			analytics_storage: s.analytics ? 'granted' : 'denied',
			ad_storage: s.marketing ? 'granted' : 'denied',
			ad_user_data: s.marketing ? 'granted' : 'denied',
			ad_personalization: s.marketing ? 'granted' : 'denied',
		} );
		if ( ( s.analytics || s.marketing ) && cfg.gtm && ! loaded.gtm ) {
			loaded.gtm = true;
			window.dataLayer.push( { 'gtm.start': Date.now(), event: 'gtm.js' } );
			inject( 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent( cfg.gtm ) );
		}
		if ( s.analytics && cfg.ga4 && ! cfg.gtm && ! loaded.ga4 ) {
			loaded.ga4 = true;
			inject( 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent( cfg.ga4 ) );
			window.gtag( 'js', new Date() );
			window.gtag( 'config', cfg.ga4, { anonymize_ip: true } );
		}
		if ( s.marketing && cfg.pixel && ! loaded.pixel ) {
			loaded.pixel = true;
			var n = function () {
				n.callMethod ? n.callMethod.apply( n, arguments ) : n.queue.push( arguments );
			};
			n.queue = [];
			n.loaded = true;
			n.version = '2.0';
			n.push = n;
			window.fbq = window._fbq = n;
			inject( 'https://connect.facebook.net/en_US/fbevents.js' );
			window.fbq( 'init', cfg.pixel );
			window.fbq( 'track', 'PageView' );
		}
	}
	function saveConsent( analytics, marketing ) {
		var s = { necessary: true, analytics: analytics, marketing: marketing, ts: Date.now(), v: 1 };
		try {
			window.localStorage.setItem( KEY, JSON.stringify( s ) );
		} catch ( e ) {}
		applyConsent( s );
	}

	function track( event, params ) {
		params = params || {};
		var data = { event: event };
		Object.keys( params ).forEach( function ( k ) {
			data[ k ] = params[ k ];
		} );
		window.dataLayer.push( data );
		if ( loaded.ga4 ) {
			window.gtag( 'event', event, params );
		}
		if ( loaded.pixel && window.fbq ) {
			if ( 'quote_request' === event || 'partner_pricing_request' === event ) {
				window.fbq( 'track', 'Lead', { content_name: event } );
			}
			if ( 'whatsapp_click' === event || 'phone_click' === event || 'email_click' === event ) {
				window.fbq( 'track', 'Contact' );
			}
		}
	}
	window.meteoraTrack = track;

	var state = readConsent();
	if ( state ) {
		applyConsent( state );
	}

	var box = document.querySelector( '[data-cookie]' );
	if ( box && cfg.consent ) {
		var prefs = box.querySelector( '[data-cookie-prefs]' );
		var saveBtn = box.querySelector( '[data-cookie-save]' );
		var customizeBtn = box.querySelector( '[data-cookie-customize]' );
		var show = function ( withPrefs ) {
			var st = readConsent();
			var a = prefs.querySelector( '[name="analytics"]' );
			var m = prefs.querySelector( '[name="marketing"]' );
			a.checked = !! ( st && st.analytics );
			if ( m ) {
				m.checked = !! ( st && st.marketing );
			}
			prefs.hidden = ! withPrefs;
			saveBtn.hidden = ! withPrefs;
			customizeBtn.hidden = withPrefs;
			box.hidden = false;
		};
		var hide = function () {
			box.hidden = true;
		};
		if ( ! state ) {
			show( false );
		}
		box.querySelector( '[data-cookie-accept]' ).addEventListener( 'click', function () {
			saveConsent( true, true );
			hide();
		} );
		box.querySelector( '[data-cookie-reject]' ).addEventListener( 'click', function () {
			saveConsent( false, false );
			hide();
		} );
		customizeBtn.addEventListener( 'click', function () {
			show( true );
		} );
		saveBtn.addEventListener( 'click', function () {
			var m = prefs.querySelector( '[name="marketing"]' );
			saveConsent( prefs.querySelector( '[name="analytics"]' ).checked, m ? m.checked : false );
			hide();
		} );
		document.addEventListener( 'click', function ( e ) {
			var opener = e.target.closest( '.meteora-cookie-open, a[href="#cookie-preferences"]' );
			if ( opener ) {
				e.preventDefault();
				show( true );
			}
		} );
	}

	/* ---------------- Delegated conversion tracking ---------------- */
	document.addEventListener(
		'click',
		function ( e ) {
			var el = e.target.closest( 'a, button' );
			if ( ! el ) {
				return;
			}
			var name = el.dataset.track;
			var label = el.dataset.trackLabel;
			var wrapper = el.closest( '[class*="meteora-track-"]' );
			if ( ! name && wrapper ) {
				name = 'cta_click';
				label = ( wrapper.className.match( /meteora-track-([\w-]+)/ ) || [] )[ 1 ];
			}
			var href = el.getAttribute( 'href' ) || '';
			if ( ! name ) {
				if ( 0 === href.indexOf( 'mailto:' ) ) {
					name = 'email_click';
				} else if ( 0 === href.indexOf( 'tel:' ) ) {
					name = 'phone_click';
				} else if ( -1 !== href.indexOf( 'wa.me/' ) ) {
					name = 'whatsapp_click';
				} else if ( -1 !== href.indexOf( 'instagram.com' ) ) {
					name = 'instagram_click';
				} else if ( el.closest( '.mt-pg__list' ) ) {
					name = 'portfolio_interaction';
				}
			}
			if ( name ) {
				track( name, { label: label || ( el.textContent || '' ).trim().slice( 0, 60 ), page_path: location.pathname, link_url: href || undefined } );
			}
		},
		true
	);

	// Contact Form 7: fire the conversion only after the mail was actually sent.
	document.addEventListener( 'wpcf7mailsent', function ( e ) {
		var form = e.target;
		var partner = form && ( form.classList.contains( 'mt-form--partner' ) || form.closest( '.mt-form--partner' ) );
		track( partner ? 'partner_pricing_request' : 'quote_request', { page_path: location.pathname } );
	} );
}() );
