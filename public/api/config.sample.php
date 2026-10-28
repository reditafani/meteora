<?php
/**
 * METEORA EVENTS — form handler configuration.
 *
 * 1. Copy this file to `config.php` in the same folder (public_html/api/config.php).
 * 2. Fill in the values below. `config.php` is never overwritten by a new build upload
 *    if you exclude it, and it is blocked from direct web access by api/.htaccess.
 *
 * Recommended on Keliweb: SMTP with a real mailbox created in cPanel
 * (e.g. noreply@meteoraevents.com). It gives far better deliverability than PHP mail().
 */
return [
    // Where requests are delivered.
    'recipient'        => 'info@meteoraevents.com',
    // Optional separate inbox for partner pricing requests (leave '' to use recipient).
    'partner_recipient'=> '',

    // Sender. Must be a mailbox on your own domain for SPF/DKIM to pass.
    'from_email'       => 'noreply@meteoraevents.com',
    'from_name'        => 'Meteora Events — Sito web',

    // 'smtp' (recommended) or 'mail' (PHP mail()).
    'transport'        => 'smtp',

    // SMTP settings — from cPanel → Email Accounts → Connect Devices.
    'smtp_host'        => 'mail.meteoraevents.com',
    'smtp_port'        => 465,          // 465 = SSL, 587 = STARTTLS
    'smtp_secure'      => 'ssl',        // 'ssl' | 'tls' | ''
    'smtp_user'        => 'noreply@meteoraevents.com',
    'smtp_pass'        => 'CHANGE-ME',
    'smtp_timeout'     => 15,

    // Send a short confirmation email to the person who filled in the form.
    'send_autoreply'   => true,

    // Accept submissions only from these hosts (anti-abuse). Add www. if you use it.
    'allowed_hosts'    => ['meteoraevents.com', 'www.meteoraevents.com', 'localhost'],

    // Basic rate limit per IP.
    'rate_limit'       => 5,     // max submissions…
    'rate_window'      => 600,   // …per this many seconds

    // Instagram feed on the home page (api/instagram.php). Leave the token '' to
    // keep the static photos.
    // · Facebook Login (Instagram linked to a Facebook Page): Page access token
    //   from a long-lived user token (it never expires) + the Instagram
    //   business account id (instagram_business_account.id of the Page).
    // · Instagram Login: long-lived token from "API setup with Instagram login",
    //   leave instagram_user_id '' — it is refreshed automatically.
    'instagram_token'   => '',
    'instagram_user_id' => '17841407045635016', // @meteoraevents (Page "Meteora Events")
    // Posts shown on the home page, in this order: paste their links from
    // Instagram ("Copy link"). As many as you like. Leave empty [] to show
    // the 7 latest posts automatically. Changes apply without a rebuild.
    'instagram_posts'   => [
        // 'https://www.instagram.com/p/XXXXXXXXXXX/',
        // 'https://www.instagram.com/reel/XXXXXXXXXXX/',
    ],
];
