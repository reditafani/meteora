"""Contact Form 7 forms (EN/IT) for the WXR. Field order matches the original lead forms."""

FORMS = {
    'quote': {
        'en': {
            'title': 'Meteora — Request a quote',
            'form': '''<p class="mt-legend">About you</p>
<div class="mt-row"><label>First name <span class="req">*</span> [text* first-name autocomplete:given-name]</label><label>Last name <span class="req">*</span> [text* last-name autocomplete:family-name]</label></div>
<div class="mt-row"><label>Email <span class="req">*</span> [email* your-email autocomplete:email]</label><label>WhatsApp / Phone <span class="mt-opt">(optional)</span> [tel your-phone autocomplete:tel placeholder "+39 …"]</label></div>
<p class="mt-legend">The event</p>
<div class="mt-row"><label>Event type <span class="req">*</span> [select* type first_as_label "Select" "Wedding" "Destination Wedding" "Corporate" "Private event" "Other"]</label><label>Event date <span class="mt-opt">(optional — an approximate date is fine)</span> [date event-date]</label></div>
<div class="mt-row"><label>Event location <span class="req">*</span> [text* event-location placeholder "Venue, town or area"]</label><label>Number of guests <span class="mt-opt">(optional)</span> [number guests min:10 max:5000]</label></div>
<label>Service requested <span class="mt-opt">(optional)</span> [select service first_as_label "Select" "Open Bar" "Aperitivo + Open Bar" "Cocktail Experience" "Signature Tower" "Bartender service" "Custom service" "Not sure yet"]</label>
<label>Event style / requirements <span class="mt-opt">(optional)</span> [text style placeholder "E.g. elegant villa wedding, Golden Mirror bar, signature cocktails"]</label>
<label>Message <span class="mt-opt">(optional)</span> [textarea your-message]</label>
[acceptance privacy] I have read the <a href="/privacy-policy/">Privacy Policy</a> and agree to the processing of my data in order to receive a reply. [/acceptance]
[submit "Request your quote →"]''',
            'subject': 'Quote request — [type] — [first-name] [last-name]',
            'body': 'Quote request from meteoraevents.com\n\nName: [first-name] [last-name]\nEmail: [your-email]\nWhatsApp / Phone: [your-phone]\n\nEvent type: [type]\nDate: [event-date]\nLocation: [event-location]\nGuests: [guests]\nService: [service]\nStyle / requirements: [style]\n\nMessage:\n[your-message]\n\n-- \nLanguage: EN',
            'reply_subject': 'We have received your request — Meteora Events',
            'reply_body': 'Hello,\n\nthank you for getting in touch. We have received your request and will reply as soon as possible with a tailored proposal.\n\nMeteora Events\nLuxury Open Bar Catering & Hospitality Services\ninfo@meteoraevents.com · meteoraevents.com',
            'ok': 'Thank you. Your event is in good hands — we will reply as soon as possible with a tailored proposal.',
            'locale': 'en_US',
        },
        'it': {
            'title': 'Meteora — Richiesta preventivo',
            'form': '''<p class="mt-legend">Voi</p>
<div class="mt-row"><label>Nome <span class="req">*</span> [text* first-name autocomplete:given-name]</label><label>Cognome <span class="req">*</span> [text* last-name autocomplete:family-name]</label></div>
<div class="mt-row"><label>Email <span class="req">*</span> [email* your-email autocomplete:email]</label><label>WhatsApp / Telefono <span class="mt-opt">(facoltativo)</span> [tel your-phone autocomplete:tel placeholder "+39 …"]</label></div>
<p class="mt-legend">L’evento</p>
<div class="mt-row"><label>Tipo di evento <span class="req">*</span> [select* type first_as_label "Seleziona" "Matrimonio" "Destination Wedding" "Evento aziendale" "Evento privato" "Altro"]</label><label>Data dell’evento <span class="mt-opt">(facoltativo — anche indicativa)</span> [date event-date]</label></div>
<div class="mt-row"><label>Luogo dell’evento <span class="req">*</span> [text* event-location placeholder "Location, città o zona"]</label><label>Numero di ospiti <span class="mt-opt">(facoltativo)</span> [number guests min:10 max:5000]</label></div>
<label>Servizio richiesto <span class="mt-opt">(facoltativo)</span> [select service first_as_label "Seleziona" "Open Bar" "Aperitivo + Open Bar" "Cocktail Experience" "Signature Tower" "Servizio solo barman" "Servizio su misura" "Non lo so ancora"]</label>
<label>Stile dell’evento / esigenze <span class="mt-opt">(facoltativo)</span> [text style placeholder "Es. elegante in villa, banco Golden Mirror, cocktail signature"]</label>
<label>Messaggio <span class="mt-opt">(facoltativo)</span> [textarea your-message]</label>
[acceptance privacy] Ho letto la <a href="/it/informativa-privacy/">Privacy Policy</a> e acconsento al trattamento dei dati per ricevere una risposta. [/acceptance]
[submit "Richiedi il tuo preventivo →"]''',
            'subject': 'Richiesta preventivo — [type] — [first-name] [last-name]',
            'body': 'Richiesta di preventivo da meteoraevents.com\n\nNome: [first-name] [last-name]\nEmail: [your-email]\nWhatsApp / Telefono: [your-phone]\n\nTipo di evento: [type]\nData: [event-date]\nLuogo: [event-location]\nOspiti: [guests]\nServizio: [service]\nStile / esigenze: [style]\n\nMessaggio:\n[your-message]\n\n-- \nLingua: IT',
            'reply_subject': 'Abbiamo ricevuto la vostra richiesta — Meteora Events',
            'reply_body': 'Buongiorno,\n\ngrazie per averci scritto. Abbiamo ricevuto la vostra richiesta e vi risponderemo al più presto con una proposta su misura.\n\nMeteora Events\nLuxury Open Bar Catering & Hospitality Services\ninfo@meteoraevents.com · meteoraevents.com',
            'ok': 'Grazie. Il vostro evento è in buone mani: vi risponderemo al più presto con una proposta su misura.',
            'locale': 'it_IT',
        },
    },
    'partner': {
        'en': {
            'title': 'Meteora — Partner pricing',
            'form': '''<div class="mt-label">You are <span class="req">*</span> [radio partner-type use_label_element "Wedding Planner" "Venue" "Catering" "Event Professional"]</div>
<div class="mt-row"><label>Name <span class="req">*</span> [text* first-name autocomplete:given-name]</label><label>Surname <span class="req">*</span> [text* last-name autocomplete:family-name]</label></div>
<div class="mt-row"><label>Company <span class="req">*</span> [text* company autocomplete:organization]</label><label>Role <span class="mt-opt">(optional)</span> [text role autocomplete:organization-title]</label></div>
<div class="mt-row"><label>Email <span class="req">*</span> [email* your-email autocomplete:email]</label><label>Phone / WhatsApp <span class="req">*</span> [tel* your-phone autocomplete:tel placeholder "+39 …"]</label></div>
<div class="mt-row"><label>Website / Instagram <span class="mt-opt">(optional)</span> [text website placeholder "www… / @…"]</label><label>Typical event location <span class="req">*</span> [text* event-location placeholder "E.g. Florence and Chianti"]</label></div>
<label>Estimated annual events <span class="mt-opt">(optional)</span> [select volume first_as_label "Select" "1–5 events" "6–15 events" "16–30 events" "30+ events"]</label>
<label>Message <span class="mt-opt">(optional)</span> [textarea your-message]</label>
[acceptance privacy] I have read the <a href="/privacy-policy/">Privacy Policy</a> and agree to the processing of my data in order to receive a reply. [/acceptance]
[submit "Request partner pricing →"]''',
            'subject': 'Partner pricing request — [company] ([partner-type])',
            'body': 'Partner pricing request from meteoraevents.com\n\nType: [partner-type]\nName: [first-name] [last-name]\nCompany: [company]\nRole: [role]\nEmail: [your-email]\nPhone / WhatsApp: [your-phone]\nWebsite / Instagram: [website]\nTypical location: [event-location]\nEvents per year: [volume]\n\nMessage:\n[your-message]\n\n-- \nLanguage: EN',
            'reply_subject': 'We have received your request — Meteora Events',
            'reply_body': 'Hello,\n\nthank you for getting in touch. We will send our partner price list and collaboration terms to this address.\n\nMeteora Events\ninfo@meteoraevents.com · meteoraevents.com',
            'ok': 'Thank you. Let’s talk soon — we will send our partner price list and collaboration terms to the address you provided.',
            'locale': 'en_US',
        },
        'it': {
            'title': 'Meteora — Listino partner',
            'form': '''<div class="mt-label">Siete <span class="req">*</span> [radio partner-type use_label_element "Wedding Planner" "Location" "Catering" "Professionista eventi"]</div>
<div class="mt-row"><label>Nome <span class="req">*</span> [text* first-name autocomplete:given-name]</label><label>Cognome <span class="req">*</span> [text* last-name autocomplete:family-name]</label></div>
<div class="mt-row"><label>Azienda <span class="req">*</span> [text* company autocomplete:organization]</label><label>Ruolo <span class="mt-opt">(facoltativo)</span> [text role autocomplete:organization-title]</label></div>
<div class="mt-row"><label>Email <span class="req">*</span> [email* your-email autocomplete:email]</label><label>Telefono / WhatsApp <span class="req">*</span> [tel* your-phone autocomplete:tel placeholder "+39 …"]</label></div>
<div class="mt-row"><label>Website / Instagram <span class="mt-opt">(facoltativo)</span> [text website placeholder "www… / @…"]</label><label>Zona in cui lavorate di solito <span class="req">*</span> [text* event-location placeholder "Es. Firenze e Chianti"]</label></div>
<label>Eventi stimati all’anno <span class="mt-opt">(facoltativo)</span> [select volume first_as_label "Seleziona" "1–5 eventi" "6–15 eventi" "16–30 eventi" "Oltre 30 eventi"]</label>
<label>Messaggio <span class="mt-opt">(facoltativo)</span> [textarea your-message]</label>
[acceptance privacy] Ho letto la <a href="/it/informativa-privacy/">Privacy Policy</a> e acconsento al trattamento dei dati per ricevere una risposta. [/acceptance]
[submit "Richiedi listino partner →"]''',
            'subject': 'Richiesta listino partner — [company] ([partner-type])',
            'body': 'Richiesta listino partner da meteoraevents.com\n\nTipologia: [partner-type]\nNome: [first-name] [last-name]\nAzienda: [company]\nRuolo: [role]\nEmail: [your-email]\nTelefono / WhatsApp: [your-phone]\nWebsite / Instagram: [website]\nZona abituale: [event-location]\nEventi / anno: [volume]\n\nMessaggio:\n[your-message]\n\n-- \nLingua: IT',
            'reply_subject': 'Abbiamo ricevuto la vostra richiesta — Meteora Events',
            'reply_body': 'Buongiorno,\n\ngrazie per averci scritto. Vi invieremo il listino riservato ai partner e le condizioni di collaborazione a questo indirizzo.\n\nMeteora Events\ninfo@meteoraevents.com · meteoraevents.com',
            'ok': 'Grazie. Parliamo presto: vi invieremo il listino riservato ai partner e le condizioni di collaborazione all’indirizzo indicato.',
            'locale': 'it_IT',
        },
    },
}


