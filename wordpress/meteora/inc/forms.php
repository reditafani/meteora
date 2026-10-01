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
	add_filter(
		'do_shortcode_tag',
		static function ( $output, $tag ) {
			if ( 'contact-form-7' === $tag ) {
				if ( function_exists( 'wpcf7_enqueue_scripts' ) ) {
					wpcf7_enqueue_scripts();
				}
				if ( function_exists( 'wpcf7_enqueue_styles' ) ) {
					wpcf7_enqueue_styles();
				}
			}
			return $output;
		},
		10,
		2
	);
}
add_action( 'plugins_loaded', 'meteora_cf7_conditional_assets', 20 );

/**
 * Fallback for the form patterns when Contact Form 7 is not active.
 */
function meteora_register_form_fallback(): void {
	if ( shortcode_exists( 'contact-form-7' ) ) {
		return;
	}
	add_shortcode( 'contact-form-7', 'meteora_form_fallback' );
}
add_action( 'init', 'meteora_register_form_fallback', 20 );

/**
 * Render the fallback block.
 *
 * @param array<string,string>|string $atts Shortcode attributes.
 */
function meteora_form_fallback( $atts = array() ): string {
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
