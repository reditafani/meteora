<?php
/**
 * Instagram strip: latest posts of @meteoraevents through the
 * "Smash Balloon Social Photo Feed" plugin (slug: instagram-feed).
 *
 * The section keeps its six curated images as a fallback: they are replaced by
 * the live feed only when the plugin is active and returns posts, so the strip
 * is never empty (plugin missing, account not connected, Instagram down).
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Rendered live feed, or an empty string when there is nothing to show.
 * Computed once per request (the strip can appear once per page).
 */
function meteora_instagram_feed_html(): string {
	static $html = null;
	if ( null !== $html ) {
		return $html;
	}
	$html = '';
	if ( ! shortcode_exists( 'instagram-feed' ) ) {
		return $html;
	}
	/**
	 * Shortcode that renders the feed. Smash Balloon numbers feeds in the order
	 * they are created: change it if the Meteora feed is not the first one.
	 *
	 * @param string $shortcode Default `[instagram-feed feed=1]`.
	 */
	$shortcode = (string) apply_filters( 'meteora_instagram_shortcode', '[instagram-feed feed=1]' );
	$output    = do_shortcode( $shortcode );
	if ( false !== strpos( $output, 'sbi_item' ) ) {
		$html = $output;
	}
	return $html;
}

/**
 * Swap the curated tiles of the strip for the live feed when available.
 *
 * @param string              $content Rendered block.
 * @param array<string,mixed> $block   Parsed block.
 */
function meteora_instagram_strip( string $content, array $block ): string {
	$class = isset( $block['attrs']['className'] ) ? (string) $block['attrs']['className'] : '';
	if ( ! preg_match( '/(^|\s)mt-ig__grid(\s|$)/', $class ) || is_admin() || wp_is_json_request() ) {
		return $content;
	}
	$feed = meteora_instagram_feed_html();
	if ( '' === $feed ) {
		return $content;
	}
	return '<div class="mt-ig__feed">' . $feed . '</div>';
}
add_filter( 'render_block_core/group', 'meteora_instagram_strip', 10, 2 );
