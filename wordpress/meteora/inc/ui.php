<?php
/**
 * Global UI printed in the footer: WhatsApp panel, mobile quote bar, cookie consent.
 *
 * Configuration (wp-config.php or the `meteora_settings` filter):
 *   define( 'METEORA_GA4_ID', 'G-XXXX' );         // Google Analytics 4 (optional)
 *   define( 'METEORA_GTM_ID', 'GTM-XXXX' );       // Google Tag Manager (optional)
 *   define( 'METEORA_META_PIXEL_ID', '123' );     // Meta Pixel (optional)
 *   define( 'METEORA_DISABLE_CONSENT', true );    // if you use a consent plugin instead
 *   define( 'METEORA_DISABLE_WHATSAPP', true );   // hide the WhatsApp button and panel
 *
 * @package Meteora
 */

defined( 'ABSPATH' ) || exit;

/**
 * Resolved settings.
 *
 * @return array{ga4:string,gtm:string,pixel:string,consent:bool,whatsapp:bool}
 */
function meteora_settings(): array {
	$c = static fn( string $name, $fallback ) => defined( $name ) ? constant( $name ) : $fallback;
	return apply_filters(
		'meteora_settings',
		array(
			'ga4'      => (string) $c( 'METEORA_GA4_ID', '' ),
			'gtm'      => (string) $c( 'METEORA_GTM_ID', '' ),
			'pixel'    => (string) $c( 'METEORA_META_PIXEL_ID', '' ),
			'consent'  => ! $c( 'METEORA_DISABLE_CONSENT', false ),
			'whatsapp' => ! $c( 'METEORA_DISABLE_WHATSAPP', false ),
		)
	);
}

/**
 * True on the quote page (the mobile quote bar is not shown there, as in the original).
 */
function meteora_is_contact_page(): bool {
	if ( ! is_page() ) {
		return false;
	}
	$contact = get_page_by_path( meteora_page_slugs()['contact'] );
	return $contact instanceof WP_Post && (int) get_queried_object_id() === meteora_translated_id( $contact->ID );
}

/**
 * Enqueue the UI script and styles.
 */
function meteora_ui_assets(): void {
	$s = meteora_settings();
	wp_enqueue_script( 'meteora-ui', meteora_asset( 'assets/js/ui.js' ), array(), METEORA_VERSION, array( 'strategy' => 'defer', 'in_footer' => true ) );
	wp_localize_script(
		'meteora-ui',
		'meteoraUI',
		array(
			'ga4'     => $s['ga4'],
			'gtm'     => $s['gtm'],
			'pixel'   => $s['pixel'],
			'consent' => $s['consent'],
			'wa'      => meteora_contact()['whatsapp'],
		)
	);
	wp_enqueue_style( 'meteora-ui', meteora_asset( 'assets/css/ui.css' ), array( 'meteora-base' ), METEORA_VERSION );
}
add_action( 'wp_enqueue_scripts', 'meteora_ui_assets' );

/**
 * Print WhatsApp panel, mobile quote bar and consent banner.
 */
