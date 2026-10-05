/**
 * Exports the original site's content data (src/data/*.ts) to JSON so the theme
 * generator uses exactly the same copy. Image imports become their file paths.
 * Usage (from repo root): node wordpress/tools/export-data.mjs > wordpress/tools/data.json
 */
import { build } from 'esbuild';
import path from 'node:path';

const imgPlugin = {
	name: 'img-paths',
	setup(b) {
		b.onResolve({ filter: /\.(jpe?g|png|webp|avif)$/ }, (args) => ({
			path: path.relative(path.resolve('src/assets/images'), path.resolve(args.resolveDir, args.path.replace(/^@\//, 'src/'))).replace(/\\/g, '/'),
			namespace: 'img',
		}));
		b.onLoad({ filter: /.*/, namespace: 'img' }, (args) => ({ contents: `export default ${JSON.stringify({ src: args.path })};`, loader: 'js' }));
	},
};
const entry = `
export * as bars from './src/data/bars.ts';
export * as cocktails from './src/data/cocktails.ts';
export * as services from './src/data/services.ts';
export * as craft from './src/data/craft.ts';
export * as events from './src/data/events.ts';
export * as destinations from './src/data/destinations.ts';
export * as faq from './src/data/faq.ts';
export * as site from './src/data/site.ts';
`;
const res = await build({
	stdin: { contents: entry, resolveDir: process.cwd(), loader: 'ts' },
	bundle: true, write: false, format: 'esm', platform: 'node',
	plugins: [imgPlugin], tsconfig: 'tsconfig.json', logLevel: 'error',
	define: { 'import.meta.env': '{}', 'import.meta.glob': 'globalThis.__glob' },
});
globalThis.__glob = () => ({});
const mod = await import('data:text/javascript;base64,' + Buffer.from(res.outputFiles[0].text).toString('base64'));
process.stdout.write(JSON.stringify(mod, null, 1));
