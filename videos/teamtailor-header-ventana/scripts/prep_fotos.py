"""Recortes verticales para la ventana (400x600 en pantalla, exportados a 480x720 para el zoom).
Uso: python3 -I scripts/prep_fotos.py <carpeta_fotos_marca> <destino>"""
import sys, os
from PIL import Image, ImageFilter
W, H = 480, 720
# id: (archivo, cx, cy, zoom)
F = {
    "tesserers": ("Oficina_Tesserers.jpg",           0.40, 0.45, 1.0),
    "equipo":    ("Equipo_Marketing_Tessera.jpg",    0.62, 0.30, 1.35),
    "despacho":  ("Despacho_Tessera.jpg",            0.64, 0.42, 1.25),
    "ciudad":    ("Ciudad_Luces_Tessera.jpg",        0.40, 0.60, 1.0),
    "reunion":   ("Reunion_Equipo_Tessera.jpg",      0.50, 0.58, 1.3),
    "molinos":   ("Molinos_Tessera.jpg",             0.68, 0.50, 1.0),
    "oficina":   ("Oficina_Minimalista_Tessera.jpg", 0.72, 0.62, 1.45),
    "granvia":   ("Madrid_GranVia_Tessera.jpg",      0.40, 0.72, 1.0),
}
src, dst = sys.argv[1], sys.argv[2]
for k, (fn, cx, cy, z) in F.items():
    im = Image.open(os.path.join(src, fn)).convert("RGB"); w, h = im.size
    s = max(W / w, H / h) * z; sw, sh = W / s, H / s
    x0 = min(max(cx * w - sw / 2, 0), w - sw); y0 = min(max(cy * h - sh / 2, 0), h - sh)
    out = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + sw, y0 + sh))
    if s > 1: out = out.filter(ImageFilter.UnsharpMask(radius=1.0, percent=50, threshold=2))
    out.save(os.path.join(dst, k + ".jpg"), quality=88); print(k, "x%.2f" % s)
