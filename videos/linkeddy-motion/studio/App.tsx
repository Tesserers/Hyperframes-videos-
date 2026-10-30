import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Player, type PlayerRef } from '@remotion/player';
import { brand } from '../src/brand/linkeddy.config';
import { pieces, upcoming, type MotionPiece } from '../src/compositions/registry';

type BgMode = 'transparent' | 'light' | 'dark' | 'video';
type Props = Record<string, any>;

const MULTILINE = ['role', 'unit'];
const STAGE_KEYS = ['background', 'scale', 'offsetY', 'pace', 'accent', 'ink', 'paper'];
const FPS = brand.video.fps;

const framing = [
  { label: 'Pantalla completa', scale: 1, offsetY: 0 },
  { label: 'Overlay bajo', scale: 0.58, offsetY: 340 },
  { label: 'Overlay alto', scale: 0.58, offsetY: -330 },
];

const fieldLabels: Record<string, string> = {
  cards: 'Ofertas',
  kicker: 'Cabecera',
  tag: 'Etiqueta',
  role: 'Puesto',
  years: 'Años',
  unit: 'Requisito',
  note: 'Comentario al margen',
};

const timecode = (frame: number) => {
  const s = Math.floor(frame / FPS);
  const f = frame % FPS;
  return `${String(s).padStart(2, '0')}:${String(f).padStart(2, '0')}`;
};

const clone = <T,>(v: T): T => JSON.parse(JSON.stringify(v));

