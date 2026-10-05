<?php
/**
 * Theme setup.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register theme supports and translations.
 */
function meteora_setup(): void {
	load_theme_textdomain( 'meteora', METEORA_DIR . '/languages' );

	add_theme_support( 'editor-styles' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 249,
			'width'       => 572,
			'flex-height' => true,
			'flex-width'  => true,
		)
	);

	add_editor_style( array( 'assets/css/base.css', 'assets/css/sections.css' ) );

	// Editorial image size for full-bleed photography (originals are up to ~3000px).
	add_image_size( 'meteora-wide', 2000, 0, false );
}
add_action( 'after_setup_theme', 'meteora_setup' );

/**
 * Remove core's default block patterns: the theme ships its own.
 */
function meteora_remove_core_patterns(): void {
	remove_theme_support( 'core-block-patterns' );
}
add_action( 'after_setup_theme', 'meteora_remove_core_patterns', 11 );

/**
 * Allow WebP/AVIF uploads to be preferred for generated sizes when the server supports them.
 *
 * @param array<string,string> $formats Output format map.
 * @return array<string,string>
 */
function meteora_image_output_format( array $formats ): array {
	if ( wp_image_editor_supports( array( 'mime_type' => 'image/webp' ) ) ) {
		$formats['image/jpeg'] = 'image/webp';
		$formats['image/png']  = 'image/webp';
	}
	return $formats;
}
add_filter( 'image_editor_output_format', 'meteora_image_output_format' );

/**
 * Body class used by CSS when the header overlays a cinematic hero.
 *
 * @param string[] $classes Body classes.
 * @return string[]
 */
function meteora_body_class( array $classes ): array {
	if ( is_front_page() || is_page_template( 'page-landing' ) ) {
		$classes[] = 'has-overlay-header';
	}
	return $classes;
}
add_filter( 'body_class', 'meteora_body_class' );

/**
 * The site uses no emoji: skip WordPress's emoji detection script and styles (≈ 22 KB).
 */
function meteora_disable_emoji(): void {
	remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
	remove_action( 'wp_print_styles', 'print_emoji_styles' );
	remove_action( 'wp_enqueue_scripts', 'wp_enqueue_emoji_styles' );
	add_filter( 'emoji_svg_url', '__return_false' );
}
add_action( 'init', 'meteora_disable_emoji' );
