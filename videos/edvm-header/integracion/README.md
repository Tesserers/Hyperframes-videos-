# Cómo montarlo en el hero

## El marcado

```html
<section id="inicio">
  <video poster="/media/edvm-header-poster.jpg"
         autoplay muted loop playsinline preload="metadata" aria-hidden="true">
    <source src="/media/edvm-header.webm" type="video/webm">
    <source src="/media/edvm-header.mp4"  type="video/mp4">
  </video>
  <!-- logo y titular encima, como ya estén -->
</section>
```

```css
#inicio { position: relative; background: #A61C1C; overflow: hidden; }
#inicio video {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover; object-position: 100% 50%;
}
```

- `object-position: 100% 50%` ancla el vídeo a la derecha. Si la pantalla es más estrecha que
  16:9, lo que se recorta es el rojo liso de la izquierda y no las fotos.
- El fondo de la sección va en `#A61C1C`. Mientras carga, o si el vídeo no cabe entero, el
  rojo de la página y el del vídeo son el mismo (medido en navegador: 166,28,28 frente a
  164,25,27).
- `muted` y `playsinline` son obligatorios para que arranque solo, también en iPhone. Los
  ficheros no llevan pista de audio.
- `aria-hidden="true"`: el vídeo es decoración. El mensaje va en el `h1`.

### El texto, en la zona libre

El vídeo deja liso de x=0 a x=760 sobre 1920, el 40 % izquierdo del cuadro. Es el bloque que
el brandkit reserva para el texto. Logo arriba a la izquierda (96/72 px) y titular abajo a la
izquierda, en minúsculas y Manrope Bold: así está montado `hero-preview.html`. El blanco sobre
`#A61C1C` da 7,6:1, que pasa AA de sobra, y en ningún fotograma pasa una foto por detrás.

### En móvil

En vertical, el recorte central metería las fotos detrás del titular, y el brandkit lo prohíbe
(«el patrón nunca pasa por detrás de las letras»). En móvil el vídeo baja a la mitad inferior y
el texto sube:

```css
@media (max-width: 899px) {
  #inicio video { top: auto; bottom: 0; height: 50%; }
  /* y el bloque de texto, arriba */
}
```

Para servir el ligero en móvil sin JavaScript:

```html
<source src="/media/edvm-header.webm"    type="video/webm" media="(min-width: 900px)">
<source src="/media/edvm-header.mp4"     type="video/mp4"  media="(min-width: 900px)">
<source src="/media/edvm-header-720.mp4" type="video/mp4">
```

Y para quien pide menos movimiento:

```css
@media (prefers-reduced-motion: reduce) {
  #inicio video { display: none; }
  #inicio { background: #A61C1C url(/media/edvm-header-poster.jpg) 100% 50% / cover; }
}
```

## Qué fichero usar

| Fichero | Para qué |
|---|---|
| `edvm-header.webm` · 1,1 MB | El principal. VP9. Va **primero** en el `<source>`; Safari cae al MP4. |
| `edvm-header.mp4` · 2,3 MB | El mismo en H.264, 1920×1080, `faststart`. |
| `edvm-header-720.mp4` · 1,1 MB | 1280×720, para móvil. |
| `edvm-header-poster.jpg` | El `poster`, que es el fotograma 0, así que al entrar no hay salto. |
| `edvm-header-carbon.*` | Igual, con marco carbón `#191919`. Para una cabecera oscura; texto en blanco y acento en `#C4433A`. |

## Una nota técnica sobre el color

El render de HyperFrames convierte a YUV con la matriz BT.601 pero marca el fichero como BT.709.
Los navegadores le hacen caso a la marca, así que el rojo salía en (177,39,25) en vez de
(166,28,28), y en móvil se veía un escalón donde el vídeo se junta con el fondo de la página.
Los entregables se recodifican con `scale=in_color_matrix=bt601:out_color_matrix=bt709`. Si se
vuelve a renderizar, hay que repetir ese paso: los comandos están en `renders/README.md`.

## Comprobarlo

`hero-preview.html` es una maqueta del hero, hecha con la retícula del brandkit y con el vídeo
ya montado. `hero-con-video.png` y `hero-movil.png` son capturas de esa maqueta.
