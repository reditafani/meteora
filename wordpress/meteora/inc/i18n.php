<?php
/**
 * Multilingual integration (Polylang / WPML). The theme works without them.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register theme strings that editors may want to translate from the
 * Polylang "Strings translations" screen (in addition to the theme .po files).
 */
function meteora_register_pll_strings(): void {
	if ( ! function_exists( 'pll_register_string' ) ) {
		return;
	}
	pll_register_string( 'meteora_tagline', 'Luxury Open Bar Catering & Hospitality Services', 'Meteora' );
}
add_action( 'init', 'meteora_register_pll_strings' );
