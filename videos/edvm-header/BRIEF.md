---
workflow: general-video
flow: automation
storyboard: no
message: "people for what's next: el plano de fondo del hero de edvm, mirado a través de la «m»."
destination: web
aspect: 1920x1080
language: es
audience: "Directores y fundadores que van a abrir una búsqueda comercial y quieren a alguien que les acompañe de principio a fin"
length: 16s
angle: "Plano de fondo en bucle exacto para la cabecera: el marco de foto de la marca con las fotos de la marca cambiando tabla a tabla, sin una sola palabra"
style_preset: brand-native
capture: client-supplied
narration: none
audio: none
loop: exact
---

## Intent

Es un **vídeo de cabecera**, no un promo. Va detrás del hero de la web de edvm (Edward del Valle
Manrique), donde la página pone el logo y el titular en HTML. Igual que en Octavo, de ahí salen
tres decisiones:

1. **Sin texto en pantalla.** El titular lo pone la web. Si el vídeo llevase uno, chocaría con el
   suyo en cuanto cambiase el ancho del navegador.
2. **Sin pista de audio.** El vídeo tiene que arrancar solo, y para eso el navegador exige
   `muted`. Así que el MP4 sale sin stream de audio.
3. **Bucle exacto.** El último fotograma empalma con el primero.

## Assets

Todo sale de `brand/EDVM_brandkit.pptx` (v1.0, 2026, 43 diapositivas). No hay stock ni nada
inventado.

- **El marco.** Es el recurso «03 — marcos de foto · mira a través de la «m»» (diapositiva 35),
  con las coordenadas de sus propias formas: tres tablas de 260 px de alto, separadas 40 px, de
  x=760 al borde derecho, con el extremo izquierdo de radio 130. El bloque liso de 0 a 760 px es
  el que la marca reserva para el texto.
- **Fotografía.** Cuatro de las fotos del brandkit: bosque nórdico, casa de Falun entre abedules,
  conversación en oficina con luz lateral y mesa con la casita roja. Ninguna es un retrato a
  cámara. Llegan a 1402×1122 (el bosque a 1122×1402). El brandkit pide 2400 px de ancho, pero
  aquí cada foto ocupa una ventana de 1160×860, así que se usan casi a su tamaño y no hace falta
  reescalarlas.
- **Logos.** Están en `brand/` en SVG (horizontal, stacked y símbolo, en blanco), sin los
  metadatos C2PA. El vídeo no los usa, pero sí `integracion/hero-preview.html`.
- **Tipografía.** Manrope 700/800 en woff2, solo para la maqueta del hero.

## Customizations

- **Colores del brandkit, sin tocar.** El marco es swedish red `#A61C1C`. Hay una variable
  `marco` que acepta `rojo`, `carbon` (`#191919`) o `claro` (`#F6F3EE`), que son los tres marcos
  de la diapositiva 36. Se entregan el rojo (principal) y el carbón.
- **«La «m» se completa».** Cada foto nueva no entra de golpe. Llega tabla a tabla, de arriba
  abajo, con 0,2 s entre una y otra: una tabla, dos de tres, completa. Es el recurso «pasos y
  escalas» del brandkit, contado con movimiento.
- **Todo va hacia la izquierda, hacia el titular.** El corte de cada tabla barre de derecha a
  izquierda, la foto que llega se posa 140 px en esa misma dirección y todas las fotos se
  desplazan a 16 px/s constantes. Al ir todo en un mismo sentido, el cambio de foto se lee como
  algo que sigue avanzando y no como un corte.
- **Nada más.** Ni sombras, ni degradados, ni grano, ni fundidos: el brandkit los prohíbe («sin
  iconos de stock, sombras ni degradados») y pide un solo asset protagonista. El borde del corte
  es duro, sin difuminar.

## Notes

- **El hueco de texto se respeta siempre.** Entre x=0 y x=760 solo hay color plano en todos los
  fotogramas. El titular en blanco sobre `#A61C1C` da 7,6:1 y pasa WCAG AA de sobra. Sobre
  carbón, 17:1.
- **Ritmo.** Una foto cada 4 s y cuatro fotos: 16 s. Cada cambio dura 1,8 s, y el resto del tiempo
  la foto solo se desplaza. Detrás de un titular conviene que el fondo no tenga más ritmo que eso.
- **CLI.** El proyecto fija `hyperframes@0.8.46`, igual que Octavo. En este entorno `npx` falla en
  silencio porque `onnxruntime-node` no puede descargar sus binarios. Se resolvió instalando el
  mismo CLI con `--ignore-scripts`; no afecta al render.
