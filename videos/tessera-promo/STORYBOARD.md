---
format: 1920x1080
duration: 48s
message: "Tessera es la pieza que le falta a tu empresa: finanzas y capital humano, dentro."
arc: PAS — pain validation → promesa → sin el coste → evidencia (finanzas · capital humano) → un solo proveedor → el remate → CTA
audience: "Dueños y directivos de pymes y startups españolas en fase de crecimiento"
mode: autonomous
music: corporate-confident
---

El motivo conductor de todo el vídeo es la **tesela**: la pieza de mosaico que da nombre a
Tessera. La retícula milimetrada del preset `cobalt-grid` es el sustrato donde las teselas
encajan. El mosaico empieza incompleto — con dos huecos — y se cierra con la marca.

## Video direction

**Sistema de color** (de `frame.md`, nada inventado). `paper` es el suelo de los ocho planos.
`ink` cobalto es la única tinta: carga la tipografía display, las teselas llenas y las dos
reglas horizontales. `ink-soft` es la segunda voz — teselas de segundo plano y etiquetas
secundarias. `ink-faint` es lo apagado: el mosaico cuando pasa a fondo, y lo tachado.
`grid` es la retícula permanente. No hay un tercer color en todo el vídeo, y esa carencia
es la marca: una consultora financiera no necesita cinco acentos.

**El mosaico es un objeto real, no una decoración.** Una malla de 6×4 teselas alineada a la
retícula, siempre en la misma posición (x 577, y 350) y a la misma escala (766×506). Existe en
siete de los ocho planos: como protagonista, como escenario o como marca de agua al 8%. La
excepción es el Frame 3, donde falta a propósito porque ese plano va de las alternativas y no
de Tessera. Sus dos huecos se abren en el Frame 1 y se cierran en el Frame 6: esa deuda abierta
durante cinco planos es lo que sostiene el vídeo.

**Gramática de movimiento.** Colas largas `power3` por defecto, nunca rebote — ni `back.out`,
ni `bounce.out`, ni `elastic.out`. La corriente del film es **LEFT**: la costura por defecto es
`push-slide LEFT`, a velocidad casada y cortada en pleno movimiento por los dos lados. El vídeo
gasta **dos transiciones y solo dos**, que es el presupuesto de la doctrina: `push-slide LEFT`
para la corriente, y `zoom-through` — el único vector reservado, Z hacia delante — en los
Frames 4 y 5, donde significa exactamente una cosa: entrar dentro de un área del mosaico. Se
gasta dos veces porque hay dos áreas, y esa repetición es la rima. Ninguna otra dirección, y
ningún fundido: un crossfade no tiene portador y rompe la ley del vector.

**Modelo de revelado.** Nada aparece antes de que la voz lo nombre. En t=0 de cada plano solo
entra lo que la locución está diciendo en ese instante; cada pieza siguiente entra en su cue
hablado, repartidas por el 50% final del plano. Las teselas y las líneas de texto son los
elementos que se revelan; el mosaico de fondo no se re-anima.

**Ritmo — planos en reposo.** Los Frames 7 y 8 son los planos quietos, y lo son a propósito:
después de dos planos de enumeración (4 y 5) y del cierre del mosaico (6), el remate necesita
silencio visual. El Frame 2 lleva su propia coma dramática de 0,4 s entre el impacto de la
tesela y el nacimiento del wordmark. Durante un reposo solo se admite jitter de amplitud baja.

**Lista negativa.** Nada de fotografía de stock. Nada de cifras que no estén verificadas —
solo "24" y las tres áreas. Nada de iconografía genérica de consultoría (maletines, apretones
de manos, engranajes, flechas ascendentes). Ni degradados azul-morado de "IA", ni bokeh, ni
sombras difusas: el preset es plano y de dos tintas. Ningún gradiente. Y los dos modos de
fallo de movimiento: **slideshow** (dispararlo todo en el primer 25% y congelar) y
**salvapantallas** (respiración, deriva, paneo lento en la segunda mitad) están prohibidos.

**Franja de subtítulos.** Todo el contenido se planifica en el 83% superior del cuadro. La
banda inferior queda libre aunque este vídeo no lleve subtítulos incrustados — el texto en
pantalla ya reproduce la locución casi palabra por palabra.

