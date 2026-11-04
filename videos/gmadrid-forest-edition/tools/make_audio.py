"""Sintetiza la pista ambiental del Forest Edition (15 s, 48 kHz, estéreo).
Todo generado por código -> libre de derechos.
Uso: python3 tools/make_audio.py assets/audio/forest-bgm.wav
Sincronía con el vídeo (mismos tiempos que assets/config.js): latido 0-2 s, arpegio desde 2 s,
oleada en la corona (4,5 s), subida que estalla cuando nace la camiseta (6,35 s), giro (7,55 s),
golpes en cada palabra (8,6 / 9,6 / 10,6 s) y en el dúo (11,6 s), impacto y acorde final con el logo (12,8 s)."""
import sys, wave
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
DUR = 15.0
GATHER, REVEAL, FLIP, WORDS, DUO, OPEN = 4.5, 6.35, 7.55, (8.6, 9.6, 10.6), 11.6, 12.8
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(2627)
L = np.zeros(N); Rch = np.zeros(N)

def hz(note):  # midi -> Hz
    return 440.0 * 2 ** ((note - 69) / 12)

def env_seg(start, end, a=0.05, r=0.3):
    e = np.zeros(N)
    start = max(0.0, start)
    i0, i1 = int(start * SR), min(N, int(end * SR))
    n = i1 - i0
    if n <= 0: return e
    x = np.arange(n) / SR
    att = np.clip(x / max(a, 1e-4), 0, 1)
    rel = np.clip((end - start - x) / max(r, 1e-4), 0, 1)
    e[i0:i1] = att * rel
    return e

def add(sig, pan=0.0, gain=1.0):
    global L, Rch
    l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L += sig * gain * l * 1.414; Rch += sig * gain * r * 1.414

def smooth(x0, x1, a, b):
    k = np.clip((t - a) / (b - a), 0, 1)
    k = k * k * (3 - 2 * k)
    return x0 + (x1 - x0) * k

# ---------------- pad (aditivo, brillo creciente) ----------------
chords = [
    (0.0, GATHER, [50, 57, 64, 65]),          # Dm(add9)
    (GATHER, REVEAL, [46, 53, 57, 60, 62]),   # Bbmaj7(add9): la corona
    (REVEAL, WORDS[0], [41, 53, 57, 60, 67]), # F(add9): nace la camiseta
    (WORDS[0], WORDS[1], [46, 53, 58, 62, 65]),  # Bb
    (WORDS[1], WORDS[2], [48, 55, 60, 64, 67]),  # C
    (WORDS[2], DUO, [45, 52, 57, 61, 64]),       # A (tensión)
    (DUO, OPEN, [46, 53, 58, 62, 65]),           # Bb
    (OPEN, 15.0, [38, 50, 57, 62, 66, 69]),      # D mayor: resolución luminosa
]
bright = smooth(0.15, 0.55, 1.5, GATHER) + smooth(0, 0.35, REVEAL - 0.7, REVEAL) + smooth(0, 0.15, OPEN - 0.2, OPEN + 0.3)
padlvl = smooth(0.0, 0.5, 0.0, 3.0) + smooth(0, 0.35, REVEAL - 0.8, REVEAL) + smooth(0, 0.2, OPEN - 0.1, OPEN + 0.2)
padlvl *= 1 - smooth(0, 1, 13.4, 15.0)
for (a, b, notes) in chords:
    e = env_seg(a - 0.04, b + 0.5, a=0.25 if a > 0 else 1.5, r=0.6)
    for j, n in enumerate(notes):
        f = hz(n)
        for det, pan in ((-0.07, -0.6), (0.07, 0.6)):
            ff = f * 2 ** (det / 12)
            s = np.zeros(N)
            for h in range(1, 9):
                if ff * h > 9000: break
                amp = (1 / h) * (bright ** (0.5 * (h - 1)))
                s += amp * np.sin(2 * np.pi * ff * h * t + j + h)
            add(s * e * padlvl, pan=pan, gain=0.028)

# ---------------- sub drone ----------------
sub = np.sin(2 * np.pi * hz(26) * t) * smooth(0, 0.5, 0.0, 2.0) * (1 - smooth(0, 1, 5.9, 6.1) * 0.0)
sub *= 1 - smooth(0, 1, 13.5, 15)
add(sub, gain=0.11)

# ---------------- latido (semilla, 0-2 s) ----------------
def thump(at, gain=0.5, f0=70, f1=38, dec=7.0):
    i0 = int(at * SR); n = int(SR * 1.2)
    x = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-x * 18)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-x * dec)
    out = np.zeros(N); out[i0:i0 + n] = s[: max(0, min(n, N - i0))]
    return out * gain
for at, g in ((0.35, 0.45), (0.62, 0.3), (1.35, 0.55), (1.62, 0.38)):
    add(thump(at, g), gain=0.9)

