import React from 'react';
import { AbsoluteFill } from 'remotion';
import { z } from 'zod';
import { brand } from '../brand/linkeddy.config';
import { Stage, stageDefaults, stageSchema } from '../components/Stage';
import { DrawPath, MaskReveal, Micro, RollingNumber, Rule } from '../components/primitives';
import { ease, mix, progress } from '../motion/ease';
import { useFrame } from '../motion/frame';

/**
 * 01 — THE EXPERIENCE PARADOX
 * «Abres una oferta y te piden dos años de experiencia. Abres otra y te piden tres.»
 *
 * Ofertas que se apilan como una torre de índice: cada una empuja a la anterior
 * hacia atrás y deja asomar su título. La ironía la pone un comentario al margen,
 * como el que harías con boli sobre un papel impreso.
 */

const cardSchema = z.object({
  kicker: z.string(),
  tag: z.string(),
  role: z.string(),
  years: z.number().int().min(0).max(9),
  unit: z.string(),
});

export const experienceParadoxSchema = stageSchema.extend({
  cards: z.array(cardSchema).min(2).max(5),
  /** Comentario al margen sobre la segunda oferta. */
  note: z.string(),
});

export type ExperienceParadoxProps = z.infer<typeof experienceParadoxSchema>;

export const experienceParadoxDefaults: ExperienceParadoxProps = {
  ...stageDefaults,
  cards: [
    { kicker: 'Oferta 0147 · Madrid', tag: 'Nueva', role: 'Junior\nPosition', years: 2, unit: 'Years of\nexperience' },
    { kicker: 'Oferta 0148 · Remoto', tag: 'Nueva', role: 'Internship', years: 3, unit: 'Years of\nexperience' },
    { kicker: 'Oferta 0151 · Barcelona', tag: 'Urgente', role: 'Trainee', years: 4, unit: 'Years of\nexperience' },
    { kicker: 'Oferta 0153 · Valencia', tag: 'Top', role: 'Entry level', years: 5, unit: 'Years of\nexperience' },
  ],
  note: '¿Becario… con 3 años?',
};

// ── Timeline (frames a pace 1) ─────────────────────────────────────────
const CARD_IN = 22;
const PILE_IN = 14;
const PUSH = 26;
const COLLAPSE = 14;
const EXIT = 22;

export const experienceParadoxTimeline = (cardCount: number) => {
  const enters = [0, 48];
  const noteAt = 86;
  let t = 128;
  for (let i = 2; i < cardCount; i++) {
    enters.push(t);
    t += 14;
  }
  const lastEnter = enters[enters.length - 1];
  const exitAt = Math.max(lastEnter + 40, cardCount > 2 ? 0 : 150);
  return { enters, noteAt, exitAt, total: exitAt + 10 + EXIT + 2 };
};

// ── Geometría ──────────────────────────────────────────────────────────
const W = 860;
const H = 600;
const LEFT = (1080 - W) / 2;
const TOP = 760;
const PAD = 54;
const RADIUS = 30;
/**
 * Cuánto sube una oferta por cada oferta que se le pone encima. La primera
 * sube lo justo para que su título quede entero a la vista; el resto solo
 * deja asomar la cabecera, como pestañas de un archivador.
 */
const pushFor = (index: number, depth: number) => {
  const first = index === 0 ? 340 : 100;
  return first * Math.min(1, depth) + 100 * Math.max(0, depth - 1);
};
const tilt = [-2.4, 2.1, -1.4, 1.6, -0.8];
const shiftX = [-22, 30, -12, 18, 0];

