# Tres Damas Events — Reel de Instagram

MP4 final: `renders/tres-damas-reel.mp4` (1080×1920, 25 s, 30 fps, H.264 + AAC).

## Cambiar el usuario de Instagram

Variable `instagram` (por defecto `@[pendiente]`). Se puede cambiar en Studio o al renderizar:

    npx hyperframes render --variables '{"instagram":"@tresdamasevents"}' -o renders/tres-damas-reel.mp4

## Música

`assets/audio/musica.mp3` es un vals de piano original y sencillo (3/4, 66 bpm, re mayor): 9 compases que resuelven en el plano del logo. Lo he compuesto y sintetizado en local con una soundfont General MIDI libre (TimGM6mb) y una reverb de sala. El script que lo genera está en `assets/audio/fuente/piano.py`. No hay derechos de terceros, pero el sonido es de piano sintetizado, no grabado: sirve para publicar, aunque un tema de librería con piano real o cuerdas sonará más rico.

Para cambiarlo:
- sustituye `assets/audio/musica.mp3` por el tema nuevo, o
- deja el archivo en `assets/audio/` y apunta la variable `musica` a él: `--variables '{"musica":"assets/audio/piano.mp3"}'`.

Envolvente de volumen: 1,2 s de entrada y 2 s de salida (atributo `data-automation` de `<audio id="musica">` en `index.html`).

## Sustituir foto-4

`assets/foto-4.png` es provisional. Basta con reemplazar el archivo por el definitivo.

## Comandos

    npm run dev      # Studio: línea de tiempo editable
    npm run check    # validación
    npm run render   # exportar a MP4
