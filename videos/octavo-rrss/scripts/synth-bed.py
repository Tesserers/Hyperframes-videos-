"""Bed musical sintetizado en local (sin descargas): house suave de verano, 120 BPM, 20 s.
Fa mayor: Fmaj7 · Am7 · Dm9 · Bbmaj7. Un compás = 2 s, así cada corte del montaje cae en parte.
Uso: python3 scripts/synth-bed.py assets/bgm/bed.wav"""
import sys, wave
import numpy as np

SR, BPM, DUR = 48000, 120, 20.0
B = 60 / BPM                      # 0.5 s por negra
N = int(SR * DUR)
rng = np.random.default_rng(8)    # semilla fija: render determinista
L = np.zeros(N); R = np.zeros(N)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def put(sig, t, gl=1.0, gr=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i >= N: return
    L[i:j] += sig[:j - i] * gl; R[i:j] += sig[:j - i] * gr

# --- piezas
def kick():
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t * 32)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5) * 0.95
def hat(dec):
    n = int(0.25 * SR); x = rng.standard_normal(n)
    x = x - lp(x, 7000); return x * env(n, 0.001, dec) * 0.5
def clap():
    n = int(0.3 * SR); x = rng.standard_normal(n); x = lp(x - lp(x, 900), 5000)
    e = sum(env(n, 0.001, 0.012) * (np.arange(n) >= int(k * SR)) for k in (0, 0.011, 0.022)) + env(n, 0.002, 0.09)
    return x * e * 0.32
def ep(m, dur, vel):   # e-piano pluck: sine + octava + armónico 3 suave
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t)*np.exp(-t*6) + 0.12*np.sin(2*np.pi*3*f*t)*np.exp(-t*9)
    return s * env(n, 0.004, 0.32) * vel
def pad(ms, dur):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for m in ms:
        for det in (-0.08, 0.08):
            ph = 2*np.pi*hz(m + det)*t
            s += np.sin(ph) + 0.3*np.sin(2*ph)
    a = np.minimum(t / 0.25, 1) * np.minimum((dur - t) / 0.3, 1)
    return s * a * 0.03
def bass(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.25*np.sin(4*np.pi*f*t)
    return s * env(n, 0.006, 0.22) * 0.42

CH = [  # (raíz bajo, voicing)
    (41, [57, 60, 64, 65]),   # Fmaj7
    (45, [55, 60, 64, 67]),   # Am7
    (38, [57, 60, 64, 65, 69]),# Dm9 (F A C E)
    (46, [57, 62, 65, 69]),   # Bbmaj7
]
STAB = [0.5, 1.5, 2.0, 2.75, 3.5]   # en negras dentro del compás: patrón house
side = np.ones(N)                   # sidechain del pad al bombo

for bar in range(10):
    t0 = bar * 4 * B
    root, v = CH[bar % 4]
    last = bar >= 9
    # pad todo el rato (respira con el bombo)
    put(pad(v, 4 * B + (2.0 if last else 0.05)), t0, 0.9, 1.0)
    # stabs de e-piano
    if bar < 9:
        for k, q in enumerate(STAB):
            for i, m in enumerate(v):
                put(ep(m + 12 if i == len(v) - 1 else m, 0.9, 0.055), t0 + q * B, 0.8 + 0.1*i, 1.1 - 0.1*i)
    else:
        for i, m in enumerate(v):
            put(ep(m, 2.5, 0.07), t0, 0.9, 1.0)
    # bombo desde el compás 1 (2 s, entra con «doce meses de casa») hasta el 8
    if 1 <= bar <= 8:
        for q in range(4):
            put(kick(), t0 + q * B)
            i = int((t0 + q * B) * SR); j = min(N, i + int(0.3 * SR))
            side[i:j] = np.minimum(side[i:j], 0.35 + 0.65 * np.linspace(0, 1, j - i) ** 0.6)
    # bajo en contratiempo
    if 1 <= bar <= 8:
        for q in range(4):
            put(bass(root, 0.4), t0 + (q + 0.5) * B)
    # hats: contratiempo abierto siempre; cerrados en semicorcheas desde el compás 2
    if bar <= 8:
        for q in range(4):
            put(hat(0.07), t0 + (q + 0.5) * B, 0.7, 1.0)
            if bar >= 2:
                for s in (0.25, 0.75):
                    put(hat(0.018) * 0.5, t0 + (q + s) * B, 1.0, 0.7)
    if 2 <= bar <= 8:
        for q in (1, 3): put(clap(), t0 + q * B)

# el pad ya está en L/R; aplicar el sidechain a todo excepto picos de bombo es caro de separar,
# así que se aplica suave al conjunto: da el bombeo de house sin aplastar el bombo
pump = 0.75 + 0.25 * side
L *= pump; R *= pump
# fade final de 1 s
f = np.ones(N); f[-SR:] = np.linspace(1, 0, SR) ** 2
L *= f; R *= f
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.89, R / peak * 0.89
out = np.stack([L, R], 1)
pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", sys.argv[1], f"{DUR}s")