## Frame 1 — Tu estructura, no

- type: hook
- blueprint: kinetic-type-beats (Adapt)
- scene: El mosaico se levanta tesela a tesela y se detiene con dos huecos abiertos
- duration: 4.38s
- transition_in: cut
- status: animated
- voiceover: "Tu empresa ha crecido. Tu estructura, no."
- asset_candidates: none
- focal: el mosaico 6×4
- roles: mosaico = cutout (protagonista) · retícula = background · reglas = chrome
- sfx: whoosh-short
- handoff_out: mosaico 6×4 — centrado (x 577px, y 330px, 766×506px), escala 1.0, opacidad 1, quieto; los dos huecos (fila 2 col 4 y fila 3 col 2) vacíos con contorno de 2px
- src: compositions/frames/01-estructura.html

Validación del dolor, en el idioma del espectador: el crecimiento ya ocurrió, lo que no
acompañó es la organización. Los dos huecos que quedan son los dos servicios de Tessera; el
espectador todavía no lo sabe, y eso es lo que le mantiene.

Adapt: conservo el movimiento firma de `kinetic-type-beats` — la frase construida en tiempos,
cada uno su propio gesto — pero el segundo tiempo no cae sobre una pantalla vacía: cae sobre
un mosaico que acaba de fallar. El texto y la geometría dicen lo mismo a la vez.

Scene 1 (0.0–1.38s): suelo `paper` con la retícula y las dos reglas cobalto. Las teselas entran
en cascada escalonada desde la izquierda — **cluster→outward expansion** (`center-outward-expansion`)
reordenada como barrido lateral — llenando la malla fila a fila con cola larga `power3`.
Simultáneamente "Tu empresa ha crecido." entra por **revelado escalonado por palabra**
(`dynamic-content-sequencing`) en `display-quote`, banda superior a todo lo ancho. Layout
centrado: la línea arriba, el mosaico debajo ocupando el 40% central del cuadro. Tres capas de
profundidad: retícula · mosaico · texto.

Scene 2 (1.38–1.78s): la cascada llega al final de la malla y **se para en seco** dejando dos
teselas sin colocar. La locución calla — este silencio de 0,4 s está grabado en el propio wav.
Nada se mueve. Es el silencio que hace la pregunta.

Scene 3 (1.78–2.88s): "Tu estructura, no." sustituye a la primera línea por **corte duro**
(`discrete-text-sequence`), sin fundido — el cambio es el golpe, y cae exactamente en la
primera sílaba del segundo tiempo. En el mismo fotograma, el contorno de 1px de los dos huecos
**se autodibuja** (`svg-path-draw`) y quedan como las dos únicas formas vacías del cuadro.

Scene 4 (2.88–4.38s): reposo. Solo jitter de amplitud baja (`sine-wave-loop`) sobre el mosaico.
Sale desplazándose a la izquierda, todavía en movimiento, hacia el Frame 2.

## Frame 2 — La pieza que falta

- type: product_intro
- blueprint: logo-assemble-lockup (Adapt)
- scene: Una tesela cobalto entra desde fuera de cuadro y encaja en el hueco; de ella nace TESSERA
- duration: 6.86s
- transition_in: push-slide LEFT
- status: animated
- voiceover: "Tessera es la pieza que falta. Dirección financiera y capital humano, dentro de tu empresa."
- asset_candidates: none
- focal: la tesela entrante
- roles: tesela entrante = cutout · mosaico = supporting · retícula = background
- sfx: whoosh-cinematic, impact-bass-1
- handoff_in: mosaico 6×4 — misma geometría exacta que el Frame 1 (x 577px, y 330px, 766×506px), escala 1.0, opacidad 1, entrando con la corriente LEFT; los dos huecos siguen abiertos en las mismas celdas
- src: compositions/frames/02-pieza.html

La promesa aterriza en el segundo plano, como manda el value-first: nadie ha visto todavía
un servicio, pero ya sabe qué hace Tessera por él. "Dentro de tu empresa" es literal y es el
diferencial — no es un informe que te entregan, es alguien que se sienta dentro.

