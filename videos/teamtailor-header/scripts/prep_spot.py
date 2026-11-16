"""Encuadres del spot. Uso: python3 -I scripts/prep_spot.py <origen> <destino>

Salen un 15 % más grandes que el hueco donde van (1920x1080, 640x1080 o 960x1080), para que
la cámara pueda moverse sin que el navegador amplíe la foto más de la cuenta.
"""
import sys, os
from PIL import Image, ImageFilter

SRC = {
    "equipo": "Equipo_Marketing_Tessera.jpg", "oficina": "Oficina_Minimalista_Tessera.jpg",
    "ciudad": "Ciudad_Luces_Tessera.jpg", "granvia": "Madrid_GranVia_Tessera.jpg",
    "molinos": "Molinos_Tessera.jpg", "reunion": "Reunion_Equipo_Tessera.jpg",
    "despacho": "Despacho_Tessera.jpg", "tesserers": "Oficina_Tesserers.jpg",
}
K = 1.15
SIZE = {"full": (1920, 1080), "p3": (640, 1080), "p2": (960, 1080)}
# nombre: (foto, formato, cx, cy, zoom)
SHOTS = {
    "full-tesserers": ("tesserers", "full", 0.50, 0.50, 1.0),
    "full-ciudad":    ("ciudad",    "full", 0.50, 0.62, 1.0),
    "full-reunion":   ("reunion",   "full", 0.50, 0.56, 1.0),
    "full-equipo":    ("equipo",    "full", 0.50, 0.30, 1.0),
    "full-molinos":   ("molinos",   "full", 0.55, 0.46, 1.0),
    "full-oficina":   ("oficina",   "full", 0.50, 0.66, 1.0),
    "p3-equipo-ella": ("equipo",    "p3", 0.30, 0.28, 1.5),
    "p3-ciudad":      ("ciudad",    "p3", 0.40, 0.62, 1.0),
    "p3-oficina":     ("oficina",   "p3", 0.72, 0.64, 1.3),
    "p2-despacho":    ("despacho",  "p2", 0.66, 0.40, 1.2),
    "p2-molinos":     ("molinos",   "p2", 0.68, 0.48, 1.0),
    "p3-granvia":     ("granvia",   "p3", 0.40, 0.72, 1.0),
    "p3-tesserers":   ("tesserers", "p3", 0.66, 0.55, 1.0),
    "p3-reunion":     ("reunion",   "p3", 0.50, 0.56, 1.4),
    "p2-ciudad":      ("ciudad",    "p2", 0.30, 0.72, 1.5),
    "p2-despacho-b":  ("despacho",  "p2", 0.45, 0.66, 1.0),
    "p3-molinos":     ("molinos",   "p3", 0.70, 0.50, 1.0),
    "p3-equipo-el":   ("equipo",    "p3", 0.72, 0.28, 1.5),
    "p3-granvia-b":   ("granvia",   "p3", 0.30, 0.50, 1.2),
}

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for name, (pid, fmt, cx, cy, zoom) in SHOTS.items():
    im = Image.open(os.path.join(src, SRC[pid])).convert("RGB")
    W, H = im.size
    w, h = [round(v * K) for v in SIZE[fmt]]
    s = max(w / W, h / H) * zoom
    sw, sh = w / s, h / s
    x0 = min(max(cx * W - sw / 2, 0), W - sw)
    y0 = min(max(cy * H - sh / 2, 0), H - sh)
    out = im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + sw, y0 + sh))
    if s > 1:
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    out.save(os.path.join(dst, name + ".jpg"), quality=88)
    print("%-18s %s ampliación x%.2f" % (name, fmt, s))
