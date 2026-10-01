/**
 * Cocktail families (.mt-cf): builds the arched frame from the row images and
 * crossfades it to the drink of the hovered/focused family.
 */
( function () {
	document.querySelectorAll( '.mt-cf' ).forEach( function ( root ) {
		var frame = root.querySelector( '.mt-cf__frame' );
		var rows = Array.prototype.slice.call( root.querySelectorAll( '.mt-cf__row' ) );
		if ( ! frame || ! rows.length ) {
			return;
		}
		frame.setAttribute( 'aria-hidden', 'true' );
		rows.forEach( function ( row, i ) {
			var slide = document.createElement( 'div' );
			slide.className = 'mt-cf__slide' + ( i === 0 ? ' is-active' : '' );
			var img = row.querySelector( '.mt-cf__img img' );
			if ( img ) {
				var clone = img.cloneNode( true );
				clone.alt = '';
				slide.appendChild( clone );
			}
			var drink = row.querySelector( '.mt-cf__drink' );
			if ( drink ) {
				var label = document.createElement( 'span' );
				label.className = 'mt-cf__label';
				label.textContent = drink.textContent;
				slide.appendChild( label );
			}
			frame.appendChild( slide );
		} );
		rows[ 0 ].classList.add( 'is-active' );
		function activate( index ) {
			rows.forEach( function ( r, i ) {
				r.classList.toggle( 'is-active', i === index );
				frame.children[ i ].classList.toggle( 'is-active', i === index );
			} );
		}
		rows.forEach( function ( row, i ) {
			row.addEventListener( 'mouseenter', function () {
				activate( i );
			} );
			row.addEventListener( 'focusin', function () {
				activate( i );
			} );
		} );
		root.classList.add( 'is-enhanced' );
	} );
}() );
