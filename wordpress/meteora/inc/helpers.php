<?php
/**
 * Helpers: contact details, page URLs resolved per language.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Company contact details (from the Meteora Events brochure).
 * Filter `meteora_contact` to change them without editing the theme.
 *
 * @return array<string,string>
 */
function meteora_contact(): array {
	return apply_filters(
		'meteora_contact',
		array(
			'email'          => 'info@meteoraevents.com',
			'phone_display'  => '+39 328 064 2479',
			'phone_e164'     => '+393280642479',
			'whatsapp'       => '393280642479',
			'instagram'      => '@meteoraevents',
			'instagram_url'  => 'https://www.instagram.com/meteoraevents/',
			'locality'       => 'Montecatini Terme',
			'postal_code'    => '51016',
			'province'       => 'PT',
			'region'         => 'Tuscany',
			'country'        => 'IT',
		)
	);
}

/**
 * Map of theme page keys to the slug of the English (default-language) page.
 * Translations are resolved through Polylang or WPML when active.
 *
 * @return array<string,string>
 */
function meteora_page_slugs(): array {
	return apply_filters(
		'meteora_page_slugs',
		array(
			'home'        => '',
			'weddings'    => 'weddings',
			'destination' => 'destination-weddings-italy',
			'bars'        => 'bars',
			'cocktails'   => 'cocktail-experience',
			'services'    => 'services',
			'corporate'   => 'corporate-private-events',
			'partners'    => 'wedding-planners-venues',
			'events'      => 'events',
			'about'       => 'about',
			'why'         => 'why-meteora',
			'contact'     => 'contact',
			'thanks'      => 'thank-you',
			'privacy'     => 'privacy-policy',
			'cookies'     => 'cookie-policy',
			'tuscany'     => 'wedding-bar-catering-tuscany',
			'bar-golden-mirror'     => 'bars/golden-mirror',
			'bar-silver-reflection' => 'bars/silver-reflection',
			'bar-pure-white'        => 'bars/pure-white',
		)
	);
}

/**
 * Current language code ('en', 'it', …) from Polylang/WPML, falling back to the site locale.
 */
function meteora_current_lang(): string {
	if ( function_exists( 'pll_current_language' ) ) {
		$lang = pll_current_language( 'slug' );
		if ( $lang ) {
			return (string) $lang;
		}
	}
	$wpml = apply_filters( 'wpml_current_language', null );
	if ( is_string( $wpml ) && '' !== $wpml ) {
		return $wpml;
	}
	return substr( get_locale(), 0, 2 );
}

/**
 * Return the translation of a post in the current language, if a multilingual plugin is active.
 *
 * @param int    $post_id   Post ID in any language.
 * @param string $post_type Post type.
 */
function meteora_translated_id( int $post_id, string $post_type = 'page' ): int {
	if ( function_exists( 'pll_get_post' ) ) {
		$translated = pll_get_post( $post_id );
		return $translated ? (int) $translated : $post_id;
	}
	$translated = apply_filters( 'wpml_object_id', $post_id, $post_type, true );
	return $translated ? (int) $translated : $post_id;
}

/**
 * Permalink of a theme page (by key) in the current language, with optional fragment.
 *
 * @param string $key  Key from meteora_page_slugs().
 * @param string $hash Optional fragment without '#'.
 */
function meteora_page_url( string $key, string $hash = '' ): string {
	static $cache = array();
	$slugs    = meteora_page_slugs();
	$fragment = '' !== $hash ? '#' . rawurlencode( $hash ) : '';

	if ( 'home' === $key || ! isset( $slugs[ $key ] ) ) {
		$home = function_exists( 'pll_home_url' ) ? pll_home_url() : home_url( '/' );
		return $home . $fragment;
	}

	$cache_key = $key . '|' . meteora_current_lang();
	if ( ! isset( $cache[ $cache_key ] ) ) {
		$page = get_page_by_path( $slugs[ $key ] );
		if ( $page instanceof WP_Post ) {
			$cache[ $cache_key ] = (string) get_permalink( meteora_translated_id( $page->ID ) );
		} else {
			// Page not imported yet: point to the expected URL so links are never empty.
			$cache[ $cache_key ] = home_url( user_trailingslashit( $slugs[ $key ] ) );
		}
	}
	return $cache[ $cache_key ] . $fragment;
}

/**
 * URL of a file bundled with the theme.
 *
 * @param string $path Relative path inside the theme, e.g. 'assets/images/bars/golden-mirror.webp'.
 */
function meteora_asset( string $path ): string {
	return get_theme_file_uri( $path );
}

/**
 * Pre-filled WhatsApp link.
 *
 * @param string $message Message text.
 */
function meteora_whatsapp_url( string $message = '' ): string {
	$contact = meteora_contact();
	$url     = 'https://wa.me/' . rawurlencode( $contact['whatsapp'] );
	return '' !== $message ? $url . '?text=' . rawurlencode( $message ) : $url;
}
