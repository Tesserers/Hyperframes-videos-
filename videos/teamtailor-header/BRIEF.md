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

## Sistema (v3)

La v1 (mosaico deslizándose) y la v2 (columnas que se juntan cada 2 s y se quedan quietas)
se vieron aburridas. La v3 no para nunca: **las columnas corren como un rodillo, frenan,
encajan y vuelven a arrancar**.

- Ocho paradas en 16 s (llegadas a 0 · 2,4 · 4 · 6,4 · 8 · 10,4 · 12 · 14,4 · 16). Las pares son
  foto entera y aguantan 1,2 s; las impares son mosaico y aguantan 0,4 s. Todo lo demás es
  carrera.
- En cada carrera, cada columna cruza de 2 a 4 paneles de relleno (`nFill`), así que cada una
  va a su velocidad. Las pares suben y las impares bajan, con `power3.inOut` y salida
  escalonada. Hacia la foto entera llegan de fuera hacia dentro.
- Cámara: sobre la foto entera empuja hasta 1,09; al arrancar se abre hasta 0,94 y vuelve a 1,0
  al frenar. Hay una columna extra a cada lado y 80 px de tesela arriba y abajo, para que al
  abrirse nunca se vea el borde.
- Las juntas Navy profundo de 8 px se cierran solo con la foto entera.
- Fotos enteras: oficina TESSERA (abre), ciudad, reunión, equipo. Las demás, en el mosaico.
- Velo Navy central (variable `velo`). Bucle exacto: 0,8/255 entre el último fotograma y el
  primero.

## Cambiar las fotos

1. Mete las fotos en `brand/` y dales un id, archivo y encuadre en `FOCUS` (`scripts/prep_photos.py`).
2. `python3 -I scripts/prep_photos.py brand assets/photos`
3. Cambia los ids en `STATES` en `index.html` (`hero` para foto entera; `F`, `h`, `B`, `S`
   para las columnas del mosaico).
4. `npx hyperframes render -o renders/master.mp4` y vuelve a codificar (ver `integracion/README.md`).
