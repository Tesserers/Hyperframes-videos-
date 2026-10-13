"""Canción original para el reel de Tina Café, sintetizada desde cero.

No hay muestras ni melodías ajenas: ukelele por Karplus-Strong, glockenspiel por
parciales sinusoidales, bajo, bombo, chasquido y shaker de ruido filtrado, más el
rasgueo del lápiz en cada transición. 120 BPM, 15 compases = 30,0 s, que es
exactamente lo que dura el vídeo.

    python3 scripts/make-song.py assets/audio/tina-song.wav
"""
import sys
import wave
import numpy as np

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
EIGHTH = BEAT / 2
TOTAL = 30.0
N = int(SR * TOTAL)
rng = np.random.default_rng(7)  # semilla fija: el audio sale idéntico cada vez

mix = {k: np.zeros(N) for k in ("uke", "glock", "bass", "drums", "fx")}


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(bus, t, sig, gain=1.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    mix[bus][i : i + len(sig)] += sig * gain


def env(n, attack=0.005, decay=0.4):
    t = np.arange(n) / SR
    a = np.minimum(1, t / attack)
    return a * np.exp(-t / decay)


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


# --- instrumentos ---------------------------------------------------------
def pluck(freq, dur=1.6, bright=0.55):
    """Karplus-Strong vectorizado por periodos: suena a ukelele de nailon."""
    p = max(2, int(round(SR / freq)))
    n = int(dur * SR)
    out = np.zeros(n + p)
    burst = rng.uniform(-1, 1, p)
    # ruido algo filtrado para un ataque más blando
    burst = bright * burst + (1 - bright) * np.convolve(burst, np.ones(4) / 4, "same")
    out[:p] = burst
    decay = 0.996
    k = p
    while k < n + p:
        prev = out[k - p : k]
        nxt = 0.5 * (prev + np.roll(prev, 1)) * decay
        m = min(p, n + p - k)
        out[k : k + m] = nxt[:m]
        k += p
    sig = out[p:]
    return sig * env(len(sig), 0.002, 0.9)


def glock(freq, dur=1.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.6)
         + 0.35 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t / 0.18)
         + 0.12 * np.sin(2 * np.pi * freq * 5.40 * t) * np.exp(-t / 0.07))
    return s * np.minimum(1, t / 0.002)


def bass(freq, dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    return s * env(n, 0.01, 0.22)


def kick():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)


def snap():
    n = int(0.12 * SR)
    noise = bandpass(rng.uniform(-1, 1, n), 1800, 7000)
    t = np.arange(n) / SR
    return noise * np.exp(-t / 0.025) * 3


def shaker():
    n = int(0.08 * SR)
    noise = bandpass(rng.uniform(-1, 1, n), 5000, 12000)
    t = np.arange(n) / SR
    return noise * np.minimum(1, t / 0.01) * np.exp(-t / 0.02) * 3


def pop(f0=420, f1=980):
    n = int(0.14 * SR)
    t = np.arange(n) / SR
    f = f0 + (f1 - f0) * np.minimum(1, t / 0.06)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.05)


