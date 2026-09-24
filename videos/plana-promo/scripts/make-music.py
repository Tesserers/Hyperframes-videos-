#!/usr/bin/env python3
"""Banda sonora de Plana, v2, sintetizada aquí mismo (no hay forma de descargar
música en este entorno). 120 BPM, compás de 2 s, progresión Am–F–C–G.

Más pegada que la v1: bombo desde el primer fotograma, bajo house en contratiempo,
un bajo «reese» que ondula en corcheas y un gancho de melodía en el drop, y tres
efectos de DJ en las costuras — frenazo de cinta (4,75 y 24,5), tartamudeo de
repetición (9,0–9,5) y un hueco de silencio antes del drop del 10.

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
HOOK = [  # corcheas por compás; None = silencio
    [76, None, 76, 74, 72, None, 69, 72],
    [72, None, 72, 69, 65, None, 69, 72],
    [76, None, 76, 79, 76, None, 72, 74],
    [74, None, 74, 71, 67, None, 71, 74],
]


def chord_at(t):
    return PROG[int(t // (4 * BEAT)) % 4]


def bar_idx(t):
    return int(t // (4 * BEAT)) % 4


def in_(t, *spans):
    return any(a <= t < b for a, b in spans)


drums = np.zeros(N)
kick_bus = np.zeros(N)
bass = np.zeros(N)
reese = np.zeros(N)
pad = np.zeros(N)
stabs = np.zeros(N)
lead = np.zeros(N)
fx = np.zeros(N)
kick_times = []

GAPS = [(4.75, 5.0), (9.875, 10.0), (24.5, 25.0)]  # donde calla la base

beats = int(DUR / BEAT)
for b in range(beats):
    t = b * BEAT
    if in_(t, *GAPS) or t >= 28.5:
        continue
    # bombo a negras todo el vídeo; en el cierre, a medio tiempo hasta el 28
    if t < 25.0 or (t < 28.0 and b % 2 == 0):
        kick_times.append((t, 1.0))
    # palmada en 2 y 4
    if b % 2 == 1 and (1.0 <= t < 9.0 or 10.0 <= t < 24.5):
        place(drums, clap(), t, 0.6)
    if 25.0 <= t < 28.0 and b % 4 == 3:
        place(drums, clap(), t, 0.55)
    # charles: abierto en el contratiempo, cerrado en semicorcheas
    for s in range(4):
        ts = t + s * BEAT / 4
        if in_(ts, *GAPS) or ts >= 28.5:
            continue
        if s == 2:
            place(drums, hat(open_=ts >= 5.0), ts, 0.30)
        elif ts >= 5.0 and not (25.0 <= ts < 28.0):
            place(drums, hat(), ts, 0.17 if s % 2 else 0.24)
    # rim en la última semicorchea de cada tiempo impar en el drop: da empuje
    if 10.0 <= t < 24.5 and b % 2 == 0:
        n = int(0.06 * SR)
        rim = bp(rng.standard_normal(n), 1800, 3200) * env_exp(n, 0.012)
        place(drums, rim, t + 3 * BEAT / 4, 0.5)

for t, g in kick_times:
    place(kick_bus, kick(), t, g)

# golpes grandes en los cambios de escena
for t in (0.0, 5.0, 10.0, 25.0, 28.0):
    place(kick_bus, kick(big=True), t, 1.0)
    place(fx, boom(), t, 0.6 if t in (10.0, 25.0) else 0.4)
    place(fx, crash(), t, 0.5)
for t in (13.0, 18.0, 20.5, 23.0):
    place(fx, crash(), t, 0.35)

# subidas
place(fx, riser(int(1.0 * SR)), 8.9, 0.55)
place(fx, riser(int(1.5 * SR)), 23.0, 0.35)

# --- bajo house en contratiempo (fuera del drop)
for b8 in range(int(DUR / (BEAT / 2))):
    t = b8 * BEAT / 2
    if b8 % 2 == 0 or in_(t, *GAPS) or in_(t, (10.0, 24.5)) or t >= 28.5:
        continue
    _, root = chord_at(t)
    m = root + 12
    n = int(BEAT / 2 * SR * 0.9)
    s = saw(mtof(m), n) * 0.7 + np.sin(2 * np.pi * mtof(m - 12) * t_of(n)) * 0.6
    s = np.tanh(lp(s, 380 + 900 * min(1.0, t / 5.0)) * 2.2) * adsr(n, 0.003, 0.04)
    place(bass, s, t, 0.8)

# --- reese: dos sierras desafinadas, filtro que ondula a corcheas (drop 10–24,5)
for bar in range(5, 13):
    t = bar * 4 * BEAT
    _, root = chord_at(t)
    n = int(4 * BEAT * SR)
    f = mtof(root)
    x = saw(f * 2 ** (-0.18 / 12), n, 0.1) + saw(f * 2 ** (0.18 / 12), n, 0.6)
    x = x * 0.5 + np.sin(2 * np.pi * f / 2 * t_of(n)) * 0.7
    lfo = 0.5 - 0.5 * np.cos(2 * np.pi * 4.0 * t_of(n))  # 4 Hz = corcheas
    out = np.zeros(n)
    sos_z = None
    blk = 128
    for i in range(0, n, blk):
        fc = 180 + 1500 * lfo[i]
        sos = butter(2, fc, "low", fs=SR, output="sos")
        if sos_z is None:
            sos_z = sosfilt_zi(sos) * 0
        out[i:i + blk], sos_z = sosfilt(sos, x[i:i + blk], zi=sos_z)
    out = np.tanh(out * 2.6) * adsr(n, 0.004, 0.03)
    if t + 4 * BEAT > 24.5:
        out[int((24.5 - t) * SR):] = 0
    place(reese, out, t, 0.62)

# --- colchón: supersierra por compás
for bar in range(int(DUR / (4 * BEAT))):
    t = bar * 4 * BEAT
    notes, _ = chord_at(t)
    n = int(4 * BEAT * SR)
    s = sum(supersaw(m, n) for m in notes) / len(notes)
    place(pad, s * adsr(n, 0.02, 0.08), t)


def pad_cut(t):
    if t < 10.0:
        return 900 + 1200 * (t / 10.0)
    if t < 25.0:
        return 3800
    return max(700, 3800 - 900 * (t - 25.0))


pad = lp_sweep(pad, pad_cut)

# --- stabs: cada palabra que entra es un golpe de acorde
STAB_T = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 5.0, 5.75, 6.5, 7.25, 8.0, 8.5,
          10.0, 13.0, 15.0, 18.0, 19.0, 20.5, 23.0, 25.0, 25.5, 28.0]
for ts in STAB_T:
    notes, _ = chord_at(ts)
    ln = 0.7 if ts in (10.0, 25.0, 28.0) else 0.2
    n = int(ln * SR)
    s = sum(supersaw(m + 12, n, 3, 0.12) for m in notes) / len(notes)
    s = lp(s, 6000) * env_exp(n, ln * 0.4) * adsr(n, 0.002, 0.02)
    place(stabs, s, ts, 0.6)

# --- gancho de melodía en el drop y, filtrado, en el cierre
for b8 in range(int(DUR / (BEAT / 2))):
    t = b8 * BEAT / 2
    if not (in_(t, (10.0, 24.5), (25.0, 28.0))):
        continue
    m = HOOK[bar_idx(t)][b8 % 8]
    if m is None:
        continue
    n = int(0.24 * SR)
    x = saw(mtof(m), n) * 0.6 + square(mtof(m + 12), n) * 0.25
    x = lp(x, 4200 if t < 25.0 else 1800) * env_exp(n, 0.11) * adsr(n, 0.002, 0.03)
    place(lead, x, t, 0.34 if t < 25.0 else 0.22)
# eco a 3/16 para el gancho
d = int(3 * BEAT / 4 * SR)
echo = np.zeros(N)
echo[d:] = lead[:-d] * 0.38
echo[2 * d:] += lead[:-2 * d] * 0.16
lead_wet = lead + lp(echo, 3000)

# ---------------------------------------------------------------- mezcla
duck = np.ones(N)
for t, g in kick_times + [(x, 1.0) for x in (0.0, 5.0, 10.0, 25.0, 28.0)]:
    i = int(t * SR)
    n = int(0.34 * SR)
    j = min(N, i + n)
    curve = 1 - 0.72 * g * np.exp(-t_of(j - i) / 0.1)
    duck[i:j] = np.minimum(duck[i:j], curve)


def reverb_ir(seconds, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    return r.standard_normal(n) * np.exp(-t_of(n) / (seconds / 5)) * 0.03


def stereo_reverb(x, seconds=1.4):
    return (fftconvolve(x, reverb_ir(seconds, 1))[:N], fftconvolve(x, reverb_ir(seconds, 2))[:N])


melodic = pad * 0.26 + bass + reese + stabs * 0.9 + lead_wet
melodic = hp(melodic, 32) * duck
send = hp(pad * 0.3 + stabs + lead * 0.8 + drums * 0.2, 280)
rv_l, rv_r = stereo_reverb(send)
dly = int(0.012 * SR)
widesrc = (pad * 0.26 + lead_wet * 0.6) * duck
wide = np.concatenate([np.zeros(dly), widesrc[:-dly]])

L = melodic + kick_bus + drums + fx + rv_l * 0.8 + wide * 0.3
R = melodic + kick_bus + drums + fx + rv_r * 0.8 - wide * 0.3 + widesrc * 0.3
mix = np.stack([L, R], axis=1)


# ---------------------------------------------------------------- efectos de DJ
def tape_stop(x, t0, dur):
    """La cinta se frena: la velocidad cae de 1 a 0 en `dur` segundos."""
    i0, n = int(t0 * SR), int(dur * SR)
    seg = x[i0:i0 + int(dur * SR * 1.05)].copy()
    rate = (1 - np.linspace(0, 1, n)) ** 1.6
    pos = np.cumsum(rate)
    out = np.stack([np.interp(pos, np.arange(len(seg)), seg[:, c]) for c in range(2)], axis=1)
    out *= np.linspace(1, 0.2, n)[:, None]
    x[i0:i0 + n] = out


def stutter(x, t0, t1):
    """Repite el primer trozo del tramo en golpes cada vez más cortos."""
    i = int(t0 * SR)
    grid = [(BEAT / 2, 2), (BEAT / 4, 2), (BEAT / 8, 4)]
    src = x[i:i + int(BEAT / 2 * SR)].copy()
    for ln, reps in grid:
        n = int(ln * SR)
        piece = src[:n] * np.linspace(1, 0.85, n)[:, None]
        for _ in range(reps):
            if i + n > int(t1 * SR):
                return
            x[i:i + n] = piece
            i += n


stutter(mix, 9.0, 9.875)
mix[int(9.875 * SR):int(10.0 * SR)] *= 0.0
tape_stop(mix, 4.62, 0.38)
tape_stop(mix, 24.25, 0.5)

# final: se apaga del 29,0 al 30,0
fade = np.ones(N)
i0 = int(29.0 * SR)
fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
mix *= fade[:, None]
mix[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]

# master: saturación suave + loudness a -14 LUFS + techo a -1 dB
mix = mix / np.percentile(np.abs(mix), 99.9) * 0.85
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
meter = pyln.Meter(SR)
lufs = meter.integrated_loudness(mix)
mix = pyln.normalize.loudness(mix, lufs, -14.0)
if np.max(np.abs(mix)) > 0.89:
    mix = np.tanh(mix / 0.89) * 0.89
print(f"entrada {lufs:.1f} LUFS -> salida {meter.integrated_loudness(mix):.1f} LUFS, pico {np.max(np.abs(mix)):.3f}")

out = ROOT / "assets/bgm/plana-bed.wav"
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print(out)
