---
workflow: general-video
flow: automation
storyboard: no
message: "Cabecera boutique con fotografía para las vacantes de TESSERA en Teamtailor"
destination: web
aspect: 1920x1080
language: es
length: 16s
angle: "La ventana: una ventana vertical que se abre como un párpado a un lado del título y enseña la fotografía de marca, como una web editorial de lujo"
style_preset: brand-native
narration: none
audio: none
loop: exact
---

## Intent

Eddy: «hazme otro más guay con los assets que tienes de TESSERA, tipo boutique». Usa la
fotografía de marca (ya tratada en blanco y negro con Navy), el eslogan, la paleta y la luz del
header boutique. El centro queda libre para el título de la vacante.

## Sistema

- Cuatro tiempos de 4 s. Una ventana de 400×600 (x = 1380 a la derecha, 140 a la izquierda,
  y = 150) se abre desde una línea horizontal (`clip-path`, 0,9 s) y se cierra igual (0,7 s).
  Alterna de lado en cada tiempo.
- Dentro de la ventana, la foto A entra con zoom lento (1,14 → 1,0) y a los 1,9 s la foto B
  entra con un barrido desde abajo. Recortes en `scripts/prep_fotos.py`, a 480×720.
- Un filete de 1,2 px en Teal claro, a 20 px de la ventana, se traza y se recoge.
- Pie tipo revista: «01 / 04» en Manrope 200 y el área en Raleway mayúsculas.
  01 Capital humano (oficina TESSERA, equipo) · 02 Finanzas (despacho, ciudad) ·
  03 Estrategia (reunión, molinos) · 04 Madrid (oficina, Gran Vía).
- Eslogan «Better decisions, *together.*» a 84 px, siempre en el lado contrario a la ventana.
  Cambia de lado con la ventana cerrada, con un fundido y un desenfoque breves.
- Luz Teal del header boutique cruzando el fondo, una vez por bucle.
- Bucle exacto (empalme 0,04/255).