def pencil(dur, strokes_per_s=11, erase=False):
    """Rasgueo de lápiz (o goma): ruido filtrado que late con cada trazo."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    lo, hi = (900, 3500) if erase else (2500, 8000)
    noise = bandpass(rng.uniform(-1, 1, n), lo, hi)
    am = 0.35 + 0.65 * np.abs(np.sin(np.pi * strokes_per_s * t))
    fade = np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.06)
    return noise * am * fade * 2.2


# --- armonía y melodía ----------------------------------------------------
UKE = {  # posiciones de ukelele (GCEA)
    "C": [67, 60, 64, 72], "Am": [69, 60, 64, 69], "F": [69, 60, 65, 69], "G": [67, 62, 67, 71],
}
ROOT = {"C": 36, "Am": 45, "F": 41, "G": 43}
PROG = ["C", "Am", "F", "G"] * 3 + ["F"]  # compases 1–13
STRUM = [(0, 1.0, "d"), (2, 0.8, "d"), (3, 0.55, "u"), (5, 0.6, "u"), (6, 0.85, "d"), (7, 0.5, "u")]

C5, D5, E5, G5, A5, B5, C6, D6, E6 = 72, 74, 76, 79, 81, 83, 84, 86, 88
MEL_A = [
    [(E5, 0), (G5, 2), (A5, 3), (G5, 4), (E5, 6)],
    [(C5, 0), (E5, 2), (G5, 3), (A5, 4)],
    [(A5, 0), (G5, 1), (A5, 2), (C6, 3), (A5, 4), (G5, 6)],
    [(G5, 0), (E5, 2), (D5, 3), (D5, 4)],
]
MEL_A2 = MEL_A[:3] + [[(G5, 0), (A5, 2), (B5, 3), (D6, 4)]]
MEL_B = [
    [(C6, 0), (A5, 1), (G5, 2), (E5, 3), (G5, 4), (C6, 6)],
    [(A5, 0), (G5, 3), (E5, 4), (D5, 6)],
    [(C5, 0), (E5, 1), (G5, 2), (A5, 3), (C6, 4)],
]
MELODY = MEL_A + MEL_A2 + MEL_A + [MEL_B[2]]  # compases 1–13


def strum(t, chord, vel, up):
    notes = UKE[chord][::-1] if up else UKE[chord]
    for j, m in enumerate(notes):
        add("uke", t + j * 0.011, pluck(midi(m)), 0.32 * vel)


# compás 0: el aro se dibuja (arpegio) y el logo aparece (acorde + pop)
for j, m in enumerate([C5, E5, G5, C6]):
    add("glock", j * EIGHTH * 0.75 + 0.25, glock(midi(m)), 0.30)
strum(1.5, "C", 1.0, False)
add("fx", 1.5, pop(), 0.35)

for b, chord in enumerate(PROG, start=1):
    t0 = b * BAR
    for pos, vel, d in STRUM:
        strum(t0 + pos * EIGHTH, chord, vel, d == "u")
    for beat, f in ((0, 1.0), (2, 0.8), (3.5, 0.6)):
        add("bass", t0 + beat * BEAT, bass(midi(ROOT[chord])), 0.55 * f)
    for beat in (0, 2):
        add("drums", t0 + beat * BEAT, kick(), 0.75)
    for beat in (1, 3):
        add("drums", t0 + beat * BEAT, snap(), 0.22)
    for e in range(8):
        add("drums", t0 + e * EIGHTH, shaker(), 0.07 if e % 2 == 0 else 0.11)
    for m, pos in MELODY[b - 1]:
        add("glock", t0 + pos * EIGHTH, glock(midi(m)), 0.26)

# compás 14: cierre plagal sobre Do, arpegio que sube y se apaga
t0 = 14 * BAR
strum(t0, "C", 0.9, False)
add("bass", t0, bass(midi(36), 1.2), 0.5)
add("drums", t0, kick(), 0.6)
for j, m in enumerate([C5, E5, G5, C6, E6]):
    add("glock", t0 + j * EIGHTH * 0.5, glock(midi(m), 1.6), 0.22)
add("fx", 28.0, pop(), 0.35)

# el lápiz: cada trazo del vídeo suena (inicio, duración, ¿goma?)
ITEMS = [7.0 + 1.5 * i for i in range(6)]  # café, matcha, tostadas, bollería, bocadillos, pinchos
PENCIL = [(0.25, 1.0, False), (2.75, 0.6, False), (4.0, 0.4, False), (5.0, 0.75, False), (5.9, 0.5, False)]
PENCIL += [(t, 0.45, False) for t in ITEMS] + [(t + 1.15, 0.3, True) for t in ITEMS]
PENCIL += [(16.4, 0.7, False), (19.0, 0.4, True), (19.5, 0.45, False), (19.95, 0.32, False),
           (20.4, 0.32, False), (20.85, 0.32, False), (21.3, 0.3, False), (23.0, 0.75, False),
           (23.9, 0.5, False), (24.7, 0.3, False), (27.0, 0.4, True), (27.5, 0.55, False), (28.12, 0.5, False)]
for t, d, er in PENCIL:
    add("fx", t, pencil(d, erase=er), 0.06)
# pops cuando cada desayuno se colorea y en cada mini del resumen
for t in [t + 0.3 for t in ITEMS] + [16.0 + 0.18 * k for k in range(6)]:
    add("fx", t, pop(500, 1150), 0.22)
add("fx", 21.85, pop(260, 140), 0.4)  # el sello del precio
add("fx", 13.84, pop(300, 160), 0.3)  # el pan del bocadillo aterriza
add("fx", 15.2, pop(700, 1400), 0.25)  # el palillo del pincho
add("fx", 12.5, pencil(0.12, strokes_per_s=30, erase=True), 0.3)  # ñam

# --- mezcla ---------------------------------------------------------------
gains = {"uke": 0.9, "glock": 0.8, "bass": 0.8, "drums": 0.7, "fx": 1.0}
out = sum(mix[k] * g for k, g in gains.items())
# reverb corta y barata: unos ecos tempranos para que respire
for delay, g in ((0.031, 0.18), (0.053, 0.13), (0.087, 0.09), (0.131, 0.06)):
    d = int(delay * SR)
    out[d:] += out[:-d] * g
# entrada y salida suaves para que el bucle no haga clic
tt = np.arange(N) / SR
out *= np.minimum(1, tt / 0.02) * np.clip((TOTAL - tt) / 0.9, 0, 1)
out = np.tanh(out * 1.2) / np.tanh(1.2)  # saturación suave, de cinta
out /= np.max(np.abs(out)) * 1.12

st = np.stack([out, out], axis=1)
# un poco de anchura: el glock algo a la derecha, el ukelele algo a la izquierda
side = (mix["glock"] - mix["uke"]) * 0.08
st[:, 0] -= side / (np.max(np.abs(side)) + 1e-9) * 0.05
st[:, 1] += side / (np.max(np.abs(side)) + 1e-9) * 0.05
pcm = (np.clip(st, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok", sys.argv[1], TOTAL, "s")