MESSAGES = {
    'en': {
        'mail_sent_ng': 'There was an error trying to send your message. Please try again later or write to info@meteoraevents.com.',
        'validation_error': 'Please check the highlighted fields.',
        'spam': 'There was an error trying to send your message. Please try again later.',
        'accept_terms': 'Your consent is required to send the request.',
        'invalid_required': 'This field is required.',
        'invalid_too_long': 'This field is too long.', 'invalid_too_short': 'This field is too short.',
        'upload_failed': 'There was an unknown error uploading the file.', 'upload_file_type_invalid': 'You are not allowed to upload files of this type.',
        'upload_file_too_large': 'The uploaded file is too large.', 'upload_failed_php_error': 'There was an error uploading the file.',
        'invalid_date': 'Please enter a valid date.', 'date_too_early': 'Please enter a later date.', 'date_too_late': 'Please enter an earlier date.',
        'invalid_number': 'Please enter a number.', 'number_too_small': 'The number is too small.', 'number_too_large': 'The number is too large.',
        'quiz_answer_not_correct': 'The answer to the quiz is incorrect.', 'captcha_not_match': 'Your entered code is incorrect.',
        'invalid_email': 'Please enter a valid email address.', 'invalid_url': 'Please enter a URL.',
        'invalid_tel': 'Please enter a valid number, including the country code.',
    },
    'it': {
        'mail_sent_ng': 'Non è stato possibile inviare la richiesta. Riprova o scrivici a info@meteoraevents.com.',
        'validation_error': 'Controlla i campi evidenziati.',
        'spam': 'Non è stato possibile inviare la richiesta. Riprova più tardi.',
        'accept_terms': 'È necessario il consenso per inviare la richiesta.',
        'invalid_required': 'Campo obbligatorio.',
        'invalid_too_long': 'Il testo inserito è troppo lungo.', 'invalid_too_short': 'Il testo inserito è troppo corto.',
        'upload_failed': 'Errore sconosciuto durante il caricamento del file.', 'upload_file_type_invalid': 'Tipo di file non consentito.',
        'upload_file_too_large': 'Il file caricato è troppo grande.', 'upload_failed_php_error': 'Errore durante il caricamento del file.',
        'invalid_date': 'Inserisci una data valida.', 'date_too_early': 'Inserisci una data successiva.', 'date_too_late': 'Inserisci una data precedente.',
        'invalid_number': 'Inserisci un numero.', 'number_too_small': 'Il numero è troppo piccolo.', 'number_too_large': 'Il numero è troppo grande.',
        'quiz_answer_not_correct': 'La risposta non è corretta.', 'captcha_not_match': 'Il codice inserito non è corretto.',
        'invalid_email': 'Inserisci un indirizzo email valido.', 'invalid_url': 'Inserisci un URL.',
        'invalid_tel': 'Inserisci un numero valido, con prefisso internazionale.',
    },
}


