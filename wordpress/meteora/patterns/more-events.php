<?php
/**
 * Title: More events
 * Slug: meteora/more-events
 * Categories: meteora-sections, query
 * Inserter: no
 * Description: Two other event stories (excludes the current one).
 *
 * @package Meteora
 */

?>
<!-- wp:group {"tagName":"section","align":"full","className":"mt-section is-style-section-alt mt-eh__more","style":{"spacing":{"padding":{"top":"var:preset|spacing|section","bottom":"var:preset|spacing|section"}}},"layout":{"type":"constrained","contentSize":"1440px"}} -->
<section class="wp-block-group alignfull mt-section is-style-section-alt mt-eh__more" style="padding-top:var(--wp--preset--spacing--section);padding-bottom:var(--wp--preset--spacing--section)"><!-- wp:heading {"className":"mt-bd__others-title"} -->
<h2 class="wp-block-heading mt-bd__others-title"><?php echo esc_html__( 'More events', 'meteora' ); ?></h2>
<!-- /wp:heading -->

<!-- wp:query {"queryId":11,"query":{"perPage":2,"pages":0,"offset":0,"postType":"post","order":"asc","orderBy":"date","inherit":false,"excludeCurrent":true},"className":"mt-pg mt-pg--two","layout":{"type":"default"}} -->
<div class="wp-block-query mt-pg mt-pg--two"><!-- wp:post-template {"className":"mt-pg__list","layout":{"type":"default"}} -->
<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"3/2","className":"mt-pg__media hover-zoom"} /-->

<!-- wp:post-terms {"term":"post_tag","separator":" — ","className":"is-style-micro mt-pg__type"} /-->

<!-- wp:post-title {"level":3,"isLink":true,"className":"mt-pg__title"} /-->

<!-- wp:post-excerpt {"excerptLength":30,"className":"mt-pg__excerpt"} /-->

<!-- wp:read-more {"content":"<?php echo esc_attr__( 'Read the story', 'meteora' ); ?>","className":"mt-pg__cta"} /-->
<!-- /wp:post-template --></div>
<!-- /wp:query --></section>
<!-- /wp:group -->
