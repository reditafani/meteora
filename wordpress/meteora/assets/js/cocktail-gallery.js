/**
 * Cocktail list filters (.mt-cg). The filter list is made of links (#family) in the
 * editor; here they become toggle buttons with counts. Cards carry `cat-<family>` classes.
 */
( function () {
	document.querySelectorAll( '.mt-cg' ).forEach( function ( root ) {
		var list = root.querySelector( '.mt-cg__filters' );
		var cards = Array.prototype.slice.call( root.querySelectorAll( '.mt-cc' ) );
		if ( ! list || ! cards.length ) {
			return;
		}
		var status = document.createElement( 'p' );
		status.className = 'screen-reader-text';
		status.setAttribute( 'aria-live', 'polite' );
		root.insertBefore( status, list.nextSibling );
		list.setAttribute( 'role', 'group' );
		list.setAttribute( 'aria-label', root.dataset.filterLabel || list.getAttribute( 'aria-label' ) || 'Filter' );

		var buttons = [];
		list.querySelectorAll( 'a[href^="#"]' ).forEach( function ( a ) {
			var id = a.getAttribute( 'href' ).slice( 1 );
			var count = id === 'all' ? cards.length : cards.filter( function ( c ) {
				return c.classList.contains( 'cat-' + id );
			} ).length;
			var btn = document.createElement( 'button' );
			btn.type = 'button';
			btn.dataset.filter = id;
			btn.setAttribute( 'aria-pressed', id === 'all' ? 'true' : 'false' );
			btn.innerHTML = a.innerHTML + ' <span class="mt-count">' + count + '</span>';
			a.replaceWith( btn );
			buttons.push( btn );
		} );

		function apply( id ) {
			var n = 0;
			buttons.forEach( function ( b ) {
				b.setAttribute( 'aria-pressed', String( b.dataset.filter === id ) );
			} );
			cards.forEach( function ( card ) {
				var show = id === 'all' || card.classList.contains( 'cat-' + id );
				card.hidden = ! show;
				if ( show ) {
					n++;
				}
			} );
			var active = buttons.filter( function ( b ) {
				return b.dataset.filter === id;
			} )[ 0 ];
			status.textContent = n + ' — ' + ( active ? active.firstChild.textContent.trim() : '' );
		}
		list.addEventListener( 'click', function ( e ) {
			var btn = e.target.closest( 'button[data-filter]' );
			if ( btn ) {
				apply( btn.dataset.filter );
			}
		} );
		var hash = window.location.hash.slice( 1 );
		if ( hash && buttons.some( function ( b ) {
			return b.dataset.filter === hash;
		} ) ) {
			apply( hash );
		}
	} );
}() );
