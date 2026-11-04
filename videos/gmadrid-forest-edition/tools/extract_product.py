"""Recorta las camisetas y los detalles de las fichas de producto (1536x1024)
y los prepara para el vídeo: recorte sin fondo (PNG con alfa) para las camisetas,
recortes rectangulares para los detalles, todo reescalado x2 (Lanczos + enfoque suave).

Uso: python3 tools/extract_product.py <ficha_oficial> <ficha_porteria> <carpeta_salida>
"""
import sys, os
import numpy as np, cv2
from PIL import Image, ImageFilter

home_p, gk_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
UP = 2

def upscale(im):
    w, h = im.size
    im = im.resize((w * UP, h * UP), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))

def cutout(sheet, box, name):
    """Quita el fondo gris claro rellenando desde los bordes del recorte."""
    x0, y0, x1, y1 = box
    crop = np.array(sheet.crop(box)).astype(np.uint8)
    h, w = crop.shape[:2]
    bg = np.median(np.concatenate([crop[0], crop[:, 0], crop[:, -1]]), axis=0)
    diff = np.abs(crop.astype(int) - bg.astype(int)).sum(-1)
    # fondo = parecido al gris del papel, o sombra suave (gris neutro claro)
    sat = crop.max(-1).astype(int) - crop.min(-1).astype(int)
    lum = crop.mean(-1)
    cand = ((diff < 46) | ((sat < 14) & (lum > 150))).astype(np.uint8)
    # solo lo conectado con el borde es fondo (protege los números blancos)
    n, lab = cv2.connectedComponents(cand, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bgmask = np.isin(lab, list(border))
    alpha = (~bgmask).astype(np.uint8) * 255
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # quedarse con el componente principal (la camiseta)
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 0).astype(np.uint8))
    if n > 1:
        big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        alpha = np.where(lab == big, 255, 0).astype(np.uint8)
    # rellenar huecos interiores
    inv = (alpha == 0).astype(np.uint8)
    n, lab = cv2.connectedComponents(inv, connectivity=4)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    holes = ~np.isin(lab, list(border)) & (inv > 0)
    alpha[holes] = 255
    im = Image.fromarray(np.dstack([crop, alpha]), "RGBA")
    im = im.resize((w * UP, h * UP), Image.LANCZOS)
    a = np.array(im)
    al = cv2.GaussianBlur(a[..., 3], (0, 0), 1.1)
    al = np.clip((al.astype(float) - 60) * 255 / 150, 0, 255).astype(np.uint8)
    rgb = Image.fromarray(a[..., :3]).filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    res = Image.fromarray(np.dstack([np.array(rgb), al]), "RGBA")
    bb = res.getbbox()
    res = res.crop(bb)
    res.save(os.path.join(out, name + ".png"), optimize=True)
    print(name, res.size)

def tile(sheet, box, name):
    im = upscale(sheet.crop(box))
    im.save(os.path.join(out, name + ".jpg"), quality=95)
    print(name, im.size)

home = Image.open(home_p).convert("RGB")
gk = Image.open(gk_p).convert("RGB")

# camisetas (y hasta antes de la sombra)
cutout(home, (34, 135, 490, 672), "home-front")
cutout(home, (487, 135, 902, 672), "home-back")
cutout(gk, (34, 135, 490, 672), "gk-front")
cutout(gk, (487, 135, 902, 672), "gk-back")

# detalles (columna derecha de la ficha oficial)
tile(home, (1148, 4, 1536, 255), "detail-collar")
tile(home, (1148, 264, 1536, 496), "detail-crest")
tile(home, (1148, 504, 1536, 746), "detail-sleeve")
tile(home, (1148, 754, 1536, 1024), "detail-fabric")
