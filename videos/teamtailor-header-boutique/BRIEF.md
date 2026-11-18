---
workflow: general-video
flow: automation
storyboard: no
message: "Cabecera boutique para las vacantes de TESSERA en Teamtailor"
destination: web
aspect: 1920x1080
language: es
length: 16s
angle: "Motion graphics sobrio y editorial: filetes, esquinas de marco, áreas y cifras verificadas, con el centro libre para el título"
style_preset: brand-native
narration: none
audio: none
loop: exact
---

## Intent

Segunda cabecera, alternativa a `../teamtailor-header` (el spot enérgico de formas). Eddy la pidió
«más boutique, más business classic, elegante». Es lo contrario del spot: calma, aire y
precisión, con la estética de un informe de banca privada.

## Sistema

- Fondo Navy → Navy profundo. Una banda ancha del degradado Teal cruza el cuadro en diagonal
  una vez por bucle (fuera de cuadro en 0 y en 16).
- Cuatro esquinas de marco y dos filetes de 1,5 px en Teal claro (y = 216 y 864). Los filetes se
  trazan desde el centro hacia fuera y se recogen al final.
- Izquierda: FINANZAS · CAPITAL HUMANO · ESTRATEGIA en Raleway 200, mayúsculas, con el
  espaciado abriéndose de 0,18 a 0,34 em. Un indicador blanco marca el área de cada cifra.
- Derecha, una cada 3 s y contando desde cero, en Manrope 200: +€500M asesorados (Finanzas),
  +40 operaciones (Estrategia), 72 h primer shortlist (Capital humano) y +15 años de experiencia
  (las tres). Son las cifras verificadas en la web (ver `../tessera-promo/BRIEF.md`). No hay
  ninguna otra.
- Eslogan: «Better decisions, *together.*» en Raleway 200 a 92 px, protagonista de la franja
  baja (Eddy: «mucho más grande, es nuestro eslogan»). Entra palabra a palabra desde su
  máscara y se queda todo el bucle; «together.» en Teal claro. Al lado, el isotipo T pequeño.
- El centro (x 480–1440) queda vacío para el título de la vacante. Velo Navy suave en el
  centro (variable `velo`).
- Ritmo: entradas de 1–1,6 s con `power2`/`power3`. Nada rebota.
- Bucle exacto: Navy liso en 0 y en 16 (empalme 0,01/255).

Variable `solo_fondo` (por defecto `false`): con `true` el render deja solo el fondo y la luz.
`npx hyperframes render --variables '{"solo_fondo":true}'`.

`index.html` se genera desde `scripts/index.template.html` (ver `scripts/README.md`).
