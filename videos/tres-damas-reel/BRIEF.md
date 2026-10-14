---
workflow: general-video
flow: automation
storyboard: no
message: "Hay momentos que merecen otra foto: fotomatón y experiencias personalizadas, presentadas con elegancia."
destination: instagram-reels
aspect: 1080x1920
language: es-ES
audience: "Parejas, anfitriones de celebraciones privadas y empresas que organizan eventos"
length: 25s
fps: 30
style_preset: brand-native
narration: none
audio: original-jazz-trio
---

## Intent

Reel vertical para Tres Damas Events con estética *old money* europea: elegante, cálida y sobria.
El servicio es divertido; la presentación, refinada. Guion en 7 tiempos, que se sigue al pie de la letra
(ver `STORYBOARD.md`).

## Assets

- `assets/foto-1.png` novia con amigas · `foto-2.png` manos con tiras · `foto-3.png` pareja. Pasadas a B/N neutro.
- `foto-3-hd.png` y `foto-2-vertical.png`: reescalados una sola vez (Lanczos + enfoque suave) para llenar el arco y el plano vertical.
  foto-2 es apaisada (1491×956): a pantalla completa en 9:16 solo cabe una franja de 538 px de ancho ampliada 2×. Se nota algo blanda. Con el original a más resolución el plano gana.
- `foto-4.png` (**PROVISIONAL**): la foto del grupo de invitados no llegó como archivo. Es un fotograma de la tira central de foto-2 con la perspectiva corregida. Basta con sustituir el archivo por el definitivo (cualquier proporción; se recorta a 4:3).
- Logo y monograma en verde `#203C32` y marfil `#F6F1E7`, con fondo transparente y a 2× de resolución, sacados del logo original.
- Cormorant Garamond y Jost (Google Fonts, OFL) en `assets/fonts/`. GSAP en `assets/vendor/`.

## Customizations

- Paleta: marfil `#F6F1E7`, verde botella `#203C32`, burdeos `#652D38` (placa del plano 5 y usuario de Instagram), oro `#A58B60` solo en filetes de 1 px.
- Una única curva de animación, `cubic-bezier(.2,.7,.2,1)`. Fundidos de 600 a 900 ms. Los textos entran con 12–18 px de desplazamiento.
- Sin degradados, brillos ni cristal. La única sombra es la de la tira de papel en el plano 4.
- El borde del botón es de 2 px, no de 1 px: a 1080 px de ancho, en el móvil un borde de 1 px se queda en medio píxel y desaparece.

## Notes

- La copia vive entre y=250 e y=1670 (zona segura de Instagram).
- «Imágenes de referencia» aparece en los planos con foto (2, 4 y 5).
- Música: trío de jazz original en swing a 126 bpm, sintetizado en local (`assets/audio/fuente/jazz.py`). Sin librería externa: el entorno bloquea las descargas y el catálogo de HeyGen requiere iniciar sesión.
- No hay precios, testimonios, clientes ni datos de contacto.
