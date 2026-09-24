#!/usr/bin/env python3
"""Banda sonora de Plana, sintetizada aquí mismo (no hay forma de descargar música
en este entorno). 120 BPM, compás de 2 s, progresión Am–F–C–G.

Todo está en la rejilla del vídeo: cada corte del montaje cae en un tiempo, y los
golpes grandes (5 s, 10 s, 18 s, 25 s, 28 s) son los cambios de escena.

    python3 scripts/make-music.py   ->  assets/bgm/plana-bed.wav (48 kHz, estéreo)
"""
import subprocess
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve

SR = 48000
BPM = 120
BEAT = 60 / BPM
DUR = 30.0
N = int(DUR * SR)
rng = np.random.default_rng(22071997)
ROOT = Path(__file__).resolve().parent.parent


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def t_of(n):
    return np.arange(n) / SR


def env_exp(n, tau):
    return np.exp(-t_of(n) / tau)


def adsr(n, a=0.005, r=0.05):
    e = np.ones(n)
    na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    na, nr = min(na, n), min(nr, n)
    e[:na] = np.linspace(0, 1, na)
    e[n - nr:] *= np.linspace(1, 0, nr)
    return e


def saw(freq, n, phase0=0.0):
    """Sierra con polyBLEP (sin aliasing audible)."""
    dt = freq / SR
    ph = (phase0 + np.cumsum(np.full(n, dt))) % 1.0
    y = 2 * ph - 1
    m = ph < dt
    x = ph[m] / dt
    y[m] -= x + x - x * x - 1
    m = ph > 1 - dt
    x = (ph[m] - 1) / dt
    y[m] -= x * x + x + x + 1
    return y


def square(freq, n):
    return np.sign(np.sin(2 * np.pi * freq * t_of(n))) * 0.8 + 0.2 * np.sin(2 * np.pi * freq * t_of(n))


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR * 0.45), "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def lp_sweep(x, cut_fn, block=256):
    """Pasa-bajos con la frecuencia de corte en función del tiempo (segundos)."""
    out = np.zeros_like(x)
    sos = butter(2, 1000, "low", fs=SR, output="sos")
    zi = sosfilt_zi(sos) * 0
    for i in range(0, len(x), block):
        fc = float(np.clip(cut_fn(i / SR), 40, SR * 0.45))
        sos = butter(2, fc, "low", fs=SR, output="sos")
        out[i:i + block], zi = sosfilt(sos, x[i:i + block], zi=zi)
    return out


def place(buf, sig, t0, gain=1.0):
    i = int(round(t0 * SR))
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


# ---------------------------------------------------------------- instrumentos
def kick(big=False):
    n = int((0.9 if big else 0.42) * SR)
    t = t_of(n)
    f = 44 + 120 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, 0.30 if big else 0.16)
    click = hp(rng.standard_normal(n), 2500) * env_exp(n, 0.004) * 0.35
    return np.tanh((body + click) * 1.6) * 0.9


def clap():
    n = int(0.45 * SR)
    nz = rng.standard_normal(n)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR)
        e[i:] += env_exp(n - i, 0.006 if k < 2 else 0.11)
    return bp(nz, 900, 4200) * e * 0.9


def hat(open_=False):
    n = int((0.26 if open_ else 0.05) * SR)
    return hp(rng.standard_normal(n), 7500, 4) * env_exp(n, 0.07 if open_ else 0.012)


def crash():
    n = int(2.4 * SR)
    return hp(rng.standard_normal(n), 3500, 2) * env_exp(n, 0.55) * 0.55


def boom():
    n = int(2.2 * SR)
    t = t_of(n)
    f = 32 + 60 * np.exp(-t / 0.12)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.7)


def supersaw(midi, n, voices=5, spread=0.14):
    out = np.zeros(n)
    for v in range(voices):
        det = (v - (voices - 1) / 2) / ((voices - 1) / 2) * spread
        out += saw(mtof(midi + det), n, rng.random())
    return out / voices


def riser(n):
    t = t_of(n)
    d = n / SR
    nz = rng.standard_normal(n)
    out = np.zeros(n)
    blk = 512
    for i in range(0, n, blk):
        k = i / n
        lo = 400 + 5000 * k ** 2
        out[i:i + blk] = bp(nz[max(0, i - 2048):i + blk], lo, lo * 1.6)[-len(out[i:i + blk]):]
    sweep = np.sin(2 * np.pi * np.cumsum(220 + 1400 * (t / d) ** 2) / SR) * 0.18
    return (out * 0.8 + sweep) * (t / d) ** 2


