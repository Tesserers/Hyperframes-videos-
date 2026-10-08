#!/usr/bin/env python3
"""Pista original para el promo de LT Impulsa, sintetizada aquí mismo (sin descargas).

120 BPM, La menor, progresión Am–F–C–G. La estructura sigue el montaje:
  0–4 s   intro: bombo filtrado + golpes que caen con cada palabra del arranque
  4–6 s   break: pad y subida; medio tiempo de silencio antes del drop
  6–30 s  drop: bombo a negras, palmas en 2 y 4, bajo a contratiempo con sidechain,
          acordes "supersaw" sincopados; arpegio desde el segundo 14
  30–32 s break corto para "Tu mejor aliado."
  32–36 s drop final con el logotipo; 36 s golpe y cola de reverb hasta el final.

  python3 scripts/synth-music.py assets/bgm/lt-track.wav
"""
import sys
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
BEAT = 0.5
LEN = 38.5
N = int(LEN * SR)
rng = np.random.default_rng(7)

def buf():
    return np.zeros(N)

def at(t):
    return int(round(t * SR))

def place(dst, sig, t, gain=1.0):
    i = at(t)
    if i >= N:
        return
    j = min(N, i + len(sig))
    dst[i:j] += sig[: j - i] * gain

def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)

def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)

def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)

def env(n, a, d):
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    na = max(1, int(a * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)

# ── instrumentos ─────────────────────────────────────────────
def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.22)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.004) * 0.35
    return np.tanh((body + click) * 1.6)

def clap():
    n = int(0.35 * SR); t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 900, 5200)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR); e[i:] += np.exp(-(t[: n - i]) / (0.008 if k < 2 else 0.11))
    return noise * e * 0.6

def hat(open_=False):
    n = int((0.16 if open_ else 0.045) * SR)
    x = hp(rng.standard_normal(n), 7500, 4)
    return x * env(n, 0.001, 0.06 if open_ else 0.012) * (0.35 if open_ else 0.28)

def saw(f, n, det=0.0):
    t = np.arange(n) / SR
    ph = (f * (1 + det) * t + rng.random()) % 1.0
    return 2 * ph - 1

def supersaw(freqs, dur, cutoff, a=0.004, d=0.18):
    n = int(dur * SR)
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.012, -0.006, 0, 0.006, 0.012):
            x += saw(f, n, det)
    x /= len(freqs) * 5
    x = lp(x, cutoff, 2)
    return x * env(n, a, d)

def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for f in freqs:
        for det in (-0.004, 0.004):
            x += saw(f, n, det)
    x = lp(x / (len(freqs) * 2), 1400, 2)
    return x * np.minimum(1, t / (dur * 0.6))

def bass(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.35 * lp(saw(f, n), 380)
    return np.tanh(x * 1.3) * env(n, 0.004, dur * 0.7) * 0.8

def pluck(f, dur=0.22):
    n = int(dur * SR)
    x = 0.6 * saw(f, n) + 0.4 * np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR))
    return lp(x, 2600) * env(n, 0.002, 0.07)

def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    seg = int(0.05 * SR)
    for s in range(0, n, seg):
        c = 400 + 7000 * (s / n) ** 2
        out[s:s + seg] = bp(noise[s:s + seg + 0], c * 0.7, min(c * 1.4, 20000))
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (t / dur) ** 2) / SR) * 0.15
    return (out * 0.5 + sweep) * (t / dur) ** 2

def boom():
    n = int(2.2 * SR); t = np.arange(n) / SR
    f = 32 + 70 * np.exp(-t / 0.12)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9)
    return np.tanh(x * 2.0) * 0.9

def hit():
    # golpe de las palabras del arranque: tom grave + ráfaga filtrada
    n = int(0.3 * SR); t = np.arange(n) / SR
    tom = np.sin(2 * np.pi * np.cumsum(90 + 120 * np.exp(-t / 0.03)) / SR) * np.exp(-t / 0.12)
    snap = bp(rng.standard_normal(n), 1500, 6000) * np.exp(-t / 0.03) * 0.5
    return tom + snap

# ── arreglo ──────────────────────────────────────────────────
PROG = [  # (acorde, raíz del bajo) por compás de 2 s
    ([57, 60, 64], 33), ([57, 60, 65], 29), ([55, 60, 64], 36), ([55, 59, 62], 31),
]
drums, bassb, chords, arp, fx, hits = buf(), buf(), buf(), buf(), buf(), buf()

def groove(t0, t1, full=True):
    k, c, h, ho = kick(), clap(), hat(), hat(True)
    t = t0
    while t < t1 - 1e-6:
        b = int(round((t - 0.0) / BEAT))
        place(drums, k, t, 1.0)
        if full and b % 2 == 1:
            place(drums, c, t, 0.9)
        place(drums, ho if full else h, t + BEAT / 2, 0.8)
        place(drums, h, t + BEAT / 4, 0.5); place(drums, h, t + 3 * BEAT / 4, 0.5)
        t += BEAT

