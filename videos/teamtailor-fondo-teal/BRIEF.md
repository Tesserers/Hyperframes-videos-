---
workflow: general-video
flow: automation
storyboard: no
message: "Fondo en movimiento para la cabecera de las vacantes de TESSERA en Teamtailor"
destination: web
aspect: 1920x1080
language: es
length: 16s
angle: "Malla difusa Teal en movimiento lento, sin texto ni logo, a partir de una referencia de Eddy"
style_preset: brand-native
narration: none
audio: none
loop: exact
---

## Intent

Eddy pasó una referencia: un fondo de malla difusa con «Better decisions together.» y el logo,
y pidió algo como eso pero con más Teal, sin logos ni textos y en movimiento. Es solo fondo:
encima va el título de la vacante que pone Teamtailor.

## Sistema

- Base: degradado de `#5E7D81` (arriba a la izquierda) a `#283141` (abajo a la derecha).
- Seis manchas con degradado radial: Teal de fondo, un pozo Navy abajo, Teal medio en el centro,
  un brillo Teal claro arriba a la derecha, otro abajo a la izquierda y un matiz que pasea por la
  derecha. Colores muestreados de la referencia y llevados hacia Teal.
- Cada mancha recorre una elipse con un número entero de vueltas en 16 s (1 o 2) y respira de
  tamaño un ±8 %. La posición sale del reloj del timeline, así que el bucle cierra solo.
- Grano fijo (`assets/grano.png`, ruido gaussiano con semilla 7) al 9 % en modo overlay, como
  en la referencia.
- Codificado con `-tune grain` a CRF 24: 2,1 MB. Con CRF 19 pesaba 9,4 MB por el grano.
