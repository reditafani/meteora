<?php
/**
 * Core block tweaks: language switcher and Site Logo fallback.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Language switcher: a Paragraph block with the class `meteora-lang-switcher`
 * (it reads "EN / IT" in the editor) is rendered as the Polylang or WPML
 * language list, and outputs nothing when no multilingual plugin is active.
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_language_switcher_block( string $content, array $block ): string {
	$class = isset( $block['attrs']['className'] ) ? (string) $block['attrs']['className'] : '';
	if ( ! preg_match( '/(^|\s)meteora-lang-switcher(\s|$)/', $class ) ) {
		return $content;
	}
	$classes = '';
	$style   = '';
	$tags    = new WP_HTML_Tag_Processor( $content );
	if ( $tags->next_tag( 'p' ) ) {
		$classes = (string) $tags->get_attribute( 'class' );
		$style   = (string) $tags->get_attribute( 'style' );
	}
	$classes = trim( preg_replace( '/(^|\s)(meteora-lang-switcher|wp-block-paragraph)(?=\s|$)/', ' ', $classes ) );
	return meteora_render_language_switcher( $classes, $style );
}
add_filter( 'render_block_core/paragraph', 'meteora_language_switcher_block', 10, 2 );

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
 * Render the language list.
 *
 * @param string $classes Extra classes (from the block).
 * @param string $style   Inline style (from the block).
 */
function meteora_render_language_switcher( string $classes = '', string $style = '' ): string {
	$langs = meteora_get_languages();
	if ( ! $langs ) {
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
	return sprintf(
		'<ul class="%1$s"%2$s aria-label="%3$s">%4$s</ul>',
		esc_attr( trim( 'meteora-lang ' . $classes ) ),
		'' !== $style ? ' style="' . esc_attr( $style ) . '"' : '',
		esc_attr__( 'Language', 'meteora' ),
		$items
	);
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

/**
 * Horizontally scrolling rails must be reachable by keyboard (WCAG 2.1.1):
 * make them focusable, labelled regions.
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_scroll_rail_a11y( string $content, array $block ): string {
	$class = isset( $block['attrs']['className'] ) ? (string) $block['attrs']['className'] : '';
	if ( ! preg_match( '/(^|\s)mt-ice__rail(\s|$)/', $class ) ) {
		return $content;
	}
	$tags = new WP_HTML_Tag_Processor( $content );
	if ( $tags->next_tag() ) {
		$tags->set_attribute( 'tabindex', '0' );
		$tags->set_attribute( 'role', 'region' );
		$tags->set_attribute( 'aria-label', __( 'Ice formats', 'meteora' ) );
		return $tags->get_updated_html();
	}
	return $content;
}
add_filter( 'render_block_core/group', 'meteora_scroll_rail_a11y', 10, 2 );

/**
 * Header menu button: the core "handle" icon draws two 1.5px filled bars on
 * half-pixel coordinates, which blur and shimmer while the header shrinks on
 * scroll. Use the thin, pixel-aligned stroked icon of the original design.
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_menu_button_icon( string $content, array $block ): string {
	$class = isset( $block['attrs']['className'] ) ? (string) $block['attrs']['className'] : '';
	if ( false === strpos( $class, 'site-header__toggle' ) ) {
		return $content;
	}
	$icon = '<svg class="meteora-menu-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M3 8h18M3 16h18"/></svg>';
	return (string) preg_replace(
		'#(<button[^>]*wp-block-navigation__responsive-container-open[^>]*>)\s*<svg\b.*?</svg>#s',
		'$1' . $icon,
		$content,
		1
	);
}
add_filter( 'render_block_core/navigation', 'meteora_menu_button_icon', 10, 2 );

/**
 * Header logo: add a light copy of the logo so the overlay header can
 * cross-fade between the two (a CSS filter transition would pass through a
 * dark grey frame while scrolling).
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_header_logo_crossfade( string $content, array $block ): string {
	$class = isset( $block['attrs']['className'] ) ? (string) $block['attrs']['className'] : '';
	if ( false === strpos( $class, 'site-header__brand' ) || ! preg_match( '#<img\b[^>]*>#', $content, $m ) ) {
		return $content;
	}
	$light = new WP_HTML_Tag_Processor( $m[0] );
	if ( ! $light->next_tag( 'img' ) ) {
		return $content;
	}
	$light->add_class( 'site-header__logo-light' );
	$light->set_attribute( 'alt', '' );
	$light->set_attribute( 'aria-hidden', 'true' );
	$light->remove_attribute( 'id' );
	$light->remove_attribute( 'fetchpriority' );
	return str_replace( $m[0], $m[0] . $light->get_updated_html(), $content );
}
add_filter( 'render_block_core/site-logo', 'meteora_header_logo_crossfade', 20, 2 );