Adapt: el movimiento firma de `logo-assemble-lockup` es que la marca **llega a existir en
pantalla construida a partir de piezas**. Lo mantengo entero; lo que cambio es el origen —
la marca no se ensambla de fragmentos abstractos, nace de la propia tesela que acaba de
tapar el agujero. Causa y efecto en la misma cadena.

Scene 1 (0.0–1.71s): el mosaico llega desde la derecha aún frenando. Sobre "Tessera es la pieza
que falta", una tesela cobalto maciza entra **desde fuera de cuadro por la izquierda a máxima
velocidad**, con **estela de desenfoque de movimiento** (`motion-blur-streak`), y **encaja** en el
hueco de la fila 2 a los ~0,95 s. Impacto: las cuatro teselas colindantes acusan el golpe con un
retroceso escalonado proporcional a su distancia (`physics-press-reaction`), las de más lejos más
tarde y menos.

Scene 2 (1.71–2.10s): **coma dramática**, y también está en el audio: la locución calla 0,39 s
aquí. Absolutamente nada se mueve.

Scene 3 (2.10–4.15s): la tesela recién encajada escala hacia el espectador y sus celdas internas
de 8×8 (el `qr-block` del preset) **se resuelven en el wordmark TESSERA** mediante **handoff por
escala** (`scale-swap-transition`) — las celdas se reorganizan, no se funden. `display-hero`,
centrado, ~45% del cuadro. Mientras la voz las nombra, dos etiquetas `micro-strong` se revelan
**una en cada hueco** del mosaico, que ha quedado detrás a `ink-soft`: "DIRECCIÓN FINANCIERA" a
los ~2,4 s y "CAPITAL HUMANO" a los ~3,3 s. Cada una en su cue, nunca juntas.

Scene 4 (4.15–5.36s): sobre "dentro de tu empresa", las teselas que rodean a las dos recién
etiquetadas **se encienden** (`asr-keyword-glow`, gobernado por la línea de tiempo del plano, no
por un raíl de palabras — esta locución no trae marcas por palabra) en un anillo que se propaga
hacia fuera desde ellas. La palabra "dentro", dicha con geometría.

Scene 5 (5.36–6.86s): reposo. Sin retroceso de cámara, sin deriva. Solo jitter bajo.

## Frame 3 — Sin la factura

- type: benefit_highlight
- blueprint: comparison-split (Adapt)
- scene: Dos columnas caen y se tachan — el comité a jornada completa y la gran consultora
- duration: 6.57s
- transition_in: push-slide LEFT
- status: animated
- voiceover: "Sin montar un comité de dirección a jornada completa. Sin la factura de una gran consultora."
- asset_candidates: none
- focal: las dos tarjetas tachadas
- roles: tarjeta izquierda = cutout · tarjeta derecha = cutout · sin mosaico (ausencia deliberada)
- sfx: click-soft
- src: compositions/frames/03-sin-factura.html

La objeción, resuelta antes de que se formule. Las dos alternativas que el espectador ya ha
descartado por caras aparecen y se tachan. Sin cifras: no tenemos ninguna verificada y una
inventada rompería la credibilidad de una consultora financiera.

**El mosaico no aparece en este plano, y es a propósito.** Es el único de los ocho donde falta:
este plano va de las dos alternativas que el espectador ya ha descartado, no de Tessera. Su
ausencia es el argumento, y hace que su vuelta en el Frame 4 pese más.

Adapt: `comparison-split` mete las dos tarjetas a la vez desde alas opuestas. Conservo su
movimiento firma — los **basculamientos 3D enfrentados tipo libro que se abre** y el
**badge que salta en el borde interior** — pero las hago **secuenciales**, una por frase, porque
la voz las nombra una detrás de otra y meterlas juntas sería adelantarse a ella. El badge deja
de ser un adorno: es el tachón. Split-screen 50/50, mosaico al fondo a `ink-faint`.

Scene 1 (0.0–2.80s): la tarjeta izquierda entra desde el ala izquierda con basculamiento en
rotationY (`split-tilt-cards`). Dentro, cinco filas `table-name` — CFO · CONTROLLER · DIR. RRHH ·
DIR. FINANCIERO · ADMIN — que se apilan por **revelado escalonado** (`dynamic-content-sequencing`)
al ritmo de la enumeración hablada. Cabecera `micro`: "JORNADA COMPLETA". Split-screen 50/50,
mosaico al fondo a `ink-faint`.

