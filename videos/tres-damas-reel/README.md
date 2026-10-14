# Tres Damas Events — Reel de Instagram

Dos versiones (1080×1920, 25 s, 30 fps, H.264 + AAC). La imagen es la misma; cambia la música:
- `renders/tres-damas-reel.mp4`: trío de jazz en swing (`assets/audio/musica.mp3`).
- `renders/tres-damas-reel-ibiza.mp4`: house balear (`assets/audio/musica-ibiza.mp3`).

## Cambiar el usuario de Instagram

Variable `instagram` (por defecto `@[pendiente]`). Se puede cambiar en Studio o al renderizar:

    npx hyperframes render --variables '{"instagram":"@tresdamasevents"}' -o renders/tres-damas-reel.mp4

## Música

**Versión Ibiza.** House balear original a 120 bpm en la menor (Am9 – Fmaj9 – Dm9 – Em7), sintetizado desde cero (`assets/audio/fuente/ibiza.py`). Va cuadrado con los cortes: intro con pad y marimba que se abre hasta un barrido en el compás anterior, entrada del bombo a los 7 s (corte a verde), hi-hats abiertos y arpegio una octava arriba a los 15 s, y a los 19 s, con el logo, se va el bombo y quedan pad y marimba. Para exportarla:

    npx hyperframes render --variables '{"musica":"assets/audio/musica-ibiza.mp3"}' -o renders/tres-damas-reel-ibiza.mp4

**Versión jazz.**
`assets/audio/musica.mp3` es un tema de jazz original para trío (piano, contrabajo andante y batería con escobillas), en swing medio a 126 bpm y en fa mayor. Son 12 compases que cierran con un acorde final en el plano del logo. Lo he compuesto y sintetizado en local con una soundfont General MIDI libre (TimGM6mb). El script que lo genera está en `assets/audio/fuente/jazz.py`. No tiene derechos de terceros, pero los instrumentos son sintetizados: un tema de librería grabado con músicos reales sonará más rico.

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