def php_serialize(v):
    """Minimal PHP serialize() for strings, ints, bools and string-keyed dicts."""
    if isinstance(v, bool):
        return f'b:{int(v)};'
    if isinstance(v, int):
        return f'i:{v};'
    if isinstance(v, str):
        return f's:{len(v.encode("utf-8"))}:"{v}";'
    if isinstance(v, dict):
        return f'a:{len(v)}:{{' + ''.join(php_serialize(k) + php_serialize(x) for k, x in v.items()) + '}'
    raise TypeError(type(v))


def form_meta(f, lang):
    mail = {'active': True, 'subject': f['subject'], 'sender': 'Meteora Events <noreply@meteoraevents.com>',
            'recipient': 'info@meteoraevents.com', 'body': f['body'], 'additional_headers': 'Reply-To: [your-email]',
            'attachments': '', 'use_html': False, 'exclude_blank': True}
    mail2 = {'active': True, 'subject': f['reply_subject'], 'sender': 'Meteora Events <noreply@meteoraevents.com>',
             'recipient': '[your-email]', 'body': f['reply_body'], 'additional_headers': 'Reply-To: info@meteoraevents.com',
             'attachments': '', 'use_html': False, 'exclude_blank': True}
    return {'_form': f['form'], '_mail': php_serialize(mail), '_mail_2': php_serialize(mail2),
            '_messages': php_serialize({'mail_sent_ok': f['ok'], **MESSAGES[lang]}), '_additional_settings': '', '_locale': f['locale']}
