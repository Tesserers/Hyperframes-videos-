---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Tessera decide contigo: +€500M asesorados, 40 operaciones, shortlist en 72 horas."
destination: web
aspect: 1920x1080
language: es
audience: "Dueños y directivos de pymes y startups españolas en fase de crecimiento"
length: 38s
angle: "Demo de marca sin voz: la identidad real de Tessera en movimiento, con sus cifras verificadas como protagonistas"
style_preset: brand-native
capture: client-supplied
narration: none
---

## Intent

Vídeo de presentación de Tessera Services. Segunda versión, y una reconstrucción, no un
retoque: la primera se hizo a ciegas sobre un preset genérico porque la política de red de
este entorno bloquea `tesseraservices.com`, y el cliente la rechazó con razón —"eso no tiene
nada que ver con el branding ni con los colores reales".

El cliente aportó entonces el `index.html`, `styles.css`, `animations.css`, la tipografía
`Ailerons` y el vídeo `herobg.webm`. Con eso el vídeo se rehízo entero sobre su identidad real
y, además, por fin pudo usar **cifras verificadas**, que es lo que le faltaba a la primera.

Encargo de esta versión, en sus palabras: **más guay, más moderno, más movimiento, menos
aburrido, y sin voz** — la locución sintética sonaba mal. Sin voz, el ritmo lo marca el corte:
7 planos en 38 s, contra 8 planos en 50 s de la primera.

## Assets

- `assets/media/herobg.webm` — vídeo de fondo del cliente. Reescalado de 4K a 1920×1080 y sin
  pista de audio, para que el render no decodifique 4K por fotograma. Abre el vídeo (0–8 s) y
  lo cierra (tramo 3,3–8,0 s), montado por la vía de *hoisting* del ensamblador.
- `assets/fonts/Ailerons.otf` — el logotipo. **Es** el logotipo: la marca que envió el cliente
  como imagen es esta tipografía, así que se reproduce como texto vivo en vez de como imagen —
  escala sin pixelar, toma el color de marca y se puede animar letra a letra.
- `assets/fonts/Raleway-{200,400,600,800}.woff2`, `Manrope-{200,700,800}.woff2` — descargadas
  de Google Fonts, que sí es alcanzable. Son las familias que declara su `styles.css`.
- `brand/` — el `index.html` y los dos CSS del cliente, guardados como fuente de verdad.

## Customizations

- **Sin locución.** Descartada por el cliente. El vídeo lleva 8 efectos de sonido de la
  librería incluida, que marcan los cortes.
- **Paleta y tipografía extraídas del `:root` de su CSS**, sin inventar: `--navy #202031`,
  `--deep #0a1a1c`, `--teal #587579`, `--teal-lt #6e9195`, `--beige #f0e8de`,
  `--yellow #fbe0a0`. Ailerons para el logotipo, Raleway para titulares, Manrope para cifras.
- **Tracking del logotipo a 0,06em**, el del logotipo que envió el cliente, no el `.22em` que
  su CSS usa en la barra de navegación.
- **Texturas suyas reutilizadas**: el plano de grano SVG (misma turbulencia), los
  `radial-gradient` teal de sus tarjetas, la barra de scroll teal, el degradado teal→amarillo
  de sus barras de progreso y el raíl H+0…H+72 de su timeline.

## Notes

- **Todo el texto en pantalla sale de su web**, literal: "Las decisiones que definen tu
  empresa.", "La profundidad de una gran firma. La cercanía de un equipo que se sienta en tu
  mesa.", "No vendemos informes. Nos sentamos en tu mesa.", "We love EBITDA.",
  "Better decisions, together.", los 7 servicios y los 5 hitos del proceso.
- **Cifras, todas verificadas en su web**: +€500M asesorados · +40 operaciones · +15 años ·
  72 h primer shortlist · 7 d informe de mercado · 87 % tasa de cierre. No hay ninguna otra.
- **Sigue sin música.** MusicGen necesita descargar su modelo de HuggingFace y el proxy lo
  bloquea (403); la biblioteca de HeyGen exige sesión iniciada. Para añadirla: `npx hyperframes
  auth login` y relanzar el paso de audio, o dejar un MP3 y lo mezclo bajo los efectos.
- **La web sigue bloqueada** por la política de red del entorno (403 en el CONNECT, igual que
  Google, LinkedIn o Wikipedia — es una lista blanca estricta). Ya no importa para este vídeo,
  porque el material lo aportó el cliente, pero sí impide capturar pantallazos de la web si en
  algún momento se quisieran planos de producto reales.
- **GSAP vendorizado** en `assets/vendor/` porque el CDN también está bloqueado. Si se
  reensambla el index, vuelve a escribir la etiqueta del CDN y hay que reapuntarla.
- `scripts/apply-brand.mjs` sigue sirviendo para cambiar la paleta de golpe, aunque ya no haga
  falta: ahora la paleta es la buena.
