# Túnel de «m»: por el rojo y se abre al beige

El símbolo de edvm en rojo `#A61C1C` sobre el beige de la marca (`#F6F3EE`). En cada pasada de
6 s:

1. Se ve la «m» entera sobre beige.
2. La cámara se mete en el trazo rojo de la tabla del medio hasta que la pantalla es roja.
3. Dentro del rojo se abre una ventana beige con forma de tabla (una cápsula), que crece.
4. Al cruzarla, estamos en la siguiente «m», igual que la primera, y vuelve a empezar.

- 1920×1080, 30 fps, sin texto y sin audio.
- Zoom exponencial, para que la velocidad se perciba constante.
- Bucle exacto de 24 s (cuatro pasadas). Al final de cada pasada el siguiente nivel llena el
  cuadro igual que el anterior al empezar. Medido: el salto del último fotograma al primero
  (RMSE 0,132) es igual que entre dos fotogramas seguidos (0,133).

| Fichero | Para qué |
|---|---|
| `edvm-tunel.mp4` · 0,6 MB | Principal, H.264. |
| `edvm-tunel.webm` · 0,7 MB | VP9. |
| `edvm-tunel-720.mp4` · 0,4 MB | Para móvil. |
| `edvm-tunel-poster.jpg` | Fotograma 0. |

```html
<video class="bg" poster="/media/edvm-tunel-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true">
  <source src="/media/edvm-tunel.mp4" type="video/mp4">
  <source src="/media/edvm-tunel.webm" type="video/webm">
</video>
```
