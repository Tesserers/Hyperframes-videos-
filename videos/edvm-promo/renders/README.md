# Entregables

| Fichero | Qué es |
|---|---|
| `edvm-promo.mp4` · 3,8 MB | 1920×1080 · 30 fps · H.264 + AAC 192 kbps · 30,0 s · −17,2 LUFS |
| `edvm-promo-ligero.mp4` · 1,8 MB | Mismo corte más comprimido, para WhatsApp o correo |

`master.mp4` (salida directa del render) no se sube. Los entregables salen de él con la
corrección de matriz de color:

```bash
VF="scale=in_color_matrix=bt601:out_color_matrix=bt709:out_range=tv" TAGS="-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv" && ffmpeg -y -i master.mp4 -vf "$VF" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -profile:v high $TAGS -c:a aac -b:a 192k -movflags +faststart edvm-promo.mp4
```
