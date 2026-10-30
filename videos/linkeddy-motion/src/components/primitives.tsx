import React from 'react';
import { useFrame } from '../motion/frame';
import { brand } from '../brand/linkeddy.config';
import { ease, progress } from '../motion/ease';

/**
 * Revelado por máscara: el contenido sube desde debajo de su propia línea
 * base, como una línea de imprenta que entra en su sitio. Sale hacia arriba.
 */
export const MaskReveal: React.FC<{
  start: number;
  duration?: number;
  exitStart?: number;
  exitDuration?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ start, duration = brand.beat.base, exitStart, exitDuration = brand.beat.short, children, style }) => {
  const frame = useFrame();
  const inP = progress(frame, start, duration, ease.enter);
  const outP = exitStart === undefined ? 0 : progress(frame, exitStart, exitDuration, ease.exit);
  const y = (1 - inP) * 105 - outP * 105;
  return (
    // padding/margin compensan descendentes y acentos para que la máscara no los corte
    <div style={{ overflow: 'hidden', paddingBottom: '0.08em', marginBottom: '-0.08em', ...style }}>
      <div style={{ transform: `translateY(${y}%)`, willChange: 'transform' }}>{children}</div>
    </div>
  );
};

/** Microtipografía en mono: metadatos, etiquetas, contadores. */
export const Micro: React.FC<{
  children: React.ReactNode;
  color?: string;
  size?: number;
  style?: React.CSSProperties;
}> = ({ children, color = brand.colors.grey, size = 22, style }) => (
  <span
    style={{
      fontFamily: brand.fonts.mono,
      fontWeight: 400,
      fontSize: size,
      letterSpacing: brand.type.tracking.mono,
      textTransform: 'uppercase',
      color,
      lineHeight: 1.2,
      ...style,
    }}
  >
    {children}
  </span>
);

/**
 * Contador de rodillo: los dígitos 0…value pasan en vertical y frenan en el
 * valor final. Sirve para cifras que "suben" con intención.
 */
export const RollingNumber: React.FC<{
  value: number;
  start: number;
  duration?: number;
  size: number;
  color: string;
  style?: React.CSSProperties;
}> = ({ value, start, duration = 22, size, color, style }) => {
  const frame = useFrame();
  const p = progress(frame, start, duration, ease.settle);
  const digits = Array.from({ length: value + 1 }, (_, i) => i);
  // la columna empieza en una línea vacía y frena en `value`
  const offset = p * (value + 1);
  return (
    <div
      style={{
        height: size * 0.86,
        overflow: 'hidden',
        fontFamily: brand.fonts.display,
        fontWeight: 600,
        fontSize: size,
        lineHeight: 0.86,
        letterSpacing: brand.type.tracking.display,
        color,
        fontVariantNumeric: 'tabular-nums',
        ...style,
      }}
    >
      <div style={{ transform: `translateY(${-offset * size * 0.86}px)` }}>
        <div style={{ height: size * 0.86 }} />
        {digits.map((d) => (
          <div key={d} style={{ height: size * 0.86 }}>
            {d}
          </div>
        ))}
      </div>
    </div>
  );
};

/** Trazo SVG que se dibuja de 0 a 1 (y opcionalmente se retira). */
export const DrawPath: React.FC<{
  d: string;
  start: number;
  duration?: number;
  stroke: string;
  strokeWidth?: number;
  width: number;
  height: number;
  style?: React.CSSProperties;
}> = ({ d, start, duration = 18, stroke, strokeWidth = 5, width, height, style }) => {
  const frame = useFrame();
  const p = progress(frame, start, duration, ease.draw);
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} style={{ overflow: 'visible', ...style }}>
      <path
        d={d}
        pathLength={1}
        fill="none"
        stroke={stroke}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray="1 1"
        strokeDashoffset={1 - p}
        opacity={p > 0 ? 1 : 0}
      />
    </svg>
  );
};

/** Regla horizontal que crece desde la izquierda. */
export const Rule: React.FC<{
  start: number;
  duration?: number;
  color: string;
  thickness?: number;
  style?: React.CSSProperties;
}> = ({ start, duration = 24, color, thickness = 2, style }) => {
  const frame = useFrame();
  const p = progress(frame, start, duration, ease.move);
  return (
    <div
      style={{
        height: thickness,
        background: color,
        transform: `scaleX(${p})`,
        transformOrigin: '0 50%',
        ...style,
      }}
    />
  );
};
