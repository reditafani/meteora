<?php
/**
 * Title: Footer
 * Slug: meteora/footer
 * Categories: footer
 * Block Types: core/template-part/footer
 * Inserter: no
 * Description: Closing statement with quote CTA, brand and address, navigation, contacts, legal links and language switcher.
 *
 * @package Meteora
 */

$meteora_contact = meteora_contact();
$meteora_links   = array(
	'weddings'    => __( 'Weddings', 'meteora' ),
	'destination' => __( 'Destination Weddings', 'meteora' ),
	'bars'        => __( 'Bars', 'meteora' ),
	'cocktails'   => __( 'Cocktail Experience', 'meteora' ),
	'services'    => __( 'Services', 'meteora' ),
	'corporate'   => __( 'Corporate', 'meteora' ),
	'partners'    => __( 'Partners', 'meteora' ),
	'events'      => __( 'Events', 'meteora' ),
	'about'       => __( 'About', 'meteora' ),
	'why'         => __( 'Why Meteora', 'meteora' ),
	'contact'     => __( 'Contact', 'meteora' ),
);
?>
<!-- wp:group {"metadata":{"name":"Footer"},"align":"full","className":"footer is-style-section-dark","layout":{"type":"constrained","contentSize":"1440px"}} -->
<div class="wp-block-group alignfull footer is-style-section-dark"><!-- wp:group {"className":"footer__cta","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between","verticalAlignment":"bottom"}} -->
<div class="wp-block-group footer__cta"><!-- wp:paragraph {"className":"footer__statement"} -->
<p class="footer__statement"><?php echo wp_kses( __( 'The bar becomes <em>part of the event.</em>', 'meteora' ), array( 'em' => array() ) ); ?></p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-button-light has-arrow meteora-track-footer_quote"} -->
<div class="wp-block-button is-style-button-light has-arrow meteora-track-footer_quote"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_page_url( 'contact' ) ); ?>"><?php echo esc_html__( 'Request a quote', 'meteora' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->

<!-- wp:columns {"className":"footer__grid"} -->
<div class="wp-block-columns footer__grid"><!-- wp:column {"width":"40%","className":"footer__brand"} -->
<div class="wp-block-column footer__brand" style="flex-basis:40%"><!-- wp:site-logo {"width":150} /-->

<!-- wp:paragraph {"className":"is-style-micro footer__tag"} -->
<p class="is-style-micro footer__tag"><?php echo esc_html__( 'Luxury Open Bar Catering & Hospitality Services', 'meteora' ); ?></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"footer__addr"} -->
<p class="footer__addr"><?php echo esc_html( $meteora_contact['locality'] ); ?><br><?php echo esc_html__( 'Tuscany · Italy', 'meteora' ); ?></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"footer__base"} -->
<p class="footer__base"><?php echo esc_html__( 'Based in Tuscany, serving events throughout Italy and abroad.', 'meteora' ); ?></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"className":"footer__col"} -->
<div class="wp-block-column footer__col"><!-- wp:heading {"level":2,"className":"is-style-micro footer__h"} -->
<h2 class="wp-block-heading is-style-micro footer__h"><?php echo esc_html__( 'Explore', 'meteora' ); ?></h2>
<!-- /wp:heading -->

<!-- wp:list {"className":"footer__nav"} -->
<ul class="wp-block-list footer__nav"><?php foreach ( $meteora_links as $meteora_key => $meteora_label ) : ?><!-- wp:list-item -->
<li><a href="<?php echo esc_url( meteora_page_url( $meteora_key ) ); ?>"><?php echo esc_html( $meteora_label ); ?></a></li>
<!-- /wp:list-item --><?php endforeach; ?></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column {"className":"footer__col"} -->
<div class="wp-block-column footer__col"><!-- wp:heading {"level":2,"className":"is-style-micro footer__h"} -->
<h2 class="wp-block-heading is-style-micro footer__h"><?php echo esc_html__( 'Contact', 'meteora' ); ?></h2>
<!-- /wp:heading -->

<!-- wp:list {"className":"footer__contact"} -->
<ul class="wp-block-list footer__contact"><!-- wp:list-item -->
<li><a href="mailto:<?php echo esc_attr( $meteora_contact['email'] ); ?>"><?php echo esc_html( $meteora_contact['email'] ); ?></a></li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="tel:<?php echo esc_attr( $meteora_contact['phone_e164'] ); ?>"><?php echo esc_html( $meteora_contact['phone_display'] ); ?></a></li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="<?php echo esc_url( meteora_whatsapp_url() ); ?>" target="_blank" rel="noreferrer noopener">WhatsApp</a></li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="<?php echo esc_url( $meteora_contact['instagram_url'] ); ?>" target="_blank" rel="noreferrer noopener">Instagram <?php echo esc_html( $meteora_contact['instagram'] ); ?></a></li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="<?php echo esc_url( meteora_page_url( 'home' ) ); ?>">meteoraevents.com</a></li>
<!-- /wp:list-item --></ul>
<!-- /wp:list -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"is-style-button-text-link footer__partner"} -->
<div class="wp-block-button is-style-button-text-link footer__partner"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_page_url( 'partners' ) ); ?>"><?php echo esc_html__( 'Request partner pricing', 'meteora' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:group {"className":"footer__bottom","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between"}} -->
<div class="wp-block-group footer__bottom"><!-- wp:paragraph {"className":"footer__copy"} -->
<p class="footer__copy">© <?php echo esc_html( gmdate( 'Y' ) ); ?> Meteora Events. <?php echo esc_html__( 'All rights reserved.', 'meteora' ); ?></p>
<!-- /wp:paragraph -->

<!-- wp:list {"className":"footer__legal"} -->
<ul class="wp-block-list footer__legal"><!-- wp:list-item -->
<li><a href="<?php echo esc_url( meteora_page_url( 'privacy' ) ); ?>"><?php echo esc_html__( 'Privacy Policy', 'meteora' ); ?></a></li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="<?php echo esc_url( meteora_page_url( 'cookies' ) ); ?>"><?php echo esc_html__( 'Cookie Policy', 'meteora' ); ?></a></li>
<!-- /wp:list-item -->

<!-- wp:list-item -->
<li><a href="#cookie-preferences" class="meteora-cookie-open"><?php echo esc_html__( 'Cookie preferences', 'meteora' ); ?></a></li>
<!-- /wp:list-item --></ul>
<!-- /wp:list -->

<!-- wp:meteora/language-switcher /--></div>
<!-- /wp:group --></div>
<!-- /wp:group -->