# ---------------- arpegio (2-12 s) ----------------
scale = [62, 65, 67, 69, 72, 74, 77, 79, 81]
step = 0.125  # semicorcheas a 120 bpm
pattern = [0, 2, 4, 1, 3, 5, 2, 4, 6, 3, 5, 7, 4, 6, 8, 5]
k = 0
at = 2.0
while at < OPEN:
    idx = pattern[k % len(pattern)]
    oct_up = 12 if at >= REVEAL else 0
    if WORDS[0] <= at < DUO:
        wi = sum(at >= w for w in WORDS) - 1
        base = (70, 72, 69)[wi]
        n = base + [0, 7, 12, 16, 19, 12, 7, 4][k % 8]
    else:
        n = scale[idx] + oct_up
    lvl = smooth(0.0, 1.0, 2.0, GATHER + 0.5) * (0.7 + 0.3 * (at >= REVEAL))
    i0 = int(at * SR); ln = int(SR * 0.6)
    x = np.arange(ln) / SR
    f = hz(n)
    s = (np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * 2 * f * x) + 0.12 * np.sin(2 * np.pi * 3 * f * x)) * np.exp(-x * 9) * np.clip(x / 0.004, 0, 1)
    seg = np.zeros(N); seg[i0:i0 + ln] = s[: max(0, min(ln, N - i0))]
    add(seg * lvl, pan=np.sin(k * 0.9) * 0.55, gain=0.06)
    k += 1
    at += step

# ---------------- subida (riser) hasta que nace la camiseta ----------------
noise = rng.standard_normal(N)
rise = np.zeros(N)
RS = REVEAL - 1.9
i0, i1 = int(RS * SR), int(REVEAL * SR)
chunk = 2400
for c in range(i0, i1, chunk):
    pos = (c - i0) / (i1 - i0)
    fc = 300 + 7000 * pos ** 2
    sos = butter(2, [fc * 0.6, min(fc * 1.4, 20000)], btype="band", fs=SR, output="sos")
    seg = sosfilt(sos, noise[c:c + chunk])
    rise[c:c + chunk] = seg * pos ** 2.2
add(rise, pan=-0.2, gain=0.22)
add(np.roll(rise, 480), pan=0.2, gain=0.22)
sweep_f = 110 * 2 ** (smooth(0, 2.0, RS, REVEAL))
sweep = np.sin(2 * np.pi * np.cumsum(sweep_f) / SR) * env_seg(RS, REVEAL + 0.02, a=1.5, r=0.02) * 0.6
add(sweep, gain=0.05)

# ---------------- impactos ----------------
def impact(at, size=1.0):
    boom = thump(at, 0.9 * size, f0=95, f1=36, dec=2.6)
    i0 = int(at * SR); n = int(SR * 0.5)
    x = np.arange(n) / SR
    nz = rng.standard_normal(n) * np.exp(-x * 14)
    sos = butter(2, 3500, btype="low", fs=SR, output="sos")
    nz = sosfilt(sos, nz)
    hit = np.zeros(N); hit[i0:i0 + n] = nz[: max(0, min(n, N - i0))]
    return boom, hit * 0.35 * size
for at, sz in ((GATHER, 0.55), (REVEAL, 1.1), (FLIP, 0.35), (WORDS[0], 0.7), (WORDS[1], 0.7), (WORDS[2], 0.75), (DUO, 0.8), (OPEN, 1.25)):
    b, h = impact(at, sz)
    add(b, gain=0.8); add(h, pan=-0.3, gain=0.8); add(np.roll(h, 300), pan=0.3, gain=0.8)

# pulso suave (bombo) 6-12 s
for beat in np.arange(REVEAL + 0.5, OPEN - 0.05, 0.5):
    if any(abs(beat - w) < 0.2 for w in (FLIP,) + WORDS + (DUO,)):
        continue
    add(thump(beat, 0.22, f0=80, f1=45, dec=12), gain=0.9)

# brillo final (shimmer) 12-15 s
for n, pan in ((86, -0.5), (90, 0.5), (93, 0.0), (98, 0.3)):
    s = np.sin(2 * np.pi * hz(n) * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 5.5 * t + n))
    add(s * env_seg(OPEN, 15.0, a=0.15, r=2.0), pan=pan, gain=0.012)

# ---------------- reverb ----------------
irn = int(SR * 2.8)
x = np.arange(irn) / SR
irL = rng.standard_normal(irn) * np.exp(-x * 2.3)
irR = rng.standard_normal(irn) * np.exp(-x * 2.3)
sos = butter(1, 5000, btype="low", fs=SR, output="sos")
irL, irR = sosfilt(sos, irL), sosfilt(sos, irR)
irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
wetL = fftconvolve(L, irL)[:N]; wetR = fftconvolve(Rch, irR)[:N]
outL = L * 0.8 + wetL * 0.45
outR = Rch * 0.8 + wetR * 0.45

# fundido final y limitador suave
fade = 1 - smooth(0, 1, 14.2, 15.0)
outL *= fade; outR *= fade
peak = max(np.abs(outL).max(), np.abs(outR).max())
outL = np.tanh(outL / peak * 1.1) * 0.89
outR = np.tanh(outR / peak * 1.1) * 0.89
st = np.stack([outL, outR], 1)
pcm = (st * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", sys.argv[1], pcm.shape)
