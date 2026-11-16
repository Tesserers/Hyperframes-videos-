# Subirlo a Teamtailor

Teamtailor → Career site → Jobs (o el bloque de cabecera de la página de empleo) → Header →
Video, y sube `renders/tessera-header.mp4`.

| Fichero | Para qué |
|---|---|
| `tessera-header.mp4` · 4,3 MB | El principal: 1920×1080, H.264, 16 s en bucle exacto, sin pista de audio, con velo Navy en el centro. |
| `tessera-header-sin-velo.mp4` · 4,7 MB | Sin velo. Úsalo solo si activas el overlay oscuro de Teamtailor, para no oscurecer dos veces. |
| `tessera-header-720.mp4` · 1,8 MB | 1280×720, por si Teamtailor pide un fichero más ligero. |
| `tessera-header-poster.jpg` | Fotograma 0, como imagen de reserva o portada. |

Con el fichero principal, el overlay de Teamtailor va **apagado o al mínimo**, porque el velo ya
viene dentro del vídeo.

Teamtailor recorta el vídeo para que cubra la cabecera, y suele cortar arriba y abajo. Está
pensado para eso: no hay nada importante en los bordes.

`maqueta-teamtailor.html` simula la cabecera de una vacante con el vídeo detrás. Las capturas
`mq-*.png` y `maqueta-4-momentos.jpg` son las cuatro fotos enteras con el título encima.

Codificación usada:

    ffmpeg -i renders/master.mp4 -an -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -profile:v high -movflags +faststart renders/tessera-header.mp4
