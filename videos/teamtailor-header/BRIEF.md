---
workflow: general-video
flow: automation
storyboard: no
message: "Cabecera de fondo para las vacantes de TESSERA en Teamtailor"
destination: web
aspect: 1920x1080
language: es
length: 16s
angle: "Mosaico de teselas (Tessera = tesela) que avanza en bucle exacto, con la fotografía tratada de la marca"
style_preset: brand-native
narration: none
audio: none
loop: exact
---

## Intent

Vídeo de fondo para la cabecera de las vacantes en Teamtailor. Teamtailor pinta encima el
título del puesto, la ubicación y el botón, centrados y en blanco. Por eso el vídeo no lleva
texto, ni logotipo, ni audio, y tiene un velo Navy en el centro.

## Fotos

Ocho, todas con el tratamiento de marca: las cuatro de la skill de marca (equipo, oficina,
ciudad, Gran Vía) y las cuatro que aportó Eddy en el chat (molinos, reunión, despacho y la
oficina de TESSERA con el portátil #TESSERERS). Las cuatro de Eddy llegaron como imagen pegada,
no como archivo, y se extrajeron del historial de la sesión a 1125–1448 px de lado. Llegan de
sobra para teselas de 312×1080. La oficina de TESSERA abre el vídeo en la primera tesela.

## Sistema

- Paleta del brandbook 2027 y nada más: Navy, Navy profundo, Teal, Teal claro, Blanco. El único
  degradado es Teal 0 % → Navy 75 %.
- Las teselas tienen 312 px y una junta de 8 px en Navy profundo. La tira avanza a 160 px/s
  constantes y recorre 2560 px en 16 s, así que el bucle cierra solo.
- Relevos: las teselas completas cambian de foto a 2,7 / 6,7 / 10,7 / 14,7 s y las medias
  dos segundos antes. Cada relevo barre la pantalla de izquierda a derecha en 0,36 s.
- Las formas de la lámina 18 (cruz, píldora, onda, arco, barra) son pequeñas y solo se
  mueven cuando cambia su columna.
- Velo: elipse Navy a transparente en el centro (variable `velo`, activa por defecto).

## Cambiar las fotos

1. Mete las fotos en `brand/` y dales un id, archivo y encuadre en `FOCUS` (`scripts/prep_photos.py`).
2. `python3 -I scripts/prep_photos.py brand assets/photos`
3. Pon los ids en `PHOTOS` en `index.html` y reparte los índices en los `seq` de `LAYOUT`
   (cuatro fotos por tesela, una por relevo).
4. `npx hyperframes render -o renders/master.mp4` y vuelve a codificar (ver `integracion/README.md`).
