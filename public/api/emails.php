<?php
/**
 * METEORA EVENTS — the two emails sent for every form request.
 *
 * - meteora_autoreply('quote' | 'partner', 'it' | 'en', $data) → [subject, text, html]:
 *   confirmation to the visitor, in the language of the page they wrote from
 *   (template email/request-received.html). It goes to an address typed by the
 *   visitor, so only short, cleaned values are echoed back (first name, date,
 *   venue, guests, areas): no free text, no links, no message. That keeps the
 *   form useless as a spam relay.
 * - meteora_notification(...) → html: the request as it reaches info@, always in
 *   Italian (template email/new-request.html).
 *
 * Both share email/head.html (fonts, dark theme, mobile rules).
 */
declare(strict_types=1);

const METEORA_SITE_URL = 'https://meteoraevents.com';
const METEORA_LOGO_URL = 'https://meteoraevents.com/images/email/logo-meteora-gold.png';
// the same logo on the server: the mailer puts it inside the email (see MeteoraMailer::send)
const METEORA_LOGO_FILE = __DIR__ . '/../images/email/logo-meteora-gold.png';
const METEORA_INLINE_IMAGES = [METEORA_LOGO_URL => METEORA_LOGO_FILE];
const METEORA_WHATSAPP = 'https://wa.me/393280642479';

/** One-line value safe to echo to a third party: no links or addresses, limited length. */
function ar_clean(string $v, int $max): string
{
    $v = trim(preg_replace('/\s+/u', ' ', $v) ?? '');
    if ($v === '' || preg_match('~https?:|www\.|://|@|\.(com|it|net|org|io|ru|cn|xyz|info|biz)\b~i', $v)) {
        return '';
    }
    if (!preg_match("/^[\\p{L}\\p{N}\\s.,'’()\\/&-]+$/u", $v)) {
        return '';
    }
    return mb_strlen($v) > $max ? '' : $v;
}

/** First name from "Nome e cognome": letters only, capitalised. */
function ar_first_name(string $full): string
{
    $first = preg_split('/\s+/u', trim($full))[0] ?? '';
    $first = preg_replace("/[^\\p{L}'’-]/u", '', $first) ?? '';
    if ($first === '' || mb_strlen($first) > 30) {
        return '';
    }
    return mb_convert_case(mb_strtolower($first), MB_CASE_TITLE);
}

