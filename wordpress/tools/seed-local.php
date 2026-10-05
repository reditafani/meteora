<?php
/**
 * DEV ONLY — seeds a local WordPress with the generated content JSON, mimicking the
 * WordPress Importer (fixed IDs, media library, URL rewrite). Run with:
 *   wp eval-file seed-local.php /path/to/meteora-content.json [en|it|all]
 *
 * @package Meteora
 */

$file = $args[0] ?? '';
$only = $args[1] ?? 'all';
$data = json_decode( (string) file_get_contents( $file ), true );
require_once ABSPATH . 'wp-admin/includes/image.php';

$theme_dir = get_template_directory() . '/assets/images/';
$uploads   = wp_upload_dir( '2026/10' );
$url_map   = array();

foreach ( $data['attachments'] as $a ) {
	if ( get_post( $a['id'] ) ) {
		$url_map[ $a['url'] ] = wp_get_attachment_url( $a['id'] );
		continue;
	}
	$name = str_replace( '/', '-', $a['path'] );
	$dest = trailingslashit( $uploads['path'] ) . $name;
	wp_mkdir_p( $uploads['path'] );
	copy( $theme_dir . $a['path'], $dest );
	$id = wp_insert_attachment(
		array(
			'import_id'      => $a['id'],
			'post_title'     => ucwords( str_replace( array( '-', '.webp', '/' ), array( ' ', '', ' — ' ), $a['path'] ) ),
			'post_mime_type' => 'image/webp',
			'post_status'    => 'inherit',
			'post_date'      => '2026-10-01 09:00:00',
		),
		$dest
	);
	wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $dest ) );
	$url_map[ $a['url'] ] = wp_get_attachment_url( $id );
}
WP_CLI::log( 'attachments: ' . count( $url_map ) );

$rewrite = static fn( string $c ): string => strtr( $c, $url_map );

foreach ( $data['pages'] as $p ) {
	if ( 'all' !== $only && $p['lang'] !== $only ) {
		continue;
	}
	$args_post = array(
		'import_id'    => $p['id'],
		'post_type'    => 'page',
		'post_status'  => 'publish',
		'post_title'   => $p['title'],
		'post_name'    => $p['slug'],
		'post_parent'  => $p['parent'],
		'menu_order'   => $p['menu_order'],
		'post_content' => $rewrite( $p['content'] ),
	);
	if ( get_post( $p['id'] ) ) {
		$args_post['ID'] = $p['id'];
		wp_update_post( wp_slash( $args_post ) );
	} else {
		wp_insert_post( wp_slash( $args_post ) );
	}
	update_post_meta( $p['id'], '_wp_page_template', $p['template'] );
}
foreach ( $data['posts'] as $p ) {
	if ( 'all' !== $only && $p['lang'] !== $only ) {
		continue;
	}
	$cats = array();
	foreach ( $p['categories'] as $slug ) {
		$term = term_exists( $slug, 'category' ) ?: wp_insert_term( ucfirst( $slug ), 'category', array( 'slug' => $slug ) );
		$cats[] = (int) ( is_array( $term ) ? $term['term_id'] : $term );
	}
	$args_post = array(
		'import_id'     => $p['id'],
		'post_type'     => 'post',
		'post_status'   => 'publish',
		'post_title'    => $p['title'],
		'post_name'     => $p['slug'],
		'post_excerpt'  => $p['excerpt'],
		'post_date'     => $p['date'],
		'post_content'  => $rewrite( $p['content'] ),
		'post_category' => $cats,
		'tags_input'    => $p['tags'],
	);
	if ( get_post( $p['id'] ) ) {
		$args_post['ID'] = $p['id'];
		wp_update_post( wp_slash( $args_post ) );
	} else {
		wp_insert_post( wp_slash( $args_post ) );
	}
	set_post_thumbnail( $p['id'], $p['thumbnail'] );
}
update_option( 'show_on_front', 'page' );
update_option( 'page_on_front', 101 );
update_option( 'page_for_posts', 0 );
wp_delete_post( 1, true ); // Hello world.
wp_delete_post( 2, true ); // Sample page.
WP_CLI::success( 'seeded' );
