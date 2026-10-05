<?php
/**
 * Technical SEO: JSON-LD (LocalBusiness + Service), robots for placeholder stories,
 * meta description fallback. Defers to Yoast SEO / Rank Math when they are active.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * True when a dedicated SEO plugin handles titles/meta.
 */
function meteora_has_seo_plugin(): bool {
	return defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' ) || defined( 'SEOPRESS_VERSION' );
}

/**
 * The LocalBusiness + Service graph. Facts only from the brochure: no street
 * address, no ratings. Filter `meteora_schema` to extend or return [] to disable.
 *
 * @return array<int,array<string,mixed>>
 */
function meteora_schema_graph(): array {
	$c    = meteora_contact();
	$home = function_exists( 'pll_home_url' ) ? pll_home_url() : home_url( '/' );
	$id   = home_url( '/#localbusiness' );
	$it   = 'it' === meteora_current_lang();

	$business = array(
		'@type'       => array( 'LocalBusiness', 'Organization' ),
		'@id'         => $id,
		'name'        => 'Meteora Events',
		'slogan'      => 'Luxury Open Bar Catering & Hospitality Services',
		'url'         => $home,
		'email'       => $c['email'],
		'telephone'   => $c['phone_e164'],
		'image'       => meteora_asset( 'assets/images/bars/golden-mirror-sunset.webp' ),
		'logo'        => meteora_asset( 'assets/images/brand/logo-gold.webp' ),
		'address'     => array(
			'@type'           => 'PostalAddress',
			'addressLocality' => $c['locality'],
			'postalCode'      => $c['postal_code'],
			'addressRegion'   => $it ? 'Toscana' : 'Tuscany',
			'addressCountry'  => $c['country'],
		),
		'areaServed'  => array(
			array( '@type' => 'AdministrativeArea', 'name' => $it ? 'Toscana' : 'Tuscany' ),
			array( '@type' => 'Country', 'name' => $it ? 'Italia' : 'Italy' ),
		),
		'sameAs'      => array( $c['instagram_url'] ),
		'knowsLanguage' => array( 'en', 'it' ),
	);

	$service = array(
		'@type'       => 'Service',
		'@id'         => home_url( '/#service-bar-catering' ),
		'name'        => $it ? 'Open bar catering per matrimoni ed eventi' : 'Open bar catering for weddings and events',
		'serviceType' => 'Bar catering',
		'provider'    => array( '@id' => $id ),
		'areaServed'  => array(
			array( '@type' => 'AdministrativeArea', 'name' => $it ? 'Toscana' : 'Tuscany' ),
			array( '@type' => 'Country', 'name' => $it ? 'Italia' : 'Italy' ),
		),
		'description' => $it
			? 'Bar catering luxury per matrimoni, destination wedding, eventi aziendali e privati. Base a Montecatini Terme, in Toscana; operativi in tutta Italia e all’estero.'
			: 'Luxury bar catering for weddings, destination weddings, corporate and private events. Based in Montecatini Terme, Tuscany; serving events throughout Italy and abroad.',
	);

	return apply_filters( 'meteora_schema', array( $business, $service ) );
}

/**
 * Print JSON-LD when no SEO plugin provides its own graph.
 */
function meteora_print_schema(): void {
	if ( defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) ) {
		return; // Added to their graph instead (see filters below).
	}
	$graph = meteora_schema_graph();
	if ( ! $graph ) {
		return;
	}
	wp_print_inline_script_tag(
		wp_json_encode(
			array(
				'@context' => 'https://schema.org',
				'@graph'   => $graph,
			),
			JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
		),
		array( 'type' => 'application/ld+json' )
	);
}
add_action( 'wp_head', 'meteora_print_schema', 20 );

/**
 * Yoast SEO: append our nodes to its graph.
 *
 * @param array<int,mixed> $data Graph.
 * @return array<int,mixed>
 */
function meteora_yoast_graph( $data ) {
	return array_merge( (array) $data, meteora_schema_graph() );
}
add_filter( 'wpseo_schema_graph', 'meteora_yoast_graph' );

/**
 * Rank Math: append our nodes.
 *
 * @param array<string,mixed> $data JSON-LD entities.
 * @return array<string,mixed>
 */
function meteora_rank_math_graph( $data ) {
	foreach ( meteora_schema_graph() as $i => $node ) {
		$data[ 'meteora_' . $i ] = $node;
	}
	return $data;
}
add_filter( 'rank_math/json_ld', 'meteora_rank_math_graph', 99 );

/**
 * Placeholder event stories (category slug starting with "placeholder") stay
 * visible but out of search engines, as in the original site.
 *
 * @param array<string,bool|string> $robots Robots directives.
 * @return array<string,bool|string>
 */
function meteora_robots( array $robots ): array {
	if ( is_single() ) {
		foreach ( (array) get_the_category() as $cat ) {
			if ( str_starts_with( $cat->slug, 'placeholder' ) ) {
				$robots['noindex'] = true;
				$robots['follow']  = true;
				break;
			}
		}
	}
	return $robots;
}
add_filter( 'wp_robots', 'meteora_robots' );

/**
 * Meta description from the page excerpt, only when no SEO plugin is active.
 * (The imported pages carry their SEO description as excerpt and as Yoast/Rank Math meta.)
 */
function meteora_meta_description(): void {
	if ( meteora_has_seo_plugin() || ! is_singular() ) {
		return;
	}
	$desc = has_excerpt() ? get_the_excerpt() : '';
	if ( '' === $desc ) {
		return;
	}
	printf( '<meta name="description" content="%s">' . "\n", esc_attr( wp_strip_all_tags( $desc ) ) );
}
add_action( 'wp_head', 'meteora_meta_description', 2 );

/**
 * Pages support excerpts (used for the meta description).
 */
function meteora_page_excerpts(): void {
	add_post_type_support( 'page', 'excerpt' );
}
add_action( 'init', 'meteora_page_excerpts' );

/**
 * Exclude placeholder stories from the XML sitemap (core sitemaps).
 *
 * @param array<string,mixed> $args Query args.
 * @return array<string,mixed>
 */
function meteora_sitemap_exclude_placeholders( array $args ): array {
	$terms = get_terms(
		array(
			'taxonomy'   => 'category',
			'fields'     => 'ids',
			'hide_empty' => false,
			'name__like' => 'placeholder',
		)
	);
	if ( $terms && ! is_wp_error( $terms ) ) {
		$args['category__not_in'] = $terms;
	}
	return $args;
}
add_filter( 'wp_sitemaps_posts_query_args', 'meteora_sitemap_exclude_placeholders' );
