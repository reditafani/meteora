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
 * Map of class name → script handle. A script is enqueued only when a rendered
 * block carries one of its classes (so pages without that section load no extra JS).
 *
 * @return array<string,string>
 */
function meteora_conditional_scripts(): array {
	return array(
		'animate-fade-up'      => 'reveal',
		'animate-image-reveal' => 'reveal',
		'mt-bc'                => 'bar-collection',
		'mt-cf'                => 'cocktail-families',
		'mt-cg'                => 'cocktail-gallery',
	);
}

/**
 * Enqueue section scripts on demand while blocks render.
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_enqueue_on_render( string $content, array $block ): string {
	if ( empty( $block['attrs']['className'] ) || ! is_string( $block['attrs']['className'] ) ) {
		return $content;
	}
	$classes = preg_split( '/\s+/', $block['attrs']['className'] );
	foreach ( meteora_conditional_scripts() as $class => $handle ) {
		if ( in_array( $class, $classes, true ) && ! wp_script_is( 'meteora-' . $handle, 'enqueued' ) ) {
			wp_enqueue_script(
				'meteora-' . $handle,
				meteora_asset( 'assets/js/' . $handle . '.js' ),
				array(),
				METEORA_VERSION,
				array(
					'strategy'  => 'defer',
					'in_footer' => true,
				)
			);
		}
	}
	return $content;
}
add_filter( 'render_block', 'meteora_enqueue_on_render', 10, 2 );

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
