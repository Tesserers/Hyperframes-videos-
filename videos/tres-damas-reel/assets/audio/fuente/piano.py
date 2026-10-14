# Original short piano waltz for the Tres Damas reel. 3/4, 66 bpm, D major.
import sys, os, numpy as np, pretty_midi, tinysoundfont
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile
OUT = sys.argv[1]
SR = 48000; BPM = 66; B = 60 / BPM; BAR = 3 * B; T0 = 0.35; TOTAL = 25.0
N = lambda s: pretty_midi.note_name_to_number(s)

# (bass, chord tones) per bar
harm = [("D2", ["F#3", "A3", "C#4"]), ("G2", ["F#3", "B3", "D4"]), ("B1", ["F#3", "A3", "D4"]),
        ("A2", ["G3", "C#4", "E4"]), ("D2", ["F#3", "A3", "C#4"]), ("E2", ["G3", "B3", "D4"]),
        ("G2", ["F#3", "B3", "D4"]), ("A2", ["E3", "G3", "C#4"]), ("D2", ["A2", "F#3", "D4"])]
# melody: (bar, beat, length in beats, note)
mel = [(1, 0, 3, "F#5"), (2, 0, 2, "E5"), (2, 2, 1, "D5"), (3, 0, 2, "C#5"), (3, 2, 1, "E5"),
       (4, 0, 3, "A5"), (5, 0, 2, "G5"), (5, 2, 1, "F#5"), (6, 0, 2, "D5"), (6, 2, 1, "B4"),
       (7, 0, 2, "C#5"), (7, 2, 1, "E5"), (8, 0, 6, "D5")]

ev = []  # (time, kind, a, b)
for i, (bass, ch) in enumerate(harm):
    t = T0 + i * BAR
    last = i == len(harm) - 1
    ev += [(t - 0.02, "cc", 64, 0), (t + 0.04, "cc", 64, 127)]
    ev += [(t, "on", N(bass), 50), (t + (6 if last else 3) * B, "off", N(bass), 0)]
    tc = t + (0 if last else B)
    for k, n in enumerate(ch):
        tt = tc + k * 0.012  # tiny roll, played by a hand, not a sequencer
        ev += [(tt, "on", N(n), 34 + 3 * k), (tt + (6 if last else 2) * B, "off", N(n), 0)]
for bar, beat, ln, n in mel:
    t = T0 + bar * BAR + beat * B + 0.008
    ev += [(t, "on", N(n), 60 if ln > 1 else 54), (t + ln * B * 0.98, "off", N(n), 0)]
ev.sort(key=lambda e: (e[0], e[1] != "off"))

sf = os.path.join(os.path.dirname(pretty_midi.__file__), "TimGM6mb.sf2")
syn = tinysoundfont.Synth(samplerate=SR)
sid = syn.sfload(sf)
syn.program_select(0, sid, 0, 0)
out = []; now = 0.0
for t, kind, a, b in [e for e in ev if e[0] < TOTAL] + [(TOTAL, "end", 0, 0)]:
    n = int(round((t - now) * SR))
    if n > 0:
        out.append(np.frombuffer(syn.generate(n), dtype=np.float32).reshape(-1, 2).copy()); now += n / SR
    if kind == "on": syn.noteon(0, a, b)
    elif kind == "off": syn.noteoff(0, a)
    elif kind == "cc": syn.control_change(0, a, b)
dry = np.concatenate(out)

# Soft hall: decaying, darkened noise impulse response (2.4 s), deterministic seed.
rng = np.random.default_rng(7)
L = int(2.4 * SR); tt = np.arange(L) / SR
ir = rng.standard_normal((L, 2)) * np.exp(-tt / 0.55)[:, None]
ir = sosfilt(butter(2, 3500, "low", fs=SR, output="sos"), ir, axis=0)
ir[: int(0.018 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum(axis=0))
wet = np.stack([fftconvolve(dry[:, c], ir[:, c])[: len(dry)] for c in range(2)], axis=1)
mix = 0.78 * dry + 0.30 * wet
mix = sosfilt(butter(1, 60, "high", fs=SR, output="sos"), mix, axis=0)
mix *= 10 ** (-3 / 20) / np.abs(mix).max()
wavfile.write(f"{OUT}/musica.wav", SR, (mix * 32767).astype(np.int16))
print("ok", len(mix) / SR, "s; last note ends", T0 + 8 * BAR + 6 * B)