Scene 2 (2.80–2.90s): una regla cobalto **barre** la tarjeta de izquierda a derecha y la tacha; el
badge del borde interior salta en el mismo fotograma del barrido (`css-marker-patterns`). Cae a
`ink-faint`. El tachón ocupa exactamente el hueco entre las dos frases.

Scene 3 (2.90–5.27s): la tarjeta derecha entra desde el ala derecha con el basculamiento espejado.
Dentro, una **columna de pixel-glitch** del preset y la cabecera "GRAN CONSULTORA". El mismo
barrido la tacha a los ~4,9 s, en el cue de "la factura".

Scene 4 (5.27–6.57s): las dos tachadas y apagadas, quietas. Entre ellas se abre una franja de
`paper` limpia — el hueco donde va lo que viene. Reposo.

## Frame 4 — Finanzas

- type: feature_showcase
- blueprint: grid-card-assemble (Adapt)
- scene: La primera tesela se abre en tres sub-teselas: dirección financiera, financiación, M&A
- duration: 6.93s
- transition_in: zoom-through
- status: animated
- voiceover: "Finanzas. Dirección financiera externa. Búsqueda de financiación. Operaciones de compraventa."
- asset_candidates: none
- focal: la tesela FINANZAS abierta
- roles: sub-teselas = cutout · tesela madre = supporting · retícula = background
- sfx: pop
- src: compositions/frames/04-finanzas.html

Primera mitad de la evidencia. Los tres servicios entran en cascada, uno por cue de voz —
nunca los tres de golpe. La tesela madre no desaparece: se abre. El servicio vive dentro
del área, no al lado.

Adapt: conservo el movimiento firma de `grid-card-assemble` — el **autoensamblado escalonado**
de N piezas — pero la cascada ocurre **dentro del contorno de la tesela madre**, que se queda en
pantalla. Es la diferencia entre "aquí tienes tres servicios" y "esto es lo que hay dentro de
esta pieza". El zoom-through de entrada es uno de los dos únicos vectores Z del vídeo.

Scene 1 (0.0–0.65s): sobre "Finanzas", la tesela de la fila 2 **avanza hacia cámara**
— zoom-through, Z hacia delante (`cut-catalog.md`, desenfoque de pico 18px por ser superficie de
cuadro completo) — hasta que su contorno enmarca el 70% del cuadro. "FINANZAS" en `display-chapter`
se ancla arriba a la izquierda, fuera del contorno. Layout asimétrico 60/40. El resto del mosaico
queda fuera de cuadro; no se desvanece.

Scene 2 (0.65–2.30s): la primera sub-tesela se ensambla dentro del contorno: `row-headline`
"DIRECCIÓN FINANCIERA EXTERNA" con un `mono-tag` "PART-TIME" pegado al borde inferior. Entrada por
asentamiento de cola larga, sin sobreimpulso.

Scene 3 (2.30–3.90s): la segunda, debajo, misma cadencia y mismo intento de ease:
"BÚSQUEDA DE FINANCIACIÓN".

Scene 4 (3.90–5.53s): la tercera: "M&A" en `row-headline` con "COMPRAVENTA DE EMPRESAS" en
`mono-tag`. Las tres forman una columna dentro de la tesela madre.

Scene 5 (5.53–6.93s): reposo. La columna se lee entera. Jitter bajo.

## Frame 5 — Capital humano

- type: feature_showcase
- blueprint: grid-card-assemble (Reproduce)
- scene: La segunda tesela repite el gesto de la primera con headhunting, directivos part-time y RPO
- duration: 7.85s
- transition_in: zoom-through
- status: animated
- voiceover: "Capital humano. Headhunting de perfiles directivos. Talento senior a tu medida. Y procesos de selección completos."
- asset_candidates: none
- focal: la tesela CAPITAL HUMANO abierta
- roles: sub-teselas = cutout · tesela madre = supporting · retícula = background
- sfx: pop
- src: compositions/frames/05-capital-humano.html

