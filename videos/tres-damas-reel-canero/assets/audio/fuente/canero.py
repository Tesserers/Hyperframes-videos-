# Original Balearic tech-house cue for the "cañero" cut of the Tres Damas reel.
# 120 bpm (one beat = 0.5 s, one bar = 2 s), A minor, synthesised from scratch.
#   0-2 s   intro: filtered pad, shaker, riser
#   2-8 s   drop 1: four-on-the-floor, rolling 16th bass, clap, hats
#   8-10 s  countdown break: three hits (3, 2, 1) then a snare roll
#   10-24 s drop 2: open hats, arp up an octave
#   24 s    final hit, ringing out
import sys, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

OUT = sys.argv[1]
SR = 48000; B = 0.5; BAR = 2.0; TOTAL = 25.0
n = int(TOTAL * SR); t_all = np.arange(n) / SR
rng = np.random.default_rng(21)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def bt(bar, beat=0.0): return bar * BAR + beat * B
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x, axis=0)
def add(buf, start, sig, g=1.0):
    i = int(round(start * SR))
    if i >= n: return
    m = min(len(sig), n - i); buf[i:i + m] += g * sig[:m]

DROP1 = [1, 2, 3]; BREAK = 4; DROP2 = list(range(5, 12)); END = 12
DRUM_BARS = DROP1 + DROP2
CH = [([57, 60, 64, 67, 71], 45), ([53, 57, 60, 64, 67], 41), ([50, 53, 57, 60, 64], 38), ([52, 55, 59, 62, 69], 40)]

def kick_hit():
    L = int(0.4 * SR); tt = np.arange(L) / SR
    f = 48 + 120 * np.exp(-tt / 0.03)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.17)
    click = hp(rng.standard_normal(L), 2000) * np.exp(-tt / 0.003) * 0.3
    return np.tanh(1.6 * (s + click))
def noise_hit(dur, tau, lo, hi):
    L = int(dur * SR); tt = np.arange(L) / SR
    return hp(lp(rng.standard_normal(L), hi), lo) * np.exp(-tt / tau)
def clap_hit():
    x = np.zeros(int(0.35 * SR))
    for k, d in enumerate((0, 0.01, 0.021)):
        h = noise_hit(0.3 if k == 2 else 0.02, 0.08 if k == 2 else 0.006, 800, 7000)
        i = int(d * SR); x[i:i + len(h)] += h[: len(x) - i]
    return x
def snare_hit(g=1.0):
    L = int(0.2 * SR); tt = np.arange(L) / SR
    body = np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.04)
    return g * (0.6 * body + noise_hit(0.2, 0.05, 1500, 9000))

kick = np.zeros(n); clap = np.zeros(n); hats = np.zeros(n); ohat = np.zeros(n); fx = np.zeros(n)
K = kick_hit()
for bar in DRUM_BARS:
    for b in range(4): add(kick, bt(bar, b), K)
    for b in (1, 3): add(clap, bt(bar, b), clap_hit())
    for b in range(4):
        for s16, g in ((0.25, 0.35), (0.5, 1.0), (0.75, 0.5)):
            add(hats, bt(bar, b + s16), noise_hit(0.04, 0.01, 7500, 16000), g)
        if bar in DROP2: add(ohat, bt(bar, b + 0.5), noise_hit(0.25, 0.08, 6000, 15000))
# intro shaker + riser into the first drop
for b in range(4): add(hats, bt(0, b + 0.5), noise_hit(0.04, 0.01, 7500, 16000), 0.5)
def riser(start, dur, g=1.0):
    L = int(dur * SR); tt = np.arange(L) / SR; x = rng.standard_normal(L)
    seg = np.concatenate([lp(x[i:i + 2400], 500 + 10000 * (i / L) ** 2) for i in range(0, L, 2400)])
    add(fx, start, seg * (tt / dur) ** 2, g)
riser(0.0, 2.0)
# countdown break: three hits on 3-2-1, then a snare roll that accelerates into drop 2
for b in (0, 1, 2):
    add(kick, bt(BREAK, b), K); add(clap, bt(BREAK, b), clap_hit())
snare = np.zeros(n)
for k in range(8): add(snare, bt(BREAK, 2 + k * 0.25), snare_hit(0.35 + 0.08 * k))
riser(bt(BREAK, 2), 1.0, 0.9)
# final hit
add(kick, bt(END), K); add(clap, bt(END), clap_hit())
crash = noise_hit(1.0, 0.35, 4000, 16000); add(ohat, bt(END), crash, 3.0)

