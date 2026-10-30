import type React from 'react';
import type { AnyZodObject } from 'zod';
import {
  ExperienceParadox,
  experienceParadoxDefaults,
  experienceParadoxSchema,
  experienceParadoxTimeline,
  type ExperienceParadoxProps,
} from './ExperienceParadox';

/**
 * Catálogo único de piezas. Lo leen Remotion (Root.tsx), el Motion Studio
 * y el script de render, así que una pieza nueva solo se da de alta aquí.
 */
export type MotionPiece<P extends Record<string, unknown> = any> = {
  id: string;
  number: string;
  title: string;
  /** Frase del guion que acompaña. */
  line: string;
  component: React.FC<P>;
  schema: AnyZodObject;
  defaultProps: P;
  /** Duración en frames calculada a partir de los props (y del pace). */
  duration: (props: P) => number;
  /** Hitos de la coreografía, para sincronizar con la voz en el montaje. */
  marks: (props: P) => { frame: number; label: string }[];
};

const withPace = (frames: number, pace: number) => Math.ceil(frames / (pace || 1));

export const pieces: MotionPiece[] = [
  {
    id: 'ExperienceParadox',
    number: '01',
    title: 'The Experience Paradox',
    line: '«Abres una oferta y te piden dos años de experiencia. Abres otra y te piden tres.»',
    component: ExperienceParadox,
    schema: experienceParadoxSchema,
    defaultProps: experienceParadoxDefaults,
    duration: (p: ExperienceParadoxProps) => withPace(experienceParadoxTimeline(p.cards.length).total, p.pace),
    marks: (p: ExperienceParadoxProps) => {
      const t = experienceParadoxTimeline(p.cards.length);
      const at = (f: number) => Math.round(f / (p.pace || 1));
      return [
        { frame: 0, label: 'Oferta 1' },
        { frame: at(t.enters[1]), label: 'Oferta 2' },
        { frame: at(t.noteAt), label: 'Comentario' },
        ...(t.enters[2] ? [{ frame: at(t.enters[2]), label: 'Pila' }] : []),
        { frame: at(t.exitAt), label: 'Salida' },
      ];
    },
  },
];

/** Piezas del encargo aún no producidas (Fase 4). */
export const upcoming = [
  { number: '02', title: 'Seven Days' },
  { number: '03', title: 'Find Your Direction' },
  { number: '04', title: "Show, Don't Tell" },
  { number: '05', title: 'The Job Search System' },
  { number: '06', title: 'The Interview Framework' },
  { number: '07', title: 'The Final Message' },
];
