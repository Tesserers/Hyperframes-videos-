---
workflow: general-video
flow: automation
storyboard: no
message: "Una pareja en un fotomatón antiguo: cada flash congela una pose, y al final sale la tira."
destination: social
aspect: 1920x1080
language: none
length: 14.5s
angle: "Montaje en blanco y negro sobre metraje real: fogonazos de flash que congelan pose tras pose, cerrando con la tira de cuatro fotos revelándose"
capture: client-supplied
narration: none
audio: source-music + shutter sfx
---

## Intent

Prompt original (Eddy): *Cinematic black and white video of a romantic couple inside a vintage
photobooth with elegant pleated curtain backdrop. Old money aesthetic. Dynamic montage of rapid
camera flashes capturing them seamlessly switching through multiple intimate, playful, and elegant
poses—looking face to face, laughing, and embracing. High contrast, classic film grain, timeless style.*

HyperFrames no genera metraje, así que el vídeo se construye sobre el clip que aportó Eddy
(`tresdamaspareja.mp4`, 10 s, 1280×720, 24 fps). El clip ya trae tres disparos con su clic de
obturador (2,07 · 4,11 · 6,16 s); los flashes del montaje caen exactamente ahí y se añaden tres
más, cada vez más seguidos (7,35 · 8,45 · 9,40), antes del flash final que da paso a la tira.

## Estructura

| Tiempo | Qué pasa |
| --- | --- |
| 0 – 9,95 s | Metraje vivo con un empuje lento de cámara (1,00 → 1,07). En cada flash la imagen se quema, aparece la pose congelada sobreexpuesta y se asienta en 0,3 s; a los 0,5 s vuelve el movimiento. |
| 9,95 s | Último flash: corte a negro de cabina, con el beso desenfocado de fondo. |
| 10 – 14,5 s | La tira de cuatro fotos (sonrisa, carcajada, frente con frente, caricia) sale de la ranura y cada foto se revela de blanco a imagen. Fundido a negro en 13,9 s. |

## Tratamiento

- Etalonado `mono-clean` + contraste alto (contraste 0,45, negros −0,35), viñeta 0,38, grano 0,30, polvo de película 0,35 — todo vía `hyperframes media-treatment`, nada con filtros CSS.
- Flash: bloque de registro `editorial-flash-overlay`, con sus tintes cálido/frío neutralizados a blanco para que no meta color en el B/N.

## Assets

- `assets/footage/photobooth.mp4` — clip aportado por Eddy.
- `assets/stills/hold-*.png` y `strip-*.png` — fotogramas extraídos del mismo clip con ffmpeg.
- `assets/sfx/shutter.wav`, `eject.wav` — sintetizados con ffmpeg (ruido con semilla fija, deterministas).

## Notes

- El audio es la música del propio clip, que se apaga al llegar la tira; los clics extra son los sintetizados.
