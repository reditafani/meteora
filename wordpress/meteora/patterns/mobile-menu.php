<?php
/**
 * Title: Mobile menu overlay
 * Slug: meteora/mobile-menu
 * Categories: header
 * Block Types: core/template-part/navigation-overlay
 * Inserter: no
 * Description: Full-screen dark overlay: logo, close, primary links, secondary links, quote CTA, language and contacts.
 *
 * @package Meteora
 */

$meteora_contact = meteora_contact();
?>
<!-- wp:group {"metadata":{"name":"Mobile menu"},"className":"mm","style":{"elements":{"link":{"color":{"text":"var:preset|color|on-dark"}}}},"backgroundColor":"dark","textColor":"on-dark","layout":{"type":"default"}} -->
<div class="wp-block-group mm has-on-dark-color has-dark-background-color has-text-color has-background has-link-color"><!-- wp:group {"className":"mm__bar","layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"space-between"}} -->
<div class="wp-block-group mm__bar"><!-- wp:site-logo {"width":104,"className":"mm__logo is-logo-light"} /-->

<!-- wp:navigation-overlay-close {"className":"mm__close"} /--></div>
<!-- /wp:group -->

<!-- wp:navigation {"overlayMenu":"never","ariaLabel":"<?php echo esc_attr__( 'Primary', 'meteora' ); ?>","className":"mm__primary","layout":{"type":"flex","orientation":"vertical"}} -->
<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Weddings', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'weddings' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Destination Weddings', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'destination' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'The Bar Collection', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'bars' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Cocktail Experience', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'cocktails' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Services', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'services' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Corporate & Private', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'corporate' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Events', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'events' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->
<!-- /wp:navigation -->

<!-- wp:navigation {"overlayMenu":"never","ariaLabel":"<?php echo esc_attr__( 'More', 'meteora' ); ?>","className":"mm__secondary","layout":{"type":"flex","orientation":"vertical"}} -->
<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Planners & venues', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'partners' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'About', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'about' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Why Meteora', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'why' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Contact', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'contact' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->
<!-- /wp:navigation -->

<!-- wp:group {"className":"mm__foot","layout":{"type":"default"}} -->
<div class="wp-block-group mm__foot"><!-- wp:buttons {"layout":{"type":"flex","orientation":"vertical","justifyContent":"stretch"}} -->
<div class="wp-block-buttons"><!-- wp:button {"width":100,"className":"is-style-button-light meteora-track-menu_quote"} -->
<div class="wp-block-button has-custom-width wp-block-button__width-100 is-style-button-light meteora-track-menu_quote"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_page_url( 'contact' ) ); ?>"><?php echo esc_html__( 'Request a quote', 'meteora' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:group {"className":"mm__meta","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between"}} -->
<div class="wp-block-group mm__meta"><!-- wp:meteora/language-switcher /-->

<!-- wp:paragraph -->
<p><a href="mailto:<?php echo esc_attr( $meteora_contact['email'] ); ?>"><?php echo esc_html( $meteora_contact['email'] ); ?></a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="<?php echo esc_url( $meteora_contact['instagram_url'] ); ?>" target="_blank" rel="noreferrer noopener"><?php echo esc_html( $meteora_contact['instagram'] ); ?></a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group --></div>
<!-- /wp:group --></div>
<!-- /wp:group -->
