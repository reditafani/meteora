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
 * - Images are downloaded once and served from this server as small JPEG
 *   thumbnails (api/ig-img/): visitors never contact Meta's servers (no
 *   personal data sent before cookie consent) and the tiles stay light
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
const IG_LATEST     = 24;            // latest posts sent; the page shows as many as fit one row
const IG_PAGE       = 50;            // posts per API page while looking for the selection
const IG_MAX_PAGES  = 6;             // search the latest 300 posts at most
const IG_IMG_DIR    = __DIR__ . '/ig-img';
const IG_IMG_URL    = '/api/ig-img/';
const IG_THUMB      = 480;           // thumbnail width: sharp on a 162px tile at 3x

/** Instagram shortcode from a post link (…/p/CODE/, …/reel/CODE/, …/tv/CODE/) or a bare code. */
function shortcode(string $s): string
{
    $s = trim($s);
    if (preg_match('#instagram\.com/(?:[^/]+/)?(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)#', $s, $m)) return $m[1];
    return preg_match('#^[A-Za-z0-9_-]{5,}$#', $s) ? $s : '';
}

// Posts chosen in config.php (in display order); empty = show the latest ones
$wanted = array_values(array_filter(array_map('shortcode', (array) ($cfg['instagram_posts'] ?? []))));
$cacheKey = md5(implode(',', $wanted) . '|' . IG_LATEST . '|local-thumbs-v1');

function respond(int $status, array $body, int $maxAge = 0): never
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header($maxAge > 0 ? "Cache-Control: public, max-age=$maxAge" : 'Cache-Control: no-store');
    echo json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

/** GET a URL; returns the raw body or null. */
function getRaw(string $url): ?string
{
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_TIMEOUT => 10, CURLOPT_CONNECTTIMEOUT => 5]);
        $raw = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
        return ($raw === false || $code >= 400) ? null : (string) $raw;
    }
    $raw = @file_get_contents($url, false, stream_context_create(['http' => ['timeout' => 10]]));
    return $raw === false ? null : $raw;
}

/**
 * Local thumbnail of a post image (downloaded once, kept while the post is shown).
 * Returns its public URL, or '' when the image cannot be fetched.
 */
function localThumb(string $code, string $remote): string
{
    $file = IG_IMG_DIR . '/' . $code . '.jpg';
    if (!is_file($file)) {
        if (!is_dir(IG_IMG_DIR)) @mkdir(IG_IMG_DIR, 0755, true);
        $raw = getRaw($remote);
        if ($raw === null) return '';
        $img = function_exists('imagecreatefromstring') ? @imagecreatefromstring($raw) : false;
        if ($img) {
            $w = imagesx($img);
            if ($w > IG_THUMB) {
                $small = imagescale($img, IG_THUMB, (int) round(imagesy($img) * IG_THUMB / $w), IMG_BICUBIC);
                if ($small) { imagedestroy($img); $img = $small; }
            }
            imageinterlace($img, true);
            $ok = @imagejpeg($img, $file, 84);
            imagedestroy($img);
            if (!$ok) return '';
        } elseif (@file_put_contents($file, $raw) === false) {
            return ''; // no image library on the server: keep the original file as is
        }
    }
    return IG_IMG_URL . $code . '.jpg?v=' . filemtime($file);
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
// (a changed selection in config.php invalidates it immediately)
$cache = readJsonFile(IG_CACHE_FILE);
if ($cache && ($cache['key'] ?? '') === $cacheKey && (time() - (int) ($cache['fetched_at'] ?? 0)) < IG_CACHE_TTL) {
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

// ── Posts: the selection from config.php, or the latest ones ──
$fields = 'id,media_type,media_url,thumbnail_url,permalink,timestamp,caption';
$endpoint = $fbMode ? FB_API . '/' . $userId . '/media' : IG_API . '/me/media';
$next = $endpoint . '?fields=' . $fields . '&limit=' . ($wanted ? IG_PAGE : IG_LATEST) . '&access_token=' . rawurlencode($token);

$found = [];   // shortcode => post, in feed order
for ($page = 0; $next && $page < ($wanted ? IG_MAX_PAGES : 1); $page++) {
    $res = getJson($next);
    if (!isset($res['data']) || !is_array($res['data'])) {
        if ($page > 0) break; // keep what the first pages gave us
        // Instagram unreachable or token invalid: keep showing the last good posts
        $cache ? respond(200, ['ok' => true, 'posts' => $cache['posts'], 'stale' => true], 300)
               : respond(502, ['ok' => false, 'error' => 'instagram_unavailable']);
    }
    foreach ($res['data'] as $m) {
        $img = ($m['media_type'] ?? '') === 'VIDEO' ? ($m['thumbnail_url'] ?? '') : ($m['media_url'] ?? '');
        $code = shortcode((string) ($m['permalink'] ?? ''));
        if ($img === '' || $code === '') continue;
        $caption = trim((string) ($m['caption'] ?? ''));
        $found[$code] = [
            'img'  => $img,
            'url'  => $m['permalink'],
            'date' => $m['timestamp'] ?? '',
            'alt'  => mb_substr(preg_replace('/\s+/', ' ', $caption), 0, 120),
        ];
    }
    if ($wanted && !array_diff($wanted, array_keys($found))) break; // all chosen posts found
    $next = $res['paging']['next'] ?? '';
}

$posts = $wanted
    ? array_filter(array_map(fn ($c) => $found[$c] ?? null, array_combine($wanted, $wanted)))   // chosen order
    : $found;

// Serve every image from this server; posts whose image can't be fetched are left out
$keep = [];
foreach ($posts as $code => $p) {
    $local = localThumb((string) $code, $p['img']);
    if ($local === '') continue;
    $p['img'] = $local;
    $keep[] = $p;
    if (!$wanted && count($keep) >= IG_LATEST) break;
}
$posts = $keep;
// remove thumbnails of posts no longer shown
$shown = array_map(fn ($p) => basename(parse_url($p['img'], PHP_URL_PATH)), $posts);
foreach (glob(IG_IMG_DIR . '/*.jpg') ?: [] as $f) {
    if (!in_array(basename($f), $shown, true)) @unlink($f);
}

writeJsonFile(IG_CACHE_FILE, ['key' => $cacheKey, 'fetched_at' => time(), 'posts' => $posts]);
respond(200, ['ok' => true, 'posts' => $posts], 900);
