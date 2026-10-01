/**
 * Header: compact and solid once the page scrolls; adds `.js` for motion CSS.
 */
( function () {
	document.documentElement.classList.add( 'js' );
	var header = document.querySelector( '.site-header' );
	if ( ! header ) {
		return;
	}
	var ticking = false;
	function update() {
		header.classList.toggle( 'is-scrolled', window.scrollY > 24 );
		ticking = false;
	}
	update();
	window.addEventListener(
		'scroll',
		function () {
			if ( ! ticking ) {
				ticking = true;
				window.requestAnimationFrame( update );
			}
		},
		{ passive: true }
	);
}() );
