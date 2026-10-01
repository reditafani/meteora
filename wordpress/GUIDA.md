# Meteora — guida al tema WordPress

Tema a blocchi (Full Site Editing) che riproduce il sito Meteora Events. Non usa page builder e non richiede plugin per funzionare.

## Contenuto del pacchetto

| File | A cosa serve |
|---|---|
| `meteora.zip` | Il tema da installare |
| `meteora-content.xml` | Contenuti (WXR): 19 pagine EN + 19 IT, 5 + 5 storie evento, 61 immagini, 4 form Contact Form 7, categorie e tag |
| `GUIDA.md` | Questa guida |

## Requisiti

- WordPress 7.0 o successivo (testato su 7.1), PHP 8.2 o successivo.
- Plugin consigliati, tutti gratuiti:
  - **Polylang**: sito bilingue EN/IT, con l'inglese come lingua principale e l'italiano sotto `/it/`.
  - **Contact Form 7**: moduli di preventivo e partner. Senza il plugin, al posto del modulo compaiono email e WhatsApp.
  - **WordPress Importer**: serve solo per importare `meteora-content.xml`.
- Facoltativi: Yoast SEO o Rank Math. Il tema li riconosce da solo (vedi [SEO](#seo)).

---

## 1. Installazione (ordine consigliato)

1. **Aspetto → Temi → Aggiungi nuovo → Carica tema**: scegli `meteora.zip` e poi **Attiva**.
2. **Plugin → Aggiungi nuovo**: installa e attiva Polylang, Contact Form 7 e WordPress Importer.
3. **Lingue → Lingue** (Polylang):
   - aggiungi prima **English (en_US)**, che diventa la lingua predefinita;
   - poi aggiungi **Italiano (it_IT)**. WordPress scarica da solo la traduzione italiana del core.
   - Puoi saltare la procedura guidata di Polylang. Se chiede di assegnare la lingua predefinita ai contenuti esistenti, accetta pure: l'importazione la correggerà.
4. **Impostazioni → Permalink**: scegli "Nome articolo" (`/%postname%/`). Se lo dimentichi, lo imposta l'importazione.

> Polylang si può anche installare *dopo* l'importazione. Al primo accesso alla bacheca con due lingue attive, il tema assegna lingue e traduzioni da solo.

## 2. Importare i contenuti

1. Vai in **Strumenti → Importa → WordPress → Esegui l'importatore** e carica `meteora-content.xml`.
2. Come autore, assegna i contenuti al tuo utente amministratore.
3. Spunta **"Scarica e importa gli allegati"**: è indispensabile per le immagini.
4. A fine importazione il tema esegue da solo questi passi:
   - imposta la pagina **Home** come homepage statica;
   - collega ogni pagina inglese alla sua traduzione italiana, così come storie, categorie e tag;
   - fa aprire l'home italiana su `/it/` (Polylang: "L'URL della home contiene il codice lingua");
   - rinomina la pagina privacy importata in `/privacy-policy/` e la imposta come pagina privacy del sito, al posto della bozza predefinita di WordPress.

**Da dove vengono le immagini.** Il file WXR scarica le immagini da `https://meteoraevents.com/wp-content/themes/meteora/assets/images/…`, cioè dal tema stesso. L'importazione funziona quindi così com'è sul dominio definitivo, purché il tema sia già installato.

**Su un sito di prova (staging o locale)** sostituisci il dominio nel file prima di importarlo. Da terminale:

```bash
sed 's#https://meteoraevents.com#https://staging.esempio.it#g' meteora-content.xml > meteora-staging.xml
```

In alternativa usa la funzione "Sostituisci" di un editor di testo. Il nuovo dominio deve essere raggiungibile dal server con il tema già attivo. Quando poi il sito passa al dominio definitivo, cambia gli URL nel database con un plugin come Better Search Replace o con `wp search-replace`.

### Dopo l'importazione

- Puoi eliminare i contenuti di esempio di WordPress e di Contact Form 7: "Ciao mondo!", "Pagina di esempio" e "Contact form 1".
- Le 5 storie evento sono **segnaposto** (categoria *Placeholder story* / *Storia segnaposto*). Il tema chiede ai motori di ricerca di non indicizzarle (`noindex`) e le esclude dalla sitemap. Quando hai le storie vere, rimuovi quella categoria oppure sostituisci testi e foto.
- **Contact Form 7 → Moduli**: controlla che il destinatario sia `info@meteoraevents.com`. I moduli inviano anche una risposta automatica al cliente. Per una consegna affidabile delle email ti consiglio un plugin SMTP (ad esempio WP Mail SMTP).

---

## 3. Modificare i testi

### Pagine

Ogni pagina è fatta di normali blocchi: apri **Pagine**, modifica testi e immagini, poi premi **Aggiorna**. Le versioni italiane si trovano sotto **Pagine** filtrando per lingua (bandierina in alto). Ogni lingua si modifica separatamente.

Template per pagina (pannello laterale → *Template*):
- **Page — sections only (no title)**: per le pagine composte da sezioni con un proprio titolo grande. È il caso di quasi tutte.
- **Landing — overlay header**: header trasparente sopra l'immagine iniziale (Destination Weddings, Corporate).
- **Pagine**: template standard, con briciole di pane e titolo.

### Sezioni riutilizzabili (pattern)

Nell'editor, premi **+ → Pattern** e scegli le categorie **Meteora — Sections** (singole sezioni: hero, collezione banchi, FAQ, CTA…) o **Meteora — Pages** (pagine intere). Una volta inserito, un pattern diventa una copia indipendente e modificabile.

I pattern nascono in inglese. Quando il sito è in italiano (`it_IT`), li trovi già tradotti.

### Header, menu mobile e footer: attenzione

Header, menu mobile e footer sono **bilingui in automatico**: etichette e link cambiano con la lingua della pagina. Per questo sono generati dal codice del tema (`patterns/header.php`, `mobile-menu.php`, `footer.php`).

- Se li modifichi in **Aspetto → Editor → Parti di template**, WordPress salva una copia fissa *nella lingua in cui stai lavorando*, e l'altra lingua mostrerebbe i link sbagliati.
- Per cambiare voci di menu o link conviene quindi modificare quei tre file. In alternativa, chiedi al tuo sviluppatore di creare due parti separate, una per lingua.
- Per annullare una modifica fatta nell'editor: **Aspetto → Editor → Pattern → Parti di template → Header (o Footer) → ⋮ → Ripristina**.

### Dati di contatto

Email, telefono, WhatsApp e Instagram sono definiti in un unico punto, la funzione `meteora_contact()` in `inc/helpers.php`. Questi dati alimentano footer, pulsante WhatsApp e dati strutturati. Per modificarli senza toccare il tema, usa il filtro `meteora_contact`, ad esempio in un piccolo plugin:

```php
add_filter( 'meteora_contact', function ( $c ) {
	$c['phone_display'] = '+39 333 000 0000';
	$c['phone_e164']    = '+393330000000';
	$c['whatsapp']      = '393330000000';
	return $c;
} );
```

Se **cambi lo slug** di una pagina inglese (ad esempio `weddings`), aggiorna anche la mappa in `meteora_page_slugs()` (filtro `meteora_page_slugs`): header e footer trovano le pagine tramite quello slug.

### Testi del tema e traduzioni

- Le stringhe fisse del tema (pulsanti, banner cookie, pannello WhatsApp…) sono in `languages/it_IT.po`. Puoi modificarle con Poedit o con il plugin Loco Translate.
- Lo slogan del sito si traduce in **Lingue → Traduzioni** (Polylang).
- **WPML** funziona al posto di Polylang: selettore lingua e link usano le sue API. In quel caso l'importazione automatica delle lingue non si applica e le traduzioni vanno collegate a mano.

---

## 4. Colori, font e spaziature

Vai in **Aspetto → Editor → Stili**.

- **Colori**: la palette Meteora ha 15 colori, tra cui Background `#f9f2e8`, Accent `#b89e72`, Accent ink `#7a5f37` e Dark `#15110e`. Se modifichi un colore della palette, cambia in tutto il sito.
- **Tipografia**: Cormorant Garamond per i titoli e Jost per il testo, entrambi ospitati nel tema (`assets/fonts`), quindi nessuna chiamata a Google Fonts. Le dimensioni da Micro a Display sono fluide.
- **Varianti di stile dei blocchi**, nel pannello laterale → *Stili*:
  - Gruppo: Dark section, Cream section, Ivory panel.
  - Pulsante: Light, Ghost on dark, Outline, Text link.
  - Paragrafo: Eyebrow, Micro label, Lead, Display, Serif italic.
  - Elenco: Ruled list, Inline with dots.

Le scelte grafiche di partenza sono in `theme.json`. Le modifiche fatte da **Stili** si salvano nel database e si possono annullare con **⋮ → Ripristina impostazioni predefinite**.

> Prima di cambiare i colori del testo, verifica il contrasto: il sito è conforme WCAG 2.2 AA (vedi la sezione [Verifiche eseguite](#verifiche-eseguite)).

## 5. Animazioni

Le animazioni si attivano dall'editor con una classe CSS. Seleziona un blocco, apri **Avanzate → Classi CSS aggiuntive** e scrivi:

| Classe | Effetto |
|---|---|
| `animate-fade-up` | Il blocco sale e appare quando entra nello schermo |
| `animate-image-reveal` | L'immagine si svela con una tendina (su blocchi Immagine o Copertina) |
| `animate-delay-1` … `animate-delay-4` | Ritardo progressivo, da combinare con le classi sopra per effetti a cascata |
| `animate-drift` | Leggero movimento dell'immagine durante lo scroll (parallax) |
| `animate-hero-settle` | Zoom lento d'apertura sull'immagine dell'hero |

Esempio: `animate-fade-up animate-delay-2`.

- Le animazioni usano JavaScript nativo (IntersectionObserver), caricato in modo differito e **solo nelle pagine che le usano**.
- Se il visitatore ha attivato "Riduci movimento" nel sistema operativo, il contenuto appare subito, senza animazioni.
- Nell'editor i blocchi sono sempre visibili.

## 6. Cookie, analytics e WhatsApp

Banner cookie (con Google Consent Mode v2) e pulsante WhatsApp sono già attivi. Gli strumenti di analisi si caricano **solo dopo il consenso** del visitatore. Per attivarli, aggiungi in `wp-config.php` le costanti che ti servono:

```php
define( 'METEORA_GA4_ID', 'G-XXXXXXXXXX' );    // Google Analytics 4
define( 'METEORA_GTM_ID', 'GTM-XXXXXXX' );     // Google Tag Manager (alternativa a GA4)
define( 'METEORA_META_PIXEL_ID', '0000000000' ); // Meta Pixel
// define( 'METEORA_DISABLE_CONSENT', true );  // se usi già un altro banner cookie
// define( 'METEORA_DISABLE_WHATSAPP', true ); // nasconde pulsante e pannello WhatsApp
```

Eventi tracciati in automatico:
- clic sui pulsanti di richiesta preventivo;
- email, telefono, WhatsApp, Instagram;
- cambio lingua;
- invio riuscito dei moduli (`quote_request` e `partner_pricing_request`).

I link come `/contact/?type=wedding&service=open-bar` preselezionano i campi del modulo.

## 7. SEO

- Ogni pagina ha **un solo H1**. Titolo e meta description di ogni pagina sono già compilati, sia per **Yoast** sia per **Rank Math**.
- Il tema stampa i dati strutturati **LocalBusiness + Service** (area servita: Toscana e Italia). Con Yoast o Rank Math attivi, il tema li aggiunge al loro grafo invece di stamparli due volte.
- Senza plugin SEO, la meta description viene dal riassunto (*excerpt*) della pagina.
- Polylang genera i tag `hreflang` tra le versioni EN e IT.

## 8. Prestazioni consigliate

- Il tema non usa jQuery.
- Gli script si caricano solo dove servono, le immagini sono WebP responsive con lazy-load e i font sono precaricati.
- Sul server: attiva una cache di pagina (ad esempio WP Super Cache, oppure quella dell'hosting) e la compressione gzip/brotli.

---

## Differenze residue rispetto al sito originale

Ho verificato le 19 pagine, una per una e sezione per sezione, a 1440 px e a 390 px:
- l'altezza delle pagine differisce in media dello **0,6% su desktop** e dell'**1,0% su mobile**;
- tutte le sezioni desktop restano entro l'8%.

Differenze che restano:

1. **Lingue e URL.** L'originale aveva l'italiano alla radice e l'inglese sotto `/en/`. Come concordato, qui l'inglese è alla radice e l'italiano sotto `/it/`. Polylang gratuito non permette lo stesso slug in due lingue, per cui una storia italiana usa `signature-tower-moments-it` e un tag italiano `signature-tower-experience-it`.
2. **Tabella Essential vs Premium su mobile.** L'originale impilava delle schede. Il tema usa il blocco Tabella nativo a due colonne: stesso contenuto, circa 255 px più corta. Si modifica come una normale tabella.
3. **Campo data del preventivo.** La nota "facoltativo — anche indicativa" sta accanto all'etichetta, invece che sotto il campo.
4. **Accessibilità migliorata rispetto all'originale** (WCAG 2.2 AA):
   - più contrasto per briciole di pane, contatori dei filtri cocktail e nomi dei banchi non selezionati;
   - il carosello del ghiaccio su mobile si raggiunge anche da tastiera;
   - il menu mobile è il menu nativo di WordPress, con la stessa grafica e animazione dell'originale.
5. **Peso tecnico.** WordPress aggiunge il proprio CSS dei blocchi, gli stili globali e lo script dell'Interactivity API (circa 40 KB) usato dal menu mobile. La pagina resta senza spostamenti di layout (CLS 0,000).
6. **Testi del core in italiano.** "Pagina non trovata" e "Risultati della ricerca" vengono dal pacchetto italiano di WordPress, che si installa quando aggiungi la lingua.
7. **Moduli.** Usano Contact Form 7 invece dell'invio personalizzato dell'originale: stessi campi, stessa grafica, stessi eventi di conversione.

## Verifiche eseguite

- `php -l` su tutti i 63 file PHP: nessun errore.
- `theme.json` e le 14 varianti di stile validati sullo schema ufficiale v3: 0 errori.
- **Theme Check**: nessun errore obbligatorio e nessun avviso, solo 3 note informative.
- Editor a blocchi: 52 pattern e tutte le pagine importate (EN e IT) senza blocchi non validi.
- **axe-core (WCAG 2.2 AA)**: 0 violazioni su 50 URL (pagine, storie, 404 e ricerca), sia a 1440 px sia a 390 px.
- Importazione WXR su un'installazione pulita:
  - 38 pagine (19 EN / 19 IT) con traduzioni collegate;
  - 10 storie collegate, 61 immagini, 4 moduli;
  - nessun link interno o immagine rotti (258 controllati su 50 URL) e un solo H1 per pagina.
