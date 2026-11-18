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
- v2, «dale algo más de movimiento»: siete manchas (un segundo brillo cruza el cuadro en
  diagonal). Las órbitas tienen el doble de amplitud, cada mancha da 1, 2 o 3 vueltas enteras por
  bucle y su tamaño respira un ±18 %. La posición sale del reloj del timeline, así que el bucle
  cierra solo.
- Para que no parezcan «orbes» (los del branding antiguo), las manchas son 1,5 veces más grandes
  y su degradado cae en cuatro tramos (100 / 72 / 32 / 8 / 0 %). Los brillos bajaron de
  intensidad para que el centro no se aclare: en el peor fotograma el texto blanco del centro da
  4,3:1 de contraste.
- Grano fijo (`assets/grano.png`, ruido gaussiano con semilla 7) al 9 % en modo overlay, como
  en la referencia.
- Codificado con `-tune grain` a CRF 24: 3,5 MB (el grano sobre más movimiento pesa más).
