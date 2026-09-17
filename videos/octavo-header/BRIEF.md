---
workflow: general-video
flow: automation
storyboard: no
message: "Una casa buena en un sitio bueno, vista en octavos: el plano de fondo del hero de octavo.es."
destination: web
aspect: 1920x1080
language: es
audience: "Quien se plantea una segunda casa y no quiere pagar doce meses para usar seis semanas"
length: 16s
angle: "Plano de fondo en bucle exacto para la cabecera: fotografía de la marca movida por la geometría de la marca, sin una sola palabra"
style_preset: brand-native
capture: client-supplied
narration: none
audio: none
loop: exact
---

## Intent

El encargo es un **vídeo de cabecera**, no un promo: va detrás del hero de `octavo.es`, en
`#inicio`, donde la propia página ya dibuja su antetítulo, su `h1`, su párrafo, sus dos botones y
la barra de cuatro cifras. Eso decide casi todo el diseño.

Tres consecuencias directas, y ninguna es una preferencia mía:

1. **Sin una palabra en pantalla.** El hero ya tiene su texto en HTML. Si el vídeo llevase
   titulares, chocarían con los suyos en cuanto cambiase el ancho del navegador. El vídeo es el
   plano de fondo; el mensaje lo pone la página encima.
2. **Sin pista de audio, literalmente.** No es que vaya en silencio: el MP4 sale sin stream de
   audio. Un vídeo de cabecera tiene que autorreproducirse, y para eso los navegadores exigen
   `muted`; sin pista no hay nada que silenciar ni que descargar.
3. **Bucle exacto.** El último fotograma empalma con el primero sin salto. Esto no sale solo:
   está construido en el montaje (ver `STORYBOARD.md`, *El cierre del bucle*).

## Assets

Todo sale del material aportado. No hay nada de stock ni nada inventado.

- **Fotografía** — las cuatro imágenes del propio `index_octavo.html`, extraídas del bundle
  autoextraíble que trae la página (18 recursos comprimidos en un mapa JSON). Llegan a
  **1672×941**, por debajo de 1080p, así que se han reescalado una sola vez a 2304×1296 con
  Lanczos y un enfoque suave, para que el navegador no las estire en cada fotograma. Es una
  limitación real del material: si existen los originales a resolución completa, el plano gana.
- **Tipografías** — `Archivo` e `Instrument Serif` en woff2, del mismo bundle. Quedan en el
  proyecto aunque esta pieza no lleve texto, para la variante rotulada.
- **Logotipo** — `brand/octavo-logo.svg`, el del bundle, con los metadatos C2PA quitados. Usa
  `currentColor`, así que se puede recolorear sin tocar el trazado.
- **Brandkit** — `brand/Brandkit_Octavo.pptx`, 17 diapositivas, es la autoridad de marca.
- **Hero del sitio** — `brand/site-hero.html`, el marcado real del hero, para calcar la zona
  segura del texto y el velo.

## Customizations

- **Paleta del brandkit, sin inventar**: `yeso #EEF0F1`, `ceniza #DCE0E2`, `basalto #15181C`,
  `grafito #2A2E33`, `almagre #A8341F`, `barro #E0764F`, `piedra #5F6469`. El suelo del lienzo es
  `#F2F4F4`, que es el que la propia página usa en `#inicio`.
- **El octógono como única figura.** El brandkit es explícito: «El octógono recorta, no dibuja
  contornos», y el marco octogonal es el recurso sancionado para la fotografía. Así que la
  costura entre planos **es** un octógono que se abre. No hay fundidos, ni barridos, ni ninguna
  figura que el brandkit no autorice.
- **Un velo de legibilidad por plano**, dentro de cada octógono, con la forma del bloque de
  texto del hero. No estaba previsto: se añadió tras medir que los planos 3 y 4 hundían el
  contraste del titular y del párrafo muy por debajo de lo que su web tiene hoy. Detalle y
  cifras en `STORYBOARD.md`, *El velo de legibilidad*, y en `integracion/README.md`.
- **Sin grano, sin viñeta, sin degradado de marca.** «El color es plano» y «prohibidos los
  degradados de marca». Un grano de película sería invención mía sobre una marca que se describe
  como «sobria como una notaría».
- **Sin el anillo de ocho en pantalla.** Es uno de los tres recursos sancionados, pero competiría
  con la barra de cifras que el hero ya dibuja justo encima. La rotación del octavo se cuenta con
  el movimiento de la apertura, no con un diagrama.

## Notes

- **El velo va aparte y a propósito.** El hero ya lleva su propio degradado de yeso
  (`linearGradient` de `#F2F4F4` al 0.99 por la izquierda hasta 0 a la derecha) como capa `<img>`
  encima de la foto. Si el vídeo lo llevase incrustado se duplicaría y el tercio izquierdo se
  quedaría en gris plano. Por eso el fichero principal va **limpio**, para sustituir solo la
  etiqueta `<img>` de la foto y dejar el velo donde está. Se entrega además una variante con el
  velo incrustado para usarla donde ese degradado no exista.
- **Zona segura.** El texto del hero ocupa un bloque de 660 px dentro de un contenedor de
  1240 px centrado en 1920, es decir de x=340 a x=1000: algo más de la mitad izquierda del
  cuadro, no un tercio. El anillo de aperturas se centró por eso en x=1340, de modo que las
  cuatro nacen entre x=1170 y x=1510, fuera del texto. Los encuadres mantienen esa mitad
  izquierda clara para que el basalto del titular siga leyéndose.
- **Cifras**: esta pieza no lleva ninguna, porque no lleva texto. Las de la web están
  verificadas y disponibles para la variante rotulada: 1/8 en propiedad · 6,5 semanas al año ·
  8 titulares por casa · 0 gestiones · 168.000 € la octava parte · 3.400 € de gastos al año.
- **Su hero ya no cumple WCAG AA** con su propia foto: la itálica en almagre da 2,78:1 (exige
  3:1) y el párrafo 4,00:1 (exige 4,5:1). Es anterior a este vídeo y no lo arregla el vídeo.
  Se entrega la variante `aa`, que sí lo cumple velando algo más la fotografía, y se apuntan
  dos arreglos de CSS que lo resolverían sin tocar la imagen.
- **GSAP vendorizado** en `assets/vendor/` porque el CDN está bloqueado por la política de red
  del entorno. Si se reensambla, hay que reapuntar la etiqueta.