def harmony(t0, t1, with_arp=False):
    bar = 2.0
    t = t0
    while t < t1 - 1e-6:
        idx = int(round(t / bar)) % 4
        notes, root = PROG[idx]
        fs = [hz(m) for m in notes]
        # bajo a contratiempo
        for q in range(4):
            place(bassb, bass(hz(root), 0.22), t + q * BEAT + BEAT / 2)
        # acordes sincopados (1, 1.75, 2.5, 3.5 en tiempos)
        for off, d in ((0, 0.22), (0.75, 0.16), (1.5, 0.22), (2.5, 0.16), (3.25, 0.3)):
            place(chords, supersaw(fs + [fs[0] * 2], 0.4, 2600 if with_arp else 2100, d=d), t + off * BEAT)
        if with_arp:
            seq = [notes[0] + 12, notes[1] + 12, notes[2] + 12, notes[1] + 24]
            for s in range(16):
                place(arp, pluck(hz(seq[s % 4])), t + s * BEAT / 4, 0.55 if s % 4 == 0 else 0.4)
        t += bar

# 0–4 · intro
k = kick()
for i in range(8):
    place(drums, k, i * BEAT, 0.8)
for i in range(16):
    place(drums, hat(), i * BEAT / 2 + BEAT / 4, 0.4)
HITS = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.25, 3.5, 3.75]
for tt in HITS:
    place(hits, hit(), tt, 0.9)
    place(chords, supersaw([hz(45), hz(57), hz(64)], 0.3, 1500, d=0.09), tt, 0.7)
place(fx, riser(2.0), 2.0, 0.6)

# 4–6 · break
place(chords, pad([hz(57), hz(60), hz(64), hz(69)], 1.6), 4.0, 1.8)
place(fx, riser(1.9), 3.7, 1.0)

# 6 · drop
place(fx, boom(), 6.0, 1.0)
groove(6.0, 30.0)
harmony(6.0, 14.0)
harmony(14.0, 30.0, with_arp=True)
# relleno de caja antes del segundo 22
for i in range(8):
    place(drums, clap(), 21.0 + i * BEAT / 8, 0.25 + i * 0.08)

# 30–32 · break
place(chords, pad([hz(57), hz(60), hz(64), hz(72)], 2.0), 30.0, 1.8)
place(fx, riser(2.0), 30.0, 0.9)

# 32–36 · drop final + golpe
place(fx, boom(), 32.0, 1.0)
groove(32.0, 36.0)
harmony(32.0, 36.0, with_arp=True)
place(fx, boom(), 36.0, 0.9)
place(chords, supersaw([hz(45), hz(57), hz(60), hz(64), hz(69)], 2.4, 2400, d=0.9), 36.0, 1.1)

# ── mezcla ───────────────────────────────────────────────────
# sidechain: todo lo que no es bombo respira con el bombo
side = np.ones(N)
kick_times = [i * BEAT for i in range(8)] + list(np.arange(6.0, 30.0, BEAT)) + list(np.arange(32.0, 36.0, BEAT))
duck = 1 - 0.75 * np.exp(-np.arange(int(0.3 * SR)) / SR / 0.09)
for kt in kick_times:
    i = at(kt); j = min(N, i + len(duck))
    side[i:j] = np.minimum(side[i:j], duck[: j - i])

def reverb(x, secs=1.8, mix=0.22):
    n = int(secs * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (secs / 5))
    ir = lp(ir, 6000)
    wet = fftconvolve(x, ir)[:N]
    wet /= (np.max(np.abs(wet)) + 1e-9) / (np.max(np.abs(x)) + 1e-9)
    return x * (1 - mix) + wet * mix

def delay(x, t=0.375, fb=0.35, mix=0.25):
    d = at(t); y = x.copy()
    for k in range(1, 5):
        y[d * k:] += x[: N - d * k] * (fb ** k)
    return x * (1 - mix) + y * mix

# el bus de batería del intro va filtrado y se abre en el drop
d_intro = lp(drums[: at(6.0)], 900)
drums[: at(6.0)] = d_intro
mix = (
    drums * 0.72
    + hits * 0.6
    + bassb * side * 0.5
    + hp(reverb(chords, 1.6, 0.25), 120) * side * 0.85
    + delay(reverb(arp, 1.2, 0.2)) * side * 0.5
    + reverb(fx, 2.4, 0.3) * 0.9
)
mix = hp(mix, 28)
# salida: cola de 36 a 38,5
t = np.arange(N) / SR
mix *= np.where(t > 37.2, np.clip(1 - (t - 37.2) / 1.3, 0, 1), 1)
mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.4) * 0.95
stereo = np.stack([mix, np.roll(mix, int(0.0006 * SR)) * 0.98 + mix * 0.02], axis=1)

import wave
out = sys.argv[1] if len(sys.argv) > 1 else "track.wav"
pcm = (np.clip(stereo, -1, 1) * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", out, LEN)
