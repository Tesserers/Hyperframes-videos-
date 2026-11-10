"""Pista original para la pizarra G·Madrid, sintetizada desde cero (sin samples ni
modelos): 124 BPM, La menor, progresión Am–F–C–G. Determinista (semilla fija).

Uso: python3 videos/_pizarra-src/music.py <salida.wav> [segundos]
"""
import sys
import wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
BPM = 124
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(7)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env_ad(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1.0) - 1


# ---------- instrumentos ----------
def kick():
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.22)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t / 0.004) * 0.35
    return np.tanh(1.6 * (body + click))


def clap():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 900, 5200)
    e = np.zeros(n)
    for off in (0, 0.009, 0.018):
        i = int(off * SR)
        e[i:] += np.exp(-(t[: n - i]) / 0.012)
    e += 0.6 * np.exp(-t / 0.11)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.4
    return (noise * e * 0.55 + tone)


def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 7000)
    return lp(x, 12000) * np.exp(-t / (0.06 if open_ else 0.012)) * (0.22 if open_ else 0.14)


def bass_note(note, dur):
    n = int(dur * SR)
    f = midi(note)
    x = saw(f, n) * 0.6 + saw(f * 0.5, n) * 0.5
    x = lp(x, 520)
    return np.tanh(2.2 * x) * env_ad(n, 0.004, 0.16)


def stab(notes, dur, cutoff=3200):
    n = int(dur * SR)
    L = np.zeros(n)
    R = np.zeros(n)
    for k, nt in enumerate(notes):
        f = midi(nt)
        for j, det in enumerate((-0.11, 0.0, 0.12)):
            ff = f * 2 ** (det / 12)
            v = saw(ff, n, phase=(k * 0.13 + j * 0.31) % 1)
            if j == 0:
                L += v
            elif j == 2:
                R += v
            else:
                L += v * 0.7
                R += v * 0.7
    e = env_ad(n, 0.003, 0.11)
    return lp(L, cutoff) * e * 0.16, lp(R, cutoff) * e * 0.16


def pluck(note, dur):
    n = int(dur * SR)
    f = midi(note)
    t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + saw(f * 2, n) * 0.3
    return lp(x, 2600) * env_ad(n, 0.002, 0.09) * 0.2


def riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n)
    seg = 2048
    for i in range(0, n, seg):
        u = i / n
        fc = 400 + 9000 * u ** 2
        out[i:i + seg] = bp(x[i:i + seg], fc * 0.6, min(fc * 1.4, 19000))
    return out * (t / dur) ** 2 * 0.2


def crash():
    n = int(1.8 * SR)
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 5000) * np.exp(-t / 0.5) * 0.12


# ---------- arreglo ----------
CHORDS = [  # (bajo, acorde)
    (45, [57, 60, 64, 69]),  # Am
    (41, [53, 57, 60, 65]),  # F
    (48, [55, 60, 64, 67]),  # C
    (43, [55, 59, 62, 67]),  # G
]
STAB_RHYTHM = [0, 0.75, 1.5, 2.5, 3.0, 3.5]  # en tiempos dentro del compás


def render(seconds):
    bars = int(np.ceil(seconds / BAR)) + 1
    n = int((bars * BAR + 2) * SR)
    drums = np.zeros(n)
    bass = np.zeros(n)
    musL = np.zeros(n)
    musR = np.zeros(n)
    fx = np.zeros(n)
    side = np.ones(n)

    K, C = kick(), clap()
    HC, HO = hat(False), hat(True)

    def put(buf, x, t, g=1.0):
        i = int(t * SR)
        j = min(n, i + len(x))
        if i < n:
            buf[i:j] += x[: j - i] * g

    breakdown = {16, 17}
    for b in range(bars):
        t0 = b * BAR
        bassn, chord = CHORDS[b % 4]
        intro = b < 2
        full = not intro and b not in breakdown
        # batería
        for beat in range(4):
            tb = t0 + beat * BEAT
            if full:
                put(drums, K, tb, 0.95)
                i = int(tb * SR)
                m = int(0.2 * SR)
                if i < n:
                    seg = side[i:i + m]
                    seg *= 1 - 0.6 * np.exp(-np.arange(len(seg)) / SR / 0.06)
            if full and beat in (1, 3):
                put(drums, C, tb, 0.8)
            put(drums, HO, tb + BEAT / 2, 0.9 if full else 0.5)
            if full or b in breakdown:
                for s in (0.25, 0.75):
                    put(drums, HC, tb + s * BEAT, 0.7)
        if intro and b == 1:
            for s in range(8):
                put(drums, C, t0 + 2 * BEAT + s * BEAT / 4, 0.25 + 0.08 * s)
        # bajo: corcheas a contratiempo + golpe en 1
        if full:
            for e8 in range(8):
                if e8 % 2 == 1 or e8 == 0:
                    note = bassn + (12 if e8 in (5,) else 0)
                    put(bass, bass_note(note, BEAT / 2), t0 + e8 * BEAT / 2, 0.55)
        # acordes
        cutoff = 900 + 1700 * min(1, b / 4) if b < 4 else (1200 if b in breakdown else 2600)
        for sb in STAB_RHYTHM:
            L, R = stab(chord, BEAT * 0.6, cutoff)
            put(musL, L, t0 + sb * BEAT)
            put(musR, R, t0 + sb * BEAT)
        # arpegio a partir del compás 18
        if b >= 18:
            arp = chord + [chord[1] + 12]
            for s16 in range(16):
                nt = arp[(s16 * 3) % len(arp)] + 12
                p = pluck(nt, BEAT / 4)
                put(musL, p, t0 + s16 * BEAT / 4, 0.8)
                put(musR, p, t0 + s16 * BEAT / 4 + 0.012, 0.8)
        # transiciones
        if b in (1, 17):
            put(fx, riser(BAR), t0)
        if b in (2, 18):
            put(fx, crash(), t0)

    bass *= side
    musL *= side
    musR *= side
    L = drums + bass + musL + fx * 0.9
    R = drums + bass + musR + fx
    st = np.stack([L, R], 1)
    st /= np.max(np.abs(st)) / 0.95
    st = np.tanh(st * 0.9) / np.tanh(0.9) * 0.89
    total = int(seconds * SR)
    st = st[:total]
    fade = int(2.5 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 1.5
    return st


def main():
    out = sys.argv[1]
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 62
    st = render(secs)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("ok", out, round(len(pcm) / SR, 2), "s")


if __name__ == "__main__":
    main()
