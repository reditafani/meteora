<?php
/**
 * After importing the Meteora content (Tools → Import → WordPress):
 * - sets the static front page and pretty permalinks;
 * - assigns languages and links translations when Polylang is active
 *   (also runs later if Polylang is installed after the import).
 *
 * Imported items carry the meta `_meteora_lang` (en|it) and `_meteora_group`
 * (ID of the English original).
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Configure reading settings and link translations.
 */
function meteora_after_import(): void {
	$home = get_page_by_path( 'home' );
	if ( $home instanceof WP_Post ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $home->ID );
	}
	if ( '' === (string) get_option( 'permalink_structure' ) ) {
		update_option( 'permalink_structure', '/%postname%/' );
	}
	meteora_claim_privacy_slug();
	meteora_sync_languages();
	flush_rewrite_rules( false );
}
add_action( 'import_end', 'meteora_after_import' );

/**
 * A fresh install ships a draft "Privacy Policy" page that takes the
 * `privacy-policy` slug, so the imported page lands on `privacy-policy-2`.
 * Trash the untouched default draft, give the imported page the clean slug
 * and register it as the site's privacy page.
 */
function meteora_claim_privacy_slug(): void {
	$imported = get_posts(
		array(
			'post_type'      => 'page',
			'post_status'    => 'any',
			'name'           => 'privacy-policy-2',
			'posts_per_page' => 1,
			'meta_key'       => '_meteora_lang', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
			'lang'           => '',
		)
	);
	if ( empty( $imported ) ) {
		return;
	}
	$default = get_posts(
		array(
			'post_type'      => 'page',
			'post_status'    => array( 'draft', 'publish', 'private' ),
			'name'           => 'privacy-policy',
			'posts_per_page' => 1,
			'lang'           => '',
		)
	);
	if ( ! empty( $default ) ) {
		if ( metadata_exists( 'post', $default[0]->ID, '_meteora_lang' ) || 'draft' !== $default[0]->post_status ) {
			return; // Not the untouched core draft: leave both pages alone.
		}
		wp_trash_post( $default[0]->ID );
	}
	wp_update_post( array( 'ID' => $imported[0]->ID, 'post_name' => 'privacy-policy' ) );
	update_option( 'wp_page_for_privacy_policy', $imported[0]->ID );
}

/**
 * Assign Polylang languages and translation groups from the imported meta.
 *
 * @return int Number of items processed.
 */
function meteora_sync_languages(): int {
	if ( ! function_exists( 'pll_set_post_language' ) || ! function_exists( 'pll_save_post_translations' ) || ! function_exists( 'pll_languages_list' ) ) {
		return 0;
	}
	$available = (array) pll_languages_list( array( 'fields' => 'slug' ) );
	// Serve each translated home page at its language root (/it/) instead of /it/<page-slug>/.
	if ( isset( PLL()->options ) && empty( PLL()->options['redirect_lang'] ) ) {
		PLL()->options['redirect_lang'] = true;
		if ( method_exists( PLL()->options, 'save' ) ) {
			PLL()->options->save();
		} elseif ( is_array( PLL()->options ) ) {
			update_option( 'polylang', PLL()->options );
		}
	}
	$items     = get_posts(
		array(
			'post_type'      => array( 'page', 'post' ),
			'post_status'    => 'any',
			'posts_per_page' => -1,
			'meta_key'       => '_meteora_lang', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
			'fields'         => 'ids',
			'lang'           => '',
		)
	);
	$groups = array();
	foreach ( $items as $id ) {
		$lang = (string) get_post_meta( $id, '_meteora_lang', true );
		if ( ! in_array( $lang, $available, true ) ) {
			continue;
		}
		pll_set_post_language( $id, $lang );
		$group                     = (int) get_post_meta( $id, '_meteora_group', true );
		$groups[ $group ][ $lang ] = $id;
	}
	foreach ( $groups as $translations ) {
		if ( count( $translations ) > 1 ) {
			pll_save_post_translations( $translations );
		}
	}
	// Categories and tags carry the same meta as posts (`_meteora_group` = taxonomy:EN slug).
	if ( function_exists( 'pll_set_term_language' ) && function_exists( 'pll_save_term_translations' ) ) {
		$terms = get_terms(
			array(
				'taxonomy'   => array( 'category', 'post_tag' ),
				'hide_empty' => false,
				'meta_key'   => '_meteora_lang', // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key
				'lang'       => '',
			)
		);
		$term_groups = array();
		foreach ( is_array( $terms ) ? $terms : array() as $term ) {
			$lang = (string) get_term_meta( $term->term_id, '_meteora_lang', true );
			if ( ! in_array( $lang, $available, true ) ) {
				continue;
			}
			pll_set_term_language( $term->term_id, $lang );
			$term_groups[ (string) get_term_meta( $term->term_id, '_meteora_group', true ) ][ $lang ] = $term->term_id;
		}
		foreach ( $term_groups as $translations ) {
			if ( count( $translations ) > 1 ) {
				pll_save_term_translations( $translations );
			}
		}
	}
	// Polylang caches each language's front page: refresh it now that translations are linked.
	if ( function_exists( 'PLL' ) && isset( PLL()->model ) && method_exists( PLL()->model, 'clean_languages_cache' ) ) {
		PLL()->model->clean_languages_cache();
	}
	update_option( 'meteora_languages_synced', count( $items ), false );
	return count( $items );
}

/**
 * If Polylang is activated after the import, link translations on the next admin load.
 */
function meteora_maybe_sync_languages(): void {
	if ( ! function_exists( 'pll_languages_list' ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}
	if ( count( (array) pll_languages_list() ) < 2 || get_option( 'meteora_languages_synced' ) ) {
		return;
	}
	meteora_sync_languages();
}
add_action( 'admin_init', 'meteora_maybe_sync_languages' );
