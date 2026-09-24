---
workflow: general-video
flow: automation
storyboard: no
message: "Selección a tarifa plana: un precio cerrado por contratación, sin porcentajes y sin sorpresas."
destination: web
aspect: 1920x1080
language: es
audience: "Startups, pymes y empresas modernas que quieren contratar rápido y bien"
length: 30s
angle: "La línea plana: todo lo que sube sin avisar (porcentajes, letra pequeña, facturas) se aplana en Plana"
style_preset: brand-native
capture: client-supplied
narration: none
---

## Intent

Promo de 30 s para Plana, para web y LinkedIn escritorio. Tono joven, listo, directo, algo
rebelde e irónico: una marca que se ríe un poco de cómo se hacía la selección hasta ahora.
Tipografía grande y bold, cortes secos al ritmo de la música, mucho aire y formas planas.

La idea que ata el vídeo es la **línea plana** de la propia marca (la barra amarilla del
logotipo y el subrayado con un pico de *be smart, be plana*): el tachado del 20 % es esa línea;
en «Facturas que nadie esperaba» la línea se dispara en picos; en el 10 s se aplana y aparece
«Plana.»; en el cierre vuelve como el subrayado del claim, con su pico de firma.

## Versión 2 — «más rompedor, más joven, más cool»

Feedback del cliente sobre la v1. Cambios:

- Tipografía a sangre (hasta 820 px), una palabra por golpe en el gancho, en minúsculas como
  su propio «be smart, be plana» (una sola regla CSS, `.lc`, para volver a mayúscula inicial).
- Ironía visual: el 20 % se tacha a machete y se cae; «letra pequeña» sale diminuta y la
  cámara se mete dentro; «facturas que nadie esperaba» tartamudea con la música.
- Destellos de color de dos fotogramas y sacudida de cámara en cada golpe; cintas de texto
  cruzadas tras «plana.»; pegatina «sin sorpresas.»; HUD editorial en las esquinas.
- Metraje en duotono de marca (navy/azul, navy/blanco, navy/amarillo).
- Música v2 con más pegada: bajo reese, gancho de melodía, frenazos de cinta y tartamudeo.

## Versión 3 — logo, guiño y entradas limpias

- Logo del cliente encima del claim en el cierre; guiña en el 28,75 s con sonido propio.
- «Nada de restos antes del texto»: las palabras ya no suben por una máscara (asomaban trozos
  de letra); aparecen enteras y opacas en su fotograma con un golpe de zoom. Fuera las líneas
  de velocidad y el desenfoque de entrada; la línea de «facturas» aparece plana y entera y los
  picos saltan a corcheas.

## Assets

- `assets/brand/borrador-referencia.mp4` — borrador de 10 s que aportó el cliente. De él salen
  los cuatro planos de gente trabajando (`scripts/prepare-footage.sh`).
- `assets/brand/ref-navy-grid.png`, `ref-tagline.png`, `wash-light.webp` — referencias de marca
  aportadas: fondo navy con retícula de 120 px, subrayado amarillo con pico, degradado claro.

## Customizations

- Paleta del cliente sin tocar: azul `#4FB3E8`, amarillo `#FFD75E`, navy `#10243A`; retícula
  `#1A3B56` medida en su referencia. Blanco sobre navy, navy sobre amarillo (y sobre azul).
- Tipografía: Hanken Grotesk 800 (Google Fonts, empaquetada), la más cercana al wordmark.
- Música sintetizada a medida (`scripts/make-music.py`), 120 BPM, −14 LUFS.
- **Hueco del logo libre** en la escena final: x 660–1260, y 190–470 (600×280 px).

## Notes

- El texto en pantalla es literal del encargo; no se ha añadido ninguna cifra ni afirmación.
- El metraje del borrador es 720p y lleva la marca de agua ✦ de Gemini, así que es generado
  por IA. Se usa recortado, en formas planas y a tamaño contenido para que no canten ni la
  resolución ni el origen. Sustituirlo por fotografía real es cambiar cuatro `src`.
- Se descartó el plano del chico: el cristal de detrás lleva un logotipo de Plana inventado
  por la IA pegado a su cabeza durante todo el plano y no hay recorte limpio.
- Las imágenes del ejecutivo rompiendo cadenas y de la gente lanzando papeles no se usan: son
  justo los clichés que el encargo pide evitar y llevan logos deformados.
- GSAP vendorizado en `assets/vendor/` (el CDN está bloqueado en este entorno).
