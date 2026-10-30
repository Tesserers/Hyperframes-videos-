import React from 'react';
import { AbsoluteFill } from 'remotion';
import { z } from 'zod';
import { zColor } from '@remotion/zod-types';
import { brand } from '../brand/linkeddy.config';
import { PaceProvider } from '../motion/frame';

/**
 * Props comunes a todas las piezas. Cada composición extiende este esquema
 * con sus textos, así Remotion Studio y el Motion Studio pueden editarlos.
 */
export const stageSchema = z.object({
  background: z.enum(['transparent', 'light', 'dark']),
  /** Escala de toda la pieza: 1 = pantalla completa, ~0.65 = overlay. */
  scale: z.number().min(0.3).max(1.3).step(0.01),
  /** Desplazamiento vertical en px (negativo = sube). */
  offsetY: z.number().min(-700).max(700).step(1),
  /** Ritmo: 1 = timing de diseño, <1 más lento, >1 más rápido. */
  pace: z.number().min(0.6).max(1.6).step(0.01),
  accent: zColor(),
  ink: zColor(),
  paper: zColor(),
});

export type StageProps = z.infer<typeof stageSchema>;

export const stageDefaults: StageProps = {
  background: 'light',
  scale: 1,
  offsetY: 0,
  pace: 1,
  accent: brand.colors.accent,
  ink: brand.colors.ink,
  paper: brand.colors.paper,
};

const backgrounds: Record<StageProps['background'], string> = {
  transparent: 'transparent',
  light: brand.colors.ivory,
  dark: brand.colors.night,
};

/**
 * Lienzo 1080×1920. El contenido se diseña siempre a pantalla completa y
 * se reencuadra con scale/offsetY para usarlo como overlay.
 */
export const Stage: React.FC<{
  props: StageProps;
  children: React.ReactNode;
}> = ({ props, children }) => (
  <AbsoluteFill style={{ backgroundColor: backgrounds[props.background] }}>
    <AbsoluteFill
      style={{
        transform: `translateY(${props.offsetY}px) scale(${props.scale})`,
        transformOrigin: '50% 50%',
      }}
    >
      <PaceProvider pace={props.pace}>{children}</PaceProvider>
    </AbsoluteFill>
  </AbsoluteFill>
);
