"""Bed hawaiano sintetizado en local (sin descargas), 120 BPM, 20 s.
Ukelele por Karplus-Strong (afinación GCEA reentrante) con rasgueo isleño, steel guitar con
glissando y vibrato, bajo suave, shaker. C · Am · F · G7, un acorde por compás (2 s).
Uso: python3 scripts/synth-aloha.py assets/bgm/aloha.wav"""
import sys, wave
import numpy as np

SR, BPM, DUR = 48000, 120, 20.0
B = 60 / BPM
N = int(SR * DUR)
rng = np.random.default_rng(808)
L = np.zeros(N); R = np.zeros(N)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def put(sig, t, gl=1.0, gr=1.0):
    i = int(t * SR)
    if i >= N: return
    j = min(N, i + len(sig)); L[i:j] += sig[:j-i] * gl; R[i:j] += sig[:j-i] * gr
def lp(x, fc):
    a = np.exp(-2*np.pi*fc/SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s = (1-a)*v + a*s; y[i] = s
    return y

def pluck(m, dur=1.6, bright=0.55, decay=0.996):
    """Karplus-Strong vectorizado por periodos."""
    P = max(2, int(round(SR / hz(m) - 0.5)))
    n = int(dur * SR); y = np.zeros(n + P + 1)
    burst = rng.uniform(-1, 1, P)
    burst = bright * burst + (1 - bright) * np.convolve(burst, np.ones(4) / 4, "same")  # cuerda de nylon: menos brillo
    y[:P] = burst
    k = P
    while k < n:
        e = min(k + P, n)
        prev = y[k-P:e-P+1]
        y[k:e] = decay * 0.5 * (prev[:-1] + prev[1:])[: e-k]
        k = e
    # el lazo promedia y[n-P] e y[n-P+1]: periodo P-0.5. El periodo entero desafina las notas agudas; remuestrear al tono exacto
    real = SR / (P - 0.5); ratio = hz(m) / real
    out = np.interp(np.arange(n) * ratio, np.arange(len(y)), y, right=0.0)
    t = np.arange(n) / SR
    return out * np.minimum(1, (dur - t) / 0.08)

UKE = {  # G C E A, reentrante
    "C":  [67, 60, 64, 72],
    "Am": [69, 60, 64, 69],
    "F":  [69, 60, 65, 69],
    "G7": [67, 62, 65, 71],
}
ROOT = {"C": 36, "Am": 45, "F": 41, "G7": 43}
PROG = ["C", "Am", "F", "G7"]
# rasgueo isleño: D . D U . U D U  (en negras)
STRUM = [(0, "D", 1.0), (1, "D", 0.8), (1.5, "U", 0.55), (2.5, "U", 0.6), (3, "D", 0.85), (3.5, "U", 0.55)]

def strum(chord, t, d, vel):
    notes = UKE[chord] if d == "D" else UKE[chord][::-1]
    for i, m in enumerate(notes):
        pan = 0.35 + 0.1 * i
        put(pluck(m, 1.1) * 0.22 * vel, t + i * 0.011, 1 - pan * 0.4, 0.8 + pan * 0.3)

def steel(m, t=None, dur=1.0, slide_from=None, vel=1.0):
    """Lap steel: glissando de entrada, vibrato lento, tono redondo."""
    n = int(dur * SR); tt = np.arange(n) / SR
    f0 = hz(m)
    f = np.full(n, f0)
    if slide_from is not None:
        g = np.minimum(tt / 0.16, 1); g = g * g * (3 - 2 * g)
        f = hz(slide_from) + (f0 - hz(slide_from)) * g
    vib = 1 + 0.006 * np.sin(2*np.pi*5.2*tt) * np.minimum(tt / 0.35, 1)
    ph = 2*np.pi*np.cumsum(f * vib) / SR
    s = np.sin(ph) + 0.45*np.sin(2*ph) + 0.18*np.sin(3*ph) + 0.08*np.sin(4*ph)
    env = np.minimum(tt / 0.03, 1) * np.exp(-tt / 1.1) * np.minimum(1, (dur - tt) / 0.12)
    return s * env * 0.11 * vel

def bass(m, dur=0.6):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.2*np.sin(4*np.pi*f*t)
    return s * np.minimum(t / 0.008, 1) * np.exp(-t / 0.28) * 0.38

def shaker(v):
    n = int(0.09 * SR); x = rng.standard_normal(n); x = x - lp(x, 5000)
    t = np.arange(n) / SR
    return x * np.minimum(t / 0.012, 1) * np.exp(-t / 0.03) * 0.11 * v

def thump():  # ipu / tambor de mano grave
    n = int(0.3 * SR); t = np.arange(n) / SR
    f = 70 + 60 * np.exp(-t * 25)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t * 11) * 0.45

