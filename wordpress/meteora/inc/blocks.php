<?php
/**
 * Theme blocks (PHP-only, auto-registered in the editor) and core block tweaks.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register the language switcher block. It renders Polylang or WPML languages
 * and outputs nothing when no multilingual plugin is active.
 */
function meteora_register_blocks(): void {
	register_block_type(
		'meteora/language-switcher',
		array(
			'api_version'     => 3,
			'title'           => __( 'Language switcher (IT / EN)', 'meteora' ),
			'category'        => 'theme',
			'icon'            => 'translation',
			'description'     => __( 'Compact IT / EN switcher. Requires Polylang or WPML.', 'meteora' ),
			'supports'        => array(
				'autoRegister' => true,
				'html'         => false,
				'color'        => array( 'text' => true ),
			),
			'render_callback' => 'meteora_render_language_switcher',
		)
	);
}
add_action( 'init', 'meteora_register_blocks' );

/**
 * Collect languages from Polylang or WPML.
 *
 * @return array<int,array{slug:string,name:string,url:string,current:bool,locale:string}>
 */
function meteora_get_languages(): array {
	$out = array();
	if ( function_exists( 'pll_the_languages' ) ) {
		$langs = pll_the_languages(
			array(
				'raw'           => 1,
				'hide_if_empty' => 0,
			)
		);
		foreach ( (array) $langs as $lang ) {
			$out[] = array(
				'slug'    => (string) $lang['slug'],
				'name'    => (string) $lang['name'],
				'url'     => (string) $lang['url'],
				'current' => ! empty( $lang['current_lang'] ),
				'locale'  => (string) ( $lang['locale'] ?? $lang['slug'] ),
			);
		}
		return $out;
	}
	$wpml = apply_filters( 'wpml_active_languages', null, array( 'skip_missing' => 0 ) );
	if ( is_array( $wpml ) ) {
		foreach ( $wpml as $lang ) {
			$out[] = array(
				'slug'    => (string) $lang['code'],
				'name'    => (string) $lang['native_name'],
				'url'     => (string) $lang['url'],
				'current' => ! empty( $lang['active'] ),
				'locale'  => (string) ( $lang['default_locale'] ?? $lang['code'] ),
			);
		}
	}
	return $out;
}

/**
 * Render callback for meteora/language-switcher.
 *
 * @param array<string,mixed> $attributes Block attributes.
 */
function meteora_render_language_switcher( array $attributes = array() ): string {
	$langs = meteora_get_languages();
	if ( ! $langs ) {
		// Helpful placeholder in the editor only (server-side render runs in a REST request).
		if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
			return '<p class="meteora-lang-placeholder">' . esc_html__( 'IT / EN — activate Polylang or WPML', 'meteora' ) . '</p>';
		}
		return '';
	}
	$items = '';
	foreach ( $langs as $lang ) {
		$label = esc_html( strtoupper( $lang['slug'] ) );
		$sr    = '<span class="screen-reader-text"> — ' . esc_html( $lang['name'] ) . '</span>';
		if ( $lang['current'] ) {
			$items .= sprintf( '<li><span aria-current="true" lang="%1$s">%2$s%3$s</span></li>', esc_attr( $lang['slug'] ), $label, $sr );
		} else {
			$items .= sprintf(
				'<li><a href="%1$s" hreflang="%2$s" lang="%2$s" data-track="language_switch" data-track-label="%2$s">%3$s%4$s</a></li>',
				esc_url( $lang['url'] ),
				esc_attr( $lang['slug'] ),
				$label,
				$sr
			);
		}
	}
	$wrapper = get_block_wrapper_attributes(
		array(
			'class'      => 'meteora-lang',
			'aria-label' => esc_attr__( 'Language', 'meteora' ),
		)
	);
	return sprintf( '<ul %1$s>%2$s</ul>', $wrapper, $items );
}

/**
 * When no custom logo is set, the Site Logo block falls back to the logo bundled with the theme.
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_site_logo_fallback( string $content, array $block ): string {
	if ( '' !== trim( $content ) || has_custom_logo() ) {
		return $content;
	}
	$width = isset( $block['attrs']['width'] ) ? (int) $block['attrs']['width'] : 140;
	$class = isset( $block['attrs']['className'] ) ? ' ' . $block['attrs']['className'] : '';
	return sprintf(
		'<div class="wp-block-site-logo%1$s"><a href="%2$s" class="custom-logo-link" rel="home"><img src="%3$s" width="%4$d" height="%5$d" alt="%6$s" class="custom-logo" decoding="async"></a></div>',
		esc_attr( $class ),
		esc_url( function_exists( 'pll_home_url' ) ? pll_home_url() : home_url( '/' ) ),
		esc_url( meteora_asset( 'assets/images/brand/logo-gold.webp' ) ),
		$width,
		(int) round( $width * 249 / 572 ),
		esc_attr( get_bloginfo( 'name' ) )
	);
}
add_filter( 'render_block_core/site-logo', 'meteora_site_logo_fallback', 10, 2 );
