import { Easing, interpolate } from 'remotion';
import { brand, type Bezier } from '../brand/linkeddy.config';

const curve = (b: Bezier) => Easing.bezier(b[0], b[1], b[2], b[3]);

export const ease = {
  enter: curve(brand.ease.enter),
  settle: curve(brand.ease.settle),
  move: curve(brand.ease.move),
  exit: curve(brand.ease.exit),
  draw: curve(brand.ease.draw),
  linear: (t: number) => t,
};

/** 0→1 entre `start` y `start + duration`, con la curva indicada y clamp. */
export const progress = (
  frame: number,
  start: number,
  duration: number,
  easing: (t: number) => number = ease.enter,
) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    easing,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

export const mix = (from: number, to: number, t: number) => from + (to - from) * t;
