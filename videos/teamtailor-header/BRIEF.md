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

## Sistema (v2)

La v1 era un mosaico que se deslizaba despacio y cambiaba alguna tesela cada 2 s. Eddy la vio
aburrida y tenía razón: era una lámina con movimiento, no una cabecera.

La v2 hace de la idea el movimiento: **las teselas se juntan**. Seis columnas de 320 px. En
ocho tiempos se alternan una foto a pantalla completa (2,5 s) y un mosaico (1,5 s). Para pasar
de uno a otro, las columnas pares suben y las impares bajan con `power4.inOut` en 0,75 s, y
las juntas Navy profundo de 8 px se cierran cuando la foto encaja y se abren justo antes de
que se rompa. Al juntarse, la foto se cierra de fuera hacia dentro, en el centro, donde va el
título. Al romperse, el mosaico barre de izquierda a derecha.

- Fotos enteras: oficina TESSERA (abre el vídeo), ciudad, reunión, equipo. La del despacho
  quedó solo en el mosaico: su pared blanca caía justo detrás del título.
- La cámara empuja hasta 1,07 sobre la foto entera y se retira en el mosaico.
- Solo hay colores del brandbook 2027 y su único degradado. Las formas de la lámina 18 van
  pequeñas, dentro de las teselas de color.
- El velo es una elipse Navy a transparente (0,76 en el centro y 0,20 en los bordes), con la
  variable `velo`.
- El bucle es exacto: el último fotograma contra el primero da 1,0/255, lo mismo que dos
  fotogramas seguidos.

## Cambiar las fotos

1. Mete las fotos en `brand/` y dales un id, archivo y encuadre en `FOCUS` (`scripts/prep_photos.py`).
2. `python3 -I scripts/prep_photos.py brand assets/photos`
3. Cambia los ids en `STATES` en `index.html` (`hero` para foto entera; `F`, `h`, `B`, `S`
   para las columnas del mosaico).
4. `npx hyperframes render -o renders/master.mp4` y vuelve a codificar (ver `integracion/README.md`).
