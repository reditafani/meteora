<?php
/**
 * METEORA EVENTS — lead form endpoint (quote + partner pricing).
 * Works on standard cPanel/PHP 8 hosting (Keliweb KeliPRO). No database, no Composer.
 *
 * - JSON response for fetch() requests (Accept: application/json)
 * - 303 redirect to the thank-you page for no-JS submissions
 * - Honeypot + minimum fill time + per-IP rate limit + origin check
 * - Header-injection-safe; all output escaped
 */
declare(strict_types=1);

require __DIR__ . '/mailer.php';

$cfgFile = __DIR__ . '/config.php';
$cfg = is_file($cfgFile) ? require $cfgFile : require __DIR__ . '/config.sample.php';

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function respond(bool $ok, int $status = 200, array $extra = [], ?string $redirect = null): never
{
    global $wantsJson;
    if (!$wantsJson && $redirect) {
        header('Location: ' . $redirect, true, 303);
        exit;
    }
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode(['ok' => $ok] + $extra, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(false, 405, ['error' => 'method_not_allowed']);
}

// Origin / referer check
$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
$originHost = $origin ? (parse_url($origin, PHP_URL_HOST) ?: '') : '';
$allowed = (array) ($cfg['allowed_hosts'] ?? []);
if ($originHost && $allowed && !in_array(strtolower($originHost), array_map('strtolower', $allowed), true)) {
    respond(false, 403, ['error' => 'forbidden_origin']);
}

$lang = ($_POST['lang'] ?? 'it') === 'en' ? 'en' : 'it';
$type = ($_POST['form_type'] ?? 'quote') === 'partner' ? 'partner' : 'quote';
$redirectPath = (string) ($_POST['redirect'] ?? '');
$redirect = preg_match('#^/[a-z0-9/_-]*$#i', $redirectPath) ? $redirectPath : ($lang === 'en' ? '/en/thank-you/' : '/grazie/');

// Spam traps: honeypot and "filled in under 3 seconds" (silently accept to not tip off bots)
$hp = trim((string) ($_POST['company_fax'] ?? ''));
$t = (int) ($_POST['_t'] ?? 0);
if ($hp !== '' || ($t > 0 && (microtime(true) * 1000 - $t) < 3000)) {
    respond(true, 200, [], $redirect);
}

// Rate limit (file-based, per IP)
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$rlDir = sys_get_temp_dir() . '/meteora_rl';
if (!is_dir($rlDir)) {
    @mkdir($rlDir, 0700, true);
}
$rlFile = $rlDir . '/' . hash('sha256', $ip);
$now = time();
$hits = [];
if (is_file($rlFile)) {
    $hits = array_filter(array_map('intval', explode(',', (string) file_get_contents($rlFile))), fn($ts) => $ts > $now - (int) $cfg['rate_window']);
}
if (count($hits) >= (int) $cfg['rate_limit']) {
    respond(false, 429, ['error' => 'rate_limited']);
}
$hits[] = $now;
@file_put_contents($rlFile, implode(',', $hits), LOCK_EX);

// ---- Input ----
function field(string $name, int $max = 200): string
{
    $v = (string) ($_POST[$name] ?? '');
    $v = str_replace(["\r", "\0"], '', $v);
    $v = trim(strip_tags($v));
    return mb_substr($v, 0, $max);
}
function oneLine(string $v): string
{
    return trim(preg_replace('/\s+/', ' ', $v) ?? '');
}

$msg = [
    'it' => ['required' => 'Campo obbligatorio.', 'email' => 'Indirizzo email non valido.', 'consent' => 'Consenso obbligatorio.'],
    'en' => ['required' => 'This field is required.', 'email' => 'Invalid email address.', 'consent' => 'Consent is required.'],
][$lang];

if ($type === 'quote') {
    $labels = $lang === 'it'
        ? ['first_name' => 'Nome', 'last_name' => 'Cognome', 'email' => 'Email', 'phone' => 'WhatsApp / Telefono', 'event_type' => 'Tipo di evento', 'event_date' => 'Data', 'event_location' => 'Luogo', 'guests' => 'Ospiti', 'service' => 'Servizio', 'style' => 'Stile / esigenze', 'message' => 'Messaggio']
        : ['first_name' => 'First name', 'last_name' => 'Last name', 'email' => 'Email', 'phone' => 'WhatsApp / Phone', 'event_type' => 'Event type', 'event_date' => 'Date', 'event_location' => 'Location', 'guests' => 'Guests', 'service' => 'Service', 'style' => 'Style / requirements', 'message' => 'Message'];
    $required = ['first_name', 'last_name', 'email', 'event_type', 'event_location'];
} else {
    $labels = $lang === 'it'
        ? ['partner_type' => 'Tipologia', 'first_name' => 'Nome', 'last_name' => 'Cognome', 'company' => 'Azienda', 'role' => 'Ruolo', 'email' => 'Email', 'phone' => 'Telefono / WhatsApp', 'website' => 'Website / Instagram', 'event_location' => 'Zona abituale', 'volume' => 'Eventi / anno', 'message' => 'Messaggio']
        : ['partner_type' => 'Type', 'first_name' => 'Name', 'last_name' => 'Surname', 'company' => 'Company', 'role' => 'Role', 'email' => 'Email', 'phone' => 'Phone / WhatsApp', 'website' => 'Website / Instagram', 'event_location' => 'Typical location', 'volume' => 'Events / year', 'message' => 'Message'];
    $required = ['partner_type', 'first_name', 'last_name', 'company', 'email', 'phone', 'event_location'];
}

$data = [];
foreach ($labels as $key => $_) {
    $data[$key] = $key === 'message' ? field($key, 3000) : oneLine(field($key));
}
$errors = [];
foreach ($required as $key) {
    if ($data[$key] === '') {
        $errors[$key] = $msg['required'];
    }
}
if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = $msg['email'];
}
if (empty($_POST['privacy'])) {
    $errors['privacy'] = $msg['consent'];
}
if ($errors) {
    respond(false, 422, ['errors' => $errors]);
}