export const App: React.FC = () => {
  const [pieceId, setPieceId] = useState(pieces[0].id);
  const piece = pieces.find((p) => p.id === pieceId)!;
  const [propsById, setPropsById] = useState<Record<string, Props>>(() =>
    Object.fromEntries(pieces.map((p) => [p.id, clone(p.defaultProps)])),
  );
  const props = propsById[pieceId];
  const setProps = (next: Props) => setPropsById((all) => ({ ...all, [pieceId]: next }));

  const [bg, setBg] = useState<BgMode>('light');
  const [guides, setGuides] = useState(true);
  const [loop, setLoop] = useState(true);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const inputProps = useMemo(
    () => ({ ...props, background: bg === 'light' || bg === 'dark' ? bg : 'transparent' }),
    [props, bg],
  );
  const duration = piece.duration(props);
  const marks = piece.marks(props);

  return (
    <div className="app">
      <header className="top">
        <div className="wordmark">
          Link<span>Eddy</span>
        </div>
        <div className="top-meta">
          <span className="micro">Motion Studio</span>
          <span className="micro dim">1080 × 1920 · {FPS} fps · 9:16</span>
        </div>
      </header>

      <aside className="library">
        <div className="micro dim section-label">Piezas</div>
        <ol>
          {pieces.map((p) => (
            <li key={p.id}>
              <button className={`piece ${p.id === pieceId ? 'active' : ''}`} onClick={() => setPieceId(p.id)}>
                <span className="num">{p.number}</span>
                <span className="name">{p.title}</span>
                <span className="micro dim">{(p.duration(propsById[p.id]) / FPS).toFixed(1)} s</span>
              </button>
            </li>
          ))}
          {upcoming.map((p) => (
            <li key={p.number}>
              <div className="piece pending" aria-disabled>
                <span className="num">{p.number}</span>
                <span className="name">{p.title}</span>
                <span className="micro dim">Fase 4</span>
              </div>
            </li>
          ))}
        </ol>
        <p className="script-line">{piece.line}</p>
      </aside>

      <main className="stage-col">
        <Viewport
          piece={piece}
          inputProps={inputProps}
          duration={duration}
          bg={bg}
          guides={guides}
          loop={loop}
          marks={marks}
          videoUrl={videoUrl}
        />
        <div className="view-options">
          <Segmented
            value={bg}
            onChange={(v) => setBg(v as BgMode)}
            options={[
              ['transparent', 'Transparente'],
              ['light', 'Claro'],
              ['dark', 'Oscuro'],
              ['video', 'Sobre vídeo'],
            ]}
          />
          <label className="toggle">
            <input type="checkbox" checked={guides} onChange={(e) => setGuides(e.target.checked)} />
            <span>Zonas seguras</span>
          </label>
          <label className="toggle">
            <input type="checkbox" checked={loop} onChange={(e) => setLoop(e.target.checked)} />
            <span>Bucle</span>
          </label>
          {bg === 'video' ? (
            <label className="file-btn">
              <input
                type="file"
                accept="video/*"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (f) setVideoUrl(URL.createObjectURL(f));
                }}
              />
              {videoUrl ? 'Cambiar clip' : 'Cargar mi clip'}
            </label>
          ) : null}
        </div>
      </main>

      <aside className="inspector">
        <Section title="Encuadre">
          <div className="chips">
            {framing.map((f) => (
              <button
                key={f.label}
                className={`chip ${props.scale === f.scale && props.offsetY === f.offsetY ? 'on' : ''}`}
                onClick={() => setProps({ ...props, scale: f.scale, offsetY: f.offsetY })}
              >
                {f.label}
              </button>
            ))}
          </div>
          <Slider label="Escala" value={props.scale} min={0.3} max={1.3} step={0.01} onChange={(v) => setProps({ ...props, scale: v })} />
          <Slider label="Posición Y" value={props.offsetY} min={-700} max={700} step={1} unit="px" onChange={(v) => setProps({ ...props, offsetY: v })} />
          <Slider
            label="Ritmo"
            value={props.pace}
            min={0.6}
            max={1.6}
            step={0.01}
            format={(v) => `${v.toFixed(2)}× · ${(duration / FPS).toFixed(2)} s`}
            onChange={(v) => setProps({ ...props, pace: v })}
          />
        </Section>

        <Section title="Color">
          <div className="colors">
            {(['accent', 'ink', 'paper'] as const).map((k) => (
              <label key={k} className="color">
                <input type="color" value={props[k]} onChange={(e) => setProps({ ...props, [k]: e.target.value })} />
                <span className="micro">{{ accent: 'Acento', ink: 'Tinta', paper: 'Papel' }[k]}</span>
                <span className="micro dim">{props[k]}</span>
              </label>
            ))}
          </div>
        </Section>

        <Section title="Textos">
          {Object.keys(props)
            .filter((k) => !STAGE_KEYS.includes(k))
            .map((k) => (
              <Field key={k} name={k} value={props[k]} onChange={(v) => setProps({ ...props, [k]: v })} />
            ))}
          <button className="link-btn" onClick={() => setProps(clone(piece.defaultProps))}>
            Restaurar valores de diseño
          </button>
        </Section>

        <Section title="Exportar">
          <ExportPanel piece={piece} props={props} bg={bg} />
        </Section>
      </aside>
    </div>
  );
};

// ── Visor ─────────────────────────────────────────────────────────────

