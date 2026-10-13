---
workflow: general-video
flow: automation
storyboard: no
message: "Tina café, tu rincón favorito: café, bollitos y mimos, promos para cada momento y horario de invierno."
destination: instagram-reels
aspect: 1080x1920
language: es-ES
audience: "Clientela de barrio, estudiantes y quien busca un café acogedor"
length: 19.6s
angle: "Reel cute y editorial sobre la marca real de Tina Café: todo sube como el vapor de una taza"
style_preset: brand-native
capture: client-supplied
narration: none
audio: none
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