Segunda mitad. Repetir el mismo gesto que en Finanzas es deliberado: dos áreas, un mismo
sistema. La rima visual dice "esto es una estructura, no un catálogo de servicios sueltos".

Reproduce: la misma instancia exacta del Frame 4 — mismo layout, misma cadencia, mismos
intentos de ease. **La rima es el argumento**, así que cualquier variación gratuita la
rompería. Lo único que cambia es de qué celda del mosaico venimos (fila 3, no fila 2), lo que
hace que la entrada llegue desde abajo-izquierda en vez de arriba-izquierda.

Scene 1 (0.0–0.95s): sobre "Capital humano", la tesela de la fila 3 avanza hacia cámara con el
mismo zoom-through y el mismo desenfoque de pico. Como viene de la fila 3 y no de la 2, la entrada
llega desde abajo-izquierda. "CAPITAL HUMANO" en `display-chapter`, arriba a la izquierda.

Scene 2 (0.95–2.90s): sub-tesela 1: `row-headline` "HEADHUNTING" + `mono-tag`
"PERFILES DIRECTIVOS Y SENIOR".

Scene 3 (2.90–4.60s): sub-tesela 2: "DIRECTIVOS PART-TIME" + `mono-tag` "TALENTO A TU MEDIDA".

Scene 4 (4.60–6.55s): sub-tesela 3: "RPO" + `mono-tag` "PROCESOS DE SELECCIÓN COMPLETOS".

Scene 5 (6.55–7.85s): reposo, idéntico al del Frame 4. Jitter bajo.

## Frame 6 — Un solo proveedor

- type: social_proof
- blueprint: dataviz-countup (Adapt)
- scene: El 24 cuenta hacia arriba mientras el mosaico se completa y aparece LT Impulsa
- duration: 6.07s
- transition_in: push-slide LEFT
- status: animated
- voiceover: "Veinticuatro profesionales en Madrid. Y gestoría propia. Un solo proveedor."
- asset_candidates: none
- focal: el numeral 24
- roles: numeral = cutout · mosaico = supporting → cutout · retícula = background
- sfx: riser, chime
- handoff_out: mosaico 6×4 completo — centro, escala 1.0, opacidad 1, quieto, sin huecos
- src: compositions/frames/06-un-proveedor.html

La prueba. Es el único número verificado que tenemos y por eso carga solo con todo el peso.
El mosaico se cierra aquí: es el pago visual de los dos huecos del Frame 1, cinco planos después.

Adapt: conservo el movimiento firma de `dataviz-countup` — el **contador que escala con su
propio valor** — y descarto sus gráficas y su parrilla de estadísticas: no tenemos más números
verificados y rellenar con datos inventados sería exactamente lo que una consultora financiera
no puede permitirse. Este plano vuelve a la corriente LEFT después de los dos zoom-through: es
la señal de que salimos del detalle y volvemos a la vista completa.

Scene 1 (0.0–2.25s): el plano entra con la corriente, todavía frenando desde la izquierda. El
numeral **cuenta de 0 a 24** (`counting-dynamic-scale`) en `vbig-numeral` centrado, creciendo de
tamaño con el valor; "PROFESIONALES · MADRID" en `micro-strong` debajo. Centrado, ~50% del cuadro.
El contador arranca en el fotograma en que la voz dice el número y termina antes que la frase.

Scene 2 (2.25–3.35s): el 24 encoge y **se acopla** a la esquina superior izquierda mientras una
tercera tesela aterriza en el centro: "LT IMPULSA" en `row-headline`, "GESTORÍA PROPIA" en
`mono-tag`. El acople y el aterrizaje son el mismo gesto continuo (`card-morph-anchor`).

Scene 3 (3.35–4.37s): el mosaico 6×4 vuelve a formarse alrededor y **los dos huecos se llenan**
por fin, con el mismo golpe de encaje del Frame 2 pero sin estela — ya no llegan de fuera, ya
estaban dentro. "UN SOLO PROVEEDOR" en `row-headline` bajo la regla superior.

