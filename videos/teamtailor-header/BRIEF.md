---
workflow: general-video
flow: automation
storyboard: no
message: "Cabecera de fondo para las vacantes de TESSERA en Teamtailor"
destination: web
aspect: 1920x1080
language: es
length: 15s
angle: "Spot de motion graphics de marca, sin fotos, en bucle exacto"
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

## Sistema (v5, motion graphics)

Tras el spot con fotos (v4, ahora en `archivo/index-spot-fotos.html`), Eddy pidió que fuese
animación pura, «como un spot de TV»: solo motion graphics, sin fotos. Lleva tipografía grande
de marca, las formas de la lámina 18, el degradado y el isotipo T original del brandbook
(`assets/brand/isotipo-t.svg`, extraído del PPTX).

`index.html` se genera desde `scripts/index.template.html` (ver `scripts/README-spot.md`).

| s | Escena |
|---|---|
| 0–2,9 | Rejilla 9×5 de formas (cruz, onda, arco, píldora, barra, triángulo) que estalla desde el centro, da medio giro y sale disparada hacia arriba |
| 2,4–5,7 | Cortinilla con el degradado diagonal y «Personas.» letra a letra; píldora, cruz, arco y triángulo |
| 4,8–8,0 | Seis paneles de color caen alternos; dos se abren; «Decisiones.» en blanco |
| 7,5–10,5 | Círculo Navy profundo; onda gigante que se dibuja de lado a lado; «Juntos.» |
| 10,0–14,0 | Degradado; el isotipo T entra desde 3,2× y desenfocado; «Better decisions, *together.*» |
| 13,1–15 | Seis barras Navy cierran el cuadro: Navy liso, igual que el fotograma 0 |

Las palabras van en Raleway 800 a 210 px, abajo a la izquierda y en Teal claro (salvo
«Decisiones.»), para que el título blanco de la vacante mande. Cada escena empuja la cámara de
1,0 a 1,07. El empalme del bucle mide 0,4/255.

## Sistema (v4, spot de TV)

Tres versiones de mosaico (v1 a v3) se rechazaron por aburridas y por el estilo. Eddy pidió
«casi un anuncio de TV», sin texto propio (Teamtailor pone el título) y en 15 s.

La v4 está planteada como un spot rodado con fotos fijas: plano general, primeros planos en
pantalla partida (2 o 3 paneles verticales con junta de 8 px) y la cámara siempre en
movimiento. Guion (s):

| | Plano | Entrada | Cámara |
|---|---|---|---|
| 0–2,0 | Oficina TESSERA, general | (empalme del bucle) | empuje lineal 1,05 → 1,14 |
| 1,6–2,6 | 3 paneles: equipo, ciudad, oficina | entran por arriba y abajo, escalonados | deriva a contrapelo |
| 2,4–3,4 | Ciudad | zoom que atraviesa (desenfoque 16 px) | 1,25 → 1,04, giro −1,5° → 0 |
| 3,4–4,0 | 2 paneles: despacho, molinos | corte seco | deriva |
| 4,0–5,3 | Reunión | corte | paneo +70 → −70 px |
| 5,0–5,6 | Cortinilla degradado Teal→Navy | izquierda a derecha | |
| 5,3–6,7 | Molinos | bajo la cortinilla | se aleja 1,22 → 1,02 |
| 6,7–7,3 | 3 paneles: Gran Vía, portátil #TESSERERS, reunión | corte | deriva |
| 7,3–8,9 | Equipo | corte | empuje lento a las caras |
| 8,6–10,1 | Oficina | barrido de cámara con desenfoque 30 px | paneo |
| 10,1–12,3 | Ráfaga: 2 paneles, 3 paneles, ciudad, reunión, equipo | cortes de 0,5 y 0,4 s | empujes cortos |
| 12,0–12,6 | Cortinilla degradado | derecha a izquierda | |
| 12,3–14,0 | Oficina TESSERA, primer plano | bajo la cortinilla | empuje lento |
| 14,0–15,0 | Oficina TESSERA, general | corte | sigue en el plano 1 |

El bucle empalma dentro del plano general de la oficina: el último plano y el primero llevan la
misma velocidad de cámara. El último fotograma contra el primero da 1,2/255, lo mismo que dos
fotogramas seguidos.

Encuadres en `scripts/prep_spot.py`, que los saca un 15 % más grandes que el hueco donde van.
Los paneles sacan las fotos verticales a su resolución nativa. Los planos generales que salen
de fotos verticales van ampliados entre 1,2 y 1,7 veces.

## Cambiar las fotos

(Para el spot: edita `SHOTS` en `scripts/prep_spot.py`, ejecútalo sobre `brand` y `assets/spot`,
y cambia los nombres en el guion de `index.html`. Los pasos de abajo eran para el mosaico.)

1. Mete las fotos en `brand/` y dales un id, archivo y encuadre en `FOCUS` (`scripts/prep_photos.py`).
2. `python3 -I scripts/prep_photos.py brand assets/photos`
3. Cambia los ids en `STATES` en `index.html` (`hero` para foto entera; `F`, `h`, `B`, `S`
   para las columnas del mosaico).
4. `npx hyperframes render -o renders/master.mp4` y vuelve a codificar (ver `integracion/README.md`).