const Viewport: React.FC<{
  piece: MotionPiece;
  inputProps: Props;
  duration: number;
  bg: BgMode;
  guides: boolean;
  loop: boolean;
  marks: { frame: number; label: string }[];
  videoUrl: string | null;
}> = ({ piece, inputProps, duration, bg, guides, loop, marks, videoUrl }) => {
  const player = useRef<PlayerRef>(null);
  const video = useRef<HTMLVideoElement>(null);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    const p = player.current;
    if (!p) return;
    const onFrame = (e: { detail: { frame: number } }) => setFrame(e.detail.frame);
    const onPlay = () => setPlaying(true);
    const onPause = () => setPlaying(false);
    p.addEventListener('frameupdate', onFrame);
    p.addEventListener('seeked', onFrame);
    p.addEventListener('play', onPlay);
    p.addEventListener('pause', onPause);
    p.addEventListener('ended', onPause);
    return () => {
      p.removeEventListener('frameupdate', onFrame);
      p.removeEventListener('seeked', onFrame);
      p.removeEventListener('play', onPlay);
      p.removeEventListener('pause', onPause);
      p.removeEventListener('ended', onPause);
    };
  }, [piece.id]);

  // El clip de fondo sigue al reproductor (no es parte del render).
  useEffect(() => {
    const v = video.current;
    if (!v) return;
    if (playing) v.play().catch(() => {});
    else {
      v.pause();
      if (v.duration) v.currentTime = (frame / FPS) % v.duration;
    }
  }, [playing, frame, videoUrl]);

  const toggle = useCallback(() => {
    const p = player.current;
    if (!p) return;
    if (p.isPlaying()) p.pause();
    else {
      if (frame >= duration - 1) p.seekTo(0);
      p.play();
    }
  }, [frame, duration]);

  const seek = (f: number) => {
    const clamped = Math.max(0, Math.min(duration - 1, Math.round(f)));
    player.current?.seekTo(clamped);
    setFrame(clamped);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement).closest('input, textarea')) return;
      if (e.code === 'Space') {
        e.preventDefault();
        toggle();
      } else if (e.code === 'ArrowRight') seek(frame + (e.shiftKey ? FPS : 1));
      else if (e.code === 'ArrowLeft') seek(frame - (e.shiftKey ? FPS : 1));
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  return (
    <div className="viewport-wrap">
      <div className={`viewport bg-${bg}`}>
        {bg === 'video' ? (
          videoUrl ? (
            <video ref={video} className="clip" src={videoUrl} muted playsInline loop />
          ) : (
            <div className="fake-shot" aria-hidden>
              <div className="fake-light" />
              <div className="fake-person" />
              <div className="fake-desk" />
              <span className="micro">Plano simulado · carga tu clip para verlo encima</span>
            </div>
          )
        ) : null}
        <Player
          ref={player}
          key={piece.id}
          component={piece.component}
          inputProps={inputProps}
          durationInFrames={duration}
          compositionWidth={brand.video.width}
          compositionHeight={brand.video.height}
          fps={FPS}
          loop={loop}
          controls={false}
          clickToPlay={false}
          acknowledgeRemotionLicense
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', background: 'transparent' }}
        />
        {guides ? <SafeGuides /> : null}
      </div>

      <div className="transport">
        <button className="play" onClick={toggle} aria-label={playing ? 'Pausar' : 'Reproducir'}>
          {playing ? (
            <svg viewBox="0 0 20 20" width="18" height="18">
              <rect x="4" y="3" width="4" height="14" rx="1" fill="currentColor" />
              <rect x="12" y="3" width="4" height="14" rx="1" fill="currentColor" />
            </svg>
          ) : (
            <svg viewBox="0 0 20 20" width="18" height="18">
              <path d="M5 3.5v13l11-6.5z" fill="currentColor" />
            </svg>
          )}
        </button>
        <button className="step" onClick={() => seek(frame - 1)} aria-label="Frame anterior">
          ‹
        </button>
        <button className="step" onClick={() => seek(frame + 1)} aria-label="Frame siguiente">
          ›
        </button>
        <div className="scrub">
          <div className="marks">
            {marks.map((m) => (
              <button
                key={`${m.label}-${m.frame}`}
                className="mark"
                style={{ left: `${(m.frame / (duration - 1)) * 100}%` }}
                onClick={() => seek(m.frame)}
                title={`${m.label} · ${timecode(m.frame)}`}
              >
                <span>{m.label}</span>
              </button>
            ))}
          </div>
          <input
            type="range"
            min={0}
            max={duration - 1}
            value={frame}
            onChange={(e) => seek(Number(e.target.value))}
            style={{ ['--p' as string]: `${(frame / (duration - 1)) * 100}%` }}
          />
        </div>
        <div className="tc">
          <span>{timecode(frame)}</span>
          <span className="dim"> / {timecode(duration - 1)}</span>
          <div className="micro dim">
            f {frame} / {duration - 1}
          </div>
        </div>
      </div>
    </div>
  );
};

