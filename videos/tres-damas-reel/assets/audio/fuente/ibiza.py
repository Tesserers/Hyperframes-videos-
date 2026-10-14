# Original Balearic deep-house cue for the Tres Damas reel, synthesised from scratch.
# 120 bpm, A minor, bar grid offset 1 s so the scene cuts fall on downbeats:
#   0-7 s  intro: pad swell, marimba arp, filter opening, riser into the drop
#   7 s    drop (cut to green): four-on-the-floor, bass, clap, hats
#   15 s   lift (strips in hand): open hats, arp up an octave
#   19 s   breakdown (logo card): kick out, pads and arp ring to the end
import sys, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

OUT = sys.argv[1]
SR = 48000; BPM = 120; B = 60 / BPM; BAR = 4 * B; T0 = 1.0; TOTAL = 25.0
n = int(TOTAL * SR); t_all = np.arange(n) / SR
rng = np.random.default_rng(11)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def bt(bar, beat=0.0): return T0 + bar * BAR + beat * B
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x, axis=0)
def add(buf, start, sig):
    i = int(round(start * SR))
    if i >= n: return
    if i < 0: sig = sig[-i:]; i = 0
    m = min(len(sig), n - i); buf[i:i + m] += sig[:m]

DROP, LIFT, BREAK = 3, 7, 9          # bar indices: 7 s, 15 s, 19 s
NBARS = 12
# Am9 - Fmaj9 - Dm9 - Em7(11), midi voicings (pad) and roots (bass)
CH = [([57, 60, 64, 67, 71], 45), ([53, 57, 60, 64, 67], 41), ([50, 53, 57, 60, 64], 38), ([52, 55, 59, 62, 69], 40)]

# ---- drums -------------------------------------------------------------------------
kick = np.zeros(n); clap = np.zeros(n); hats = np.zeros(n); ohat = np.zeros(n); riser = np.zeros(n)
def kick_hit():
    L = int(0.42 * SR); tt = np.arange(L) / SR
    f = 46 + 95 * np.exp(-tt / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt / 0.16) + 0.25 * np.exp(-tt / 0.004) * rng.standard_normal(L) * 0.1
def noise_hit(dur, tau, lo, hi):
    L = int(dur * SR); tt = np.arange(L) / SR
    return hp(lp(rng.standard_normal(L), hi), lo) * np.exp(-tt / tau)
def clap_hit():
    x = np.zeros(int(0.3 * SR))
    for k, d in enumerate((0, 0.011, 0.022)):
        h = noise_hit(0.25 if k == 2 else 0.02, 0.06 if k == 2 else 0.006, 900, 6000)
        i = int(d * SR); x[i:i + len(h)] += h[: len(x) - i]
    return x
K = kick_hit()
for bar in range(DROP, BREAK):
    for b in range(4): add(kick, bt(bar, b), K)
    for b in (1, 3): add(clap, bt(bar, b), clap_hit())
    for b in range(4):
        add(hats, bt(bar, b + 0.5), noise_hit(0.05, 0.012, 7000, 15000) * (1.0 if b % 2 else 0.8))
        add(hats, bt(bar, b + 0.75), noise_hit(0.03, 0.006, 8000, 15000) * 0.35)
        if bar >= LIFT: add(ohat, bt(bar, b + 0.5), noise_hit(0.22, 0.07, 6000, 14000))
# light shaker through the intro and outro so it never stops moving
for bar in list(range(1, DROP)) + list(range(BREAK, NBARS)):
    for b in range(4): add(hats, bt(bar, b + 0.5), noise_hit(0.04, 0.01, 7500, 15000) * 0.45)
# riser into the drop: filtered noise sweeping up over the last bar of the intro
L = int(BAR * SR); tt = np.arange(L) / SR; x = rng.standard_normal(L)
seg = np.concatenate([lp(x[i:i + 2400], 600 + 9000 * (i / L) ** 2) for i in range(0, L, 2400)])
add(riser, bt(DROP - 1), seg * (tt / BAR) ** 2)

# ---- sidechain envelope (pads and bass duck under each kick) ----------------------
duck = np.ones(n)
for bar in range(DROP, BREAK):
    for b in range(4):
        i = int(bt(bar, b) * SR); L = int(0.3 * SR); tt = np.arange(L) / SR
        m = min(L, n - i); duck[i:i + m] = np.minimum(duck[i:i + m], 1 - 0.65 * np.exp(-tt[:m] / 0.09))

# ---- pads: detuned saws, slow attack, low-pass that opens across the intro ---------
def saw(f, L, phase=0.0):
    tt = np.arange(L) / SR
    return 2 * ((f * tt + phase) % 1.0) - 1
