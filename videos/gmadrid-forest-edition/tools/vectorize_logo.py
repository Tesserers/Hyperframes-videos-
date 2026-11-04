"""Vectoriza la estrella de G·Madrid (PNG 256px) a paths SVG por color.
Uso: python3 tools/vectorize_logo.py <logo.png> <salida.js>
Asigna cada pixel al color de marca más cercano y traza contornos suavizados."""
import sys, json
import numpy as np, cv2
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert("RGBA")).astype(np.float32)
SCALE = 8
H, W = im.shape[:2]
big = cv2.resize(im, (W*SCALE, H*SCALE), interpolation=cv2.INTER_CUBIC)
rgb, alpha = big[..., :3], big[..., 3]
# Colores de referencia muestreados del logo -> color de marca exacto del brief
REF = {
    "red":    ((220, 10, 20),  "#E30613"),
    "orange": ((245, 170, 10), "#F39200"),
    "yellow": ((248, 225, 10), "#FFDD00"),
    "green":  ((150, 180, 20), "#95C11F"),
    "blue":   ((10, 155, 225), "#009FE3"),
    "purple": ((145, 15, 110), "#8E1E7E"),
    "grey":   ((110, 128, 130), "#9AA3A6"),
}
names = list(REF)
refs = np.array([REF[n][0] for n in names], np.float32)
d = ((rgb[..., None, :] - refs[None, None]) ** 2).sum(-1)
lab = d.argmin(-1)
shapes = []
for i, n in enumerate(names):
    m = ((lab == i) & (alpha > 128)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), SCALE * 0.9)
    m = (m > 0.5).astype(np.uint8)
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    d_parts = []
    for c in cs:
        if cv2.contourArea(c) < (SCALE * 2) ** 2:
            continue
        c = cv2.approxPolyDP(c, SCALE * 0.18, True)[:, 0, :]
        cxy = c / (W * SCALE)  # normalizado 0..1
        pts = " L".join(f"{x:.4f} {y:.4f}" for x, y in cxy)
        d_parts.append("M" + pts + "Z")
    shapes.append({"name": n, "color": REF[n][1], "d": " ".join(d_parts)})
with open(out, "w") as f:
    f.write("// Generado por tools/vectorize_logo.py — estrella G·Madrid, coords normalizadas 0..1\n")
    f.write("window.GMADRID_STAR = " + json.dumps(shapes) + ";\n")
print({s["name"]: len(s["d"]) for s in shapes})
