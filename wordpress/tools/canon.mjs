/**
 * Canonical block serializer.
 * Reads {key: blockSpec[]} from a JSON file, creates the blocks in a running
 * WordPress editor (createBlock) and writes {key: serializedMarkup} — markup that
 * is, by construction, exactly what the editor itself would save (no validation errors).
 *
 * blockSpec = [name, attributes, innerBlockSpecs?]
 * Usage: node canon.mjs <wp-base-url> <in.json> <out.json>
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';

const [, , base, inFile, outFile] = process.argv;
const specs = JSON.parse(readFileSync(inFile, 'utf8'));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.route((u) => !u.href.startsWith(base), (r) => r.abort());
await page.goto(base + '/wp-login.php');
await page.fill('#user_login', 'admin');
await page.fill('#user_pass', 'admin');
await page.click('#wp-submit');
await page.waitForURL(/wp-admin/);
await page.goto(base + '/wp-admin/post-new.php?post_type=page', { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.blocks && wp.blocks.getBlockType('core/accordion'), null, { timeout: 90000 });

const result = await page.evaluate((all) => {
	const out = {};
	const errors = [];
	const make = (spec, path) => {
		const [name, attrs = {}, inner = []] = spec;
		if (!wp.blocks.getBlockType(name)) errors.push(path + ': unknown block ' + name);
		return wp.blocks.createBlock(name, attrs, inner.map((s, i) => make(s, path + '/' + i)));
	};
	for (const [key, list] of Object.entries(all)) {
		const blocks = list.map((s, i) => make(s, key + '#' + i));
		out[key] = wp.blocks.serialize(blocks);
		// Round-trip check: re-parse and verify every block is valid.
		const walk = (bs) => bs.forEach((b) => { if (!b.isValid) errors.push(key + ': invalid after round-trip ' + b.name); walk(b.innerBlocks); });
		walk(wp.blocks.parse(out[key]));
	}
	return { out, errors };
}, specs);

writeFileSync(outFile, JSON.stringify(result.out, null, 1));
if (result.errors.length) {
	console.error(result.errors.join('\n'));
	process.exitCode = 1;
}
console.log('serialized', Object.keys(result.out).length, 'groups');
await browser.close();
