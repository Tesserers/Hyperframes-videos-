---
format: 1920x1080
fps: 30
duration: 16s
loop: exact
message: "Una casa buena en un sitio bueno, vista en octavos."
arc: "Amanecer → mesa puesta → llegada con la maleta → la casa llena, y vuelta al amanecer"
audience: "Quien se plantea una segunda casa"
mode: autonomous
music: none
narration: none
text_on_screen: none
---

Plano de fondo para el hero de `octavo.es`. Una sola composición, cuatro planos de 4 s, bucle
exacto de 16 s. No lleva texto: lo pone la página encima.

## Video direction

**La idea.** Octavo no vende una casa, vende **una octava parte**. Así que la película no enseña
cuatro casas: enseña **una casa en cuatro momentos de un día**, y cada momento entra por un
octógono que se abre. Lo que se repite no es el sitio, es el gesto de la marca.

**Sistema de color — el del brandkit, sin tocarlo.** `yeso #EEF0F1`, `ceniza #DCE0E2`,
`basalto #15181C`, `grafito #2A2E33`, `almagre #A8341F`, `barro #E0764F`, `piedra #5F6469`. El
suelo del lienzo es `#F2F4F4`, el mismo que la página usa en `#inicio`. La regla de proporción
(55 % yeso · 25 % basalto · 12 % grafito · 8 % acento) se cumple sola aquí: la pieza es
fotografía de hora dorada y el acento no aparece. **No hay ningún degradado de marca** —el
brandkit los prohíbe— y no hay grano ni viñeta, porque el brandkit dice que el color es plano.

**Tipografía.** Ninguna. Es la consecuencia de que el hero ya tenga la suya.

**El octógono es la única figura, y recorta.** El brandkit lo dice con todas las letras: «El
octógono recorta, no dibuja contornos», y el marco octogonal es el recurso autorizado para la
fotografía. La costura entre planos es por tanto un **octógono regular que crece** hasta pasarse
del cuadro, con canto duro —nunca difuminado, nunca con borde dibujado—. La orientación es la del
brandkit: lados planos arriba y abajo, esquinas a 45°.

**La rotación del octavo.** La apertura no nace en el centro. Nace desplazada del centro, y cada
plano avanza **dos octavos** (90°) alrededor: arriba-derecha → abajo-derecha → abajo-izquierda →
arriba-izquierda. En los cuatro planos la apertura da **una vuelta completa** al anillo de ocho.
El espectador no ve un diagrama; siente que el cuadro gira. Es el calendario rotativo contado con
movimiento en vez de con una infografía.

**Movimiento.** Una sola cámara para los 16 s: **todos los planos empujan hacia delante**, escala
1,04 → 1,11, a velocidad constante. Constante a propósito: si los dos lados de una costura van a
la misma velocidad, la costura no se nota como un corte sino como una continuación. Cada plano
lleva además una deriva lateral pequeña (±22 px) en la dirección que pide su contenido.

**La apertura también va a velocidad constante, y eso corrige una decisión mía anterior.** El
primer montaje usaba para la apertura la curva única del brandkit, `cubic-bezier(.2,.8,.2,1)`.
Al verlo renderizado no funcionaba: esa curva está pensada para entradas de interfaz —arranca
muy rápida y se posa larga— y aplicada a una apertura a cuadro completo abre el octógono en dos
décimas de segundo. El resultado era un parpadeo, no una figura: **la forma octogonal no llegaba
a leerse**. La apertura crece ahora a radio constante durante 1,1 s, así que el octógono es
legible a todos sus tamaños y además sale del cuadro a la misma velocidad a la que viaja la
cámara. La curva de marca sigue en el fichero, documentada, para la variante rotulada, que es
donde el brandkit la pone: en las entradas de texto.

**Nada oscila.** No hay respiración, ni balanceo, ni vaivén. La cámara va a un sitio durante
dieciséis segundos.

