# Patrón fachada en movimiento

El «patrón fachada» del brandkit (diapositivas 34 y 40): la «m» repetida como el revestimiento
de una casa de Falun, con las medidas de la ppt (cada «m» de 432×162 px, cada 480 px en
horizontal y cada 200 px en vertical). El patrón sube a velocidad constante, 50 px/s, una fila
cada 4 s. Entra con un fundido abajo y se desvanece arriba. Sin texto ni audio.

Bucle exacto de 20 s: el patrón se repite cada 200 px y sube cinco filas por vuelta.

| Fichero | Para qué |
|---|---|
| `edvm-patron.mp4` · 2,9 MB | Principal: «m» en blanco cálido sobre rojo. |
| `edvm-patron.webm` · 2,9 MB | El mismo en VP9. |
| `edvm-patron-tono.mp4` / `.webm` | Tono sobre tono, `#8E1616` sobre rojo, como en la ppt. Más sutil, para ir detrás de texto. |
| `*-poster.jpg` | Fotograma 0. |

## Versión que reacciona al scroll

Un vídeo se mueve solo; no puede seguir la rueda del ratón. Si lo que quieres es que las «m»
suban **cuando** haces scroll, `../web/patron-scroll.html` lo hace con CSS y diez líneas de
JavaScript: el patrón es un SVG de 1 KB (`../web/patron-m.svg`), va fijo detrás de la página y
sube a la mitad de la velocidad del scroll, con el mismo degradado arriba y abajo. Pesa mucho
menos que el vídeo, es nítido en cualquier pantalla y respeta `prefers-reduced-motion`.
