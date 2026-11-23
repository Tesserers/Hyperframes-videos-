# Fondo desenfocado para la web

Bucle exacto de 20 s, 1920×1080, sin texto ni pista de audio. Son las cuatro fotos del brandkit
(bosque, casa de Falun, conversación y mesa) a sangre, una cada 5 s. Cada una entra con un
fundido de 1,6 s, se acerca muy despacio y se desplaza en su propia dirección. El desenfoque
(28 px) va incrustado en el vídeo, y por eso pesa tan poco.

| Fichero | Para qué |
|---|---|
| `edvm-fondo.webm` · 0,4 MB | El principal (VP9). Va primero en el `<source>`. |
| `edvm-fondo.mp4` · 2,5 MB | El mismo en H.264, para Safari. |
| `edvm-fondo-720.mp4` · 0,9 MB | 1280×720, para móvil. |
| `edvm-fondo-poster.jpg` | Fotograma 0, para el `poster`. |
| `edvm-fondo-nitido.mp4` · 6,7 MB | Sin desenfocar, por si preferís desenfocarlo con CSS (`filter: blur()`). Las fotos están a menos de 1080p, así que nítido se nota algo blando. |

```html
<video class="bg" poster="/media/edvm-fondo-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true">
  <source src="/media/edvm-fondo.webm" type="video/webm">
  <source src="/media/edvm-fondo.mp4" type="video/mp4">
</video>
```

```css
.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; }
```

Si el texto que va encima necesita más contraste, se pone un velo en CSS encima del vídeo
(por ejemplo `background: rgb(25 25 25 / .45)` para texto blanco), sin tocar el vídeo.

Para volver a generarlo: `npx hyperframes render -o renders/master.mp4` (y
`--variables '{"blur":0}'` para el nítido). Después se codifica con la corrección de matriz
BT.601 → BT.709, igual que en `../edvm-header/renders/README.md`.
