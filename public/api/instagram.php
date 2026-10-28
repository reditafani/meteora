<?php
/**
 * METEORA EVENTS — Instagram feed endpoint for the home page.
 * Works on standard cPanel/PHP 8 hosting (Keliweb KeliPRO). No database, no Composer.
 *
 * - Reads the latest posts through the Instagram API, in one of two modes:
 *   · Facebook Login (config `instagram_user_id` set): graph.facebook.com/{ig-user-id}/media
 *     with a Page access token, which does not expire — no refresh needed
 *   · Instagram Login (no user id): graph.instagram.com/me/media with a long-lived
 *     token (60 days), refreshed here about once a week
 * - Caches the posts for a few hours, so visitors never wait for Instagram
 * - Serves the last good copy if Instagram is unreachable
 *
 * Token and id: `instagram_token` / `instagram_user_id` in config.php. A refreshed
 * Instagram Login token is stored next to this file (ig-token.json); cache and token
 * files are blocked from web access by api/.htaccess.
 */
declare(strict_types=1);

$cfgFile = __DIR__ . '/config.php';
$cfg = is_file($cfgFile) ? require $cfgFile : require __DIR__ . '/config.sample.php';

const IG_API        = 'https://graph.instagram.com';
const FB_API        = 'https://graph.facebook.com/v21.0';
const IG_CACHE_FILE = __DIR__ . '/ig-cache.json';
const IG_TOKEN_FILE = __DIR__ . '/ig-token.json';
const IG_CACHE_TTL  = 3 * 3600;      // refetch posts every 3 hours
const IG_REFRESH    = 7 * 86400;     // refresh the token once a week
const IG_POSTS      = 6;             // the home grid shows 6 posts

function respond(int $status, array $body, int $maxAge = 0): never
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header($maxAge > 0 ? "Cache-Control: public, max-age=$maxAge" : 'Cache-Control: no-store');
    echo json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

/** GET a JSON URL; returns the decoded array or null. */
function getJson(string $url): ?array
{
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8, CURLOPT_CONNECTTIMEOUT => 5]);
        $raw = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
    } else {
        $ctx = stream_context_create(['http' => ['timeout' => 8, 'ignore_errors' => true]]);
        $raw = @file_get_contents($url, false, $ctx);
        $code = 200;
        foreach ($http_response_header ?? [] as $h) {
            if (preg_match('#^HTTP/\S+\s+(\d{3})#', $h, $m)) $code = (int) $m[1];
        }
    }
    if ($raw === false || $code >= 400) return null;
    $data = json_decode((string) $raw, true);
    return is_array($data) ? $data : null;
}

function readJsonFile(string $file): ?array
{
    if (!is_file($file)) return null;
    $data = json_decode((string) @file_get_contents($file), true);
    return is_array($data) ? $data : null;
}

function writeJsonFile(string $file, array $data): void
{
    @file_put_contents($file, json_encode($data, JSON_UNESCAPED_SLASHES), LOCK_EX);
}

// ── Fresh cache: serve it straight away ──
$cache = readJsonFile(IG_CACHE_FILE);
if ($cache && (time() - (int) ($cache['fetched_at'] ?? 0)) < IG_CACHE_TTL) {
    respond(200, ['ok' => true, 'posts' => $cache['posts']], 900);
}

$userId = preg_replace('/\D/', '', (string) ($cfg['instagram_user_id'] ?? ''));
$fbMode = $userId !== '';

// ── Token: Facebook mode uses the config token as is (Page tokens don't expire);
//    Instagram mode prefers the refreshed copy ──
$stored = $fbMode ? null : readJsonFile(IG_TOKEN_FILE);
$token = (string) ($stored['token'] ?? ($cfg['instagram_token'] ?? ''));
if ($token === '') {
    $cache ? respond(200, ['ok' => true, 'posts' => $cache['posts'], 'stale' => true], 300)
           : respond(503, ['ok' => false, 'error' => 'not_configured']);
}

// Instagram Login only: refresh the long-lived token about once a week (it must be >24h old)
if (!$fbMode && time() - (int) ($stored['refreshed_at'] ?? 0) > IG_REFRESH) {
    $r = getJson(IG_API . '/refresh_access_token?grant_type=ig_refresh_token&access_token=' . rawurlencode($token));
    if (!empty($r['access_token'])) {
        $token = (string) $r['access_token'];
        writeJsonFile(IG_TOKEN_FILE, ['token' => $token, 'refreshed_at' => time()]);
    } elseif (!$stored) {
        // first run with a brand-new token: try again tomorrow, keep using it meanwhile
        writeJsonFile(IG_TOKEN_FILE, ['token' => $token, 'refreshed_at' => time() - IG_REFRESH + 86400]);
    }
}

// ── Latest posts ──
$fields = 'id,media_type,media_url,thumbnail_url,permalink,timestamp,caption';
$endpoint = $fbMode ? FB_API . '/' . $userId . '/media' : IG_API . '/me/media';
$res = getJson($endpoint . '?fields=' . $fields . '&limit=12&access_token=' . rawurlencode($token));

if (!isset($res['data']) || !is_array($res['data'])) {
    // Instagram unreachable or token invalid: keep showing the last good posts
    $cache ? respond(200, ['ok' => true, 'posts' => $cache['posts'], 'stale' => true], 300)
           : respond(502, ['ok' => false, 'error' => 'instagram_unavailable']);
}

$posts = [];
foreach ($res['data'] as $m) {
    $img = ($m['media_type'] ?? '') === 'VIDEO' ? ($m['thumbnail_url'] ?? '') : ($m['media_url'] ?? '');
    if ($img === '' || empty($m['permalink'])) continue;
    $caption = trim((string) ($m['caption'] ?? ''));
    $posts[] = [
        'img'  => $img,
        'url'  => $m['permalink'],
        'date' => $m['timestamp'] ?? '',
        'alt'  => mb_substr(preg_replace('/\s+/', ' ', $caption), 0, 120),
    ];
    if (count($posts) >= IG_POSTS) break;
}

writeJsonFile(IG_CACHE_FILE, ['fetched_at' => time(), 'posts' => $posts]);
respond(200, ['ok' => true, 'posts' => $posts], 900);