pad = np.zeros((n, 2))
for bar in range(-1, NBARS):
    notes, _ = CH[bar % 4]
    start = bt(bar); L = int((BAR + 0.6) * SR); tt = np.arange(L) / SR
    env = np.minimum(1, tt / 0.45) * np.minimum(1, np.maximum(0, (BAR + 0.6 - tt) / 0.6))
    for side, det in ((0, -1), (1, 1)):
        v = sum(saw(hz(m) * 2 ** (det * c / 1200), L, (m * 0.137 + c * 0.31) % 1) for m in notes for c in (7, 13))
        add(pad[:, side], start, v * env)
cut = np.clip((t_all - 0.0) / (bt(DROP) - 0.0), 0, 1)  # 0 -> 1 across the intro
pad_out = np.zeros_like(pad)
for k in range(0, n, 4800):          # block-wise filter sweep, 300 Hz -> 2.6 kHz
    f = 300 + 2300 * cut[k] ** 1.5
    pad_out[k:k + 4800] = lp(pad[k:k + 4800], f)
pad = pad_out * duck[:, None]

# ---- bass: sine + a little square, off-beat deep-house pattern --------------------
bass = np.zeros(n)
for bar in range(DROP, NBARS if False else BREAK):
    _, root = CH[bar % 4]
    for pos, ln in ((0.5, 0.4), (1.5, 0.4), (2.5, 0.3), (2.75, 0.2), (3.5, 0.4)):
        L = int(ln * B * SR); tt = np.arange(L) / SR; f = hz(root - 12 + (12 if pos == 2.75 else 0))
        s = np.sin(2 * np.pi * f * tt) + 0.18 * np.sign(np.sin(2 * np.pi * f * tt))
        add(bass, bt(bar, pos), lp(s, 900) * np.minimum(1, tt / 0.005) * np.exp(-tt / 0.22))
bass *= duck

# ---- marimba arp with dotted-eighth delay: the Ibiza sunset hook ------------------
arp = np.zeros(n)
pat = [0, 2, 4, 3, 1, 4, 2, 3]
for bar in range(0, NBARS):
    notes, _ = CH[bar % 4]
    up = 12 if LIFT <= bar < BREAK else 0
    for k in range(8):
        if bar < 1 and k < 4: continue
        m = notes[pat[k]] + 12 + up
        L = int(0.5 * SR); tt = np.arange(L) / SR; f = hz(m)
        s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.18) + 0.35 * np.sin(2 * np.pi * f * 3.93 * tt) * np.exp(-tt / 0.03))
        add(arp, bt(bar, k * 0.5), s * (0.9 if k % 2 == 0 else 0.7))
d = int(0.75 * B * SR); echo = np.zeros(n)
for k, g in ((1, 0.45), (2, 0.22), (3, 0.1)):
    echo[k * d:] += lp(arp, 3000)[: n - k * d] * g
arpL = arp + echo; arpR = arp + np.roll(echo, int(0.012 * SR))

# ---- mix --------------------------------------------------------------------------
def nrm(x): return x / (np.abs(x).max() + 1e-9)
mix = np.zeros((n, 2))
mix += 0.95 * nrm(kick)[:, None]
mix += 0.30 * nrm(clap)[:, None]
mix[:, 0] += 0.16 * nrm(hats); mix[:, 1] += 0.13 * nrm(hats)
mix[:, 0] += 0.08 * nrm(ohat); mix[:, 1] += 0.11 * nrm(ohat)
mix += 0.22 * nrm(riser)[:, None]
mix += 0.55 * nrm(bass)[:, None]
mix += 0.42 * pad / (np.abs(pad).max() + 1e-9)
mix[:, 0] += 0.30 * nrm(arpL); mix[:, 1] += 0.30 * nrm(arpR)
# room tail on everything but kick and bass
L = int(1.6 * SR); tt = np.arange(L) / SR
ir = lp(rng.standard_normal((L, 2)) * np.exp(-tt / 0.4)[:, None], 5000); ir[:600] = 0; ir /= np.sqrt((ir ** 2).sum(0))
send = 0.3 * pad / (np.abs(pad).max()) + 0.25 * np.stack([nrm(arpL), nrm(arpR)], 1) + 0.15 * nrm(clap)[:, None]
mix += 0.35 * np.stack([fftconvolve(send[:, c], ir[:, c])[:n] for c in range(2)], 1)
mix = hp(mix, 30)
mix = np.tanh(1.4 * mix / np.abs(mix).max()) ; mix *= 10 ** (-1.5 / 20) / np.abs(mix).max()
wavfile.write(f"{OUT}/musica-ibiza.wav", SR, (mix * 32767).astype(np.int16))
print("ok", TOTAL, "s; drop", bt(DROP), "lift", bt(LIFT), "break", bt(BREAK))
