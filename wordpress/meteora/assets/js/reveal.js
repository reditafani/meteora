/**
 * Scroll reveal for blocks with the classes animate-fade-up / animate-image-reveal.
 * Each element is revealed once. Respects prefers-reduced-motion.
 */
( function () {
	var els = document.querySelectorAll( '.animate-fade-up, .animate-image-reveal' );
	if ( ! els.length ) {
		return;
	}
	var reduce = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	if ( reduce || ! ( 'IntersectionObserver' in window ) ) {
		els.forEach( function ( el ) {
			el.classList.add( 'is-visible' );
		} );
		return;
	}
	var io = new IntersectionObserver(
		function ( entries ) {
			entries.forEach( function ( entry ) {
				if ( entry.isIntersecting ) {
					entry.target.classList.add( 'is-visible' );
					io.unobserve( entry.target );
				}
			} );
		},
		{ rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
	);
	els.forEach( function ( el ) {
		io.observe( el );
	} );
}() );
