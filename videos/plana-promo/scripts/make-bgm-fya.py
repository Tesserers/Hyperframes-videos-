#!/usr/bin/env python3
"""Pista del vídeo con «Fix Your Accent» (Fake Blood), solo para uso interno.

El tema va a 128 BPM y el montaje estaba en una rejilla de 120: el vídeo se acelera
×16/15 (cada tiempo pasa de 0,5 s a 0,46875 s) y la música no se toca.

- El drop del tema (3:46,149) cae en el «plana.» del vídeo (9,375 s reales).
- El corte arranca 20 tiempos antes, en la subida (3:36,774).
- Frenazo de cinta en 4,33 s y en 22,73 s (los del montaje), silencio hasta 23,4375,
  y el tema vuelve en su sitio exacto con el golpe del cierre.
- Se apaga de 29,0 a 30,0 s. Normalizado a -14 LUFS.
"""
from pathlib import Path
import numpy as np
import pyloudnorm as pyln
from scipy.io import wavfile

ROOT = Path(__file__).resolve().parent.parent
SR = 48000
B = 60 / 128
DROP = 226.149
START = DROP - 20 * B
DUR = 30.0

sr, x = wavfile.read(ROOT / "assets/bgm/src/fix-your-accent.wav")
assert sr == SR
x = x.astype(np.float64) / 32768
seg = x[int(START * SR):int(START * SR) + int(DUR * SR)].copy()


def tape_stop(y, t0, dur):
    i0, n = int(t0 * SR), int(dur * SR)
    src = y[i0:i0 + int(dur * SR * 1.05)].copy()
    rate = (1 - np.linspace(0, 1, n)) ** 1.6
    pos = np.cumsum(rate)
    out = np.stack([np.interp(pos, np.arange(len(src)), src[:, c]) for c in range(2)], axis=1)
    y[i0:i0 + n] = out * np.linspace(1, 0.2, n)[:, None]


g = 15 / 16  # rejilla de 120 -> tiempo real a 128
tape_stop(seg, 4.62 * g, 0.38 * g)
tape_stop(seg, 24.25 * g, 0.5 * g)
seg[int(24.75 * g * SR):int(25.0 * g * SR)] = 0

fade = np.ones(len(seg))
i0 = int(29.0 * SR)
fade[i0:] = np.linspace(1, 0, len(seg) - i0) ** 1.5
seg *= fade[:, None]
seg[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]

meter = pyln.Meter(SR)
lufs = meter.integrated_loudness(seg)
seg = pyln.normalize.loudness(seg, lufs, -14.0)
pk = np.max(np.abs(seg))
if pk > 0.95:
    seg = np.tanh(seg / 0.95) * 0.95
print(f"{lufs:.1f} -> {meter.integrated_loudness(seg):.1f} LUFS, pico {np.max(np.abs(seg)):.3f}, desde {START:.3f}s")
wavfile.write(ROOT / "assets/bgm/plana-fix-your-accent.wav", SR, (seg * 32767).astype(np.int16))
