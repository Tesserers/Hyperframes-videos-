"""Recorta las fotos de marca en teselas exactas para el mosaico.

Uso: python3 -I scripts/prep_photos.py <carpeta_origen> <carpeta_destino>

Cada foto sale en dos formatos, al tamaño exacto en pantalla (sin reescalar en el navegador):
  <id>-full.jpg  320x1080   tesela de altura completa
  <id>-half.jpg  320x536    media tesela (detalle)
  <id>-hero.jpg  1920x1080  solo las de HERO: la foto entera que forman las seis columnas al juntarse
FOCUS dice, en fracciones de la foto, dónde centrar cada recorte y cuánto acercar el detalle.
"""
import sys, os
from PIL import Image, ImageFilter

TW, FH, HH = 320, 1080, 536
FOCUS = {
    # id: (archivo, full_cx, full_cy, full_zoom, half_cx, half_cy, half_zoom)
    "equipo":  ("Equipo_Marketing_Tessera.jpg",   0.42, 0.50, 1.00, 0.70, 0.30, 1.9),
    "oficina": ("Oficina_Minimalista_Tessera.jpg", 0.70, 0.62, 1.00, 0.72, 0.66, 2.2),
    "ciudad":  ("Ciudad_Luces_Tessera.jpg",        0.38, 0.55, 1.00, 0.30, 0.70, 1.7),
    "granvia": ("Madrid_GranVia_Tessera.jpg",      0.38, 0.62, 1.00, 0.40, 0.80, 1.3),
    "molinos": ("Molinos_Tessera.jpg",             0.62, 0.55, 1.00, 0.70, 0.42, 1.6),
    "reunion": ("Reunion_Equipo_Tessera.jpg",      0.50, 0.55, 1.00, 0.50, 0.56, 1.8),
    "despacho":("Despacho_Tessera.jpg",            0.64, 0.50, 1.00, 0.66, 0.36, 1.9),
    "tesserers":("Oficina_Tesserers.jpg",          0.445, 0.50, 1.00, 0.78, 0.62, 1.6),
}
# Las que se ven enteras al juntarse las columnas: (cx, cy) del encuadre 16:9
HERO = {
    "tesserers": (0.50, 0.50),
    "ciudad":    (0.50, 0.62),
    "reunion":   (0.50, 0.56),
    "equipo":    (0.50, 0.30),
}

def crop(im, w, h, cx, cy, zoom):
    W, H = im.size
    s = max(w / W, h / H) * zoom          # escala que cubre la tesela, más el zoom pedido
    sw, sh = w / s, h / s                 # ventana en píxeles de la foto original
    x0 = min(max(cx * W - sw / 2, 0), W - sw)
    y0 = min(max(cy * H - sh / 2, 0), H - sh)
    out = im.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + sw, y0 + sh))
    if s > 1:  # ampliación: enfoque suave para no ir blando
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    return out

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for pid, (fn, fx, fy, fz, hx, hy, hz) in FOCUS.items():
    im = Image.open(os.path.join(src, fn)).convert("RGB")
    crop(im, TW, FH, fx, fy, fz).save(os.path.join(dst, pid + "-full.jpg"), quality=92)
    crop(im, TW, HH, hx, hy, hz).save(os.path.join(dst, pid + "-half.jpg"), quality=92)
    if pid in HERO:
        crop(im, 1920, 1080, *HERO[pid], 1.0).save(os.path.join(dst, pid + "-hero.jpg"), quality=90)
    print(pid, im.size)
