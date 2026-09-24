#!/usr/bin/env python3
"""Pista original de electro house para la versión publicable (LinkedIn/web).

Mismo espíritu que la versión interna con «Fix Your Accent», sin usar nada de ese
tema: 128 BPM, bajo sucio a semicorcheas pasado por un «bitcrusher», palmada gorda,
charles en contratiempo y un parón antes del drop. La estructura calca la del
montaje (tiempos reales a 128 BPM, un tiempo = 0,46875 s):

  tiempos 0–18   subida: bombo desde el primer fotograma, bajo filtrado que se abre
  18–20          parón (coincide con el tartamudeo de «facturas»)
  20             DROP en «plana.» (9,375 s)
  20–48,5        drop completo; golpes en los cambios de escena
  48,5–50        frenazo de cinta y silencio
  50–64          cierre con golpe; se apaga de 29,0 a 30,0 s

    python3 scripts/make-music-electro.py  ->  assets/bgm/plana-electro.wav
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / "make-music.py").read_text()
exec(src[src.index("import subprocess"):src.index("# ---------------------------------------------------------------- instrumentos bass house")])

B = 60 / 128           # un tiempo
S16 = B / 4
BAR = 4 * B
DUR = 30.0
N = int(DUR * SR)


def tb(beat):
    return beat * B


def bitcrush(x, bits=5, down=4):
    y = np.repeat(x[::down], down)[: len(x)]
    q = 2 ** (bits - 1)
    return np.round(y * q) / q


def electro_bass(midi, ln, bright=1.0):
    """Stab de bajo electro: sierras desafinadas + cuadrada, distorsión, barrido de
    filtro por nota (el «wah») y bitcrush."""
    n = int(ln * SR)
    f = mtof(midi)
    x = saw(f, n, 0.2) * 0.6 + saw(f * 1.012, n, 0.7) * 0.5 + square(f, n) * 0.35
    x = np.tanh(x * 3.0)
    out = np.zeros(n)
    blk = 96
    z = None
    for i in range(0, n, blk):
        fc = 300 + (3200 * bright) * np.exp(-(i / SR) / 0.06)
        sos = butter(2, min(fc, SR * 0.45), "low", fs=SR, output="sos")
        if z is None:
            z = sosfilt_zi(sos) * 0
        out[i:i + blk], z = sosfilt(sos, x[i:i + blk], zi=z)
    out = bitcrush(np.tanh(out * 2.2), 6, 3)
    sub = np.sin(2 * np.pi * (f if f < 90 else f / 2) * t_of(n)) * 0.5
    return (out * 0.7 + sub) * adsr(n, 0.002, 0.012)


def chord_stab(notes, ln=0.16):
    n = int(ln * SR)
    x = sum(saw(mtof(m), n, rng.random()) + saw(mtof(m) * 1.008, n, rng.random()) for m in notes) / (2 * len(notes))
    x = bp(np.tanh(x * 2.5), 500, 5500) * env_exp(n, ln * 0.4) * adsr(n, 0.002, 0.015)
    return bitcrush(x, 7, 2) * 0.9


def fat_clap():
    return np.tanh(clap() * 1.6 + np.concatenate([np.zeros(int(0.004 * SR)), clap()])[: len(clap())] * 0.6)


def reverse_crash(n):
    return crash()[:n][::-1] * np.linspace(0, 1, n) ** 2


ROOTS = [45, 45, 41, 43]              # A F G en el registro del bajo (A2 A2 F2 G2)
CH = [(69, 72, 76), (69, 72, 76), (65, 69, 72), (67, 71, 74)]     # Am Am F G
PAT = [(0, 0), (2, 0), (3, 12), (5, 0), (6, 0), (8, 0), (10, 12), (11, 0), (13, 7), (14, 12)]
PAT_B = [(0, 0), (1, 0), (3, 12), (4, 0), (6, 7), (8, 0), (9, 0), (11, 12), (12, 0), (14, 10), (15, 12)]

kick_bus, drums, bass, keys, fx = (np.zeros(N) for _ in range(5))
kicks = []


def K(beat, g=1.0, big=False):
    place(kick_bus, kick(big=big), tb(beat), g)
    kicks.append((tb(beat), g))


def bass_bar(bar, beat_end, pat, bright=1.0, gain=0.75, cut=None):
    root = ROOTS[bar % 4]
    for st, semi in pat:
        beat = bar * 4 + st / 4
        if beat >= beat_end:
            continue
        y = electro_bass(root + semi, S16 * 0.85, bright)
        if cut:
            y = lp(y, cut)
        place(bass, y, tb(beat), gain)


# ---- 0–18 · subida
for b in range(0, 18):
    K(b, 0.95)
    if b >= 4 and b % 2 == 1:
        place(drums, fat_clap(), tb(b), 0.5)
    place(drums, hat(open_=b >= 6), tb(b + 0.5), 0.22)
    if b >= 8:
        for s in (1, 3):
            place(drums, hat(), tb(b + s / 4), 0.14)
K(5, 1.0, big=True)                                  # el «20%»
place(fx, boom(), tb(5), 0.5)
place(fx, crash(), tb(5), 0.3)
place(drums, fat_clap(), tb(6), 0.8)                 # el tajo
for bar in range(0, 5):
    # el bajo se va abriendo durante la subida
    bass_bar(bar, 18, PAT, bright=0.25 + 0.15 * bar, gain=0.6, cut=600 + 700 * bar)
for b in (0, 1, 2, 3, 4):                            # un stab por palabra del gancho
    place(keys, chord_stab(CH[0], 0.18), tb(b), 0.45)
# redoble que acelera 14–18 y subida
beat, step = 14.0, 0.5
while beat < 18:
    place(drums, fat_clap(), tb(beat), 0.2 + 0.12 * (beat - 14))
    beat += step
    if beat >= 16:
        step = 0.25
    if beat >= 17:
        step = 0.125
place(fx, riser(int(tb(8) * SR / SR * SR) if False else int(tb(8) * SR)), tb(10), 0.5)

# ---- 18–20 · parón: solo un platillo al revés que aspira hacia el drop
place(fx, reverse_crash(int(tb(2) * SR)), tb(18), 0.5)

# ---- 20–48,5 · drop
K(20, 1.0, big=True)
place(fx, boom(), tb(20), 0.75)
place(fx, crash(), tb(20), 0.5)
for b in range(20, 64):
    if 48.5 <= b < 50:
        continue
    if b >= 60:
        break
    if b != 20 and b != 50:
        K(b, 1.0)
    if b % 2 == 1:
        place(drums, fat_clap(), tb(b), 0.62)
    place(drums, hat(open_=True), tb(b + 0.5), 0.26)
    for s in (1, 3):
        place(drums, hat(), tb(b + s / 4), 0.13)
    # stabs de acorde en el contratiempo, cortados
    place(keys, chord_stab(CH[(b // 4) % 4], 0.14), tb(b + 0.5), 0.42)
for bar in range(5, 15):
    for st, semi in (PAT if bar % 2 == 1 else PAT_B):
        beat = bar * 4 + st / 4
        if 48.5 <= beat < 50 or beat >= 60:
            continue
        place(bass, electro_bass(ROOTS[bar % 4] + semi, S16 * 0.85, 1.0), tb(beat), 0.8)
for bt in (26, 32, 36, 41, 46):                      # cambios de escena del montaje
    place(fx, crash(), tb(bt), 0.3)
    place(keys, chord_stab(CH[(bt // 4) % 4], 0.3), tb(bt), 0.55)
# remates de redoble cada 2 compases
for bar in range(6, 15, 2):
    for k in range(4):
        beat = bar * 4 + 3.5 + k * 0.125
        if not (48.5 <= beat < 50) and beat < 60:
            place(drums, fat_clap(), tb(beat), 0.2 + 0.08 * k)
place(fx, riser(int(tb(3) * SR)), tb(45.5), 0.4)

# ---- 50–64 · cierre
K(50, 1.0, big=True)
place(fx, boom(), tb(50), 0.7)
place(fx, crash(), tb(50), 0.45)
K(56, 1.0, big=True)                                 # «beplana.com»
place(fx, crash(), tb(56), 0.35)
place(keys, chord_stab(CH[0], 0.9), tb(60), 0.5)
place(bass, lp(electro_bass(45, 1.2, 0.6), 900), tb(60), 0.6)

# ---------------------------------------------------------------- mezcla
duck = np.ones(N)
for t, g in kicks:
    i = int(t * SR)
    n = int(0.25 * SR)
    j = min(N, i + n)
    duck[i:j] = np.minimum(duck[i:j], 1 - 0.75 * g * np.exp(-t_of(j - i) / 0.07))


def ir(seconds, seed):
    r = np.random.default_rng(seed)
    n = int(seconds * SR)
    return r.standard_normal(n) * np.exp(-t_of(n) / (seconds / 5)) * 0.03


send = hp(keys * 0.8 + drums * 0.15, 400)
rl = fftconvolve(send, ir(1.0, 1))[:N]
rr = fftconvolve(send, ir(1.0, 2))[:N]
bass_bus = np.tanh(hp(bass, 30) * duck * 1.4) / np.tanh(1.4)
keys_bus = keys * duck
dl = int(0.012 * SR)
kw = np.concatenate([np.zeros(dl), keys_bus[:-dl]])
L = kick_bus + bass_bus + drums + fx + keys_bus * 0.75 + kw * 0.25 + rl * 0.6
R = kick_bus + bass_bus + drums + fx + keys_bus * 0.25 + kw * 0.75 + rr * 0.6
mix = np.stack([L, R], axis=1)


def tape_stop(x, t0, dur):
    i0, n = int(t0 * SR), int(dur * SR)
    seg = x[i0:i0 + int(dur * SR * 1.05)].copy()
    rate = (1 - np.linspace(0, 1, n)) ** 1.6
    pos = np.cumsum(rate)
    out = np.stack([np.interp(pos, np.arange(len(seg)), seg[:, c]) for c in range(2)], axis=1)
    x[i0:i0 + n] = out * np.linspace(1, 0.2, n)[:, None]


g = 15 / 16
tape_stop(mix, 4.62 * g, 0.38 * g)
mix[int(5.0 * g * SR) - int(0.01 * SR):int(5.0 * g * SR)] *= 0
tape_stop(mix, 24.25 * g, 0.5 * g)
mix[int(24.75 * g * SR):int(tb(50) * SR)] = 0

fade = np.ones(N)
i0 = int(29.0 * SR)
fade[i0:] = np.linspace(1, 0, N - i0) ** 1.5
mix *= fade[:, None]
mix[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]

mix = mix / np.percentile(np.abs(mix), 99.9) * 0.85
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
meter = pyln.Meter(SR)
lufs = meter.integrated_loudness(mix)
mix = pyln.normalize.loudness(mix, lufs, -14.0)
if np.max(np.abs(mix)) > 0.9:
    mix = np.tanh(mix / 0.9) * 0.9
print(f"{lufs:.1f} -> {meter.integrated_loudness(mix):.1f} LUFS, pico {np.max(np.abs(mix)):.3f}")
out = ROOT / "assets/bgm/plana-electro.wav"
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print(out)
