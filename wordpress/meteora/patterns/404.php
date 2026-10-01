<?php
/**
 * Title: 404 — page not found
 * Slug: meteora/404
 * Categories: meteora-sections
 * Inserter: no
 *
 * @package Meteora
 */

?>
<!-- wp:group {"tagName":"section","align":"full","className":"mt-section mt-nf","style":{"spacing":{"padding":{"top":"var:preset|spacing|section","bottom":"var:preset|spacing|section"}}},"layout":{"type":"constrained","contentSize":"62rem"}} -->
<section class="wp-block-group alignfull mt-section mt-nf" style="padding-top:var(--wp--preset--spacing--section);padding-bottom:var(--wp--preset--spacing--section)"><!-- wp:paragraph {"className":"is-style-eyebrow"} -->
<p class="is-style-eyebrow">404</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading"><?php echo wp_kses_post( __( 'Page not found. <em>Let’s get you back to the bar.</em>', 'meteora' ) ); ?></h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"is-style-lead is-muted"} -->
<p class="is-style-lead is-muted"><?php echo esc_html__( 'The page you are looking for does not exist or has moved.', 'meteora' ); ?></p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"className":"mt-cta-row"} -->
<div class="wp-block-buttons mt-cta-row"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_page_url( 'home' ) ); ?>"><?php echo esc_html__( 'Back to home', 'meteora' ); ?></a></div>
<!-- /wp:button -->

<!-- wp:button {"className":"is-style-button-text-link"} -->
<div class="wp-block-button is-style-button-text-link"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_page_url( 'contact' ) ); ?>"><?php echo esc_html__( 'Request a quote', 'meteora' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></section>
<!-- /wp:group -->
