---
format: 1920x1080
fps: 30
duration: 16s
loop: exact
message: "people for what's next."
arc: "Bosque → casa de Falun → conversación → la mesa con la casita roja, y vuelta al bosque"
mode: autonomous
music: none
narration: none
text_on_screen: none
---

Plano de fondo para el hero de edvm. Una sola composición, cuatro fotos de 4 s, bucle exacto de
16 s. No lleva texto: lo pone la página encima.

## La idea

El brandkit tiene un recurso que lo dice casi todo: **«mira a través de la «m»»**. El símbolo de
edvm son tres tablas (una fachada, una «E», una lista), y el marco de foto es esas tres tablas
abiertas sobre una fotografía. El vídeo deja el marco quieto y cambia lo que se ve a través de él.

El recorrido va de fuera hacia dentro: el bosque, la casa, la conversación y la mesa de trabajo
con la casita roja encima, que vuelve a llevar a la casa. Lo nórdico y lo humano, sin forzar
ninguno de los dos.

## Los cuatro planos

| t | Foto | Encuadre |
|---|---|---|
| 0–4 s | `01-bosque.jpg` | abedules a la izquierda, sotobosque con los arándanos rojos en la tabla de abajo |
| 4–8 s | `02-casa.jpg` | la casa de Falun entera dentro de la tabla central |
| 8–12 s | `03-conversacion.jpg` | las dos caras dentro de la tabla central, nunca en el hueco de 40 px |
| 12–16 s | `04-mesa.jpg` | la casita roja en la tabla central, el portátil a la derecha |

## Cómo cambia una foto

- La foto nueva entra **tabla a tabla**: arriba en t, en medio en t+0,2 s y abajo en t+0,4 s.
  Cada tabla tarda 1,4 s (`power2.inOut`), así que el cambio completo dura 1,8 s.
- El corte es una línea vertical dura que barre de derecha a izquierda, hasta el extremo
  redondeado de la tabla.
- La foto que llega viene desplazada 140 px a la derecha y se posa mientras el corte avanza, en
  el mismo sentido que él.
- Todas las fotos se desplazan a 16 px/s constantes hacia la izquierda mientras están en
  pantalla. No hay zoom ni balanceo.

## El cierre del bucle

En t=0 ya está entrando el bosque sobre la mesa. Por eso la pila de capas empieza con una **cola
de la foto 4**: la misma mesa, con su desplazamiento contado desde t=−4 s, que es justo el
estado en que la deja t=16 s. Cada fotograma se calcula como función pura del reloj
(`draw(t)`), sin depender de que un tween se haya disparado. Así se puede saltar a cualquier
fotograma, y el 479 empalma con el 0 sin salto.
