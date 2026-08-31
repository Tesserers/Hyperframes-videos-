---
format: 1920x1080
duration: 38s
message: "Tessera decide contigo: +€500M asesorados, 40 operaciones, shortlist en 72 horas."
arc: Marca → cifras → finanzas → posición → talento → guiño → cierre
audience: "Dueños y directivos de pymes y startups españolas en fase de crecimiento"
mode: autonomous
music: none
---

Segunda versión, reconstruida sobre la marca real de Tessera (index.html + styles.css +
Ailerons + herobg.webm aportados por el cliente). La primera usaba un preset genérico y
llevaba locución sintética; esta usa la paleta, la tipografía, el vídeo y **las cifras
verificadas de la propia web**, y va sin voz.

## Video direction

**Sistema de color — el de la web, sin inventar nada.** `--deep #0a1a1c` y `--navy #202031`
son los dos suelos oscuros; `--beige #f0e8de` es todo el texto principal; `--teal #587579`
y `--teal-lt #6e9195` son la voz secundaria (reglas, etiquetas, raíles); `--yellow #fbe0a0`
es el acento **escaso**: solo la palabra que remata cada plano. El vídeo corre oscuro de
principio a fin salvo un plano — el 6 — que es amarillo a sangre. Ese contraste es la razón
de que el amarillo signifique algo el resto del tiempo.

**Tipografía — la suya.** `Ailerons` es el logotipo y **solo** el logotipo (planos 1 y 7),
con el tracking del logotipo que ellos han aportado, no el `.22em` de la navegación web.
`Raleway` carga los titulares, y su contraste 200/800 — fino enorme contra negrita — es el
gesto tipográfico de la marca. `Manrope` lleva todas las cifras, igual que en la web.

**Sin voz.** El cliente descartó la locución. Eso quita la muleta y sube el listón: el ritmo
ya no lo marca una frase hablada sino el propio corte. Cada plano se construye sobre una
rejilla de tiempos fija y los reveals caen en ella. La consecuencia buscada: mucho más
movimiento y planos más cortos que en la primera versión (38 s en 7 planos, contra 50 s en 8).

**Movimiento.** Colas largas `power3`/`expo` y nunca rebote. La corriente es **LEFT**:
`push-slide LEFT` es la costura por defecto. Se gastan dos vectores reservados y solo dos:
`zoom-through` al entrar en el plano 4 (la frase que fija la posición, se viene encima del
espectador) y un **corte duro sin transición** al entrar en el 6 (el flash amarillo). Nada de
fundidos: un crossfade no tiene portador.

**Textura.** El plano de grano SVG de la web (misma turbulencia, mismo peso) va sobre los
siete planos y es lo que cose el metraje real con la tipografía. Los `radial-gradient` teal
de sus tarjetas se reutilizan como iluminación de fondo, y son lo único que deriva despacio
durante un plano — nunca el texto.

**Solo cifras verificadas**, todas leídas de su web: +€500M asesorados, +40 operaciones,
+15 años, 72 h, 7 d, 87 % de cierre, 7 servicios, 5 hitos del proceso.

**Lista negativa.** Sin stock. Sin iconos genéricos de consultoría. Sin degradados morados
de "IA". Sin cifras que no estén en su web. Y los dos fallos de movimiento: slideshow
(disparar todo en el primer 25 % y congelar) y salvapantallas (respirar, derivar, paneo lento
en la segunda mitad).

## Frame 1 — Apertura

- type: branding
- blueprint: logo-assemble-lockup (Adapt)
- scene: El logotipo se asienta sobre el vídeo de la web y da paso al titular real del hero
- duration: 8s
- transition_in: cut
- status: animated
- sfx: whoosh-cinematic
- asset_candidates: none — el vídeo va montado por hoisting, no por el catálogo de capture
- focal: el logotipo Ailerons
- roles: herobg.webm = background (velado al 60%) · logotipo = cutout · grano = treatment
- src: compositions/frames/01-apertura.html

Ocho segundos es el plano más largo del vídeo y es deliberado: es el único momento en que la
marca se presenta sola. Ailerons entra apretado y **abre el tracking letra a letra** hasta el
del logotipo. El tracking se anima con `x` por glifo y no con `letter-spacing`, porque
`letter-spacing` reflowea y engancha a píxel entero bajo la captura fotograma a fotograma.

Costura interna a 3,36 s: **zoom-through** (`cut-catalog.md`, desenfoque de pico 10px por ser
escala de texto). El logotipo acelera hacia cámara y el titular continúa esa misma Z desde
detrás — un solo movimiento, dos textos. El titular es literalmente el suyo: "Las decisiones
que **definen tu empresa.**", con el remate en amarillo como en su CSS.

## Frame 2 — Cifras

- type: social_proof
- blueprint: dataviz-countup (Reproduce)
- scene: Los tres números del hero cuentan en cascada y cierran con la promesa de la web
- duration: 7s
- transition_in: push-slide LEFT
- status: animated
- sfx: riser, pop
- asset_candidates: none
- focal: +€500M
- roles: numerales = cutout · glow radial = background
- src: compositions/frames/02-cifras.html

