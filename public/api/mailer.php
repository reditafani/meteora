<?php
/**
 * Minimal, dependency-free mail transport: SMTP (SSL/STARTTLS + AUTH LOGIN) or PHP mail().
 * Kept deliberately small so the site needs no Composer install on shared hosting.
 */
declare(strict_types=1);

final class MeteoraMailer
{
    /** @param array<string,mixed> $cfg */
    public function __construct(private array $cfg) {}

    /**
     * @param array<string,string> $inline image URL used in $html => local file. Each URL
     *   found in $html is swapped for an image carried inside the email itself (cid:), so
     *   it shows even when the mail program does not download images from the web.
     */
    public function send(string $to, string $subject, string $text, string $html, ?string $replyTo = null, array $inline = []): bool
    {
        $boundary = 'b_' . bin2hex(random_bytes(12));
        $parts = [];
        foreach ($inline as $url => $file) {
            $data = str_contains($html, $url) && is_file($file) ? @file_get_contents($file) : false;
            if ($data === false) {
                continue;
            }
            $cid = 'img' . count($parts) . '.' . bin2hex(random_bytes(6)) . '@meteoraevents.com';
            $html = str_replace($url, 'cid:' . $cid, $html);
            $parts[] = ['cid' => $cid, 'name' => basename($file), 'data' => $data];
        }
        $fromEmail = (string) $this->cfg['from_email'];
        $fromName = (string) $this->cfg['from_name'];
        $headers = [
            'From' => $this->encodeName($fromName) . " <{$fromEmail}>",
            'MIME-Version' => '1.0',
            'Content-Type' => "multipart/alternative; boundary=\"{$boundary}\"",
            'X-Mailer' => 'MeteoraEvents/1.0',
            'Date' => date('r'),
            'Message-ID' => '<' . bin2hex(random_bytes(10)) . '@' . substr(strrchr($fromEmail, '@') ?: '@localhost', 1) . '>',
        ];
        if ($replyTo) {
            $headers['Reply-To'] = $replyTo;
        }
        $htmlPart = "Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
            . chunk_split(base64_encode($html));
        if ($parts) {
            // multipart/alternative { text, multipart/related { html, images } }
            $rel = 'r_' . bin2hex(random_bytes(12));
            $related = "--{$rel}\r\n" . $htmlPart;
            foreach ($parts as $p) {
                $related .= "--{$rel}\r\n"
                    . "Content-Type: image/png; name=\"{$p['name']}\"\r\n"
                    . "Content-Transfer-Encoding: base64\r\n"
                    . "Content-ID: <{$p['cid']}>\r\n"
                    . "Content-Disposition: inline; filename=\"{$p['name']}\"\r\n\r\n"
                    . chunk_split(base64_encode($p['data']));
            }
            $htmlPart = "Content-Type: multipart/related; type=\"text/html\"; boundary=\"{$rel}\"\r\n\r\n"
                . $related . "--{$rel}--\r\n";
        }
        $body = "--{$boundary}\r\n"
            . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
            . chunk_split(base64_encode($text))
            . "--{$boundary}\r\n"
            . $htmlPart
            . "--{$boundary}--\r\n";
        $encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

        if (($this->cfg['transport'] ?? 'mail') === 'smtp') {
            return $this->smtp($to, $encSubject, $headers, $body);
        }
        $h = '';
        foreach ($headers as $k => $v) {
            $h .= "{$k}: {$v}\r\n";
        }
        return mail($to, $encSubject, $body, rtrim($h), '-f' . $fromEmail);
    }

    private function encodeName(string $name): string
    {
        return '=?UTF-8?B?' . base64_encode($name) . '?=';
    }

    /** @param array<string,string> $headers */
    private function smtp(string $to, string $subject, array $headers, string $body): bool
    {
        $host = (string) $this->cfg['smtp_host'];
        $port = (int) $this->cfg['smtp_port'];
        $secure = (string) ($this->cfg['smtp_secure'] ?? '');
        $timeout = (int) ($this->cfg['smtp_timeout'] ?? 15);
        $remote = ($secure === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
        $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
        $fp = @stream_socket_client($remote, $errno, $errstr, $timeout, STREAM_CLIENT_CONNECT, $ctx);
        if (!$fp) {
            error_log("[meteora] SMTP connect failed: {$errstr} ({$errno})");
            return false;
        }
        stream_set_timeout($fp, $timeout);
        try {
            $this->expect($fp, 220);
            $ehlo = $_SERVER['SERVER_NAME'] ?? 'localhost';
            $this->cmd($fp, "EHLO {$ehlo}", 250);
            if ($secure === 'tls') {
                $this->cmd($fp, 'STARTTLS', 220);
                if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT | STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT)) {
                    throw new RuntimeException('STARTTLS failed');
                }
                $this->cmd($fp, "EHLO {$ehlo}", 250);
            }
            if (!empty($this->cfg['smtp_user'])) {
                $this->cmd($fp, 'AUTH LOGIN', 334);
                $this->cmd($fp, base64_encode((string) $this->cfg['smtp_user']), 334);
                $this->cmd($fp, base64_encode((string) $this->cfg['smtp_pass']), 235);
            }
            $this->cmd($fp, 'MAIL FROM:<' . $this->cfg['from_email'] . '>', 250);
            $this->cmd($fp, "RCPT TO:<{$to}>", [250, 251]);
            $this->cmd($fp, 'DATA', 354);
            $data = "To: <{$to}>\r\nSubject: {$subject}\r\n";
            foreach ($headers as $k => $v) {
                $data .= "{$k}: {$v}\r\n";
            }
            $data .= "\r\n" . $body;
            // Dot-stuffing
            $data = preg_replace('/^\./m', '..', $data) ?? $data;
            fwrite($fp, $data . "\r\n.\r\n");
            $this->expect($fp, 250);
            $this->cmd($fp, 'QUIT', 221);
            return true;
        } catch (Throwable $e) {
            error_log('[meteora] SMTP error: ' . $e->getMessage());
            return false;
        } finally {
            fclose($fp);
        }
    }

    /** @param resource $fp @param int|int[] $code */
    private function cmd($fp, string $line, int|array $code): void
    {
        fwrite($fp, $line . "\r\n");
        $this->expect($fp, $code);
    }

    /** @param resource $fp @param int|int[] $code */
    private function expect($fp, int|array $code): void
    {
        $codes = (array) $code;
        $resp = '';
        while (($line = fgets($fp, 515)) !== false) {
            $resp .= $line;
            if (isset($line[3]) && $line[3] === ' ') {
                break;
            }
        }
        $got = (int) substr($resp, 0, 3);
        if (!in_array($got, $codes, true)) {
            throw new RuntimeException('Unexpected SMTP response: ' . trim($resp));
        }
    }
}