duck = np.ones(n)
for bar in DRUM_BARS + [BREAK, END]:
    beats = range(4) if bar in DRUM_BARS else ((0, 1, 2) if bar == BREAK else (0,))
    for b in beats:
        i = int(bt(bar, b) * SR); L = int(0.3 * SR); tt = np.arange(L) / SR
        m = min(L, n - i); duck[i:i + m] = np.minimum(duck[i:i + m], 1 - 0.7 * np.exp(-tt[:m] / 0.09))

def saw(f, L, ph=0.0):
    tt = np.arange(L) / SR; return 2 * ((f * tt + ph) % 1.0) - 1
pad = np.zeros((n, 2))
for bar in range(0, END + 1):
    notes, _ = CH[bar % 4]
    L = int((BAR + 0.8) * SR); tt = np.arange(L) / SR
    env = np.minimum(1, tt / 0.08) * np.minimum(1, np.maximum(0, (BAR + 0.8 - tt) / 0.8))
    if bar == END: env = np.minimum(1, tt / 0.02) * np.exp(-tt / 0.6)
    for side, det in ((0, -1), (1, 1)):
        v = sum(saw(hz(m) * 2 ** (det * c / 1200), L, (m * 0.137 + c * 0.31) % 1) for m in notes for c in (8, 15))
        add(pad[:, side], bt(bar), v * env)
fc = np.where(t_all < 2, 400 + 2600 * (t_all / 2) ** 2, np.where((t_all >= 8) & (t_all < 10), 900 + 2000 * ((t_all - 8) / 2) ** 2, 3200))
po = np.zeros_like(pad)
for k in range(0, n, 2400): po[k:k + 2400] = lp(pad[k:k + 2400], fc[k])
pad = po * duck[:, None]

bass = np.zeros(n)
for bar in DRUM_BARS:
    _, root = CH[bar % 4]
    for b in range(4):
        for s16, oct_ in ((0.25, 0), (0.5, 0), (0.75, 12)):
            L = int(0.11 * SR); tt = np.arange(L) / SR; f = hz(root - 12 + oct_)
            s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sign(np.sin(2 * np.pi * f * tt))
            add(bass, bt(bar, b + s16), lp(s, 1100) * np.minimum(1, tt / 0.003) * np.exp(-tt / 0.07))
bass *= duck

arp = np.zeros(n); pat = [0, 2, 4, 3, 1, 4, 2, 3]
for bar in list(range(0, BREAK)) + DROP2:
    notes, _ = CH[bar % 4]; up = 12 if bar in DROP2 else 0
    for k in range(8):
        m = notes[pat[k]] + 12 + up; L = int(0.4 * SR); tt = np.arange(L) / SR; f = hz(m)
        s = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.14) + 0.35 * np.sin(2 * np.pi * f * 3.93 * tt) * np.exp(-tt / 0.025)
        add(arp, bt(bar, k * 0.5), s, 0.9 if k % 2 == 0 else 0.7)
d = int(0.75 * B * SR); echo = np.zeros(n)
for k, g in ((1, 0.4), (2, 0.18)): echo[k * d:] += lp(arp, 3000)[: n - k * d] * g
arpL = arp + echo; arpR = arp + np.roll(echo, int(0.012 * SR))

def nrm(x): return x / (np.abs(x).max() + 1e-9)
mix = np.zeros((n, 2))
mix += 1.0 * nrm(kick)[:, None]
mix += 0.38 * nrm(clap)[:, None]
mix += 0.3 * nrm(snare)[:, None]
mix[:, 0] += 0.17 * nrm(hats); mix[:, 1] += 0.14 * nrm(hats)
mix[:, 0] += 0.08 * nrm(ohat); mix[:, 1] += 0.11 * nrm(ohat)
mix += 0.25 * nrm(fx)[:, None]
mix += 0.6 * nrm(bass)[:, None]
mix += 0.38 * pad / (np.abs(pad).max() + 1e-9)
mix[:, 0] += 0.26 * nrm(arpL); mix[:, 1] += 0.26 * nrm(arpR)
L = int(1.4 * SR); tt = np.arange(L) / SR
ir = lp(rng.standard_normal((L, 2)) * np.exp(-tt / 0.35)[:, None], 5000); ir[:600] = 0; ir /= np.sqrt((ir ** 2).sum(0))
send = 0.3 * pad / np.abs(pad).max() + 0.2 * np.stack([nrm(arpL), nrm(arpR)], 1) + 0.15 * nrm(clap)[:, None] + 0.15 * nrm(snare)[:, None]
mix += 0.3 * np.stack([fftconvolve(send[:, c], ir[:, c])[:n] for c in range(2)], 1)
mix = hp(mix, 30)
mix = np.tanh(1.8 * mix / np.abs(mix).max()); mix *= 10 ** (-1.2 / 20) / np.abs(mix).max()
wavfile.write(f"{OUT}/musica-canera.wav", SR, (mix * 32767).astype(np.int16))
print("ok")
