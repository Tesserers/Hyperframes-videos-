# Entregables

| Fichero | Qué es | Cuándo usarlo |
| --- | --- | --- |
| `video.mp4` | Master. 1920×1080 · 30 fps · H.264 High + AAC-LC estéreo 48 kHz · 39,6 s · −16,2 LUFS · 25 MB | Web, YouTube, LinkedIn |
| `video-ligero.mp4` | Mismo corte a CRF 26 y audio 44,1 kHz · 4 MB | Mandar por correo o WhatsApp, y para descartar problemas de reproducción |
| `audio-del-video.mp3` | Solo la banda sonora · 192 kbps | Comprobar el audio aislado del contenedor |

## Si no se oye nada

El audio del master está verificado y es correcto: AAC-LC estéreo, marcada como
pista por defecto, `start_time` 0, los 39,6 s completos, `moov` antes de `mdat`
(faststart), pico 0,687 y RMS 0,13 sin componente continua, con el espectro
repartido 40 % graves / 42 % medios / 18 % agudos. Es música, no silencio.

Así que si no se oye, el problema está aguas abajo. Por orden de probabilidad:

1. **El reproductor arranca en mudo.** Los navegadores lo imponen en autoplay, y
   muchas vistas previas de chat no muestran control de volumen. Descarga el
   fichero y ábrelo en un reproductor de escritorio.
2. **La vista previa del cliente no reproduce audio en absoluto**, solo imagen.
3. **Se está reproduciendo una entrega anterior.** Durante esta sesión se
   enviaron varias versiones, y las primeras iban sin música: solo efectos, que
   son escasos y suenan bajos. Comprueba que es la última.

`audio-del-video.mp3` existe justamente para separar los casos: si el MP3 suena
y el MP4 no, es el contenedor o el reproductor, no la mezcla.
