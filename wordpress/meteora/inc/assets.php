<?php
/**
 * Styles and scripts. Global CSS is small; section CSS and scripts load only
 * when a block on the page uses them (see meteora_conditional_assets()).
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Global front-end assets.
 */
function meteora_enqueue_assets(): void {
	wp_enqueue_style( 'meteora-base', meteora_asset( 'assets/css/base.css' ), array(), METEORA_VERSION );
	wp_enqueue_style( 'meteora-sections', meteora_asset( 'assets/css/sections.css' ), array( 'meteora-base' ), METEORA_VERSION );

	wp_enqueue_script(
		'meteora-header',
		meteora_asset( 'assets/js/header.js' ),
		array(),
		METEORA_VERSION,
		array(
			'strategy'  => 'defer',
			'in_footer' => true,
		)
	);
}
add_action( 'wp_enqueue_scripts', 'meteora_enqueue_assets' );

/**
 * Preload the two most used font files (display roman + body) for faster first paint.
 */
function meteora_preload_fonts(): void {
	$fonts = array(
		'assets/fonts/cormorant-garamond-latin-wght-normal.woff2',
		'assets/fonts/jost-latin-wght-normal.woff2',
	);
	foreach ( $fonts as $font ) {
		printf(
			'<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n",
			esc_url( meteora_asset( $font ) )
		);
	}
}
add_action( 'wp_head', 'meteora_preload_fonts', 1 );

/**
 * Flag JavaScript support before first paint so scroll animations never flash.
 */
function meteora_js_flag(): void {
	wp_print_inline_script_tag( "document.documentElement.classList.add('js');" );
}
add_action( 'wp_head', 'meteora_js_flag', 0 );
