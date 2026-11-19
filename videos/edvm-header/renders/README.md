# Renders

Los `master*.mp4` (CRF 16, ~16 MB) no se suben: se regeneran con el render. Los entregables
salen de ellos así:

```bash
npx hyperframes render -o renders/master.mp4
```

```bash
npx hyperframes render -o renders/master-carbon.mp4 --variables '{"marco":"carbon"}'
```

```bash
cd renders && VF="scale=in_color_matrix=bt601:out_color_matrix=bt709:out_range=tv" TAGS="-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv" && ffmpeg -y -i master.mp4 -an -vf "$VF" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -profile:v high $TAGS -movflags +faststart edvm-header.mp4 && ffmpeg -y -i master.mp4 -an -vf "$VF" -c:v libvpx-vp9 -b:v 0 -crf 36 -row-mt 1 -pix_fmt yuv420p $TAGS edvm-header.webm && ffmpeg -y -i master.mp4 -an -vf "$VF,scale=1280:720:flags=lanczos" -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p $TAGS -movflags +faststart edvm-header-720.mp4 && ffmpeg -y -i master.mp4 -vf "select=eq(n\,0),scale=in_color_matrix=bt601,format=rgb24" -frames:v 1 -q:v 2 edvm-header-poster.jpg
```

El cambio de matriz no es opcional. El render marca BT.709 pero codifica con BT.601; sin
corregirlo, el rojo de la marca sale desplazado en el navegador (ver `integracion/README.md`).

## Verificado

- 480 fotogramas a 30 fps, 16,0 s, sin pista de audio.
- Bucle: la diferencia entre el fotograma 479 y el 0 (RMSE 0,0104) está dentro de la que hay
  entre dos fotogramas seguidos (0,009–0,011). No hay salto.
- `hyperframes check`: 0 errores y 0 avisos.