**Zona segura.** Medida sobre su propio marcado, no estimada: el bloque de texto del hero tiene
660 px de ancho dentro de un contenedor de 1240 px centrado en 1920, así que ocupa de x=340 a
x=1000 —algo más de la mitad izquierda del cuadro—. Por eso el anillo de las ocho aperturas no
está centrado en el cuadro sino en x=1340, con radio 240: **las cuatro aperturas nacen entre
x=1170 y x=1510**, enteramente a la derecha del texto. Y los cuatro encuadres dejan esa mitad
izquierda clara —cielo, mar, pared blanca— para que el basalto del titular siga leyéndose sin
que el vídeo tenga que oscurecerse.

**Lista negativa.** Sin texto. Sin logotipo incrustado (la web ya lo lleva en la barra). Sin
fundidos. Sin grano. Sin viñeta. Sin degradados de marca. Sin anillo de ocho dibujado. Sin
ninguna figura que el brandkit no sancione.

## Frame 1 — Amanecer

- src: `assets/photos/01-amanecer.jpg`
- beat: 0,0 – 4,0 s
- apertura: octavo 1 · arriba-derecha (14,9 – 16,0 s, la que cierra el bucle)
- deriva: hacia la puerta abierta
- status: animated

La casa se abre. Ella abre la corredera sobre la bahía a primera hora. Es el plano que la web ya
usa de hero, así que el vídeo empieza exactamente donde la página estaba: quien ya conocía el
sitio no nota el cambio hasta que el cuadro se mueve. El tercio izquierdo es sofá claro y cielo
—la zona del titular—.

## Frame 2 — La mesa puesta

- src: `assets/photos/02-desayuno.jpg`
- beat: 4,0 – 8,0 s
- apertura: octavo 3 · abajo-derecha (2,9 – 4,0 s)
- deriva: hacia el mar
- status: animated

«Casas habitadas: una mesa puesta», dice el brandkit en el apartado de fotografía. Esta es
literalmente esa foto. Café, fruta, la bahía de Altea detrás. El plano que explica por qué 6,5
semanas al año son suficientes.

## Frame 3 — Llegas con la maleta

- src: `assets/photos/03-llegada.jpg`
- beat: 8,0 – 12,0 s
- apertura: octavo 5 · abajo-izquierda (6,9 – 8,0 s)
- deriva: hacia la puerta
- status: animated

La promesa de la marca, sin tener que escribirla: «Tú llegas con la maleta.» Cuatro personas
cruzando la puerta con el equipaje. Es el único plano con movimiento humano real dentro del
encuadre, así que va en el tercer tiempo, donde una película necesita subir.

## Frame 4 — La casa llena

- src: `assets/photos/04-piscina.jpg`
- beat: 12,0 – 16,0 s
- apertura: octavo 7 · arriba-izquierda (10,9 – 12,0 s)
- deriva: hacia la casa
- status: animated

Tres generaciones en la piscina al atardecer. Cierra el día que abrió el plano 1 y cierra el
argumento: la casa se usa. Desde aquí el bucle vuelve al amanecer, que es justo lo que hace un
calendario que rota.

## El cierre del bucle

El bucle exacto está construido, no encontrado. El montaje real es de **cinco capas**, no de
cuatro: el plano 1 aparece dos veces, al principio y al final.

- Cada apertura dura 1,1 s y **termina** en el límite del tiempo: la del plano 2 corre de 2,9 a
  4,0; la del 3, de 6,9 a 8,0; la del 4, de 10,9 a 12,0; y la del plano 1 de cierre, de 14,9 a
  16,0.
- El octógono **se pasa de largo un 12 %**. No es un capricho: sin ese margen la figura termina
  de cubrir el cuadro justo en el límite del tiempo, y el último fotograma que se renderiza
  (15,967 s, uno antes del 16) todavía enseñaba una cuña del plano saliente en las esquinas.
  Con el margen, la cobertura se completa hacia el 89 % de la apertura y el octógono sigue
  creciendo sin que se vea. Se detectó comparando píxel a píxel ese fotograma con el primero.
