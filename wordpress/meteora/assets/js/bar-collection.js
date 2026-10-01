/**
 * The Bar Collection (.mt-bc): on wide screens the rail becomes a luxury index —
 * names on the left, a large sticky image on the right that crossfades on hover/focus.
 * The stage is built from the images already in each row (edited once in the editor).
 */
( function () {
	var mq = window.matchMedia( '(min-width: 1024px)' );
	document.querySelectorAll( '.mt-bc' ).forEach( function ( root ) {
		var rows = Array.prototype.slice.call( root.querySelectorAll( ':scope > .mt-bar' ) );
		if ( ! rows.length ) {
			return;
		}
		var stage = document.createElement( 'div' );
		stage.className = 'mt-bc__stage';
		stage.setAttribute( 'aria-hidden', 'true' );
		rows.forEach( function ( row, i ) {
			var media = row.querySelector( '.mt-bar__media' );
			var slide = document.createElement( 'div' );
			slide.className = 'mt-bc__slide' + ( i === 0 ? ' is-active' : '' );
			if ( media ) {
				var clone = media.cloneNode( true );
				clone.querySelectorAll( 'img' ).forEach( function ( img ) {
					img.alt = '';
					img.loading = i === 0 ? 'eager' : 'lazy';
				} );
				slide.appendChild( clone );
			}
			stage.appendChild( slide );
			if ( i === 0 ) {
				row.classList.add( 'is-active' );
			}
			if ( ! row.querySelector( 'a' ) ) {
				// Coming-soon bars have no link: make them focusable so keyboard users can preview them.
				row.tabIndex = 0;
			}
		} );
		// The stage spans every row plus a final flexible track that absorbs its height,
		// so the index rows keep their natural (compact) height.
		stage.style.gridRow = '1 / span ' + ( rows.length + 1 );

		function activate( index ) {
			rows.forEach( function ( r, i ) {
				r.classList.toggle( 'is-active', i === index );
				stage.children[ i ].classList.toggle( 'is-active', i === index );
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

		function sync() {
			if ( mq.matches ) {
				if ( ! stage.parentNode ) {
					root.appendChild( stage );
				}
				root.classList.add( 'is-enhanced' );
				root.style.gridTemplateRows = 'repeat(' + rows.length + ', auto) 1fr';
			} else {
				root.classList.remove( 'is-enhanced' );
				root.style.gridTemplateRows = '';
				if ( stage.parentNode ) {
					stage.remove();
				}
			}
		}
		sync();
		mq.addEventListener( 'change', sync );
	} );
}() );
