"""Sustituye las camisetas del deck Propuesta_GMADRID_BM_ROOTS_.pptx (diapositivas 6-10)
por el diseño nuevo, sin tocar el maquetado: cada imagen nueva conserva el tamaño de la
original y cada camiseta ocupa el mismo hueco.

  image6.png  (diap. 6 y 7)  oficial frontal + espalda, fondo transparente
  image7.png  (diap. 8)      ficha completa de la oficial (recortada en 3 trozos en la diapositiva)
  image8.png  (diap. 9)      portería frontal + espalda, fondo blanco
  image9.png  (diap. 10)     ficha completa de portería (recortada en 3 trozos)

Uso: python3 tools/update_deck.py <deck.pptx> <ficha_oficial> <ficha_porteria> <salida.pptx>
"""
import sys, os, shutil, zipfile, tempfile
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_product import cutout  # noqa: E402

deck, home_p, gk_p, out = sys.argv[1:5]
home = Image.open(home_p).convert("RGB")
gk = Image.open(gk_p).convert("RGB")

# recortes a resolución nativa (sin reescalar) para el deck
FRONT, BACK = (34, 135, 490, 672), (487, 135, 902, 672)
home_front, home_back = cutout(home, FRONT, up=1), cutout(home, BACK, up=1)
gk_front, gk_back = cutout(gk, FRONT, up=1), cutout(gk, BACK, up=1)

def fit(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

tmp = tempfile.mkdtemp()
with zipfile.ZipFile(deck) as z:
    z.extractall(tmp)
media = os.path.join(tmp, "ppt", "media")

# --- image6: oficial frontal + espalda (1430x928, transparente) ---
old = Image.open(os.path.join(media, "image6.png"))
W, H = old.size
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
b = fit(home_back, 905)                       # espalda: pegada a la derecha, y=22
canvas.alpha_composite(b, (W - b.width, 22))
f = fit(home_front, 924)                      # frontal: pegada a la izquierda, y=0, encima
canvas.alpha_composite(f, (0, 0))
canvas.save(os.path.join(media, "image6.png"), optimize=True)

# --- image8: portería frontal + espalda sobre blanco (1536x1024) ---
old = Image.open(os.path.join(media, "image8.png"))
W, H = old.size
canvas = Image.new("RGBA", (W, H), (253, 253, 253, 255))
for im, (x, y, w, h) in ((gk_front, (39, 58, 736, 903)), (gk_back, (788, 69, 708, 892))):
    r = fit(im, h)
    if r.width > w:
        r = r.resize((w, round(r.height * w / r.width)), Image.LANCZOS)
    canvas.alpha_composite(r, (x + (w - r.width) // 2, y + (h - r.height) // 2))
canvas.convert("RGB").save(os.path.join(media, "image8.png"), optimize=True)

# --- image7 / image9: fichas completas (mismo tamaño y misma maqueta) ---
for name, sheet in (("image7.png", home), ("image9.png", gk)):
    old = Image.open(os.path.join(media, name))
    assert old.size == sheet.size, (name, old.size, sheet.size)
    sheet.save(os.path.join(media, name), optimize=True)

# reempaquetar (mismo orden de entradas que el original)
if os.path.exists(out):
    os.remove(out)
with zipfile.ZipFile(deck) as zin, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        zout.write(os.path.join(tmp, item.filename), item.filename)
shutil.rmtree(tmp)
print("ok", out)