# ---------------------------------------------------------------- partitura
PROG = [  # (acorde, raíz del bajo)
    ((57, 60, 64, 69), 45),   # Am
    ((57, 60, 65, 69), 41),   # F
    ((55, 60, 64, 67), 36),   # C
    ((55, 59, 62, 67), 43),   # G
]


def chord_at(t):
    return PROG[int(t // (4 * BEAT)) % 4]


drums = np.zeros(N)
kick_bus = np.zeros(N)
bass = np.zeros(N)
pad = np.zeros(N)
stabs = np.zeros(N)
arp = np.zeros(N)
fx = np.zeros(N)
kick_times = []

beats = int(DUR / BEAT)
for b in range(beats):
    t = b * BEAT
    # --- bombo
    if t < 24.99:
        if not (9.5 <= t < 10.0) and not (4.75 <= t < 5.0):
            if t < 5.0 and t >= 0:
                kick_times.append((t, 0.75))
            else:
                kick_times.append((t, 1.0))
    elif t < 28.0:
        if b % 2 == 0:
            kick_times.append((t, 0.85))
    # --- palmada en 2 y 4 desde el 5
    if 5.0 <= t < 9.5 or 10.0 <= t < 25.0:
        if b % 2 == 1:
            place(drums, clap(), t, 0.55)
    if 25.0 <= t < 28.0 and b % 4 == 2:
        place(drums, clap(), t, 0.5)
    # --- charles
    for s in range(4):
        ts = t + s * BEAT / 4
        if ts >= 29.0:
            continue
        if ts < 5.0:
            if s == 2:
                place(drums, hat(), ts, 0.30 + 0.25 * ts / 5)
        elif 9.5 <= ts < 10.0:
            continue
        elif ts < 25.0:
            if s == 2:
                place(drums, hat(open_=(b % 2 == 1 and ts >= 10)), ts, 0.28)
            else:
                place(drums, hat(), ts, 0.16 if s % 2 else 0.22)
        elif s == 2:
            place(drums, hat(), ts, 0.2)

for t, g in kick_times:
    place(kick_bus, kick(), t, g)

# golpes grandes en los cambios de escena
for t in (10.0, 25.0, 28.0):
    place(kick_bus, kick(big=True), t, 1.0)
    place(fx, boom(), t, 0.55)
    place(fx, crash(), t, 0.5)
for t in (5.0, 18.0, 20.5, 23.0):
    place(fx, crash(), t, 0.32)
place(fx, crash(), 2.5, 0.22)

# redoble de caja 9.0–9.75 acelerando
t = 9.0
step = BEAT / 2
while t < 9.75:
    place(drums, clap(), t, 0.25 + 0.5 * (t - 9.0) / 0.75)
    t += step
    step = max(BEAT / 8, step * 0.72)

# subidas
place(fx, riser(int(1.5 * SR)), 3.5, 0.5)
place(fx, riser(int(1.25 * SR)), 8.5, 0.6)
place(fx, riser(int(1.0 * SR)), 24.0, 0.35)

# --- bajo: corcheas con octava, entra en el 2,5
for b8 in range(int(DUR / (BEAT / 2))):
    t = b8 * BEAT / 2
    if t < 2.5 or 9.75 <= t < 10.0 or t >= 28.0:
        continue
    if 25.0 <= t < 28.0 and b8 % 2:
        continue
    _, root = chord_at(t)
    m = root + (12 if b8 % 2 else 0)
    n = int(BEAT / 2 * SR * 0.92)
    s = saw(mtof(m), n) * 0.6 + np.sin(2 * np.pi * mtof(m - 12) * t_of(n)) * 0.5
    s = lp(s, 700 if t >= 10 else 450) * adsr(n, 0.003, 0.03)
    place(bass, s, t, 0.55 if t < 5 else 0.7)

# --- colchón: supersierra por compás, filtro que se abre en la intro
for bar in range(int(DUR / (4 * BEAT))):
    t = bar * 4 * BEAT
    notes, _ = chord_at(t)
    n = int(4 * BEAT * SR)
    s = sum(supersaw(m, n) for m in notes) / len(notes)
    place(pad, s * adsr(n, 0.02, 0.08), t)


def pad_cut(t):
    if t < 5.0:
        return 350 + 2600 * (t / 5.0) ** 2
    if t < 10.0:
        return 1800
    if t < 25.0:
        return 4200
    return max(500, 4200 - 1400 * (t - 25.0))


pad = lp_sweep(pad, pad_cut)

# --- stabs: acordes cortos en cada palabra que entra
STAB_T = [0.0, 0.5, 1.0, 1.5, 2.5, 5.0, 6.5, 8.0, 10.0, 10.75, 12.0, 14.0, 16.0,
          18.0, 20.5, 23.0, 25.0, 28.0]
for ts in STAB_T:
    notes, _ = chord_at(ts)
    ln = 0.6 if ts in (10.0, 25.0, 28.0) else 0.22
    n = int(ln * SR)
    s = sum(supersaw(m + 12, n, 3, 0.1) for m in notes) / len(notes)
    s = lp(s, 5200) * env_exp(n, ln * 0.45) * adsr(n, 0.002, 0.02)
    place(stabs, s, ts, 0.55 if ts >= 5 else 0.35)

# --- arpegio de semicorcheas en la parte grande (10–25) y suave en el cierre
for s16 in range(int(DUR / (BEAT / 4))):
    t = s16 * BEAT / 4
    if not (10.0 <= t < 25.0 or 25.0 <= t < 29.0):
        continue
    notes, _ = chord_at(t)
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    m = notes[pattern[s16 % 8]] + 12
    n = int(0.16 * SR)
    s = lp(square(mtof(m), n), 3800) * env_exp(n, 0.045)
    place(arp, s, t, 0.16 if t < 25.0 else 0.11 * max(0.0, 1 - (t - 25.0) / 4))

# ---------------------------------------------------------------- mezcla
# sidechain: todo lo melódico respira con el bombo
duck = np.ones(N)
for t, g in kick_times + [(10.0, 1.0), (25.0, 1.0), (28.0, 1.0)]:
    i = int(t * SR)
    n = int(0.32 * SR)
    j = min(N, i + n)
    curve = 1 - 0.62 * g * np.exp(-t_of(j - i) / 0.09)
    duck[i:j] = np.minimum(duck[i:j], curve)


def reverb_ir(seconds, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    return r.standard_normal(n) * np.exp(-t_of(n) / (seconds / 5)) * 0.03


def stereo_reverb(x, seconds=1.6):
    return (fftconvolve(x, reverb_ir(seconds, 1))[:N], fftconvolve(x, reverb_ir(seconds, 2))[:N])


melodic = pad * 0.30 + bass * 1.0 + stabs * 0.9 + arp * 1.0
melodic = hp(melodic, 35) * duck
send = hp(pad * 0.3 + stabs * 0.9 + arp + drums * 0.25, 250)
rv_l, rv_r = stereo_reverb(send)

# pequeño ensanche del colchón y el arpegio
dly = int(0.013 * SR)
wide = np.concatenate([np.zeros(dly), (pad * 0.3 + arp)[:-dly]]) * duck

L = melodic + kick_bus + drums + fx + rv_l * 0.9 + wide * 0.25
R = melodic + kick_bus + drums + fx + rv_r * 0.9 - wide * 0.25 + (pad * 0.3 + arp) * duck * 0.25
mix = np.stack([L, R], axis=1)

# final: se apaga del 29,0 al 30,0
fade = np.ones(N)
i0 = int(29.0 * SR)
fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
mix *= fade[:, None]
mix[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]

# master: saturación suave + loudness a -14 LUFS + techo a -1 dB
pre = np.max(np.abs(mix))
print(f'pico antes del master {pre:.2f}')
mix = mix / np.percentile(np.abs(mix), 99.9) * 0.8
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
meter = pyln.Meter(SR)
lufs = meter.integrated_loudness(mix)
mix = pyln.normalize.loudness(mix, lufs, -14.0)
peak = np.max(np.abs(mix))
if peak > 0.89:
    mix = np.tanh(mix / 0.89 * 1.0) * 0.89
print(f"entrada {lufs:.1f} LUFS -> salida {meter.integrated_loudness(mix):.1f} LUFS, pico {np.max(np.abs(mix)):.3f}")

out = ROOT / "assets/bgm/plana-bed.wav"
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print(out)