const JobCard: React.FC<{
  index: number;
  card: ExperienceParadoxProps['cards'][number];
  props: ExperienceParadoxProps;
  enter: number;
  depth: number;
  /** 0→1: la pila se cuadra antes de salir. */
  collapse: number;
  annotate?: { at: number; note: string };
}> = ({ index, card, props, enter, depth, collapse, annotate }) => {
  const frame = useFrame();
  const pile = index >= 2;
  const inDur = pile ? PILE_IN : CARD_IN;
  const p = progress(frame, enter, inDur, ease.enter);
  if (frame < enter) return null;

  // cascada interna: más comprimida en las ofertas de la pila
  const k = pile ? 0.45 : 1;
  const at = (offset: number) => enter + offset * k;

  const d = depth * (1 - collapse);
  const scale = Math.pow(0.93, d);
  const y = TOP + (1 - p) * 150 - pushFor(index, d);
  const rot = mix(tilt[index] * 2.6, tilt[index], p) * (1 - collapse * 0.5);
  const clipBottom = (1 - p) * 100;
  const dim = Math.min(0.2, depth * 0.07);
  const lines = card.role.split('\n');
  const unitLines = card.unit.split('\n');
  const titleSize = lines.length > 1 ? 118 : 128;

  return (
    <div
      style={{
        position: 'absolute',
        left: LEFT + shiftX[index],
        top: y,
        width: W,
        height: H,
        transform: `rotate(${rot}deg) scale(${scale})`,
        transformOrigin: '50% 0%',
        zIndex: 10 + index,
      }}
    >
      {/* Sombra en una capa propia para que la máscara de entrada no la recorte. */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: RADIUS,
          boxShadow: `0 40px 80px -30px rgba(20,18,15,0.45), 0 2px 0 rgba(20,18,15,0.06)`,
          opacity: Math.pow(p, 3),
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: RADIUS,
          background: props.paper,
          color: props.ink,
          overflow: 'hidden',
          clipPath: `inset(0 0 ${clipBottom}% 0 round ${RADIUS}px)`,
        }}
      >
        {/* cabecera de la oferta */}
        <div style={{ position: 'absolute', left: PAD, right: PAD, top: PAD - 6 }}>
          <MaskReveal start={at(5)} duration={16}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Micro color={props.ink} style={{ opacity: 0.62 }}>
                {card.kicker}
              </Micro>
              <span style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{ width: 12, height: 12, borderRadius: 6, background: props.accent }} />
                <Micro color={props.ink}>{card.tag}</Micro>
              </span>
            </div>
          </MaskReveal>
          <Rule start={at(7)} duration={26} color={props.ink} thickness={2} style={{ marginTop: 22, opacity: 0.14 }} />
        </div>

        {/* puesto */}
        <div style={{ position: 'absolute', left: PAD - 4, top: 136 }}>
          {lines.map((line, i) => (
            <MaskReveal key={i} start={at(8 + i * 4)} duration={22}>
              <div
                style={{
                  fontFamily: brand.fonts.display,
                  fontWeight: 700,
                  fontSize: titleSize,
                  lineHeight: 0.9,
                  letterSpacing: brand.type.tracking.display,
                  textTransform: 'uppercase',
                }}
              >
                {line}
              </div>
            </MaskReveal>
          ))}
        </div>

        {/* requisito */}
        <div
          style={{
            position: 'absolute',
            left: PAD - 6,
            right: PAD,
            bottom: PAD - 8,
            display: 'flex',
            alignItems: 'flex-end',
            gap: 26,
          }}
        >
          <RollingNumber value={card.years} start={at(16)} duration={pile ? 14 : 26} size={210} color={props.accent} />
          <div style={{ paddingBottom: 14 }}>
            <MaskReveal start={at(18)} duration={16}>
              <Micro color={props.ink} size={20} style={{ opacity: 0.55 }}>
                Requisito mínimo
              </Micro>
            </MaskReveal>
            <div style={{ height: 10 }} />
            {unitLines.map((line, i) => (
              <MaskReveal key={i} start={at(20 + i * 3)} duration={18}>
                <div
                  style={{
                    fontFamily: brand.fonts.display,
                    fontWeight: 600,
                    fontSize: 46,
                    lineHeight: 0.98,
                    letterSpacing: brand.type.tracking.title,
                    textTransform: 'uppercase',
                  }}
                >
                  {line}
                </div>
              </MaskReveal>
            ))}
          </div>
        </div>

        {/* la oferta retrocede: se oscurece un poco al quedar debajo */}
        <AbsoluteFill style={{ background: props.ink, opacity: dim, pointerEvents: 'none' }} />
      </div>

      {annotate ? <Annotation at={annotate.at} note={annotate.note} props={props} depth={depth + collapse} /> : null}
    </div>
  );
};