El plano que la primera versión no pudo hacer, porque entonces no había ni un número fiable.
Ahora hay tres, y son suyos: **+€500M asesorados · +40 operaciones · +15 años**. Cada uno entra
en su tiempo y **cuenta**; el contador es el movimiento, no un adorno encima de él. Debajo cae
su propia frase del hero, en dos tiempos: "La profundidad de una gran firma." / "La cercanía de
un equipo que se sienta en tu mesa." Los números se ganan la frase.

## Frame 3 — Finanzas

- type: feature_showcase
- blueprint: fixed-anchor-cycle (Adapt)
- scene: Los siete servicios pasan por una ranura y al aterrizar se despliegan como catálogo
- duration: 6.2s
- transition_in: push-slide LEFT
- status: animated
- sfx: click-soft
- asset_candidates: none
- focal: la ranura de servicios
- roles: ranura = cutout · titular = supporting · glow = background
- src: compositions/frames/03-finanzas.html

Siete servicios en seis segundos sin que parezca una lista. El ancla fija a la izquierda
("De principio **a fin.**", su propio titular de sección); a la derecha una ranura por la que
los siete **ruedan hacia arriba**, cada uno entrando por abajo mientras el anterior sale por
arriba — un único vector ascendente, siete cortes, **acelerando** (0,50 s → 0,36 s entre
cortes). El séptimo se queda, y entonces los siete se rellenan debajo como píldoras: la
amplitud dicha una vez, después de haberla recorrido.

## Frame 4 — No vendemos informes

- type: benefit_highlight
- blueprint: kinetic-type-beats (Reproduce)
- scene: La frase que fija la posición, a sangre y encima del espectador
- duration: 3s
- transition_in: zoom-through
- status: animated
- sfx: impact-bass-1
- asset_candidates: none
- focal: la frase
- roles: tipografía = cutout
- src: compositions/frames/04-informes.html

Tres segundos, una frase, su frase. El plano entra **en pleno vuelo** continuando el
zoom-through que estampa el inyector — misma dirección de escala, nunca desde el reposo. "No
vendemos informes." y, tras la regla teal, el giro: "Nos sentamos en tu mesa." Es el plano más
corto y el más ruidoso; va justo antes de la parte densa para que la densidad se agradezca.

## Frame 5 — Capital humano

- type: feature_showcase
- blueprint: dataviz-countup (Adapt)
- scene: 72h y 7d cuentan, el proceso corre por el raíl y la tasa de cierre se llena
- duration: 6.4s
- transition_in: push-slide LEFT
- status: animated
- sfx: pop
- asset_candidates: none
- focal: el raíl de proceso H+0 → H+72
- roles: raíl = cutout · numerales = cutout · barra de cierre = supporting
- src: compositions/frames/05-talento.html

El plano más denso, y lo aguanta porque todo lo que aparece es un compromiso que ellos
publican. **72 h** y **7 d** cuentan arriba. Después el raíl del proceso corre de izquierda a
derecha y **cada hito aterriza cuando el relleno lo alcanza** — el proceso ejecutado, no
dibujado: H+0 Kickoff · H+12 Estrategia · H+24 Outreach · H+48 Screening · H+72 Shortlist.
Cierra la barra de **87 % de tasa de cierre** con su degradado teal→amarillo, el mismo de sus
barras de progreso.

## Frame 6 — We love EBITDA

- type: branding
- blueprint: titlecard-reveal (Adapt)
- scene: Flash amarillo a sangre con su propia frase
- duration: 2.5s
- transition_in: cut
- status: animated
- sfx: impact-bass-2
- asset_candidates: none
- focal: "We love EBITDA."
- roles: tipografía navy = cutout · amarillo = ground
- src: compositions/frames/06-ebitda.html

El único plano claro del vídeo y el único corte duro sin transición: los dos hechos a la vez
convierten el cambio en un golpe. Es su frase literal, la que ellos mismos publican en voz
alta, y da al vídeo el punto de humor que le faltaba a la primera versión. Dos segundos y
medio: entra, remata, se va. Si durase más dejaría de ser un chiste.

## Frame 7 — Cierre

- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- scene: Vuelve el vídeo, el logotipo se asienta y el dominio se queda
- duration: 4.7s
- transition_in: push-slide LEFT
- status: animated
- sfx: chime
- asset_candidates: none — el vídeo va montado por hoisting, no por el catálogo de capture
- focal: el logotipo
- roles: herobg.webm = background (velado al 72%) · logotipo = cutout
- src: compositions/frames/07-cierre.html

Cierra donde abrió, con el mismo metraje pero otro tramo (`data-media-start: 3.3`), para que
rime sin repetirse. Logotipo, su línea de footer — "Better decisions, together." — y el
dominio en amarillo. Después, quieto: es el último fotograma y tiene que aguantar congelado
como imagen fija. Es el único plano con salida propia del vídeo.
