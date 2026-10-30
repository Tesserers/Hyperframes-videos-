import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import react from '@vitejs/plugin-react';
import { defineConfig, type Plugin } from 'vite';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rendersDir = path.join(root, 'renders');

type Job = { id: string; piece: string; format: string; progress: number; status: 'running' | 'done' | 'error'; file?: string; error?: string };

/**
 * API local de exportación. Solo existe con `npm run studio` (servidor de
 * desarrollo): el Studio publicado como página estática no la tiene y lo dice.
 */
const renderApi = (): Plugin => ({
  name: 'linkeddy-render-api',
  configureServer(server) {
    const jobs = new Map<string, Job>();
    const json = (res: import('node:http').ServerResponse, body: unknown, status = 200) => {
      res.statusCode = status;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(body));
    };

    server.middlewares.use((req, res, next) => {
      const url = (req.url ?? '').split('?')[0];

      if (url === '/api/health') return json(res, { ok: true });
      if (url === '/api/jobs') return json(res, [...jobs.values()].reverse());

      if (url === '/api/render' && req.method === 'POST') {
        let body = '';
        req.on('data', (c) => (body += c));
        req.on('end', () => {
          const { piece, format, props } = JSON.parse(body);
          if (!/^[A-Za-z0-9]+$/.test(piece) || !['mp4', 'prores', 'png', 'webm'].includes(format)) {
            return json(res, { error: 'Petición no válida' }, 400);
          }
          const id = `${Date.now().toString(36)}`;
          fs.mkdirSync(path.join(rendersDir, '.props'), { recursive: true });
          const propsFile = path.join(rendersDir, '.props', `${id}.json`);
          fs.writeFileSync(propsFile, JSON.stringify(props));
          const job: Job = { id, piece, format, progress: 0, status: 'running' };
          jobs.set(id, job);
          const child = spawn(process.execPath, ['scripts/render.mjs', piece, format, '--props', propsFile], { cwd: root });
          let log = '';
          child.stdout.on('data', (d: Buffer) => {
            for (const line of d.toString().split('\n')) {
              const p = line.match(/^PROGRESS ([\d.]+)/);
              if (p) job.progress = Number(p[1]);
              const done = line.match(/^DONE (.+)/);
              if (done) job.file = done[1].replace(/^renders\//, '');
            }
          });
          child.stderr.on('data', (d: Buffer) => (log += d.toString()));
          child.on('close', (code) => {
            job.status = code === 0 ? 'done' : 'error';
            if (code !== 0) job.error = log.split('\n').filter(Boolean).slice(-4).join('\n');
          });
          json(res, job);
        });
        return;
      }

      if (url.startsWith('/renders/')) {
        const file = path.join(rendersDir, decodeURIComponent(url.slice('/renders/'.length)));
        if (!file.startsWith(rendersDir) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return next();
        res.setHeader('Content-Disposition', `attachment; filename="${path.basename(file)}"`);
        return fs.createReadStream(file).pipe(res);
      }

      next();
    });
  },
});

export default defineConfig({
  root: path.join(root, 'studio'),
  base: './',
  publicDir: false,
  plugins: [react(), renderApi()],
  build: { outDir: path.join(root, 'studio/dist'), emptyOutDir: true, assetsInlineLimit: 0 },
  server: { port: 5180, host: true },
});
