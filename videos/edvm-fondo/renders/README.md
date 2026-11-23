# Fondo animado para la web

Bucle exacto de 20 s, 1920×1080, sin texto, sin letras y sin pista de audio. Es un vídeo
abstracto: las tablas de la «m», convertidas en cápsulas de luz roja, cruzan de derecha a
izquierda sobre carbón a distintas profundidades. Las de detrás son grandes, muy
desenfocadas y lentas; las de delante, pequeñas, casi nítidas y rápidas. Lleva un grano fino
animado, que le da textura y evita los escalones en los fundidos de color.

Todo movimiento da un número entero de vueltas en 20 s, así que el bucle es exacto por
construcción. Medido: el salto del último fotograma al primero (RMSE 0,0046) es el mismo que
entre dos fotogramas seguidos.

| Fichero | Para qué |
|---|---|
| `edvm-fondo.webm` · 0,25 MB | Principal, sobre carbón (VP9). Va primero en el `<source>`. |
| `edvm-fondo.mp4` · 5,3 MB | El mismo en H.264, para Safari. Pesa más porque conserva el grano. |
| `edvm-fondo-720.mp4` · 1,1 MB | 1280×720, para móvil. |
| `edvm-fondo-rojo.webm` / `.mp4` | Variante sobre rojo `#A61C1C`, con las formas en carbón y granate. |
| `edvm-fondo-poster.jpg` / `-rojo-poster.jpg` | Fotograma 0, para el `poster`. |

```html
<video class="bg" poster="/media/edvm-fondo-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true">
  <source src="/media/edvm-fondo.webm" type="video/webm">
  <source src="/media/edvm-fondo.mp4" type="video/mp4">
</video>
```

```css
.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; }
section { background: #191919; } /* el mismo carbón, para que no haya salto mientras carga */
```

Para regenerarlo: `npx hyperframes render -o renders/master.mp4` (y
`--variables '{"base":"rojo"}'` para la variante roja). Después se codifica con la corrección de
matriz BT.601 → BT.709, igual que en `../../edvm-header/renders/README.md`.
