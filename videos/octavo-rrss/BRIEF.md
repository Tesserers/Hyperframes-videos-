---
workflow: general-video
flow: automation
storyboard: no
message: "Nadie necesita doce meses de casa: tu octava parte, 6,5 semanas al año, frente al mar."
destination: instagram-reels / tiktok / shorts
aspect: 1080x1920
language: es
length: 20s
angle: "Verano y lifestyle con las fotos de la marca, cortado a compás de 120 BPM; cifras de la web, cierre con claim y mioctavo.com"
capture: client-supplied
narration: none
audio: bgm-synth
---

## Intent
Pieza de RRSS para Octavo (mioctavo.com) en clave *cool living / summer*. La web no es accesible desde
este entorno (bloqueo de red), así que el contenido sale del material que ya estaba en el repo para
el header (`videos/octavo-header`): brandkit, fotos, tipografías, logo y el marcado del hero.

## Guion (cortes a compás, 1 compás = 2 s)
| t | Plano | Texto |
|---|---|---|
| 0–2 | Piscina, niños | COPROPIEDAD POR SEMANAS · *Nadie necesita* |
| 2–4 | Amanecer, terraza | *doce meses de casa.* |
| 4–6 | Desayuno frente al mar | Tu octava parte de la casa de tu vida. |
| 6–8 | Llegada | 6,5 semanas al año, con escritura ante notario. |
| 8–10 | Piscina / vistas (cortes a 1 s) | — |
| 10–12 | Mar desde la mesa | FRENTE AL MAR, TODO INCLUIDO · 523 € la semana. |
| 12–14 | Llegada con maletas | Llegas con la maleta. |
| 14–16 | Basalto + anillo de ocho | OCHO CASAS EN OCHO SITIOS · un sitio por corchea |
| 16–20 | Yeso | Foto en marco octogonal, logo, claim, CTA «Ver las casas», mioctavo.com |

## Notas
- Transición propia: la imagen entra en **ocho cuñas**, dos fotogramas cada una (la octava parte, hecha movimiento).
- Música sintetizada en local (`scripts/synth-bed.py`, house suave en Fa mayor, 120 BPM, −16 LUFS):
  los servicios de música están bloqueados en este entorno. Si hay pista licenciada, se sustituye `assets/bgm/bed.wav`.
- Las cifras (523 €, 6,5 semanas, 8 sitios) son las de la web tal y como estaban en el header; conviene confirmarlas con la web actual.
- Las fotos originales llegan a 1672×941; en vertical se reescalan ~2×. Con originales a más resolución el vídeo gana nitidez.
