#!/usr/bin/env node
/**
 * Render de piezas LinkEddy.
 *
 *   node scripts/render.mjs <ComposicionId> <formato> [--props props.json] [--out renders/...]
 *
 * Formatos:
 *   mp4     H.264, previsualización SIN transparencia (fondo claro u oscuro)
 *   prores  ProRes 4444 .mov CON canal alfa (Premiere, Final Cut, DaVinci)
 *   png     Secuencia PNG CON transparencia (cualquier editor)
 *   webm    VP9 con alfa (navegador / After Effects con plugin)
 *
 * Imprime líneas "PROGRESS 0.42" y al final "DONE <ruta>" para el Motion Studio.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { bundle } from '@remotion/bundler';
import { renderFrames, renderMedia, selectComposition } from '@remotion/renderer';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [id, format = 'mp4', ...rest] = process.argv.slice(2);
const flag = (name) => {
  const i = rest.indexOf(`--${name}`);
  return i >= 0 ? rest[i + 1] : undefined;
};

if (!id) {
  console.error('Uso: node scripts/render.mjs <ComposicionId> <mp4|prores|png|webm> [--props f.json] [--out ruta]');
  process.exit(1);
}

const userProps = flag('props') ? JSON.parse(fs.readFileSync(flag('props'), 'utf8')) : {};
const alpha = format !== 'mp4';
// Un MP4 no tiene alfa: si piden transparente, se previsualiza sobre oscuro.
const background = alpha ? 'transparent' : userProps.background === 'light' ? 'light' : 'dark';
const inputProps = { ...userProps, background };

const preinstalled = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const browserExecutable = fs.existsSync(preinstalled) ? preinstalled : null;

const ext = { mp4: 'mp4', prores: 'mov', webm: 'webm', png: '' }[format];
if (ext === undefined) {
  console.error(`Formato desconocido: ${format}`);
  process.exit(1);
}
const stamp = new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '');
const out = path.resolve(
  root,
  flag('out') ?? `renders/${id}-${format === 'prores' ? 'prores4444' : format}-${stamp}${ext ? `.${ext}` : ''}`,
);

const serveUrl = await bundle({ entryPoint: path.join(root, 'src/index.ts') });
const composition = await selectComposition({ serveUrl, id, inputProps, browserExecutable });
const onProgress = ({ progress }) => console.log(`PROGRESS ${progress.toFixed(3)}`);

if (format === 'png') {
  fs.mkdirSync(out, { recursive: true });
  await renderFrames({
    serveUrl,
    composition,
    inputProps,
    browserExecutable,
    imageFormat: 'png',
    outputDir: out,
    onStart: () => {},
    onFrameUpdate: (done) => console.log(`PROGRESS ${(done / composition.durationInFrames).toFixed(3)}`),
  });
  // Empaqueta la secuencia en un .zip si hay `zip` disponible.
  const zipped = spawnSync('zip', ['-qr', `${path.basename(out)}.zip`, path.basename(out)], { cwd: path.dirname(out) });
  if (zipped.status === 0) {
    console.log(`DONE ${path.relative(root, out)}.zip`);
    process.exit(0);
  }
} else {
  await renderMedia({
    serveUrl,
    composition,
    inputProps,
    browserExecutable,
    outputLocation: out,
    onProgress,
    ...(format === 'mp4' && { codec: 'h264', crf: 16, imageFormat: 'jpeg', jpegQuality: 95, pixelFormat: 'yuv420p' }),
    ...(format === 'prores' && {
      codec: 'prores',
      proResProfile: '4444',
      imageFormat: 'png',
      pixelFormat: 'yuva444p10le',
    }),
    ...(format === 'webm' && { codec: 'vp9', imageFormat: 'png', pixelFormat: 'yuva420p' }),
  });
}

console.log(`DONE ${path.relative(root, out)}`);