/** "12/06/2027" → "Sabato 12 giugno 2027" / "Saturday, 12 June 2027"; anything else is echoed only if harmless. */
function ar_date(string $raw, string $lang): string
{
    $raw = trim($raw);
    if (preg_match('~^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2}|\d{4})$~', $raw, $m)) {
        [$d, $mo, $y] = [(int) $m[1], (int) $m[2], (int) $m[3]];
        if ($y < 100) {
            $y += 2000;
        }
        if (checkdate($mo, $d, $y)) {
            $w = (int) date('w', mktime(12, 0, 0, $mo, $d, $y));
            if ($lang === 'it') {
                $days = ['Domenica', 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato'];
                $months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
                return "{$days[$w]} {$d} {$months[$mo - 1]} {$y}";
            }
            $days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            $months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            return "{$days[$w]}, {$d} {$months[$mo - 1]} {$y}";
        }
    }
    return ar_clean($raw, 40);
}

/** Guests: the first number only. */
function ar_guests(string $raw, string $lang): string
{
    if (!preg_match('/\d{1,5}/', $raw, $m)) {
        return '';
    }
    $n = (int) $m[0];
    return $lang === 'it' ? "{$n} circa" : "Approx. {$n}";
}

function ar_esc(string $s): string
{
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

/** Fills {{placeholders}}; values are inserted as given (escape them first). */
function ar_fill(string $tpl, array $vars): string
{
    return preg_replace_callback('/\{\{(\w+)\}\}/', fn ($m) => $vars[$m[1]] ?? '', $tpl) ?? '';
}

/** A template from email/ with the shared <head>, and its repeatable blocks (<!--BLOCK:name--> … <!--/BLOCK:name-->). */
function ar_template(string $file, array $needed): array
{
    $src = (string) @file_get_contents(__DIR__ . '/email/' . $file);
    $head = (string) @file_get_contents(__DIR__ . '/email/head.html');
    if ($src === '' || $head === '') {
        throw new RuntimeException("email template: {$file} or head.html missing");
    }
    $blocks = [];
    preg_match_all('/<!--BLOCK:(\w+)-->\R?(.*?)<!--\/BLOCK:\1-->/s', $src, $all, PREG_SET_ORDER);
    foreach ($all as $b) {
        $blocks[$b[1]] = $b[2];
    }
    foreach ($needed as $name) {
        if (!isset($blocks[$name])) {
            throw new RuntimeException("email template {$file}: block '{$name}' missing");
        }
    }
    $page = trim(substr($src, 0, (int) strpos($src, '<!--BLOCK:'))) . "\n";
    return [str_replace('{{head}}', trim($head), $page), $blocks];
}

function ar_copy(string $type, string $lang): array
{
    $it = $lang === 'it';
    $common = $it ? [
        'summary_title' => 'Riepilogo della richiesta',
        'steps_title'   => 'Cosa succede adesso',
        'regards'       => 'Un caro saluto,',
        'role'          => 'Fondatore · Meteora Events',
        'reply_line'    => 'Per qualsiasi domanda è possibile rispondere direttamente a questa email.',
        'whatsapp_line' => 'Per richieste urgenti è possibile contattarci su WhatsApp al',
        'follow'        => 'Seguici su Instagram: @meteoraevents',
        'legal'         => 'Meteora Events SRLS · Via Nofretti 21, 51016 Montecatini Terme (PT) · P.IVA 02132520475',
        'thanks'        => 'Grazie',
        'no_name'       => 'a presto',
        'done'          => 'Fatto',
        'today'         => 'oggi',
        'within'        => 'entro 48 ore',
        'subject_name'  => 'Grazie di averci contattati, %s: abbiamo ricevuto la richiesta',
        'subject_plain' => 'Grazie di averci contattati: abbiamo ricevuto la richiesta',
    ] : [
        'summary_title' => 'Request summary',
        'steps_title'   => 'What happens next',
        'regards'       => 'Kind regards,',
        'role'          => 'Founder · Meteora Events',
        'reply_line'    => 'If you have any questions, simply reply to this email.',
        'whatsapp_line' => 'For urgent requests, you can reach us on WhatsApp at',
        'follow'        => 'Follow us on Instagram: @meteoraevents',
        'legal'         => 'Meteora Events SRLS · Via Nofretti 21, 51016 Montecatini Terme (PT), Italy · VAT IT02132520475',
        'thanks'        => 'Thank you',
        'no_name'       => 'talk soon',
        'done'          => 'Done',
        'today'         => 'today',
        'within'        => 'within 48 hours',
        'subject_name'  => "Thank you for getting in touch, %s: we've received your request",
        'subject_plain' => "Thank you for getting in touch: we've received your request",
    ];

    // preheader, steps and note are optional: empty = left out of the email.
    // 'signature' set = one line "Redi <signature>" instead of "Redi" + role.
    if ($type === 'partner') {
        return $common + ($it ? [
            'preheader' => '',
            'eyebrow'   => 'Richiesta partner ricevuta',
            'intro'     => 'Abbiamo ricevuto la richiesta e risponderemo <strong>entro 48 ore</strong>.',
            'steps'     => [],
            'note'      => '',
            'signature' => 'di Meteora Events',
        ] : [
            'preheader' => '',
            'eyebrow'   => 'Partner request received',
            'intro'     => "We've received your request and will get back to you <strong>within 48 hours</strong>.",
            'steps'     => [],
            'note'      => '',
            'signature' => 'from Meteora Events',
        ]);
    }

    return $common + ($it ? [
        'preheader' => 'Risponderemo entro 48 ore con una proposta su misura.',
        'eyebrow'   => 'Richiesta ricevuta',
        'intro'     => 'Abbiamo ricevuto la richiesta e risponderemo <strong>entro 48 ore</strong>.',
        'steps'     => [
            ['Richiesta ricevuta', 'today', true],
            ['Verifica della disponibilità', 'within', false],
            ['Proposta su misura', '', false],
            ['La perfezioniamo insieme', "fino all'ultimo dettaglio", false],
        ],
        'note'      => 'Le date tra maggio e settembre si riempiono in fretta: confermeremo la disponibilità il prima possibile.',
        'signature' => 'di Meteora Events',
    ] : [
        'preheader' => "We'll get back to you within 48 hours with a tailored proposal.",
        'eyebrow'   => 'Request received',
        'intro'     => "We've received your request and will get back to you <strong>within 48 hours</strong>.",
        'steps'     => [
            ['Request received', 'today', true],
            ['Availability check', 'within', false],
            ['Tailored proposal', '', false],
            ['We refine it together', 'down to the last detail', false],
        ],
        'note'      => 'Dates between May and September fill up quickly: we\'ll confirm availability as soon as possible.',
        'signature' => 'from Meteora Events',
    ]);
}

/** Summary rows [label, value] built from the cleaned form data (empty values are left out). */
function ar_rows(string $type, string $lang, array $data): array
{
    $it = $lang === 'it';
    if ($type === 'partner') {
        $proTypes = $it
            ? ['wedding-planner' => 'Wedding planner', 'location' => 'Location / Villa']
            : ['wedding-planner' => 'Wedding planner', 'location' => 'Venue / Villa'];
        $rows = [
            [$it ? 'Tipologia' : 'Type', $proTypes[$data['pro_type_raw'] ?? ''] ?? ''],
            [$it ? 'Zone' : 'Areas', ar_clean((string) ($data['zones'] ?? ''), 80)],
        ];
    } else {
        $rows = [
            [$it ? 'Data' : 'Date', ar_date((string) ($data['event_date'] ?? ''), $lang)],
            [$it ? 'Location' : 'Venue', ar_clean((string) ($data['event_location'] ?? ''), 80)],
            [$it ? 'Ospiti' : 'Guests', ar_guests((string) ($data['guests'] ?? ''), $lang)],
        ];
    }
    return array_values(array_filter($rows, fn ($r) => $r[1] !== ''));
}

/** @return array{0:string,1:string,2:string} subject, plain text, html */
function meteora_autoreply(string $type, string $lang, array $data): array
{
    $lang = $lang === 'it' ? 'it' : 'en';
    $type = $type === 'partner' ? 'partner' : 'quote';
    $c = ar_copy($type, $lang);
    $name = ar_first_name((string) ($data['full_name'] ?? ''));
    $rows = ar_rows($type, $lang, $data);
    [$page, $b] = ar_template('request-received.html', ['preheader', 'summary', 'row', 'steps', 'step', 'step_sub', 'note', 'signature_role', 'signature_inline']);
    $sign = $c['signature'] ?? '';

    $subject = $name !== '' ? sprintf($c['subject_name'], $name) : $c['subject_plain'];

    // ---- HTML ----
    $gold = 'font-style:italic;color:#a8874f;';
    $headline = ar_esc($c['thanks']) . ', <em class="em-gold" style="' . $gold . '">'
        . ar_esc($name !== '' ? $name : $c['no_name']) . '.</em>';

    $rowsHtml = '';
    foreach ($rows as [$label, $value]) {
        $rowsHtml .= ar_fill($b['row'], ['label' => ar_esc($label), 'value' => ar_esc($value)]);
    }
    $summary = $rowsHtml !== ''
        ? ar_fill($b['summary'], ['summary_title' => ar_esc($c['summary_title']), 'rows' => $rowsHtml])
        : '';

    $stepsHtml = '';
    foreach ($c['steps'] as $i => [$title, $sub, $done]) {
        $sub = $c[$sub] ?? $sub; // 'today' / 'within' are shared words
        $stepsHtml .= ar_fill($b['step'], [
            'num'       => sprintf('%02d', $i + 1),
            'num_class' => $done ? 'em-gold' : 'em-num-off',
            'num_color' => $done ? '#a8874f' : '#cdbfae',
            'title'     => ar_esc($title),
            'sub_html'  => $sub !== '' ? ar_fill($b['step_sub'], ['sub' => ar_esc($sub)]) : '',
            'badge'     => $done ? ar_esc($c['done']) : '',
        ]);
    }

    $html = ar_fill($page, [
        'lang'            => $lang,
        'subject'         => ar_esc($subject),
        'preheader_block' => $c['preheader'] !== '' ? ar_fill($b['preheader'], ['preheader' => ar_esc($c['preheader'])]) : '',
        'site_url'        => METEORA_SITE_URL . ($lang === 'it' ? '/it/' : '/'),
        'logo_url'        => METEORA_LOGO_URL,
        'whatsapp_url'    => METEORA_WHATSAPP,
        'headline_html'   => $headline,
        'eyebrow'         => ar_esc($c['eyebrow']),
        'intro_html'      => $c['intro'], // trusted copy with <strong>
        'summary_block'   => $summary,
        'steps_block'     => $stepsHtml !== ''
            ? ar_fill($b['steps'], ['steps_title' => ar_esc($c['steps_title']), 'steps' => $stepsHtml])
            : '',
        // without steps the summary box already leaves room above the sign-off
        'signoff_pad'     => $stepsHtml !== '' ? '24px' : '0',
        'note_block'      => $c['note'] !== '' ? ar_fill($b['note'], ['note' => ar_esc($c['note'])]) : '',
        'regards_margin'  => $c['note'] !== '' ? '28px' : '0',
        'signature_block' => $sign !== ''
            ? ar_fill($b['signature_inline'], ['signature_tail' => ar_esc($sign)])
            : ar_fill($b['signature_role'], ['role' => ar_esc($c['role'])]),
        'regards'         => ar_esc($c['regards']),
        'reply_line'    => ar_esc($c['reply_line']),
        'whatsapp_line' => ar_esc($c['whatsapp_line']),
        'follow'        => ar_esc($c['follow']),
        'legal'         => ar_esc($c['legal']),
    ]);

    // ---- Plain text ----
    $t = $c['thanks'] . ', ' . ($name !== '' ? $name : $c['no_name']) . ".\n\n"
        . strip_tags($c['intro']) . "\n\n";
    if ($rows) {
        $t .= mb_strtoupper($c['summary_title']) . "\n";
        foreach ($rows as [$label, $value]) {
            $t .= "{$label}: {$value}\n";
        }
        $t .= "\n";
    }
    if ($c['steps']) {
        $t .= mb_strtoupper($c['steps_title']) . "\n";
        foreach ($c['steps'] as $i => [$title, $sub, $done]) {
            $sub = $c[$sub] ?? $sub;
            $t .= sprintf('%02d', $i + 1) . " {$title}" . ($sub !== '' ? " ({$sub})" : '') . ($done ? ' ✓' : '') . "\n";
        }
        $t .= "\n";
    }
    if ($c['note'] !== '') {
        $t .= "{$c['note']}\n\n";
    }
    $t .= "{$c['regards']}\n" . ($sign !== '' ? "Redi {$sign}" : "Redi\n{$c['role']}") . "\n\n"
        . "{$c['reply_line']}\n{$c['whatsapp_line']} +39 328 064 2479.\n\n"
        . "{$c['follow']}\n{$c['legal']}\n";

    return [$subject, $t, $html];
}

/** Phone number as digits for wa.me / tel: links (Italian mobiles without prefix get +39). */
function ar_phone_digits(string $phone): string
{
    $digits = preg_replace('/\D+/', '', $phone) ?? '';
    if (str_starts_with($digits, '00')) {
        $digits = substr($digits, 2);
    }
    if (strlen($digits) === 10 && str_starts_with($digits, '3')) {
        $digits = '39' . $digits;
    }
    return strlen($digits) >= 8 && strlen($digits) <= 15 ? $digits : '';
}

/**
 * The request as it reaches info@: same look as the confirmation, always in Italian.
 * $data holds the cleaned form fields; pro_type is already the readable label.
 */
function meteora_notification(string $type, string $lang, array $data, string $ip): string
{
    $partner = $type === 'partner';
    [$page, $b] = ar_template('new-request.html', ['row', 'message']);

    $name = trim((string) ($data['full_name'] ?? ''));
    $first = ar_first_name($name) ?: $name;
    $email = (string) ($data['email'] ?? '');
    $phone = (string) ($data['phone'] ?? '');
    $digits = ar_phone_digits($phone);

    // ---- detail rows: label => value already as html ----
    $link = fn (string $href, string $text): string => '<a class="em-link" href="' . ar_esc($href)
        . '" style="color:#7a5f37;text-decoration:none;border-bottom:1px solid #c7ad80;">' . ar_esc($text) . '</a>';
    $rows = ['Nome' => ar_esc($name)];
    if ($partner) {
        $rows['Tipologia'] = ar_esc((string) ($data['pro_type'] ?? ''));
    }
    $rows['Email'] = $email !== '' ? $link('mailto:' . $email, $email) : '';
    $rows['Telefono'] = $phone === '' ? '' : ($digits !== '' ? $link('tel:+' . $digits, $phone) : ar_esc($phone));
    if ($partner) {
        $web = trim((string) ($data['instagram'] ?? ''));
        $href = '';
        if (preg_match('~^https?://\S+$~i', $web)) {
            $href = $web;
        } elseif (preg_match('/^@?([A-Za-z0-9._]{1,30})$/', $web, $m)) {
            $href = 'https://www.instagram.com/' . $m[1] . '/';
        }
        $rows['Sito / Instagram'] = $web === '' ? '' : ($href !== '' ? $link($href, $web) : ar_esc($web));
        $rows['Zone'] = ar_esc((string) ($data['zones'] ?? ''));
    } else {
        $date = (string) ($data['event_date'] ?? '');
        $pretty = $date !== '' ? ar_date($date, 'it') : '';
        $rows['Data'] = ar_esc($pretty !== '' && $pretty !== $date ? "{$pretty} ({$date})" : $date);
        $rows['Ospiti'] = ar_esc((string) ($data['guests'] ?? ''));
        $rows['Location'] = ar_esc((string) ($data['event_location'] ?? ''));
    }
    $rowsHtml = '';
    foreach ($rows as $label => $valueHtml) {
        if ($valueHtml !== '') {
            $rowsHtml .= ar_fill($b['row'], ['label' => ar_esc($label), 'value_html' => $valueHtml]);
        }
    }

    $message = trim((string) ($data['message'] ?? ''));
    $messageBlock = $message === '' ? '' : ar_fill($b['message'], [
        'message_title' => 'Messaggio',
        'message_html'  => nl2br(ar_esc($message)),
    ]);

    $guests = (string) ($data['guests'] ?? '');
    $summary = $partner
        ? [(string) ($data['pro_type'] ?? ''), (string) ($data['zones'] ?? '')]
        : [(string) ($data['event_date'] ?? ''), (string) ($data['event_location'] ?? ''), $guests !== '' ? "{$guests} ospiti" : ''];
    $summary = implode(' · ', array_filter($summary, 'strlen'));

    return ar_fill($page, [
        'lang'          => 'it',
        'subject'       => ar_esc($partner ? 'Nuova richiesta da professionista' : 'Nuova richiesta di preventivo'),
        'preheader'     => ar_esc($name . ($summary !== '' ? ' — ' . $summary : '')),
        'logo_url'      => METEORA_LOGO_URL,
        'eyebrow'       => ar_esc($partner ? 'Richiesta da professionista' : 'Richiesta di preventivo'),
        'headline_html' => 'Nuova richiesta, <em class="em-gold" style="font-style:italic;color:#a8874f;">'
            . ar_esc($first !== '' ? $first : 'dal sito') . '.</em>',
        'received'      => ar_esc('Ricevuta il ' . date('d/m/Y') . ' alle ' . date('H:i') . ' · ' . ($lang === 'it' ? 'modulo in italiano' : 'modulo in inglese')),
        'details_title' => $partner ? 'Dati del professionista' : 'Dati del cliente',
        'rows'          => $rowsHtml,
        'message_block' => $messageBlock,
        'meta'          => ar_esc('Inviata dal modulo del sito · IP ' . $ip),
    ]);
}
