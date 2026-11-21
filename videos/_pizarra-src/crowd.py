"""Público aplaudiendo, sintetizado (sin samples): muchas palmas individuales con
ritmo propio + murmullo de pabellón. Más fuerte en las ovaciones (intro, decisión
final, clave y cierre). Determinista.

Uso: python3 crowd.py <salida.wav> <segundos> '<marks json>'
"""
import json
import sys
import wave
import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
rng = np.random.default_rng(1997)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def lp(x, fc):
    return sosfilt(butter(2, fc, "low", fs=SR, output="sos"), x)


def clap_kernel(center):
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = bp(x, center * 0.55, min(center * 1.8, 9000))
    return x * np.exp(-t / (0.008 + rng.random() * 0.01))


def main():
    out, secs, marks = sys.argv[1], float(sys.argv[2]), json.loads(sys.argv[3])
    n = int(secs * SR)
    t = np.arange(n) / SR
    # intensidad del público a lo largo del vídeo
    level = np.full(n, 0.18)

    def ovation(t0, dur, peak):
        a = np.clip((t - t0) / 0.35, 0, 1) * np.clip((t0 + dur - t) / 1.2, 0, 1)
        np.maximum(level, peak * a, out=level)

    ovation(0.0, 3.6, 1.0)
    ovation(marks["decision"] + 0.6, 2.8, 0.7)
    ovation(marks["key"], 2.4, 0.55)
    ovation(marks["outro"], secs - marks["outro"], 1.0)
    level = lp(level, 3)

    L = np.zeros(n)
    R = np.zeros(n)
    kernels = [clap_kernel(c) for c in rng.uniform(900, 2600, 48)]
    for p in range(70):
        rate = rng.uniform(3.2, 5.0)
        pan = rng.uniform(0.15, 0.85)
        gain = rng.uniform(0.4, 1.0)
        k = kernels[p % len(kernels)]
        tt = rng.uniform(0, 1 / rate)
        while tt < secs:
            i = int(tt * SR)
            j = min(n, i + len(k))
            g = gain * level[i]
            if g > 0.02 and rng.random() < 0.6 + 0.4 * level[i]:
                L[i:j] += k[: j - i] * g * (1 - pan)
                R[i:j] += k[: j - i] * g * pan
            tt += (1 / rate) * rng.uniform(0.85, 1.15)
    # murmullo de pabellón
    mur = lp(np.cumsum(rng.standard_normal(n)) * 0.002, 700)
    mur = mur - lp(mur, 80)
    mur *= 0.5 + 0.5 * level
    L += mur * 0.6
    R += mur * 0.6
    st = np.stack([L, R], 1)
    st /= np.max(np.abs(st)) / 0.8
    fade = int(1.5 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    st[: int(0.15 * SR)] *= np.linspace(0, 1, int(0.15 * SR))[:, None]
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