// ---- Compose ----
$isPartner = $type === 'partner';
$subject = $isPartner
    ? "Richiesta listino partner — {$data['company']} ({$data['partner_type']})"
    : "Richiesta preventivo — {$data['event_type']} — {$data['first_name']} {$data['last_name']}";

$rowsText = '';
$rowsHtml = '';
foreach ($labels as $key => $label) {
    if ($data[$key] === '') {
        continue;
    }
    $rowsText .= "{$label}: {$data[$key]}\n";
    $val = nl2br(htmlspecialchars($data[$key], ENT_QUOTES, 'UTF-8'));
    $rowsHtml .= '<tr><td style="padding:8px 16px 8px 0;color:#675d53;font:12px/1.4 Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;vertical-align:top;white-space:nowrap">'
        . htmlspecialchars($label, ENT_QUOTES, 'UTF-8') . '</td><td style="padding:8px 0;font:15px/1.5 Georgia,serif;color:#1c1614">' . $val . '</td></tr>';
}
$meta = 'Lingua: ' . strtoupper($lang) . ' · ' . date('d/m/Y H:i') . ' · IP ' . $ip;
$text = ($isPartner ? "Nuova richiesta listino partner\n\n" : "Nuova richiesta di preventivo\n\n") . $rowsText . "\n" . $meta;
$html = '<div style="background:#f9f2e8;padding:32px"><div style="max-width:640px;margin:auto;background:#fffaf3;padding:32px;border:1px solid #ddd0bc">'
    . '<p style="font:12px Arial,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:#7a5f37;margin:0 0 16px">Meteora Events</p>'
    . '<h1 style="font:400 26px Georgia,serif;margin:0 0 24px;color:#1c1614">' . ($isPartner ? 'Richiesta listino partner' : 'Richiesta di preventivo') . '</h1>'
    . '<table role="presentation" style="border-collapse:collapse;width:100%">' . $rowsHtml . '</table>'
    . '<p style="font:12px Arial,sans-serif;color:#675d53;margin-top:24px">' . htmlspecialchars($meta, ENT_QUOTES, 'UTF-8') . '</p></div></div>';

$to = $isPartner && !empty($cfg['partner_recipient']) ? (string) $cfg['partner_recipient'] : (string) $cfg['recipient'];
$replyTo = oneLine($data['first_name'] . ' ' . $data['last_name']);
$replyTo = '=?UTF-8?B?' . base64_encode($replyTo) . "?= <{$data['email']}>";

$mailer = new MeteoraMailer($cfg);
$sent = $mailer->send($to, $subject, $text, $html, $replyTo);

if (!$sent) {
    respond(false, 500, ['error' => 'send_failed'], $redirect . '?error=1');
}

// Optional auto-reply to the sender
if (!empty($cfg['send_autoreply'])) {
    // Deliberately generic: no user-supplied text is echoed back, so the
    // auto-reply cannot be abused to relay content to third parties.
    if ($lang === 'it') {
        $arSubject = 'Abbiamo ricevuto la vostra richiesta — Meteora Events';
        $arText = "Buongiorno,\n\ngrazie per averci scritto. Abbiamo ricevuto la vostra richiesta e vi risponderemo al più presto.\n\nMeteora Events\nLuxury Open Bar Catering & Hospitality Services\ninfo@meteoraevents.com · meteoraevents.com";
        $arBody = "<p>Buongiorno,</p><p>grazie per averci scritto. Abbiamo ricevuto la vostra richiesta e vi risponderemo al più presto.</p>";
    } else {
        $arSubject = 'We have received your request — Meteora Events';
        $arText = "Hello,\n\nthank you for getting in touch. We have received your request and will reply as soon as possible.\n\nMeteora Events\nLuxury Open Bar Catering & Hospitality Services\ninfo@meteoraevents.com · meteoraevents.com";
        $arBody = "<p>Hello,</p><p>thank you for getting in touch. We have received your request and will reply as soon as possible.</p>";
    }
    $arHtml = '<div style="background:#f9f2e8;padding:32px"><div style="max-width:560px;margin:auto;background:#fffaf3;padding:32px;border:1px solid #ddd0bc;font:16px/1.6 Georgia,serif;color:#1c1614">'
        . '<p style="font:12px Arial,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:#7a5f37">Meteora Events</p>'
        . $arBody . '<p style="font:13px Arial,sans-serif;color:#675d53">Meteora Events · Luxury Open Bar Catering &amp; Hospitality Services<br>info@meteoraevents.com · meteoraevents.com</p></div></div>';
    $mailer->send($data['email'], $arSubject, $arText, $arHtml, (string) $cfg['recipient']);
}

respond(true, 200, [], $redirect);