Scene 4 (4.37–6.07s): reposo sobre el mosaico completo. Es la primera vez en el vídeo que la malla
no tiene ni un hueco, y hay que darle tiempo a que se note.

## Frame 7 — Sin tener que vender

- type: benefit_highlight
- blueprint: kinetic-type-beats (Adapt)
- scene: El mosaico completo se queda quieto y la frase cae en dos tiempos sobre él
- duration: 6.41s
- transition_in: push-slide LEFT
- status: animated
- voiceover: "Para que crezcas y te profesionalices. Sin tener que vender tu empresa."
- asset_candidates: none
- focal: la línea "Sin tener que vender tu empresa"
- roles: tipografía = cutout · mosaico completo = background (ink-faint) · retícula = background
- sfx: none
- handoff_in: mosaico 6×4 completo — entra desplazándose a la izquierda a la velocidad de salida del Frame 6, escala 1.0, opacidad 1 cayendo a ink-faint durante los primeros 0,4 s
- src: compositions/frames/07-sin-vender.html

El remate emocional, y el plano más quieto del vídeo. Es la posición de Tessera dicha en
sus propias palabras (Eduardo Serrano). Va después de la prueba y no antes: primero te
demuestro que puedo, luego te digo lo que eso significa para ti.

Adapt: `kinetic-type-beats` en su forma más desnuda — dos tiempos, corte duro entre ellos,
y nada más en pantalla. El movimiento firma es el cambio de línea; aquí es lo único que se
mueve en seis segundos, y por eso pega.

Scene 1 (0.0–2.37s): el mosaico completo baja a `ink-faint` en los primeros 0,4 s y se convierte
en fondo. "Para que crezcas y te profesionalices." entra por **revelado escalonado por palabra**
(`dynamic-content-sequencing`) en `display-quote`, centrado sobre él.

Scene 2 (2.37–2.79s): quietud total. La coma antes del remate — 0,42 s de silencio insertados en
el propio wav para que exista de verdad, no solo en el montaje.

Scene 3 (2.79–4.71s): **corte duro** (`discrete-text-sequence`) a "Sin tener que vender tu
empresa." en `display-closing`. En el mismo fotograma, una **regla cobalto tacha la palabra
"vender"** (`css-marker-patterns`) — no la borra, la niega.

Scene 4 (4.71–6.41s): reposo absoluto. Ni jitter. Es el plano más quieto del vídeo y esa quietud
es la carga útil.

## Frame 8 — Tessera

- type: branding
- blueprint: titlecard-reveal (Reproduce)
- scene: Lockup centrado, bajada y dominio bajo la línea de cobalto
- duration: 5.37s
- transition_in: push-slide LEFT
- status: animated
- voiceover: "Tessera. Finanzas y capital humano para pymes."
- asset_candidates: none
- focal: el wordmark TESSERA
- roles: wordmark = cutout · retícula = background
- sfx: impact-bass-2
- src: compositions/frames/08-cierre.html

Cierre en calma. Un solo movimiento, y quieto. El dominio se queda en pantalla el tiempo
suficiente para leerlo dos veces.

Reproduce: `titlecard-reveal` tal cual — **un único movimiento contenido y después quietud**.
La baja energía es la carga útil, no una carencia: llega detrás de siete planos que sí se
mueven. Es el único plano con salida propia del vídeo.

Scene 1 (0.0–0.60s): todo lo anterior sale por la izquierda. Sobre "Tessera", el wordmark sube y
aparece en el centro con **un solo gesto** (`spring-pop-entrance` en registro de asentamiento
suave, sin sobreimpulso), `display-hero`. Centrado. La retícula y las dos reglas se mantienen.

Scene 2 (0.60–2.77s): bajo la regla, "Finanzas y capital humano para pymes." en `body-lede`,
revelada en su cue. Una fila de cuatro teselas macizas se asienta bajo la línea como firma.

Scene 3 (2.77–5.37s): "tesseraservices.com" en `mono-chrome` aparece debajo a los ~3,1 s y **se
queda** el resto del plano — tiempo para leerlo dos veces. Quietud total, sin jitter: es el último
fotograma y tiene que poder congelarse como imagen fija. Salida del vídeo, la única del film:
fundido a `paper` en los últimos 0,3 s.
