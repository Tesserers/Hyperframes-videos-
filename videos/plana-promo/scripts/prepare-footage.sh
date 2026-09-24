#!/usr/bin/env bash
# Recorta los cuatro planos limpios del borrador del cliente (720p, 10 s) y los
# ralentiza con interpolación de movimiento para que llenen su hueco en el montaje.
# Cada recorte evita el texto quemado, el logotipo del cristal y la marca de agua ✦.
set -euo pipefail
cd "$(dirname "$0")/.."
V=assets/brand/borrador-referencia.mp4
mk() { # nombre inicio duración recorte factor [filtro extra]
  ffmpeg -v error -y -ss "$2" -t "$3" -i "$V" -an -vf "crop=$4,setpts=$5*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=iw*2:ih*2:flags=lanczos,unsharp=5:5:0.5${6:-},format=yuv420p" -c:v libx264 -crf 15 -preset slow "assets/media/$1.mp4"
}
mk tablet         2.29 1.10 455:620:40:50  1.9
mk manos          2.52 0.88 585:530:545:45 3.0
mk curly-oficina  6.38 0.34 570:720:540:0  7.8
# el amarillo del borrador (#FAD263) se lleva al de marca (#FFD75E)
mk curly-amarillo 6.86 0.46 410:720:690:0  4.6 ",colorchannelmixer=rr=1.022:gg=1.026:bb=0.95"
# tablet: ida, vuelta e ida (5,1 s)
ffmpeg -v error -y -i assets/media/tablet.mp4 -filter_complex "[0]split=3[a][b][c];[b]reverse[br];[c]trim=0:1.1,setpts=PTS-STARTPTS[ct];[a][br][ct]concat=n=3:v=1[v]" -map "[v]" -c:v libx264 -crf 15 -preset slow -pix_fmt yuv420p assets/media/tablet-loop.mp4
rm assets/media/tablet.mp4
