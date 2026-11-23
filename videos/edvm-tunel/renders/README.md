# Túnel de «m»

El símbolo de edvm en rojo `#A61C1C` sobre el beige de la marca (warm white `#F6F3EE`). Cada
«m» lleva dentro, en el hueco entre sus dos tablas de arriba, otra «m» cinco veces más pequeña,
y esa otra, y así sucesivamente. La cámara avanza sin parar y atraviesa cada «m» por ese hueco.
La siguiente ya está esperando dentro.

- 1920×1080, 30 fps, sin texto y sin audio.
- Una «m» atravesada cada 3,3 s; seis por vuelta.
- Zoom exponencial, para que la velocidad se perciba constante.
- Bucle exacto de 20 s: tras cada pasada el conjunto es el mismo desplazado una posición.
  Medido: el salto del último fotograma al primero (RMSE 0,0743) es igual que entre dos
  fotogramas seguidos.

| Fichero | Para qué |
|---|---|
| `edvm-tunel.mp4` · 0,9 MB | Principal, H.264. |
| `edvm-tunel.webm` · 1,2 MB | VP9. Aquí el MP4 pesa menos: mejor ponerlo primero. |
| `edvm-tunel-720.mp4` · 0,6 MB | Para móvil. |
| `edvm-tunel-poster.jpg` | Fotograma 0. |

```html
<video class="bg" poster="/media/edvm-tunel-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true">
  <source src="/media/edvm-tunel.mp4" type="video/mp4">
  <source src="/media/edvm-tunel.webm" type="video/webm">
</video>
```