# melodía de steel guitar: (compás, negra, nota, duración en negras, desde)
MEL = [
    (0, 0, 72, 1.5, 64), (0, 1.5, 74, 0.5, None), (0, 2, 76, 2, 74),   # entrada: el steel abre el vídeo
    (1, 0, 76, 1.5, 72), (1, 1.5, 79, 0.5, None), (1, 2, 81, 2, 79),
    (2, 0, 79, 1.5, 76), (2, 1.5, 76, 0.5, None), (2, 2, 72, 2, 74),
    (3, 0, 74, 1.5, 72), (3, 1.5, 77, 0.5, None), (3, 2, 79, 2, 77),
    (4, 0, 84, 3, 81),
    (5, 0, 81, 1.5, 79), (5, 1.5, 79, 0.5, None), (5, 2, 76, 2, 74),
    (6, 0, 77, 1.5, 76), (6, 1.5, 81, 0.5, None), (6, 2, 79, 2, 77),
    (7, 0, 79, 1, 77), (7, 1, 77, 1, None), (7, 2, 74, 2, 72),
    (8, 0, 76, 2, 74), (8, 2, 79, 2, 76),
    (9, 0, 84, 4, 79),
]

for bar in range(10):
    t0 = bar * 4 * B
    ch = PROG[bar % 4] if bar < 9 else "C"
    if bar < 9:
        for q, d, v in STRUM:
            strum(ch, t0 + q * B, d, v)
    else:
        strum("C", t0, "D", 1.0)                      # último acorde, dejado sonar
        for i, m in enumerate(UKE["C"]):
            put(pluck(m, 3.0, decay=0.998) * 0.12, t0 + 0.6 + i * 0.09)   # arpegio de cierre
    if 1 <= bar <= 8:
        r = ROOT[ch]
        put(bass(r), t0); put(bass(r + 7), t0 + 2 * B)
        put(bass(r + 12, 0.3) * 0.6, t0 + 3.5 * B)
        put(thump(), t0); put(thump() * 0.6, t0 + 1.5 * B); put(thump() * 0.8, t0 + 2 * B)
    if bar <= 8:
        for e in range(8):
            put(shaker((1.0 if e % 2 else 0.55) * (0.6 if bar == 0 else 1)), t0 + e * 0.5 * B, 0.8, 1.0)

for bar, q, m, d, fr in MEL:
    put(steel(m, t=None, dur=d * B + 0.5, slide_from=fr), bar * 4 * B + q * B, 1.0, 0.75)

# reverb pobre pero suficiente: ecos cortos difusos (playa, no catedral)
for dl, g in ((0.031, .22), (0.047, .18), (0.071, .14), (0.113, .10), (0.167, .07)):
    k = int(dl * SR)
    L[k:] += R[:-k] * g * 0.5; R[k:] += L[:-k] * g * 0.5

f = np.ones(N); f[-SR:] = np.linspace(1, 0, SR) ** 2
L *= f; R *= f
peak = max(np.abs(L).max(), np.abs(R).max()); L, R = L/peak*0.89, R/peak*0.89
pcm = (np.clip(np.stack([L, R], 1), -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", sys.argv[1])
