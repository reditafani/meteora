<?php
/**
 * Meteora theme bootstrap.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

define( 'METEORA_VERSION', wp_get_theme( get_template() )->get( 'Version' ) );
define( 'METEORA_DIR', get_template_directory() );
define( 'METEORA_URI', get_template_directory_uri() );

require METEORA_DIR . '/inc/helpers.php';
require METEORA_DIR . '/inc/setup.php';
require METEORA_DIR . '/inc/assets.php';
require METEORA_DIR . '/inc/blocks.php';
require METEORA_DIR . '/inc/patterns.php';
require METEORA_DIR . '/inc/i18n.php';
require METEORA_DIR . '/inc/forms.php';
require METEORA_DIR . '/inc/ui.php';
require METEORA_DIR . '/inc/seo.php';
require METEORA_DIR . '/inc/import.php';
