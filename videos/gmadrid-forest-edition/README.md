# G·Madrid Balonmano — Forest Edition

Vídeo promocional de 15 s para presentar la equipación "Forest Edition" (temporada 26/27).
Concepto: un bosque que nace. Un tallo de luz brota, se ramifica y llena la pantalla de hojas.
Las hojas giran hasta formar una corona con los colores de la estrella del club, y al abrirse
dejan el logo.

Todo está hecho con código (HyperFrames: HTML + Canvas + GSAP) y es vectorial. No hay
imágenes generadas por IA. La música también está sintetizada por código, así que es libre
de derechos.

## Entregables (`renders/`)

| Archivo | Formato |
| --- | --- |
| `gmadrid-forest-edition-1080x1920.mp4` | Vertical (stories / reels), 15 s, 30 fps, H.264 + AAC |
| `gmadrid-forest-edition-1920x1080.mp4` | Horizontal, 15 s, 30 fps, H.264 + AAC |
| `portada-1080x1920.png` | Fotograma de portada vertical (8,6 s) |
| `portada-1920x1080.png` | Fotograma de portada horizontal (8,6 s) |

## Guion

| Tiempo | Escena |
| --- | --- |
| 0–2 s | Fondo casi negro, latido de luz y un tallo lima que crece desde abajo |
| 2–6 s | Brotan hojas con muelle (escala, giro y leve rebote) y se ramifican. Polen flotando. Tres capas de profundidad |
| 6–9 s | Las hojas giran hacia el centro y forman la corona (rojo arriba, naranja, amarillo, verde, azul y morado, como la estrella). FOREST EDITION / TEMPORADA 26/27 |
| 9–12 s | NATURALEZA (lima) · CRECIMIENTO (rosa) · DIVERSIDAD (azul), con un corte en cada segundo |
| 12–15 s | Las hojas se abren, el logo brota desde el centro, G·MADRID / BALONMANO, zoom out y fundido |

## Cómo editar textos, colores y tiempos

Todo está en **`assets/config.js`**: textos, colores de marca, tonos de hoja, los segundos de cada
escena y la semilla del bosque (cámbiala y saldrá otra distribución de ramas y hojas).
Los dos formatos leen ese mismo archivo.

- Tamaños de letra por formato: `assets/forest.css` (bloques `.landscape` y `.portrait`).
- Animación de los textos: `assets/timeline.js`.
- Bosque, corona y logo (canvas): `assets/forest.js`.
- Música: `tools/make_audio.py` (regenerar con `python3 tools/make_audio.py assets/audio/forest-bgm.wav`; requiere numpy y scipy).
- Logo: `assets/star.js` es la estrella vectorizada a partir de `assets/src/gmadrid-star.png`
  (`tools/vectorize_logo.py`; requiere opencv-python-headless). Si el club tiene el logo en SVG
  original, conviene sustituirlo por ese.

## Renderizar

```bash
npx hyperframes@0.9.12 render . -q high -o renders/gmadrid-forest-edition-1920x1080.mp4
```

```bash
npx hyperframes@0.9.12 render . -c compositions/vertical.html -q high -o renders/gmadrid-forest-edition-1080x1920.mp4
```

Vista previa en el navegador: `npx hyperframes@0.9.12 preview`.

## Notas

- El vídeo no muestra marcas de patrocinadores ni de la equipación (la marca técnica es BKA).
- La estrella del logo usa exactamente los colores Pride del brief; los arcos grises van en gris
  neutro `#9AA3A6`.
- El wordmark original del logo es azul marino y no se leería sobre el fondo oscuro, así que en
  el cierre se usa la estrella más «G·MADRID / BALONMANO» en blanco, tal como pide el guion.
