<?php
/**
 * Contact Form 7 integration (recommended plugin, not required).
 *
 * - CF7 assets load only on pages that actually contain a form.
 * - When CF7 is not active, the [contact-form-7] shortcode used by the form
 *   patterns renders a refined fallback (email + WhatsApp) instead of raw text.
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Load CF7 scripts/styles only where a form is rendered.
 */
function meteora_cf7_conditional_assets(): void {
	if ( ! defined( 'WPCF7_VERSION' ) ) {
		return;
	}
	add_filter( 'wpcf7_load_js', '__return_false' );
	add_filter( 'wpcf7_load_css', '__return_false' );
	// Block themes render the content before `wp_enqueue_scripts`: note the form, enqueue after CF7 registers.
	add_filter(
		'do_shortcode_tag',
		static function ( $output, $tag ) {
			if ( 'contact-form-7' === $tag ) {
				$GLOBALS['meteora_has_cf7_form'] = true;
			}
			return $output;
		},
		10,
		2
	);
	add_action(
		'wp_enqueue_scripts',
		static function () {
			if ( empty( $GLOBALS['meteora_has_cf7_form'] ) ) {
				return;
			}
			if ( function_exists( 'wpcf7_enqueue_scripts' ) ) {
				wpcf7_enqueue_scripts();
			}
			if ( function_exists( 'wpcf7_enqueue_styles' ) ) {
				wpcf7_enqueue_styles();
			}
		},
		20
	);
	add_filter( 'wpcf7_autop_or_not', 'meteora_cf7_autop', 10, 2 );
}
add_action( 'after_setup_theme', 'meteora_cf7_conditional_assets' );

/**
 * The theme's forms (markup with `mt-row` grids) are laid out by CSS: CF7's
 * automatic <p>/<br> would break the grid. Other forms keep CF7's default.
 *
 * @param bool         $autop   Whether CF7 adds paragraphs.
 * @param array|string $options Context passed by CF7.
 */
function meteora_cf7_autop( $autop, $options = array() ): bool {
	if ( is_array( $options ) && isset( $options['for'] ) && 'form' !== $options['for'] ) {
		return (bool) $autop;
	}
	$form = class_exists( 'WPCF7_ContactForm' ) ? WPCF7_ContactForm::get_current() : null;
	if ( $form && false !== strpos( (string) $form->prop( 'form' ), 'class="mt-row"' ) ) {
		return false;
	}
	return (bool) $autop;
}

/**
 * Fallback for the form patterns when Contact Form 7 is not active: the
 * Shortcode block that holds `[contact-form-7 …]` shows email and WhatsApp instead.
 *
 * @param string $content Block content (shortcodes are expanded later by the_content).
 */
function meteora_form_block_fallback( string $content ): string {
	if ( shortcode_exists( 'contact-form-7' ) || false === strpos( $content, '[contact-form-7' ) ) {
		return $content;
	}
	return meteora_form_fallback();
}
add_filter( 'render_block_core/shortcode', 'meteora_form_block_fallback' );

/**
 * Render the fallback block.
 */
function meteora_form_fallback(): string {
	$contact = meteora_contact();
	$message = __( 'Hello Meteora Events, I would like to request information about a bar catering service for my event.', 'meteora' );
	ob_start();
	?>
	<div class="mt-form-fallback">
		<p class="is-style-eyebrow"><?php esc_html_e( 'Write to us', 'meteora' ); ?></p>
		<p class="is-style-lead"><?php esc_html_e( 'Tell us the date, the place and the number of guests: we will reply with a tailored proposal.', 'meteora' ); ?></p>
		<div class="wp-block-buttons mt-cta-row">
			<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="mailto:<?php echo esc_attr( $contact['email'] ); ?>"><?php echo esc_html( $contact['email'] ); ?></a></div>
			<div class="wp-block-button is-style-button-text-link"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( meteora_whatsapp_url( $message ) ); ?>" target="_blank" rel="noopener">WhatsApp</a></div>
		</div>
	</div>
	<?php
	return (string) ob_get_clean();
}
