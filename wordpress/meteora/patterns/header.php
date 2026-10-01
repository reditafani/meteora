<?php
/**
 * Title: Header
 * Slug: meteora/header
 * Categories: header
 * Block Types: core/template-part/header
 * Inserter: no
 * Description: Minimal luxury header: logo, main navigation, partner area, IT/EN, Request a quote, mobile menu.
 *
 * @package Meteora
 */

?>
<!-- wp:group {"align":"full","className":"site-header__inner","layout":{"type":"flex","flexWrap":"nowrap","justifyContent":"space-between"}} -->
<div class="wp-block-group alignfull site-header__inner"><!-- wp:site-logo {"width":118,"className":"site-header__brand"} /-->

<!-- wp:navigation {"overlayMenu":"never","ariaLabel":"<?php echo esc_attr__( 'Main navigation', 'meteora' ); ?>","className":"site-header__nav","layout":{"type":"flex","justifyContent":"center"}} -->
<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Weddings', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'weddings' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Experience', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'cocktails' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Bars', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'bars' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'Events', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'events' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->

<!-- wp:navigation-link {"label":"<?php echo esc_attr__( 'About', 'meteora' ); ?>","url":"<?php echo esc_url( meteora_page_url( 'about' ) ); ?>","kind":"custom","isTopLevelLink":true} /-->
<!-- /wp:navigation -->

<!-- wp:group {"className":"site-header__actions","layout":{"type":"flex","flexWrap":"nowrap"}} -->
<div class="wp-block-group site-header__actions"><!-- wp:paragraph {"className":"site-header__partner"} -->
<p class="site-header__partner"><a href="<?php echo esc_url( meteora_page_url( 'partners' ) ); ?>"><?php echo esc_html__( 'Partner area', 'meteora' ); ?></a></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"meteora-lang-switcher site-header__lang"} -->
<p class="meteora-lang-switcher site-header__lang">EN / IT</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"className":"site-header__cta"} -->
<div class="wp-block-buttons site-header__cta"><!-- wp:button {"className":"meteora-track-header_quote"} -->
<div class="wp-block-button meteora-track-header_quote"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_page_url( 'contact' ) ); ?>"><?php echo esc_html__( 'Request a quote', 'meteora' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons -->

<!-- wp:navigation {"overlayMenu":"always","overlay":"mobile-menu","hasIcon":true,"icon":"handle","ariaLabel":"<?php echo esc_attr__( 'Menu', 'meteora' ); ?>","className":"site-header__toggle"} -->
<!-- wp:home-link {"label":"<?php echo esc_attr__( 'Home', 'meteora' ); ?>"} /-->
<!-- /wp:navigation --></div>
<!-- /wp:group --></div>
<!-- /wp:group -->
