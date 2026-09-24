#!/usr/bin/env python3
"""Sonido del guiño final: un «bloop» que sube y un brillo de campanita encima."""
from pathlib import Path
import numpy as np
from scipy.io import wavfile

SR = 48000
n = int(0.7 * SR)
t = np.arange(n) / SR
out = np.zeros(n)

# bloop: seno que sube de 520 a 1250 Hz en 90 ms
nb = int(0.16 * SR)
tb = t[:nb]
f = 520 + 730 * (1 - np.exp(-tb / 0.03))
bloop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tb / 0.05) * np.minimum(1, tb / 0.004)
out[:nb] += bloop * 0.8

# campanita: parciales inarmónicos, entra a los 70 ms
i0 = int(0.07 * SR)
tt = t[: n - i0]
bell = sum(a * np.sin(2 * np.pi * fr * tt) * np.exp(-tt / d)
           for fr, a, d in [(2637, 0.5, 0.22), (3951, 0.3, 0.14), (5274, 0.18, 0.09), (7040, 0.08, 0.05)])
out[i0:] += bell * np.minimum(1, tt / 0.002) * 0.6

out /= np.max(np.abs(out)) / 0.8
dl = int(0.011 * SR)
stereo = np.stack([out, np.concatenate([np.zeros(dl), out[:-dl]])], axis=1)
dst = Path(__file__).resolve().parent.parent / "assets/sfx/guino.wav"
wavfile.write(dst, SR, (stereo * 32767).astype(np.int16))
print(dst)
