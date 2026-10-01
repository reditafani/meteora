/**
 * Creates meteora-events-dist.zip from dist/ (including .htaccess files),
 * ready to upload and extract in cPanel → File Manager → public_html.
 * Uses the system `zip` (macOS/Linux) or PowerShell (Windows).
 */
import { execSync } from 'node:child_process';
import { existsSync, rmSync } from 'node:fs';

const out = 'meteora-events-dist.zip';
if (!existsSync('dist')) {
  console.error('dist/ not found — run `npm run build` first.');
  process.exit(1);
}
if (existsSync(out)) rmSync(out);
try {
  if (process.platform === 'win32') {
    execSync(`powershell -NoProfile -Command "Compress-Archive -Path dist\\* -DestinationPath ${out} -Force"`, { stdio: 'inherit' });
  } else {
    execSync(`cd dist && zip -qr ../${out} . -x "api/config.php"`, { stdio: 'inherit' });
  }
  console.log(`✓ ${out} created. Upload it to public_html and extract.`);
} catch {
  console.error('Could not create the zip automatically. Compress the CONTENTS of dist/ (including hidden .htaccess files) manually.');
  process.exit(1);
}