/** Zonas de UI de Reels/TikTok y zonas de cara/subtítulos de referencia. */
const SafeGuides: React.FC = () => {
  const { width: W, height: H } = brand.video;
  const s = brand.safe;
  const pct = (v: number, of: number) => `${(v / of) * 100}%`;
  return (
    <div className="guides" aria-hidden>
      <div className="g-ui" style={{ top: 0, left: 0, right: 0, height: pct(s.top, H) }}>
        <span>UI superior</span>
      </div>
      <div className="g-ui" style={{ bottom: 0, left: 0, right: 0, height: pct(s.bottom, H) }}>
        <span>Descripción · audio · CTA</span>
      </div>
      <div className="g-ui g-right" style={{ top: pct(s.top, H), bottom: pct(s.bottom, H), right: 0, width: pct(s.right, W) }} />
      <div className="g-face" style={{ top: pct(330, H), height: pct(560, H), left: pct(300, W), width: pct(480, W) }}>
        <span>Cara (plano medio)</span>
      </div>
      <div className="g-subs" style={{ top: pct(1250, H), height: pct(200, H), left: pct(s.left, W), right: pct(s.right, W) }}>
        <span>Subtítulos</span>
      </div>
    </div>
  );
};

// ── Exportación ───────────────────────────────────────────────────────

type Job = { id: string; piece: string; format: string; progress: number; status: string; file?: string; error?: string };

const formats = [
  { id: 'prores', name: 'ProRes 4444', note: '.mov con alfa · Premiere, Final Cut, DaVinci' },
  { id: 'png', name: 'Secuencia PNG', note: '.zip con alfa · cualquier editor' },
  { id: 'webm', name: 'WebM VP9', note: 'con alfa · web, After Effects' },
  { id: 'mp4', name: 'MP4 preview', note: 'sin alfa · fondo claro u oscuro' },
];

