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
| `portada-1080x1920.png` | Fotograma de portada vertical (7,3 s, camiseta) |
| `portada-1920x1080.png` | Fotograma de portada horizontal (7,3 s, camiseta) |

## Guion

| Tiempo | Escena |
| --- | --- |
| 0–2 s | Fondo casi negro, latido de luz y un tallo lima que crece desde abajo |
| 2–4,5 s | Brotan hojas con muelle y se ramifican hasta llenar la pantalla. Polen, tres capas de profundidad |
| 4,5–6,3 s | Las hojas forman la corona con los colores de la estrella (rojo arriba). FOREST EDITION / TEMPORADA 26/27 |
| 6,3–8,5 s | La corona se abre en un marco y la camiseta oficial nace de la luz: frontal y giro a la espalda |
| 8,6–11,6 s | NATURALEZA + tejido de hojas · CRECIMIENTO + escudo y BKA · DIVERSIDAD + manga Pride |
| 11,6–12,8 s | Oficial y portería juntas |
| 12,8–15 s | Las hojas se abren y el logo original nace de un halo de luz. Zoom out y fundido |

## Cómo editar textos, colores y tiempos

Todo está en **`assets/config.js`**: textos, colores de marca, tonos de hoja, los segundos de cada
escena y la semilla del bosque (cámbiala y saldrá otra distribución de ramas y hojas).
Los dos formatos leen ese mismo archivo.

- Tamaños de letra por formato: `assets/forest.css` (bloques `.landscape` y `.portrait`).
- Animación de los textos: `assets/timeline.js`.
- Bosque, corona y logo (canvas): `assets/forest.js`.
- Música: `tools/make_audio.py` (regenerar con `python3 tools/make_audio.py assets/audio/forest-bgm.wav`; requiere numpy y scipy).
- Camisetas y detalles: `assets/product/`, recortados de las fichas oficiales
  (`assets/src/ficha-*.webp`) con `tools/extract_product.py`. Para cambiarlos, sustituye los
  archivos manteniendo el nombre.
- Logo: `assets/logo/`, el logo original con el fondo blanco quitado (`tools/clean_logo.py`).
  Se muestra sobre un halo claro porque las letras son azul marino.
  (`assets/star.js` es una versión vectorial de la estrella que ya no se usa; se activa con `vectorLogo: true` en config.)

## Renderizar

```bash
npx hyperframes@0.9.12 render . -q high -o renders/gmadrid-forest-edition-1920x1080.mp4
```

```bash
npx hyperframes@0.9.12 render . -c compositions/vertical.html -q high -o renders/gmadrid-forest-edition-1080x1920.mp4
```

Vista previa en el navegador: `npx hyperframes@0.9.12 preview`.

## Notas

- La marca técnica es BKA (la del rinoceronte); aparece porque va en las propias camisetas.
- Las camisetas salen de fichas de 1536×1024 px y están reescaladas x2. Si hay renders a más
  resolución (o el logo en PNG/SVG grande), sustituirlos mejora la nitidez.
