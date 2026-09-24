#!/usr/bin/env python3
"""Banda sonora de Plana, v3: phonk-house, sintetizada aquí mismo (no hay forma de
descargar música en este entorno). 120 BPM, compás de 2 s, en La menor.

Lo que la hace «cool»: el cencerro 808 con melodía (la firma del phonk), un 808
saturado que resbala entre notas, charles de trap con redobles a fusas y bombo
a negras en el drop. La intro es a medio tiempo, con tensión; el drop del 10 abre
a cuatro por cuatro. Se mantienen los efectos de DJ en las costuras: frenazo de
cinta (4,62 y 24,25), tartamudeo (9,0–9,875) y hueco de silencio antes del drop.

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


# ---------------------------------------------------------------- instrumentos phonk
def cowbell(midi, ln=0.32):
    """Cencerro 808 afinado: dos cuadradas en proporción 1:1,48, pasa-banda y cola corta."""
    n = int(ln * SR)
    f1 = mtof(midi)
    x = square(f1, n) * 0.6 + square(f1 * 1.48, n) * 0.4
    x = bp(x, max(300, f1 * 0.8), min(SR * 0.45, f1 * 4.5), 2)
    e = 0.65 * env_exp(n, 0.018) + 0.35 * env_exp(n, 0.16)
    return np.tanh(x * e * 2.2) * 0.8


def snare():
    n = int(0.35 * SR)
    tone = np.sin(2 * np.pi * 190 * t_of(n)) * env_exp(n, 0.05)
    nz = bp(rng.standard_normal(n), 1200, 8000) * env_exp(n, 0.11)
    return np.tanh((tone * 0.7 + nz * 0.9) * 1.8) * 0.8


def bass808(notes, t0, total, drive=3.0):
    """808 con deslizamiento: notes = [(t_rel, midi)], suena de t0 a t0+total."""
    n = int(total * SR)
    t = t_of(n)
    f = np.zeros(n)
    for i, (tr, m) in enumerate(notes):
        a = int(tr * SR)
        b = int(notes[i + 1][0] * SR) if i + 1 < len(notes) else n
        f[a:b] = mtof(m)
        # deslizamiento de 60 ms hacia la nota
        if i > 0:
            g = min(int(0.06 * SR), b - a)
            f[a:a + g] = np.linspace(mtof(notes[i - 1][1]), mtof(m), g)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph)
    env = np.ones(n)
    for tr, _ in notes:  # golpe al inicio de cada nota
        a = int(tr * SR)
        k = min(n - a, int(0.25 * SR))
        env[a:a + k] *= 1 + 0.6 * np.exp(-t_of(k) / 0.05)
    x = np.tanh(x * env * drive) / np.tanh(drive)
    x = x * adsr(n, 0.003, 0.05)
    return x


def roll_hats(buf, t0, t1, step, gain, rise=False):
    t = t0
    k = 0
    while t < t1 - 1e-6:
        g = gain * (0.55 + 0.45 * (k / max(1, (t1 - t0) / step)) if rise else 1)
        place(buf, hat(), t, g)
        t += step
        k += 1


# ---------------------------------------------------------------- partitura
ROOTS = [33, 29, 36, 31]            # A1 F1 C2 G1, un compás cada una
RIFF = [                            # cencerro, semicorcheas; None = silencio
    [81, None, None, 81, None, None, 84, None, 81, None, 79, None, 76, None, 79, None],
    [81, None, None, 81, None, None, 84, None, 86, None, 84, None, 81, None, 79, None],
]
S16 = BEAT / 4


def bar_of(t):
    return int(t // (4 * BEAT))


def in_(t, *spans):
    return any(a <= t < b for a, b in spans)


drums = np.zeros(N)
kick_bus = np.zeros(N)
bass = np.zeros(N)
bell = np.zeros(N)
pad = np.zeros(N)
fx = np.zeros(N)
kick_times = []

GAPS = [(4.62, 5.0), (9.875, 10.0), (24.25, 25.0)]

# ---- 0–4,62 · gancho: un 808 por palabra, subiendo; el «20%» cae a plomo
hook = [(0.0, 45), (0.5, 45), (1.0, 48), (1.5, 50), (2.0, 52)]
for t, m in hook:
    place(kick_bus, kick(), t, 0.9)
    kick_times.append((t, 0.9))
    place(bass, bass808([(0, m - 12)], 0, 0.45), t, 0.8)
place(kick_bus, kick(big=True), 2.5, 1.0)
kick_times.append((2.5, 1.0))
place(bass, bass808([(0, 33), (0.5, 33), (0.9, 21)], 0, 1.4, 3.5), 2.5, 0.9)   # cae al 3,4
place(fx, boom(), 2.5, 0.5)
place(drums, snare(), 3.0, 0.8)          # el tajo
place(drums, clap(), 3.0, 0.5)
place(fx, crash(), 3.0, 0.3)
place(kick_bus, kick(), 3.9, 0.9)
kick_times.append((3.9, 0.9))
place(bass, bass808([(0, 33), (0.35, 36), (0.5, 33)], 0, 0.72), 3.9, 0.85)
# charles corcheas desde el principio, redoble a fusas antes del 20 %
roll_hats(drums, 0.0, 2.25, BEAT / 2, 0.22)
roll_hats(drums, 2.25, 2.5, BEAT / 8, 0.2, rise=True)
roll_hats(drums, 2.5, 4.62, BEAT / 4, 0.2)
# cencerro solo a partir del tajo: presenta el riff
for i in range(int((4.62 - 3.0) / S16)):
    t = 3.0 + i * S16
    m = RIFF[0][i % 16]
    if m is not None:
        place(bell, cowbell(m), t, 0.55)

# ---- 5–9,875 · medio tiempo con tensión: bombo trap, caja en el 3, riff completo
for bar in range(2, 5):
    t0 = bar * 4 * BEAT
    for step, g in [(0, 1.0), (6, 0.8), (9, 0.85), (14, 0.7)]:   # bombo trap
        t = t0 + step * S16
        if in_(t, (5.0, 9.0)):
            place(kick_bus, kick(), t, g)
            kick_times.append((t, g))
    for bt in (2,):                                              # caja en el 3
        t = t0 + bt * BEAT
        if in_(t, (5.0, 9.0)):
            place(drums, snare(), t, 0.85)
            place(drums, clap(), t, 0.45)
    # 808 con deslizamientos siguiendo el riff
    root = ROOTS[bar % 4]
    notes = [(0, root), (6 * S16, root), (9 * S16, root + 3), (12 * S16, root + 7), (14 * S16, root)]
    x = bass808(notes, 0, 4 * BEAT, 3.2)
    if t0 + 4 * BEAT > 9.0:
        x[int((9.0 - t0) * SR):] = 0
    place(bass, x, t0, 0.85)
for i in range(int((9.0 - 5.0) / S16)):
    t = 5.0 + i * S16
    m = RIFF[bar_of(t) % 2][i % 16]
    if m is not None:
        place(bell, cowbell(m), t, 0.6)
roll_hats(drums, 5.0, 6.5, BEAT / 4, 0.2)
roll_hats(drums, 6.5, 6.75, BEAT / 12, 0.18, rise=True)          # tresillo de fusas
roll_hats(drums, 6.75, 8.0, BEAT / 4, 0.2)
roll_hats(drums, 8.0, 8.5, BEAT / 8, 0.18)
roll_hats(drums, 8.5, 9.0, BEAT / 4, 0.2)
place(fx, riser(int(0.9 * SR)), 8.97, 0.5)
for t in (5.0,):
    place(kick_bus, kick(big=True), t, 1.0)
    place(fx, crash(), t, 0.4)
    place(fx, boom(), t, 0.4)
# golpe de la palabra en 6,5 y el zoom de 7,5
place(drums, snare(), 7.5, 0.7)
place(fx, crash(), 7.5, 0.3)

# ---- 10–24,25 · drop phonk-house: bombo a negras, 808 saturado, cencerro arriba
for b in range(20, 49):
    t = b * BEAT
    if in_(t, *GAPS):
        continue
    kick_times.append((t, 1.0))
    place(kick_bus, kick(), t, 1.0)
    if b % 2 == 1:
        place(drums, clap(), t, 0.55)
        place(drums, snare(), t, 0.5)
for bar in range(5, 13):
    t0 = bar * 4 * BEAT
    root = ROOTS[bar % 4]
    # contratiempos con octava y un deslizamiento al final del compás
    notes = []
    for q8 in range(8):
        m = root + (12 if q8 in (3, 7) else 0)
        notes.append((q8 * BEAT / 2 + BEAT / 4, m))
    notes.insert(0, (0, root))
    x = bass808(notes, 0, 4 * BEAT, 4.0)
    if t0 + 4 * BEAT > 24.25:
        x[int((24.25 - t0) * SR):] = 0
    place(bass, x, t0, 0.75)
for i in range(int((24.25 - 10.0) / S16)):
    t = 10.0 + i * S16
    m = RIFF[bar_of(t) % 2][i % 16]
    if m is None:
        continue
    oct_ = 12 if in_(t, (18.0, 24.25)) and (i // 16) % 2 == 1 else 0
    place(bell, cowbell(m + oct_), t, 0.62)
for t0 in np.arange(10.0, 24.25, 4 * BEAT):
    roll_hats(drums, t0, t0 + 3 * BEAT, BEAT / 4, 0.2)
    roll_hats(drums, t0 + 3 * BEAT, t0 + 3.5 * BEAT, BEAT / 8, 0.17, rise=True)
    roll_hats(drums, t0 + 3.5 * BEAT, t0 + 4 * BEAT, BEAT / 12, 0.15, rise=True)
    place(drums, hat(open_=True), t0 + 1.5 * BEAT, 0.25)
for t in (10.0, 13.0, 18.0, 20.5, 23.0):
    place(fx, crash(), t, 0.45 if t == 10.0 else 0.3)
place(kick_bus, kick(big=True), 10.0, 1.0)
place(fx, boom(), 10.0, 0.7)
place(fx, riser(int(1.2 * SR)), 23.05, 0.35)

# ---- 25–30 · cierre: golpe, riff filtrado a medio tiempo, golpe final en el 28
for t in (25.0, 28.0):
    place(kick_bus, kick(big=True), t, 1.0)
    kick_times.append((t, 1.0))
    place(fx, boom(), t, 0.6)
    place(fx, crash(), t, 0.45)
    place(bass, bass808([(0, 33), (1.2, 33)], 0, 1.6 if t == 25.0 else 1.9, 3.5), t, 0.85)
for t in (26.0, 27.0):
    place(kick_bus, kick(), t, 0.8)
    kick_times.append((t, 0.8))
    place(drums, snare(), t + BEAT, 0.6)
roll_hats(drums, 25.0, 28.0, BEAT / 4, 0.16)
for i in range(int((28.0 - 25.0) / S16)):
    t = 25.0 + i * S16
    m = RIFF[0][i % 16]
    if m is not None:
        place(bell, lp(cowbell(m), 2200), t, 0.5)

# ---- colchón oscuro de fondo, casi subliminal
PADCH = [(57, 60, 64), (53, 57, 60), (55, 60, 64), (55, 59, 62)]
for bar in range(15):
    t = bar * 4 * BEAT
    n = int(4 * BEAT * SR)
    s = sum(supersaw(m - 12, n, 3, 0.1) for m in PADCH[bar % 4]) / 3
    place(pad, lp(s, 900) * adsr(n, 0.05, 0.1), t)

# ---------------------------------------------------------------- mezcla
duck = np.ones(N)
for t, g in kick_times:
    i = int(t * SR)
    n = int(0.3 * SR)
    j = min(N, i + n)
    duck[i:j] = np.minimum(duck[i:j], 1 - 0.6 * g * np.exp(-t_of(j - i) / 0.09))


def reverb_ir(seconds, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    return r.standard_normal(n) * np.exp(-t_of(n) / (seconds / 5)) * 0.03


def stereo_reverb(x, seconds=1.2):
    return (fftconvolve(x, reverb_ir(seconds, 1))[:N], fftconvolve(x, reverb_ir(seconds, 2))[:N])


# eco a corchea con puntillo en el cencerro: el «rebote» típico del phonk
d = int(3 * BEAT / 4 * SR)
bell_e = bell.copy()
bell_e[d:] += bell[:-d] * 0.32
bell_e[2 * d:] += bell[:-2 * d] * 0.12

bass_bus = hp(bass, 28) * duck
bass_bus = np.tanh(bass_bus * 1.6) / np.tanh(1.6)
send = hp(bell_e * 0.8 + drums * 0.15 + pad * 0.2, 300)
rv_l, rv_r = stereo_reverb(send)
dl = int(0.009 * SR)
bell_w = np.concatenate([np.zeros(dl), bell_e[:-dl]])

L = kick_bus + bass_bus + drums + fx + pad * 0.14 * duck + bell_e * 0.85 + bell_w * 0.15 + rv_l * 0.7
R = kick_bus + bass_bus + drums + fx + pad * 0.14 * duck + bell_e * 0.55 + bell_w * 0.45 + rv_r * 0.7
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
