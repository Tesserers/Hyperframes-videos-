---
workflow: product-launch-video
flow: automation
storyboard: no
message: "LT Impulsa: la gestoría 100% online que te quita trabajo, no que te lo da. Tu mejor aliado."
destination: web
aspect: 1920x1080
language: es
audience: "Fundadores y gerentes de pymes y empresas en crecimiento en España"
length: 40s
angle: "Del ruido administrativo a la calma: online sin perder la cercanía"
style_preset: brand-native
capture: client-supplied
narration: none
---

## Intent

Vídeo promo horizontal de LT Impulsa. Encargo de Eddy: que se vea qué empresa somos —una gestoría
cool y de confianza aunque sea 100% online, el mejor aliado de las empresas—, potente y diferencial.

## Assets

- La web (`ltimpulsa.com`) está bloqueada por la política de red del entorno, así que toda la marca
  sale de las tres presentaciones aportadas: propuesta fuerte, plantilla y "Formas para presentaciones".
- `assets/brand/logo-white.png` — logotipo blanco de la propuesta.
- `assets/brand/clientes-white.png` — rejilla de logos de clientes, invertida a blanco con alfa.
- `assets/brand/clientes/*.png` — cada logo de cliente recortado por separado para la cinta en movimiento.
- `assets/fonts/Inter-var-latin.woff2` — Inter variable (la tipografía de las presentaciones).
- `assets/bgm/lt-track.wav` — pista original sintetizada con `scripts/synth-music.py` (120 BPM,
  La menor, Am–F–C–G), compuesta sobre el montaje: intro con un golpe por palabra, break con
  silencio, drop a los 6 s, break a los 30 s y drop final con el logotipo a los 32 s.

## Customizations

- Paleta de las presentaciones: navy `#202031`, fondo `#0F0A1E`, azules `#2563EB` / `#3B82F6` /
  `#60A5FA`, claro `#F4F6FC`, gris `#54657E`.
- Elemento conductor: el paralelogramo azul del logotipo convertido en barrido diagonal (el
  "impulso"); corriente hacia la izquierda. Cortes sobre la rejilla de la música.
- Sin locución (en el vídeo de Tessera la voz sintética no gustó).

## Notes

- Todo el texto sale de las presentaciones. No se usa el precio (250 €) porque era de una propuesta
  concreta. La tarjeta "Este mes, en orden" es una ilustración genérica, no una captura de Holded.
- Testimonio: "Son una extensión de mi empresa… mi departamento financiero." — CEO, Conservas Huerta.

## Versión 2 (feedback de Eddy)

- Fuera las fotos y los nombres de los partners: ahora es "Profesionales de verdad" con +15 años
  y la experiencia en conjunto (Big4, CFOs de startups, fondos de VC, fiscal, laboral, contable,
  mercantil).
- Fuera la música de Tessera ("muy vista"): pista nueva hecha a medida para este corte.
- "Se nota que lo ha hecho Claude": se quitan las etiquetas pequeñas tipo diapositiva y las
  rejillas de columnas, y el vídeo pasa a tipografía cinética a pantalla completa, sincronizada a
  la música. Golpes de palabra con estrobo al arrancar, el paralelogramo del logo que revienta en
  el drop, ruedas de palabras, folios que salen volando, el 1→4→1 de "áreas/equipo", tarjeta en
  3D con notificaciones y un chat del asesor, cinta de logos y grano de película encima.

## Versión 4 (feedback de Eddy)

- Música: "Runway Groove", aportada por Eddy (`assets/bgm/runway-groove.mp3`). Se usa el tramo
  2:03,41–2:43,40 (`runway-groove-cut.wav`), 128,6 BPM. Es el que mejor encaja con el montaje:
  golpes fuertes durante las palabras del arranque, casi silencio para "¿Te suena?", drop en el
  2:11,31 (vídeo 7,90 s) con el estallido azul, break de 2 compases en el 2:22,48 (19,07 s) para
  "Sin oficinas. Sin papeles." y segundo drop en el 2:26,19 (22,78 s) justo en "100% cercanos".
- El montaje se diseñó sobre una rejilla de 0,5 s; la tabla `MAP` del index lo recoloca sobre los
  golpes reales de la canción (posiciones y duraciones). Los cortes caen en compás.
- Letras: se eliminan las máscaras de recorte en las entradas de texto; ahora entran con
  desenfoque y fundido, sin ningún recorte posible durante la animación.
- `scripts/synth-music.py` queda como referencia de la v2; ya no se usa.
