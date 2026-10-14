# Original medium-swing jazz trio cue for the Tres Damas reel.
# Piano + walking acoustic bass + brushes and ride. F major, 126 bpm, 4/4, 12 bars.
# Deterministic: no randomness except a seeded reverb tail.
import sys, os, numpy as np, pretty_midi, tinysoundfont
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

OUT = sys.argv[1]
SR = 48000; BPM = 126; B = 60 / BPM; BAR = 4 * B; T0 = 0.25; TOTAL = 25.0
N = pretty_midi.note_name_to_number
PIANO, BASS, DR = 0, 1, 9

def at(bar, beat):
    """Swung time: an off-beat eighth lands two-thirds of the way through the beat."""
    whole = int(beat); frac = beat - whole
    return T0 + bar * BAR + (whole + (2 / 3 if abs(frac - 0.5) < 1e-6 else frac)) * B

ev = []
def note(ch, t, n, vel, dur):
    ev.append((t, 1, ch, N(n) if isinstance(n, str) else n, vel))
    ev.append((t + dur, 0, ch, N(n) if isinstance(n, str) else n, 0))

# --- Harmony: one chord per bar, bar 10 splits into two -----------------------
voic = {
    "Fmaj7": ["A3", "C4", "E4", "G4"], "D7": ["F#3", "B3", "C4", "E4"],
    "Gm7": ["Bb3", "D4", "F4", "A4"], "C7": ["Bb3", "D4", "E4", "A4"],
    "Am7": ["G3", "C4", "E4", "B4"], "Bb7": ["Ab3", "C4", "D4", "G4"],
    "F6/9": ["A3", "D4", "E4", "G4", "C5"],
}
bars = ["Fmaj7", "D7", "Gm7", "C7", "Am7", "D7", "Gm7", "C7", "Fmaj7", "Bb7", ("Gm7", "C7"), "F6/9"]

# --- Walking bass: four quarters a bar, last bar is the held tonic ------------
walk = [["F2", "A2", "C3", "C#3"], ["D3", "C3", "A2", "Ab2"], ["G2", "A2", "Bb2", "B2"],
        ["C3", "Bb2", "G2", "Bb2"], ["A2", "C3", "E3", "Eb3"], ["D3", "C3", "A2", "Ab2"],
        ["G2", "Bb2", "D3", "Db3"], ["C3", "Bb2", "G2", "E2"], ["F2", "A2", "C3", "B2"],
        ["Bb2", "D3", "F2", "Ab2"], ["G2", "Bb2", "C3", "E2"]]
for i, w in enumerate(walk):
    for k, n in enumerate(w):
        note(BASS, at(i, k), n, 92 if k == 0 else 80, B * 0.92)
note(BASS, at(11, 0), "F2", 96, 3.2)

# --- Piano comping: Charleston (1 and the and-of-2), short and light ----------
for i, c in enumerate(bars):
    halves = [(c, 0)] if isinstance(c, str) else [(c[0], 0), (c[1], 2)]
    for ch, off in halves:
        if i == 11:
            for k, n in enumerate(voic[ch]):
                note(PIANO, at(i, 0) + k * 0.015, n, 62, 3.4)
            continue
        hits = [(off, 0.9)] if len(halves) == 2 else [(0, 0.9), (1.5, 0.45)]
        if len(halves) == 2 and off == 2: hits = [(2, 0.45), (3.5, 0.4)]
        for pos, ln in hits:
            for k, n in enumerate(voic[ch]):
                note(PIANO, at(i, pos) + k * 0.006, n, 44 if pos else 48, ln * B)

