"""Quita el fondo blanco del logo original de G·Madrid Balonmano sin tocar colores ni letras.
Bordes descontaminados (sin halo blanco). Exporta el logo completo y, por separado,
la estrella y el texto para animarlos con un pequeño desfase.
Uso: python3 tools/clean_logo.py <logo.png> <carpeta_salida>"""
import sys, os
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert("RGB")
w, h = im.size
im = im.resize((w * 2, h * 2), Image.LANCZOS)  # bordes más suaves
c = np.array(im).astype(float)
d = (255 - c).max(-1)                      # distancia al blanco
a = np.clip((d - 14) / 46, 0, 1)
# descontaminar: quitar la mezcla con blanco en los bordes
aa = np.maximum(a, 1e-3)[..., None]
rgb = np.clip((c - 255 * (1 - aa)) / aa, 0, 255)
rgb = np.where(a[..., None] > 0.98, c, rgb)
rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
logo = Image.fromarray(rgba, "RGBA")
logo = logo.crop(logo.getbbox())
logo.save(os.path.join(out, "gmadrid-logo.png"))
# separar estrella y texto por la franja vacía entre ambos
al = np.array(logo)[..., 3]
rows = al.max(1) > 20
H = len(rows)
gap = None
for y in range(int(H * 0.5), int(H * 0.85)):
    if not rows[y]:
        gap = y
        break
star = logo.crop((0, 0, logo.width, gap)); star = star.crop(star.getbbox())
text = logo.crop((0, gap, logo.width, logo.height))
bb = text.getbbox(); text_off = gap + bb[1]; text = text.crop(bb)
star.save(os.path.join(out, "gmadrid-logo-star.png"))
text.save(os.path.join(out, "gmadrid-logo-text.png"))
print("logo", logo.size, "gap", gap, "star", star.size, "text", text.size, "text_top", text_off, "text_left", bb[0])
