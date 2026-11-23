# Fondo animado para la web: la «m» se construye

Bucle exacto de 24 s, 1920×1080, sin texto y sin pista de audio. Calmado.

1. **0–3 s.** El símbolo de edvm se dibuja de un solo trazo, en blanco cálido sobre el rojo, en
   pequeño y a la derecha.
2. **3,6–8 s.** Crece hasta salirse del cuadro por la derecha (12 veces su tamaño) y su trazo se
   abre como una ventana a las fotos de la marca. Es la diapositiva «logo.» del brandkit, en
   movimiento.
3. **8–19 s.** Reposa y se desplaza muy despacio mientras las fotos cambian con fundidos lentos:
   bosque, casa de Falun y la mesa con la casita roja.
4. **19–24 s.** Se recoge al tamaño pequeño, las fotos vuelven al blanco y el trazo se borra en
   el mismo sentido en que se dibujó. El último fotograma es rojo liso, igual que el primero.

La mitad izquierda del cuadro queda siempre en color liso, para el titular. Las fotos llevan un
desenfoque muy suave (2 px) para que el trazo se lea limpio por encima.

| Fichero | Para qué |
|---|---|
| `edvm-fondo.webm` · 0,8 MB | Principal, sobre rojo (VP9). Va primero en el `<source>`. |
| `edvm-fondo.mp4` · 1,4 MB | El mismo en H.264, para Safari. |
| `edvm-fondo-720.mp4` · 0,7 MB | 1280×720, para móvil. |
| `edvm-fondo-carbon.webm` / `.mp4` | Variante sobre carbón `#191919`. |
| `edvm-fondo-poster.jpg` | Fotograma 0 (rojo liso), para el `poster`: así no hay salto al arrancar. |
| `edvm-fondo-still.jpg` | Fotograma de los 11 s, con la «m» grande. Para `prefers-reduced-motion`. |

```html
<video class="bg" poster="/media/edvm-fondo-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true">
  <source src="/media/edvm-fondo.webm" type="video/webm">
  <source src="/media/edvm-fondo.mp4" type="video/mp4">
</video>
```

```css
.bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 100% 50%; z-index: -1; }
section { background: #A61C1C; }
@media (prefers-reduced-motion: reduce) {
  .bg { display: none; }
  section { background: #A61C1C url(/media/edvm-fondo-still.jpg) 100% 50% / cover; }
}
```

Para regenerarlo: `npx hyperframes render -o renders/master.mp4` (y
`--variables '{"base":"carbon"}'` para la variante en carbón). Después se codifica con la
corrección de matriz BT.601 → BT.709, igual que en `../../edvm-header/renders/README.md`.
