#!/usr/bin/env python3
"""Banda sonora de Plana, v5: bass house, sintetizada aquí mismo (no hay forma de
descargar música en este entorno). 120 BPM, compás de 2 s, en La menor.

Sin melodías pentatónicas (la v4 sonaba «oriental» por eso). Lo que manda es el
ritmo: bombo a negras, un bajo «growl» que cambia de vocal a semicorcheas, palmada
en 2 y 4, charles en contratiempo, y acordes de house (menor 9, maj7) en golpes
cortos. Efectos de DJ en las costuras: frenazo de cinta (4,62 y 24,25),
tartamudeo (9,0–9,875) y hueco de silencio antes del drop del 10.

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


# ---------------------------------------------------------------- instrumentos bass house
VOWELS = {"a": (800, 1250), "o": (520, 900), "u": (340, 760), "e": (560, 1750), "i": (320, 2250)}


def growl(midi, ln, vowels, drive=3.5):
    """Bajo growl: sierra + cuadrada desafinadas, dos formantes que se mueven entre
    vocales a lo largo de la nota, saturación y sub en seno."""
    n = int(ln * SR)
    f = mtof(midi)
    x = saw(f, n, 0.1) * 0.6 + saw(f * 1.006, n, 0.4) * 0.5 + square(f * 0.5, n) * 0.35
    out = np.zeros(n)
    blk = 128
    z1 = z2 = None
    for i in range(0, n, blk):
        k = i / max(1, n - 1)
        pos = k * (len(vowels) - 1)
        j = min(int(pos), len(vowels) - 2) if len(vowels) > 1 else 0
        fr = pos - j
        va = VOWELS[vowels[j]]
        vb = VOWELS[vowels[min(j + 1, len(vowels) - 1)]]
        f1 = va[0] + (vb[0] - va[0]) * fr
        f2 = va[1] + (vb[1] - va[1]) * fr
        s1 = butter(2, [f1 * 0.7, f1 * 1.3], "band", fs=SR, output="sos")
        s2 = butter(2, [f2 * 0.8, f2 * 1.2], "band", fs=SR, output="sos")
        if z1 is None:
            z1 = sosfilt_zi(s1) * 0
            z2 = sosfilt_zi(s2) * 0
        seg = x[i:i + blk]
        y1, z1 = sosfilt(s1, seg, zi=z1)
        y2, z2 = sosfilt(s2, seg, zi=z2)
        out[i:i + blk] = y1 * 1.4 + y2 * 0.9
    out = np.tanh(out * drive) / np.tanh(drive)
    sub = np.sin(2 * np.pi * (f / 2 if f > 70 else f) * t_of(n)) * 0.55
    y = (out * 0.75 + sub) * adsr(n, 0.004, 0.025)
    return y


def stab(notes, ln=0.22, cut=4200):
    """Acorde de house corto (tipo órgano/piano digital)."""
    n = int(ln * SR)
    x = np.zeros(n)
    for m in notes:
        fr = mtof(m)
        x += saw(fr, n, rng.random()) * 0.5 + square(fr * 2, n) * 0.15 + np.sin(2 * np.pi * fr * t_of(n)) * 0.4
    x = lp(x / len(notes), cut) * env_exp(n, ln * 0.35) * adsr(n, 0.002, 0.02)
    return np.tanh(x * 1.8) * 0.8


def snare():
    n = int(0.3 * SR)
    tone = np.sin(2 * np.pi * 200 * t_of(n)) * env_exp(n, 0.04)
    nz = bp(rng.standard_normal(n), 1500, 9000) * env_exp(n, 0.09)
    return np.tanh((tone * 0.6 + nz) * 1.7) * 0.75


def shaker():
    n = int(0.05 * SR)
    return bp(rng.standard_normal(n), 5000, 12000) * env_exp(n, 0.012) * np.minimum(1, t_of(n) / 0.004)


def downlifter(n):
    t = t_of(n)
    d = n / SR
    sweep = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t / (d * 0.35)) + 40) / SR)
    return (sweep * 0.5 + hp(rng.standard_normal(n), 2000) * 0.2) * np.exp(-t / (d * 0.5))


# ---------------------------------------------------------------- partitura
S16 = BEAT / 4
ROOTS = [33, 33, 29, 31]                                    # Am Am F G (i i VI VII)
CHORDS = [(57, 60, 64, 67, 71), (57, 60, 64, 67, 71), (53, 57, 60, 64, 67), (55, 59, 62, 64, 69)]
# patrón de bajo por compás: (paso de semicorchea, semitonos sobre la raíz, largo en pasos, vocales)
BASSPAT = [(0, 0, 2, "ua"), (3, 0, 2, "oa"), (6, 12, 2, "ae"), (8, 0, 1, "u"),
           (10, 0, 2, "ua"), (11, 7, 1, "a"), (13, 12, 1, "e"), (14, 0, 2, "oi")]
BASSPAT_B = [(0, 0, 4, "uoa"), (4, 12, 1, "a"), (6, 0, 2, "ue"), (9, 0, 2, "oa"),
             (11, 12, 1, "i"), (12, 0, 2, "ua"), (14, 10, 2, "ae")]


def bar_of(t):
    return int(t // (4 * BEAT))


def in_(t, *spans):
    return any(a <= t < b for a, b in spans)


drums = np.zeros(N)
kick_bus = np.zeros(N)
bass = np.zeros(N)
keys = np.zeros(N)
fx = np.zeros(N)
kick_times = []
GAPS = [(4.62, 5.0), (9.875, 10.0), (24.25, 25.0)]


def bass_bar(bar, t_end, pat=BASSPAT, gain=0.8, cut=None):
    t0 = bar * 4 * BEAT
    root = ROOTS[bar % 4]
    for step, semi, ln, vw in pat:
        t = t0 + step * S16
        if t >= t_end or in_(t, *GAPS):
            continue
        y = growl(root + semi, ln * S16 * 0.95, vw)
        if cut:
            y = lp(y, cut)
        place(bass, y, t, gain)


def kick4(t0, t1, g=1.0):
    t = t0
    while t < t1 - 1e-6:
        if not in_(t, *GAPS):
            place(kick_bus, kick(), t, g)
            kick_times.append((t, g))
        t += BEAT


def house_hats(t0, t1, g=0.28):
    t = t0
    while t < t1 - 1e-6:
        if not in_(t, *GAPS):
            place(drums, hat(open_=True), t + BEAT / 2, g)          # contratiempo abierto
            for s in (1, 3):
                place(drums, shaker(), t + s * S16, g * 0.5)
        t += BEAT


def claps(t0, t1, g=0.6):
    t = t0 + BEAT
    while t < t1 - 1e-6:
        if not in_(t, *GAPS):
            place(drums, clap(), t, g)
            place(drums, snare(), t, g * 0.5)
        t += 2 * BEAT


# ---- 0–2,5 · gancho: bombo y un golpe de growl por palabra
for i, t in enumerate([0.0, 0.5, 1.0, 1.5, 2.0]):
    place(kick_bus, kick(), t, 0.95)
    kick_times.append((t, 0.95))
    place(bass, growl(33 + (12 if i % 2 else 0), 0.3, "ua"), t, 0.75)
    place(drums, shaker(), t + BEAT / 2, 0.2)
place(fx, riser(int(0.5 * SR)), 2.0, 0.35)
# ---- 2,5 · el 20 %: impacto y sub que cae; 3,0 el tajo
place(kick_bus, kick(big=True), 2.5, 1.0)
kick_times.append((2.5, 1.0))
place(fx, boom(), 2.5, 0.6)
place(fx, crash(), 2.5, 0.35)
place(drums, snare(), 3.0, 0.8)
place(drums, clap(), 3.0, 0.55)
place(fx, downlifter(int(0.5 * SR)), 3.5, 0.45)            # el 20 % se cae
# ---- 3,0–4,62 · entra el groove
kick4(3.0, 4.62)
house_hats(3.0, 4.62, 0.24)
claps(3.0, 4.62, 0.5)
bass_bar(1, 4.62, gain=0.7)

# ---- 5–9 · groove con el bajo filtrado y acordes en contratiempo
place(kick_bus, kick(big=True), 5.0, 1.0)
kick_times.append((5.0, 1.0))
place(fx, crash(), 5.0, 0.35)
kick4(5.0, 9.0)
house_hats(5.0, 9.0)
claps(5.0, 9.0)
for bar in (2, 3, 4):
    bass_bar(bar, 9.0, gain=0.75, cut=1600)
for t in np.arange(5.0, 9.0, BEAT):
    ch = CHORDS[bar_of(t) % 4]
    place(keys, stab(ch, 0.2, 3000), t + BEAT / 2, 0.5)
for t in (6.5, 7.5, 8.0):
    place(keys, stab(CHORDS[bar_of(t) % 4], 0.35, 5000), t, 0.7)
# redoble 8,0–9,0 que acelera + subida
tt, step = 8.0, BEAT / 2
while tt < 9.0:
    place(drums, snare(), tt, 0.3 + 0.5 * (tt - 8.0))
    tt += step
    step = max(BEAT / 8, step * 0.8)
place(fx, riser(int(1.4 * SR)), 8.45, 0.55)

# ---- 10–24,25 · drop: growl a tope, bombo a negras, acordes en los cortes
place(kick_bus, kick(big=True), 10.0, 1.0)
kick_times.append((10.0, 1.0))
place(fx, boom(), 10.0, 0.75)
place(fx, crash(), 10.0, 0.5)
kick4(10.0, 24.25)
house_hats(10.0, 24.25, 0.3)
claps(10.0, 24.25, 0.65)
for t in np.arange(10.0, 24.25, S16):
    if int(round(t / S16)) % 2 == 1:
        place(drums, shaker(), t, 0.12)
for bar in range(5, 13):
    bass_bar(bar, 24.25, pat=BASSPAT if bar % 2 == 1 else BASSPAT_B, gain=0.85)
for t in (10.0, 13.0, 15.0, 18.0, 19.0, 20.5, 23.0):
    place(keys, stab(CHORDS[bar_of(t) % 4], 0.45, 6000), t, 0.75)
    if t != 10.0:
        place(fx, crash(), t, 0.25)
# remates de redoble al final de cada 2 compases
for t0 in np.arange(10.0, 24.25, 8 * BEAT):
    for k in range(4):
        tt = t0 + 7.5 * BEAT + k * BEAT / 8
        if tt < 24.25:
            place(drums, snare(), tt, 0.25 + 0.1 * k)
place(fx, riser(int(1.2 * SR)), 23.05, 0.4)

# ---- 25–30 · cierre: impacto, groove a medio tiempo con acordes largos, golpe en el 28
for t in (25.0, 28.0):
    place(kick_bus, kick(big=True), t, 1.0)
    kick_times.append((t, 1.0))
    place(fx, boom(), t, 0.65)
    place(fx, crash(), t, 0.45)
    place(bass, growl(33, 1.2 if t == 25.0 else 1.6, "uoa", 2.5), t, 0.75)
    place(keys, stab(CHORDS[0], 1.4, 3500), t, 0.7)
for t in (26.0, 27.0):
    place(kick_bus, kick(), t, 0.85)
    kick_times.append((t, 0.85))
    place(drums, clap(), t + BEAT, 0.5)
house_hats(25.0, 28.0, 0.2)
place(keys, stab(CHORDS[2], 0.9, 3000), 26.0, 0.45)
place(keys, stab(CHORDS[3], 0.9, 3000), 27.0, 0.45)

# ---------------------------------------------------------------- mezcla
duck = np.ones(N)
for t, g in kick_times:
    i = int(t * SR)
    n = int(0.3 * SR)
    j = min(N, i + n)
    duck[i:j] = np.minimum(duck[i:j], 1 - 0.7 * g * np.exp(-t_of(j - i) / 0.08))


def reverb_ir(seconds, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    return r.standard_normal(n) * np.exp(-t_of(n) / (seconds / 5)) * 0.03


def stereo_reverb(x, seconds=1.3):
    return (fftconvolve(x, reverb_ir(seconds, 1))[:N], fftconvolve(x, reverb_ir(seconds, 2))[:N])


bass_bus = np.tanh(hp(bass, 30) * duck * 1.5) / np.tanh(1.5)
keys_bus = keys * duck
send = hp(keys * 0.9 + drums * 0.2, 300)
rv_l, rv_r = stereo_reverb(send)
dl = int(0.011 * SR)
keys_w = np.concatenate([np.zeros(dl), keys_bus[:-dl]])

L = kick_bus + bass_bus + drums + fx + keys_bus * 0.8 + keys_w * 0.2 + rv_l * 0.75
R = kick_bus + bass_bus + drums + fx + keys_bus * 0.2 + keys_w * 0.8 + rv_r * 0.75
mix = np.stack([L, R], axis=1)


# ---------------------------------------------------------------- efectos de DJ
def tape_stop(x, t0, dur):
    i0, n = int(t0 * SR), int(dur * SR)
    seg = x[i0:i0 + int(dur * SR * 1.05)].copy()
    rate = (1 - np.linspace(0, 1, n)) ** 1.6
    pos = np.cumsum(rate)
    out = np.stack([np.interp(pos, np.arange(len(seg)), seg[:, c]) for c in range(2)], axis=1)
    out *= np.linspace(1, 0.2, n)[:, None]
    x[i0:i0 + n] = out
    x[i0 + n:i0 + n + int(0.02 * SR)] *= 0


def stutter(x, t0, t1):
    i = int(t0 * SR)
    src = x[i:i + int(BEAT / 2 * SR)].copy()
    for ln, reps in [(BEAT / 2, 2), (BEAT / 4, 2), (BEAT / 8, 4)]:
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
mix[int(24.75 * SR):int(25.0 * SR)] *= 0.0

fade = np.ones(N)
i0 = int(29.0 * SR)
fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
mix *= fade[:, None]
mix[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]

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
