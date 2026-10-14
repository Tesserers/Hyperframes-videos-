# Tres Damas Events — Reel de Instagram

MP4 final: `renders/tres-damas-reel.mp4` (1080×1920, 25 s, 30 fps, H.264 + AAC).

## Cambiar el usuario de Instagram

Variable `instagram` (por defecto `@[pendiente]`). Se puede cambiar en Studio o al renderizar:

    npx hyperframes render --variables '{"instagram":"@tresdamasevents"}' -o renders/tres-damas-reel.mp4

## Añadir la música

Ahora la pista de música está vacía (`assets/audio/musica.mp3` son 25 s de silencio). Hay dos opciones:
- sustituir ese archivo por el tema, o
- dejar el archivo en `assets/audio/` y apuntar la variable `musica` a él: `--variables '{"musica":"assets/audio/piano.mp3"}'`.

Volumen base 0,8, con 1,2 s de entrada y 2 s de salida (atributo `data-automation` de `<audio id="musica">` en `index.html`).

## Sustituir foto-4

`assets/foto-4.png` es provisional. Basta con reemplazar el archivo por el definitivo.

## Comandos

    npm run dev      # Studio: línea de tiempo editable
    npm run check    # validación
    npm run render   # exportar a MP4
