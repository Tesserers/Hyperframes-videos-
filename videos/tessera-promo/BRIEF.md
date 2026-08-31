---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Tessera es la pieza que le falta a tu empresa: finanzas y capital humano, dentro."
destination: web
aspect: 1920x1080
language: es
audience: "Dueños y directivos de pymes y startups españolas en fase de crecimiento"
length: 45s
angle: "La pieza que faltaba — el nombre (tessera = tesela de mosaico) como sistema visual: piezas sueltas que encajan hasta formar la empresa completa"
style_preset: cobalt-grid
capture: none
---

## Intent

Vídeo de presentación de Tessera Services (tesseraservices.com), consultora boutique
de Madrid: finanzas y capital humano para pymes. El usuario lo pidió "guay" — la pieza
tiene que sentirse contemporánea y con carácter, no un corporativo genérico de stock.

Concepto elegido de una ronda de cinco: **"La pieza que faltaba"**. *Tessera* es la tesela,
la pieza de un mosaico. El vídeo entero es ese sistema: la empresa del espectador empieza
como un mosaico incompleto — huecos donde deberían estar la dirección financiera y el
capital humano — y Tessera va colocando las piezas hasta cerrar la figura. La metáfora no
se explica con palabras, se ejecuta con movimiento.

Tono: sobrio pero con nervio. Rigor de finanzas, no frialdad. Tipografía y geometría hacen
el trabajo pesado; nada de fotografía de stock de gente dándose la mano.

## Notes

- **La web está bloqueada por la política de red de este entorno** (`EGRESS_BLOCKED` en
  tesseraservices.com). No hay captura: ni screenshots, ni logo, ni tokens de marca. El
  material de abajo se reconstruyó por búsqueda web y lo confirmó el usuario. El sistema de
  diseño sale de un preset propio, no de la marca capturada.
- Si más adelante se aportan el logo y los colores reales de Tessera, se remezclan en
  `capture/extracted/tokens.json` y se regenera `frame.md` — el resto de la composición
  no cambia.
- Nada de fotografía de stock. Nada de gráficas inventadas con cifras que no existen.
- Los únicos números verificados son "24 profesionales" y las tres áreas. No inventar
  facturación, número de clientes, ni años de trayectoria.

## Decisiones tomadas durante la producción

- **Idioma: español de España.** Confirmado por el usuario a mitad de producción. El texto usa
  léxico peninsular (jornada completa, financiación, gestoría, pymes) y el pretérito perfecto
  compuesto ("ha crecido", no "creció"). La locución se sintetiza con `--lang es`, que en
  espeak-ng es castellano con distinción: se verificó en los fonemas que "crezcas" sale
  `kɾˈeθkas` y "financiera" `finanθjˈeɾa`, no seseo. **No he podido escuchar el resultado**:
  la voz es `ef_dora` (Kokoro, modelo local abierto). La fonemización es castellana con certeza;
  el timbre y la prosodia del modelo no los puedo juzgar sin oírlos.
- **Sin música.** La cama musical se genera con MusicGen en local, pero el modelo
  (`facebook/musicgen-small`) se descarga de HuggingFace y la política de red del entorno
  devuelve 403. La biblioteca musical de HeyGen tampoco está disponible sin sesión iniciada.
  El vídeo va con locución + 9 efectos de sonido de la librería incluida, que sí marcan los
  golpes. Para añadir música: iniciar sesión con `npx hyperframes auth login` y relanzar el
  paso de audio, o aportar una pista propia.
- **Sin subtítulos incrustados.** El vídeo es tipográfico: el texto en pantalla ya reproduce
  casi literalmente lo que dice la voz, así que un raíl de subtítulos duplicaría el mensaje.
  Se ha respetado igualmente la franja inferior del 17% libre, por si se quieren activar.
- **Duraciones de plano = voz + reposo.** La sincronización mecánica deja cada plano exactamente
  igual de largo que su locución, sin aire, lo que elimina los silencios que el montaje necesita
  (la coma dramática, el reposo del clímax). Se ha usado la voz como suelo y se ha añadido un
  reposo deliberado por plano. Además se insertaron 0,40 s y 0,42 s de silencio real dentro de
  los wav 01 y 07, para que la pausa exista en el audio y no solo en la imagen.
- **GSAP vendorizado en `assets/vendor/`.** El CDN (jsdelivr) está bloqueado por el proxy y el
  navegador de render fallaba con `ERR_TUNNEL_CONNECTION_FAILED`. La librería se sirve local.
  Si se reensambla el index con `assemble-index.mjs`, vuelve a escribir la etiqueta del CDN y
  hay que volver a apuntarla a `assets/vendor/gsap.min.js`.
- **Fuentes descargadas a `assets/fonts/`.** El preset `cobalt-grid` no las incluye y el render
  corre en un Chrome limpio sin fuentes de sistema.