/**
 * Marginalia: círculo a mano alrededor de la cifra y comentario en cursiva.
 * Vive en el espacio de la tarjeta, así que la acompaña cuando retrocede.
 */
const Annotation: React.FC<{
  at: number;
  note: string;
  props: ExperienceParadoxProps;
  depth: number;
}> = ({ at, note, props, depth }) => {
  const frame = useFrame();
  const words = note.split(' ');
  const fade = 1 - Math.min(1, depth * 1.6);
  if (fade <= 0) return null;
  // trazo imperfecto: no cierra del todo, como hecho con boli
  const ring =
    'M 120 12 C 50 2, 4 60, 10 128 C 16 200, 80 232, 136 220 C 196 206, 214 136, 196 74 C 182 30, 146 8, 84 22';
  const arrow = 'M 170 574 C 194 622, 244 652, 322 664 M 298 646 L 324 665 L 296 680';
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: W, height: H, opacity: fade, zIndex: 2, pointerEvents: 'none' }}>
      <DrawPath
        d={ring}
        start={at}
        duration={18}
        stroke={props.accent}
        strokeWidth={6}
        width={210}
        height={232}
        style={{ position: 'absolute', left: 6, top: 350 }}
      />
      <DrawPath
        d={arrow}
        start={at + 12}
        duration={14}
        stroke={props.accent}
        strokeWidth={4}
        width={W}
        height={H + 100}
        style={{ position: 'absolute', left: 0, top: 0 }}
      />
      <div
        style={{
          position: 'absolute',
          left: 338,
          top: H + 34,
          display: 'flex',
          flexWrap: 'wrap',
          gap: '0 0.26em',
          width: 600,
          fontFamily: brand.fonts.serif,
          fontStyle: 'italic',
          fontSize: 68,
          lineHeight: 1,
          color: props.accent,
          letterSpacing: '-0.01em',
          transform: 'rotate(-2deg)',
        }}
      >
        {words.map((w, i) => (
          <MaskReveal key={i} start={at + 16 + i * 3} duration={18}>
            {w}
          </MaskReveal>
        ))}
      </div>
    </div>
  );
};

export const ExperienceParadox: React.FC<ExperienceParadoxProps> = (props) => (
  <Stage props={props}>
    <Scene {...props} />
  </Stage>
);

const Scene: React.FC<ExperienceParadoxProps> = (props) => {
  const frame = useFrame();
  const { enters, noteAt, exitAt } = experienceParadoxTimeline(props.cards.length);
  const n = props.cards.length;

  // Salida: la pila se cuadra y se desliza hacia arriba a través de una
  // máscara fija, como si entrara por una ranura.
  const collapse = progress(frame, exitAt, COLLAPSE, ease.move);
  const exitP = progress(frame, exitAt + 10, EXIT, ease.exit);
  const maskTop = exitP > 0 ? TOP - 70 : -2000;

  return (
    <AbsoluteFill style={{ clipPath: `inset(${maskTop}px -200px -400px -200px)` }}>
      <AbsoluteFill style={{ transform: `translateY(${-exitP * 760}px)` }}>
        {props.cards.map((card, i) => {
          // profundidad continua: cuántas ofertas (en fracción) tiene encima
          let depth = 0;
          for (let j = i + 1; j < n; j++) depth += progress(frame, enters[j], PUSH, ease.move);
          return (
            <JobCard
              key={i}
              index={i}
              card={card}
              props={props}
              enter={enters[i]}
              depth={depth}
              collapse={collapse}
              annotate={i === 1 && props.note ? { at: noteAt, note: props.note } : undefined}
            />
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
