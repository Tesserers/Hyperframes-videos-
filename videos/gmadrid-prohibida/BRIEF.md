---
workflow: general-video
flow: automation
storyboard: no
message: "Cómo se ejecuta La Prohibida (o «Escándalo»), paso a paso"
destination: tiktok
aspect: 1080x1920
language: es
audience: "Jugadores de G-Madrid Balonmano"
length: 57.4s
angle: "Tutorial de pizarra táctica: pista en perspectiva, muñecos por posición, flechas de trayectoria y un texto por paso"
narration: none
---

## Intent

Jugada 2 de 3 de la serie de tutoriales de G-Madrid Balonmano. Cada jugada va en
su propio vídeo, con su título, explicada paso a paso y repetida al final en espejo (el otro
lado). El vídeo de referencia que pasó Eddy (pizarra táctica vertical) es solo inspiración: no
se imita su diseño.

## Assets

- assets/gmadrid-logo.png — logo del club (intro y cierre).

## Notes

- Fuente de verdad: `videos/_pizarra-src/` (motor `pizarra.js`, `template.html`, datos de las
  jugadas en `build.py`). No editar `index.html` a mano: regenerar con
  `python3 videos/_pizarra-src/build.py`. La duración va en `.duration`.
- Colores de jugador = colores del logo. Defensa 6:0 en gris, bascula con cada pase.
- Vídeo independiente: sin numeración de serie ni "próxima jugada".
- Música: «Brisk Beat» (aportada por Eddy), recortada a la duración del vídeo con fundido final y normalizada a -16 LUFS.
