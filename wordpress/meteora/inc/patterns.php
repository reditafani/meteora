<?php
/**
 * Pattern categories. Pattern files live in /patterns and are registered by core.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Register the theme's pattern categories.
 */
function meteora_register_pattern_categories(): void {
	register_block_pattern_category(
		'meteora-sections',
		array(
			'label'       => __( 'Meteora — Sections', 'meteora' ),
			'description' => __( 'Editorial sections of the Meteora Events site.', 'meteora' ),
		)
	);
	register_block_pattern_category(
		'meteora-pages',
		array(
			'label'       => __( 'Meteora — Full pages', 'meteora' ),
			'description' => __( 'Complete page layouts with real content.', 'meteora' ),
		)
	);
	register_block_pattern_category(
		'meteora-forms',
		array(
			'label' => __( 'Meteora — Forms', 'meteora' ),
		)
	);
}
add_action( 'init', 'meteora_register_pattern_categories', 9 );