function meteora_render_ui(): void {
	$s        = meteora_settings();
	$contact  = meteora_contact();
	$message  = __( 'Hello Meteora Events, I would like to request information about a bar catering service for my event.', 'meteora' );
	$show_bar = ! meteora_is_contact_page();
	$wa_icon  = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 20l1.2-4.2A8.2 8.2 0 1 1 8.4 19z"/><path d="M9.2 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .5.4l.7 1.6c.1.2 0 .4-.1.6l-.5.6c-.1.1-.2.3 0 .5a6 6 0 0 0 2.8 2.4c.2.1.4.1.5-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.2.1.3.2.3.4 0 .5-.2 1.2-.8 1.5-.6.4-1.6.5-2.9 0a8.9 8.9 0 0 1-4.4-4c-.6-1.1-.6-2.3-.2-3.4z"/></svg>';
	$x_icon   = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true" focusable="false"><path d="M5 5l14 14M19 5L5 19"/></svg>';
	$allowed  = array(
		'svg'  => array( 'width' => true, 'height' => true, 'viewbox' => true, 'fill' => true, 'stroke' => true, 'stroke-width' => true, 'stroke-linecap' => true, 'stroke-linejoin' => true, 'aria-hidden' => true, 'focusable' => true ),
		'path' => array( 'd' => true ),
	);

	if ( $s['whatsapp'] ) :
		?>
		<div class="wa<?php echo $show_bar ? '' : ' wa--solo'; ?>" data-wa>
			<div class="wa__panel" id="wa-panel" role="dialog" aria-labelledby="wa-title" hidden data-wa-panel>
				<div class="wa__head">
					<p id="wa-title" class="wa__title"><?php esc_html_e( 'Message us on WhatsApp', 'meteora' ); ?></p>
					<button type="button" class="wa__x" data-wa-close><?php echo wp_kses( $x_icon, $allowed ); ?><span class="screen-reader-text"><?php esc_html_e( 'Close', 'meteora' ); ?></span></button>
				</div>
				<label for="wa-message" class="wa__intro"><?php esc_html_e( 'You can edit the message before sending it.', 'meteora' ); ?></label>
				<textarea id="wa-message" rows="4" data-wa-message><?php echo esc_textarea( $message ); ?></textarea>
				<a class="wp-element-button wa__send" href="<?php echo esc_url( meteora_whatsapp_url( $message ) ); ?>" target="_blank" rel="noopener" data-wa-send data-track="whatsapp_click" data-track-label="panel"><?php echo wp_kses( $wa_icon, $allowed ); ?> <?php esc_html_e( 'Open WhatsApp', 'meteora' ); ?></a>
			</div>
			<button type="button" class="wa__fab" aria-expanded="false" aria-controls="wa-panel" data-wa-toggle>
				<?php echo wp_kses( $wa_icon, $allowed ); ?>
				<span class="screen-reader-text"><?php esc_html_e( 'Message us on WhatsApp', 'meteora' ); ?></span>
			</button>
		</div>
		<?php
	endif;

	if ( $show_bar ) :
		?>
		<div class="mobile-cta">
			<a class="wp-element-button mobile-cta__quote" href="<?php echo esc_url( meteora_page_url( 'contact' ) ); ?>" data-track="cta_click" data-track-label="mobile_bar_quote"><?php esc_html_e( 'Request a quote', 'meteora' ); ?></a>
			<?php if ( $s['whatsapp'] ) : ?>
				<button type="button" class="mobile-cta__wa" aria-controls="wa-panel" aria-expanded="false" data-wa-toggle>
					<?php echo wp_kses( $wa_icon, $allowed ); ?>
					<span class="screen-reader-text"><?php esc_html_e( 'Message us on WhatsApp', 'meteora' ); ?></span>
				</button>
			<?php endif; ?>
		</div>
		<?php
	endif;

	if ( $s['consent'] ) :
		$has_marketing = '' !== $s['pixel'];
		?>
		<div class="cookie" id="cookie-preferences" role="region" aria-label="<?php esc_attr_e( 'Your privacy', 'meteora' ); ?>" hidden data-cookie>
			<div class="cookie__inner">
				<div>
					<p class="cookie__title"><?php esc_html_e( 'Your privacy', 'meteora' ); ?></p>
					<p class="cookie__text">
						<?php esc_html_e( 'We use technical cookies that the site needs to work. With your consent we will also use analytics cookies to understand how to improve it. No non-essential cookie is set until you choose.', 'meteora' ); ?>
						<a href="<?php echo esc_url( meteora_page_url( 'cookies' ) ); ?>"><?php esc_html_e( 'Cookie Policy', 'meteora' ); ?></a>.
					</p>
				</div>
				<form class="cookie__prefs" hidden data-cookie-prefs>
					<fieldset>
						<legend class="screen-reader-text"><?php esc_html_e( 'Cookie preferences', 'meteora' ); ?></legend>
						<label class="cookie__opt"><input type="checkbox" checked disabled> <span><strong><?php esc_html_e( 'Necessary', 'meteora' ); ?></strong> — <?php esc_html_e( 'Required for the site to work and to remember your choices. Always active.', 'meteora' ); ?></span></label>
						<label class="cookie__opt"><input type="checkbox" name="analytics"> <span><strong><?php esc_html_e( 'Analytics', 'meteora' ); ?></strong> — <?php esc_html_e( 'Anonymous, aggregated statistics about how the site is used (e.g. Google Analytics).', 'meteora' ); ?></span></label>
						<?php if ( $has_marketing ) : ?>
							<label class="cookie__opt"><input type="checkbox" name="marketing"> <span><strong><?php esc_html_e( 'Marketing', 'meteora' ); ?></strong> — <?php esc_html_e( 'Advertising campaign measurement (e.g. Meta Pixel).', 'meteora' ); ?></span></label>
						<?php endif; ?>
					</fieldset>
				</form>
				<div class="cookie__actions">
					<button type="button" class="wp-element-button is-outline" data-cookie-reject><?php esc_html_e( 'Necessary only', 'meteora' ); ?></button>
					<button type="button" class="wp-element-button is-outline" data-cookie-customize><?php esc_html_e( 'Customise', 'meteora' ); ?></button>
					<button type="button" class="wp-element-button is-outline" data-cookie-save hidden><?php esc_html_e( 'Save preferences', 'meteora' ); ?></button>
					<button type="button" class="wp-element-button" data-cookie-accept><?php esc_html_e( 'Accept all', 'meteora' ); ?></button>
				</div>
			</div>
		</div>
		<?php
	endif;
}
add_action( 'wp_footer', 'meteora_render_ui', 5 );