# --- Melody: right hand, swung, conversational --------------------------------
mel = {
    1: [(3, .5, "C5"), (3.5, .5, "D5")],
    2: [(0, 1.5, "F5"), (1.5, .5, "D5"), (2, 1, "Bb4"), (3, .5, "A4"), (3.5, .5, "Bb4")],
    3: [(0, 2, "E5"), (2.5, .5, "D5"), (3, 1, "C5")],
    4: [(0, 1.5, "E5"), (1.5, .5, "G5"), (2, 2, "E5")],
    5: [(0, .5, "F#5"), (.5, .5, "A5"), (1, 1, "C6"), (2, 1, "A5"), (3, .5, "F#5"), (3.5, .5, "G5")],
    6: [(0, 2, "A5"), (2.5, .5, "F5"), (3, 1, "D5")],
    7: [(0, 1.5, "E5"), (1.5, .5, "G5"), (2, 1, "Bb5"), (3, 1, "A5")],
    8: [(0, 1.5, "A5"), (1.5, .5, "G5"), (2, 1, "F5"), (3, .5, "C5"), (3.5, .5, "D5")],
    9: [(0, 1.5, "F5"), (1.5, .5, "Ab5"), (2, 2, "G5")],
    10: [(0, 1, "F5"), (1, 1, "D5"), (2, 1, "E5"), (3, 1, "G5")],
    11: [(0, 4, "F5")],
}
for i, ph in mel.items():
    for pos, ln, n in ph:
        accent = 74 if pos == int(pos) else 64  # off-beats a touch lighter, as swing is played
        note(PIANO, at(i, pos), n, accent, (ln * B * 0.9) if ln < 4 else 3.4)

# --- Drums (brush kit): ride "ding, ding-da", hi-hat and a brush tap on 2 and 4 --
RIDE, HAT, SLAP = 51, 44, 38
for i in range(11):
    for k in range(4):
        note(DR, at(i, k), RIDE, 58 if k % 2 else 50, 0.3)
        if k % 2:
            note(DR, at(i, k), HAT, 56, 0.1)
            note(DR, at(i, k), SLAP, 30, 0.1)  # brush tap on 2 and 4
    note(DR, at(i, 1.5), RIDE, 40, 0.2)
    note(DR, at(i, 3.5), RIDE, 40, 0.2)
    if i in (3, 7): note(DR, at(i, 3.5), SLAP, 52, 0.2)  # small fills into the phrase turns
    if i == 10: note(DR, at(i, 3.5), SLAP, 60, 0.2)
note(DR, at(11, 0), RIDE, 70, 2.5); note(DR, at(11, 0), SLAP, 58, 0.3)

# --- Render ---------------------------------------------------------------------
ONLY = os.environ.get("ONLY")
if ONLY is not None: ev = [e for e in ev if e[2] == int(ONLY)]
ev.sort(key=lambda e: (e[0], e[1]))
sf = os.path.join(os.path.dirname(pretty_midi.__file__), "TimGM6mb.sf2")
syn = tinysoundfont.Synth(samplerate=SR); sid = syn.sfload(sf)
syn.program_select(PIANO, sid, 0, 0)
syn.program_select(BASS, sid, 0, 32)
syn.program_select(DR, sid, 128, 40, True)
out = []; now = 0.0
for t, on, ch, n, vel in [e for e in ev if e[0] < TOTAL] + [(TOTAL, -1, 0, 0, 0)]:
    k = int(round((t - now) * SR))
    if k > 0:
        out.append(np.frombuffer(syn.generate(k), dtype=np.float32).reshape(-1, 2).copy()); now += k / SR
    if on == 1: syn.noteon(ch, n, vel)
    elif on == 0: syn.noteoff(ch, n)
dry = np.concatenate(out)

# Small room: short darkened noise tail, seeded.
rng = np.random.default_rng(7)
L = int(1.3 * SR); tt = np.arange(L) / SR
ir = rng.standard_normal((L, 2)) * np.exp(-tt / 0.3)[:, None]
ir = sosfilt(butter(2, 4000, "low", fs=SR, output="sos"), ir, axis=0)
ir[: int(0.012 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum(axis=0))
wet = np.stack([fftconvolve(dry[:, c], ir[:, c])[: len(dry)] for c in range(2)], axis=1)
mix = 0.85 * dry + 0.2 * wet
mix = sosfilt(butter(1, 40, "high", fs=SR, output="sos"), mix, axis=0)
if ONLY is None: mix *= 10 ** (-3 / 20) / np.abs(mix).max()
wavfile.write(f"{OUT}/musica.wav", SR, (mix * 32767).astype(np.int16))
print("ok", round(len(mix) / SR, 2), "s; final chord at", round(at(11, 0), 2), "s")
