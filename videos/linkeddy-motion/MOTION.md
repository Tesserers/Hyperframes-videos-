# LinkEddy — lenguaje de motion

Fase 1. Las reglas que comparten todas las piezas. Los valores viven en
`src/brand/linkeddy.config.ts`; este documento explica el porqué.

## La idea

**Papel editorial que se mueve con intención.** Las piezas se comportan como
material impreso (fichas, recortes, notas al margen) que entra en cuadro con
decisión y se asienta despacio. Nada flota, nada rebota, nada brilla.

## Paleta provisional

| Rol | Color | Uso |
|---|---|---|
| Papel | `#FBF8F2` | Superficie de tarjetas e interfaces |
| Marfil | `#F1EBDF` | Fondo claro de marca |
| Tinta | `#1B1A17` | Tipografía. Negro suave, nunca `#000` |
| Noche | `#141311` | Fondo oscuro de marca |
| Gris cálido | `#8C867B` / `#D9D2C5` | Metadatos, reglas, bordes |
| Acento "tomate" | `#F04E23` | **Una cosa por plano**: la cifra, el trazo, el comentario |

## Tipografía

- **Familjen Grotesk** (estudio Familjen, Estocolmo): titulares y cuerpo.
  Grotesca con carácter, escandinava de verdad, en mayúsculas y con
  tracking negativo (-0.04em) para titulares grandes.
- **Instrument Serif cursiva**: la voz irónica. Solo comentarios al margen,
  apartes, la "voz de Eddy" encima del diseño.
- **DM Mono**: microtipografía (metadatos, etiquetas, contadores), siempre en
  mayúsculas con tracking +0.08em.

El contraste de escala manda: titulares de 110–130 px frente a micro de 20–22 px.

## Movimiento

| Curva | Bezier | Para qué |
|---|---|---|
| `enter` | 0.16, 1, 0.3, 1 | Entradas: llegan rápido y frenan largo |
| `settle` | 0.22, 1, 0.36, 1 | Detalles que se asientan (contadores) |
| `move` | 0.65, 0, 0.35, 1 | Desplazamientos de composición |
| `exit` | 0.7, 0, 0.84, 0 | Salidas: aceleran y se van limpias |
| `draw` | 0.45, 0, 0.2, 1 | Trazos de línea |

Reglas:

1. **Máscara antes que fundido.** El texto entra subiendo desde su propia línea
   base (`MaskReveal`). Los fundidos solo para retirar lo secundario.
2. **Cascada corta.** Dentro de un bloque, 3–4 frames entre elementos. Más,
   y parece PowerPoint.
3. **Causa y efecto.** Si algo entra, empuja a lo que ya estaba (profundidad,
   escala 0.93, leve oscurecido). Nada aparece "porque sí".
4. **Salidas por máscara fija.** La pieza se recoge y se desliza a través de
   un borde invisible, como entrando en una ranura. Sin zoom out.
5. **Sin rebotes, sin springs con overshoot, sin zooms exagerados.**
6. **Quietud antes del remate.** El chiste o la cifra clave se quedan
   quietos ~1 s para que se lean.

## Componentes base

`src/components/`

- `Stage`: lienzo 1080×1920 con fondo (transparente / claro / oscuro),
  reencuadre (`scale`, `offsetY`) y ritmo global (`pace`).
- `MaskReveal`: revelado de línea por máscara, con salida opcional.
- `Micro`: microtipografía mono.
- `RollingNumber`: contador de rodillo que frena en la cifra.
- `DrawPath`: trazo SVG que se dibuja (círculos a mano, flechas, diagramas).
- `Rule`: regla que crece desde la izquierda.

## Zonas seguras (Reels / TikTok, 1080×1920)

- Arriba: 220 px (pestañas, cabecera).
- Abajo: 440 px (descripción, audio, CTA).
- Derecha: 150 px (columna de botones).
- Cara en plano medio: aprox. y 330–890.
- Subtítulos de referencia: aprox. y 1250–1450.

A pantalla completa, todo el contenido se diseña entre y 220 y y 1480.
