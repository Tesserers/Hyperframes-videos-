// Empaqueta el Studio en un único HTML autocontenido (JS, CSS y fuentes
// inline) para publicarlo como página. Sin motor de render: solo preview.
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
execSync('npx vite build --config studio/vite.config.ts', { cwd: root, stdio: 'inherit', env: { ...process.env, INLINE: '1' } });
const dist = path.join(root, 'studio/dist');
const html = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
const js = html.match(/<script type="module" crossorigin src="\.\/(assets\/[^"]+)"><\/script>/)[1];
const css = html.match(/<link rel="stylesheet" crossorigin href="\.\/(assets\/[^"]+)">/)[1];
const read = (f) => fs.readFileSync(path.join(dist, f), 'utf8');
const out = `<title>LinkEddy Motion Studio</title>
<style>${read(css)}</style>
<div id="root"></div>
<script type="module">${read(js).replace(/<\/script/gi, '<\\/script')}</script>
`;
const target = process.argv[2] ?? path.join(dist, 'linkeddy-motion-studio.html');
fs.writeFileSync(target, out);
console.log(`${target} · ${(out.length / 1024).toFixed(0)} KB`);