- Cada foto arranca su empuje de cámara **cuando empieza su apertura**, no cuando termina, así
  que dentro del octógono la imagen ya viene en marcha y las dos mitades de la costura van a la
  misma velocidad.
- El plano 1 de cabeza no arranca en su estado inicial: arranca en el estado que el plano 1 de
  cierre tendrá a los 0,9 s de su apertura. Ese valor se calcula en el propio guion de la
  composición, no se escribe a mano, para que no pueda desviarse.

Comprobado, no supuesto. En el navegador, la matriz de transformación del plano 1 de cabeza en
t = 0 y la del plano 1 de cierre en t = 16 son idénticas: `matrix(1.0551, 0, 0, 1.0551, -4.7451,
1.7255)`. Y comparando píxel a píxel el último fotograma renderizado (15,967 s) con el primero,
la diferencia media es de 1,16 sobre 255 —un fotograma de recorrido de cámara, que es
exactamente lo que tiene que haber entre dos fotogramas consecutivos de un movimiento continuo—
y no hay ninguna cuña en las esquinas. El navegador puede repetir el vídeo indefinidamente sin
que se vea la juntura.

## El velo de legibilidad

No estaba en el plan y se añadió tras medirlo. Montado el vídeo dentro de su hero real y
ocultando el texto para leer el fondo que queda debajo, el percentil 5 de luminancia bajo cada
bloque daba esto:

| Texto | Su hero de hoy | Plano 3 sin corregir | Plano 4 sin corregir | Exige AA |
|---|---|---|---|---|
| `h1` 104 px basalto | 9,79:1 | 4,63:1 | 4,09:1 | 3:1 |
| itálica 104 px almagre | 2,78:1 | **1,77:1** | **1,58:1** | 3:1 |
| párrafo 21 px | 4,00:1 | **2,25:1** | **1,83:1** | 4,5:1 |

Dos conclusiones distintas, y conviene no mezclarlas. La primera es suya y es anterior al
vídeo: **su hero ya no llega a AA** ni en la itálica ni en el párrafo. La segunda sí era mía:
los planos 3 y 4 llevan masa oscura —la copa del olivo, las colinas del atardecer— justo donde
cae el texto, y hundían esas cifras muy por debajo de su propio punto de partida.

Lo que no funcionó, y por qué:

- **Reforzar su degradado.** Ni duplicándolo se llega: su gradiente ya ha caído al 7 % en
  x=1267, y el bloque de texto termina en x=1014, así que justo donde hace falta no hay velo
  que reforzar.
- **Reencuadrar.** El plano 3 se salvaba subiendo la escala base a 1,16 y desplazando el
  encuadre, pero con margen cero y con la imagen ya a 1,33× de ampliación. El plano 4 no se
  salvaba de ninguna manera.

Lo que sí funciona es **cambiar la forma del velo, no su fuerza**: plano hasta x=940 y cayendo
a cero en x=1460, siguiendo al texto en vez de al borde del cuadro. Cada plano lleva el suyo,
dentro de su propio octógono, con la intensidad mínima que necesita: 0 · 0,10 · 0,35 · 0,40.
El plano 1 se queda en cero, es decir **exactamente como se ve su web hoy**. Y como la
intensidad solo cambia en los cortes, donde la imagen cambia entera, no se percibe.

Medido otra vez sobre el hero real: itálica de 2,81 a 2,91 y párrafo de 3,95 a 4,00 en los
cuatro planos, contra 2,78 y 4,00 de su hero actual. El `h1` baja de 9,79 a 7,40 en el peor
plano, que sigue siendo dos veces y media el umbral. El vídeo no empeora nada.

La variante `aa` sube esos velos a 0,125 · 0,20 · 0,425 · 0,475 y deja los cuatro planos por
encima de AA (itálica ≥ 3,12 · párrafo ≥ 4,51). Va aparte porque vela algo más la fotografía y
esa es una decisión del cliente, no mía.