const ExportPanel: React.FC<{ piece: MotionPiece; props: Props; bg: BgMode }> = ({ piece, props, bg }) => {
  const [api, setApi] = useState<boolean | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [copied, setCopied] = useState<string | null>(null);

  useEffect(() => {
    fetch('./api/health')
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => setApi(Boolean(d?.ok)))
      .catch(() => setApi(false));
  }, []);

  const running = jobs.some((j) => j.status === 'running');
  useEffect(() => {
    if (!api) return;
    const tick = () => fetch('./api/jobs').then((r) => r.json()).then(setJobs).catch(() => {});
    tick();
    if (!running) return;
    const t = setInterval(tick, 700);
    return () => clearInterval(t);
  }, [api, running]);

  const exportProps = { ...props, background: bg === 'dark' ? 'dark' : bg === 'light' ? 'light' : 'transparent' };

  const render = async (format: string) => {
    const r = await fetch('./api/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ piece: piece.id, format, props: exportProps }),
    });
    const job = await r.json();
    setJobs((j) => [job, ...j]);
  };

  const downloadProps = () => {
    const blob = new Blob([JSON.stringify(exportProps, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `${piece.id}.props.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const copy = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(text);
      setTimeout(() => setCopied(null), 1400);
    });
  };

  if (api === null) return <p className="micro dim">Comprobando el motor de render…</p>;

  if (api) {
    return (
      <div className="export">
        <div className="formats">
          {formats.map((f) => (
            <button key={f.id} className="format" onClick={() => render(f.id)}>
              <span className="fname">{f.name}</span>
              <span className="micro dim">{f.note}</span>
            </button>
          ))}
        </div>
        <p className="hint">
          Los formatos con alfa ignoran el fondo elegido. El MP4 usa {bg === 'light' ? 'el fondo claro' : 'el fondo oscuro'}.
        </p>
        {jobs.filter((j) => j.piece === piece.id).length ? (
          <ul className="jobs">
            {jobs
              .filter((j) => j.piece === piece.id)
              .map((j) => (
                <li key={j.id}>
                  <span className="micro">{formats.find((f) => f.id === j.format)?.name}</span>
                  {j.status === 'running' ? (
                    <span className="bar">
                      <span style={{ width: `${Math.round(j.progress * 100)}%` }} />
                    </span>
                  ) : j.status === 'done' && j.file ? (
                    <a href={`./renders/${j.file}`} download>
                      Descargar
                    </a>
                  ) : (
                    <span className="err" title={j.error}>
                      Error
                    </span>
                  )}
                </li>
              ))}
          </ul>
        ) : null}
      </div>
    );
  }

  const cmds = formats.map((f) => `node scripts/render.mjs ${piece.id} ${f.id} --props ${piece.id}.props.json`);
  return (
    <div className="export">
      <p className="hint">
        Estás en la versión publicada del Studio: aquí no hay motor de render. En tu ordenador, dentro de
        <code> videos/linkeddy-motion</code>, ejecuta <code>npm run studio</code> y estos botones renderizan de verdad. O descarga
        tus ajustes y lanza el comando:
      </p>
      <button className="format" onClick={downloadProps}>
        <span className="fname">Descargar ajustes (.json)</span>
        <span className="micro dim">textos, colores y encuadre actuales</span>
      </button>
      {cmds.map((c, i) => (
        <button key={c} className="cmd" onClick={() => copy(c)} title="Copiar">
          <span className="micro dim">{formats[i].name}</span>
          <code>{c}</code>
          <span className="micro">{copied === c ? 'Copiado' : 'Copiar'}</span>
        </button>
      ))}
    </div>
  );
};

// ── Controles ─────────────────────────────────────────────────────────

const Section: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <section className="section">
    <h3>{title}</h3>
    {children}
  </section>
);

const Segmented: React.FC<{ value: string; onChange: (v: string) => void; options: [string, string][] }> = ({
  value,
  onChange,
  options,
}) => (
  <div className="segmented">
    {options.map(([v, l]) => (
      <button key={v} className={v === value ? 'on' : ''} onClick={() => onChange(v)}>
        {l}
      </button>
    ))}
  </div>
);

const Slider: React.FC<{
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit?: string;
  format?: (v: number) => string;
  onChange: (v: number) => void;
}> = ({ label, value, min, max, step, unit = '', format, onChange }) => (
  <label className="slider">
    <span className="row">
      <span className="micro">{label}</span>
      <span className="micro dim">{format ? format(value) : `${value}${unit}`}</span>
    </span>
    <input type="range" min={min} max={max} step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} />
  </label>
);

/** Editor genérico: strings, números, objetos y listas de objetos. */
const Field: React.FC<{ name: string; value: any; onChange: (v: any) => void }> = ({ name, value, onChange }) => {
  const label = fieldLabels[name] ?? name;
  if (Array.isArray(value)) {
    return (
      <div className="field-group">
        <div className="micro group-label">{label}</div>
        {value.map((item, i) => (
          <div key={i} className="field-item">
            <div className="item-head">
              <span className="micro dim">
                {String(i + 1).padStart(2, '0')}
              </span>
              {value.length > 2 ? (
                <button className="link-btn" onClick={() => onChange(value.filter((_, j) => j !== i))}>
                  Quitar
                </button>
              ) : null}
            </div>
            <Field name="" value={item} onChange={(v) => onChange(value.map((x, j) => (j === i ? v : x)))} />
          </div>
        ))}
        {value.length < 5 ? (
          <button className="link-btn" onClick={() => onChange([...value, clone(value[value.length - 1])])}>
            + Añadir
          </button>
        ) : null}
      </div>
    );
  }
  if (value && typeof value === 'object') {
    return (
      <div className="field-obj">
        {Object.keys(value).map((k) => (
          <Field key={k} name={k} value={value[k]} onChange={(v) => onChange({ ...value, [k]: v })} />
        ))}
      </div>
    );
  }
  if (typeof value === 'number') {
    return (
      <label className="field">
        <span className="micro">{label}</span>
        <input type="number" min={0} max={9} value={value} onChange={(e) => onChange(Math.max(0, Math.min(9, Number(e.target.value))))} />
      </label>
    );
  }
  const multiline = MULTILINE.includes(name) || String(value).includes('\n');
  return (
    <label className="field">
      <span className="micro">
        {label}
        {multiline ? <span className="dim"> · Intro = salto de línea</span> : null}
      </span>
      {multiline ? (
        <textarea rows={2} value={value} onChange={(e) => onChange(e.target.value)} />
      ) : (
        <input type="text" value={value} onChange={(e) => onChange(e.target.value)} />
      )}
    </label>
  );
};
