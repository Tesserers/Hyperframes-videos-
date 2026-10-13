---
workflow: general-video
flow: automation
storyboard: no
message: "Empieza el día en Tina café: desayunos para todos los gustos (café de todos los tipos, matcha de varios sabores, tostadas, bollería, bocadillos y pinchos), promos y horario de invierno."
destination: instagram-reels
aspect: 1080x1920
language: es-ES
audience: "Clientela de barrio, estudiantes y quien busca un café acogedor"
length: 30s
angle: "Reel cute y editorial dibujado a lápiz: el lápiz pinta, escribe y borra cada escena"
style_preset: brand-native
capture: client-supplied
narration: none
audio: original-synth
loop: exact
---

## Intent

Encargo completo en `brand/PROMPT.md` (el prompt que acompañaba al zip). Se ha seguido su guion
de seis escenas casi al pie de la letra; los tiempos se han estirado un poco (19,6 s en vez de
18 s, dentro del margen de 15–20 s) para que cada texto quede en pantalla al menos 1,5 s.

El prompt recomendaba Remotion y aceptaba HTML/CSS/GSAP como alternativa. Se ha hecho en
HyperFrames (HTML + GSAP con render a MP4), que es la herramienta de este repositorio. El
equivalente del `brand.ts` pedido es `brand.css`, y cada escena es su propio componente en
`compositions/` (`intro`, `hook`, `character`, `promos`, `hours`, `outro`, más `base`, el
suelo común de chocolate y vapor).

## Assets

- `assets/tina-logo-circle.png` — el logo principal, usado tal cual a 1:1, nunca redibujado.
  El aro dorado que se dibuja en la apertura es un trazo SVG colocado exactamente encima del
  aro del PNG (r = 0,492 del lado) y se retira en cuanto entra el logo real.
- `assets/tina-logo.png`, `assets/tina-logo.svg` — guardados, no usados.
- `assets/ilustraciones/01-bizcocho.png` — **no es una ilustración de Tina**: es una captura
  de un cartel con el logo. No se ha usado. Como no hay ninguna ilustración real del personaje,
  la escena 3 lleva el hueco marcado `[ILUSTRACIÓN TINA]` que pedía el propio prompt.
- Fuentes de Google Fonts, descargadas a `assets/fonts/`: Fraunces (variable, redonda e
  itálica), Inter (400–500), JetBrains Mono (500).
- GSAP 3.14.2 vendorizado en `assets/vendor/` (el CDN está bloqueado en este entorno).

## Customizations

- **Paleta cerrada de diez colores**, en `brand.css`. Ningún color fuera de ella; sin
  degradados.
- **Marco fino** en todas las escenas (2 px en vez de 1,5 px: a 1,5 px desaparece con la
  compresión de Instagram), crema sobre chocolate y chocolate sobre hueso.
- **Granitos felices** y la taza dibujados en SVG con la paleta. Son decoración de marca
  descrita en el prompt, no logotipos.
- **Transiciones**: barrido circular desde el centro (gancho → personaje), ola de chocolate
  desde abajo (promos → horario), y cortes en movimiento hacia arriba en el resto.
- **Bucle**: el primer y el último fotograma son el mismo plano (chocolate, marco, vapor). El
  vapor hace cinco ciclos exactos en 19,6 s, así que el patrón también empalma.

## Notes

- **Copy añadido por mí**, en el tono pedido y sin datos nuevos: «CAFETERÍA» (etiqueta del
  gancho) y «para cada momento —» (cabecera de las promos). Todo lo demás sale del prompt.
- **No incluido**: la tarjeta de fidelidad (10 consumiciones + 1 gratis), porque no estaba en
  el guion. Cabe como cuarta tarjeta en promos si se quiere.
- **Sin audio**: el MP4 sale sin pista. La música se añade mejor en Instagram al subirlo.
- **Para meter la ilustración real de Tina**: en `compositions/character.html`, sustituir el
  `div#ch-tina` por `<img class="ch-tina" src="assets/ilustraciones/tina-taza.png">` (PNG con
  transparencia, 300×390, con la parte de abajo pensada para quedar oculta tras la taza) y
  volver a renderizar.

## Segunda versión (petición de Eddy)

> ponme una canción cute sin copy - habla sobre los desayunos variados - matcha etc pon más
> movimiento es aburrido y que el cambio de animaciones sea como dibujando y borrando a lápiz

- **Canción original** sintetizada en `scripts/make-song.py` (ukelele Karplus-Strong,
  glockenspiel, bajo, bombo, chasquido, shaker): 120 BPM, 13 compases = 26,0 s, lo mismo que
  el vídeo. Sin muestras ni melodías ajenas, así que no hay derechos de terceros. Lleva además
  el rasgueo del lápiz y de la goma en cada trazo del vídeo y un «pop» en cada aparición.
  Normalizada a −16 LUFS (`assets/audio/tina-song.mp3`).
- **El lápiz** (`assets/tina-pencil.js`): un lápiz amarillo de la paleta que colorea el cuadro
  entero a zigzag al cambiar de fondo, borra con la goma cuando el fondo no cambia, escribe las
  frases en itálica y repasa contornos (el aro del logo, los desayunos, los marcos de las
  tarjetas, los subrayados).
- **Escena nueva de desayunos** (`compositions/breakfast.html`), sustituye a la de la taza con
  el hueco de Tina: café, matcha, tostadas y bollería, cada uno dibujado, con su gracia (vapor,
  batidor, tostadas que saltan, mordisco) y borrado; cierra con «¿cuál es el tuyo?».
- **Más movimiento**: letras que saltan, granitos que botan a ritmo, chispitas, latidos y saltos
  sincronizados con los tiempos fuertes de la canción.
- **Excepción a la paleta**: un verde matcha `#9CB071` en `brand.css`, solo para el matcha.
- **Copy y carta, a confirmar**: los cuatro desayunos y sus coletillas («recién hecho», «verde
  y suave», «bien crujientes», «para mojar») son míos; el matcha lo pidió Eddy, el resto es
  genérico. Ajustar a la carta real.
- La escena del hueco `[ILUSTRACIÓN TINA]` ya no está; Tina puede volver cuando haya ilustración.

## Tercera versión (petición de Eddy)

> quita el guion del final a la derecha y centra te esperamos - añade en la comida bocadillos y
> pinchos y añade en lo de matcha que tienes de diferentes sabores y cafés de diferentes tipos
> no solo café y que no se vea el lapiz que sea como escrito pero sin que se vea el lapiz

- «te esperamos», sin guion, centrado.
- Dos desayunos más: **bocadillos** («para coger fuerzas») y **pinchos** («para picar algo»).
  El resumen pasa a una rejilla de 3×2.
- Café: «de todos los tipos», y van pasando SOLO · CON LECHE · CORTADO · CAPUCHINO (tipos
  genéricos, a confirmar con la carta). Matcha: «de varios sabores» (sin nombrarlos, porque no
  los sabemos).
- **El lápiz ya no se ve**: los trazos, el coloreado, la goma y la escritura siguen igual, pero
  sin el lápiz. Está en `SHOW_PENCIL` de `assets/tina-pencil.js` por si vuelve.
- El vídeo y la canción pasan a 30,0 s (15 compases a 120 BPM).
