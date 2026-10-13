# Prompt para Claude Code — Reel de Instagram "Tina Café"

## Objetivo
Crea un vídeo vertical para Instagram Reels/Stories de **Tina Café**, una cafetería con estética *cute*, cálida y editorial. Debe dar ganas de entrar a tomar un café: acogedor, tierno, con humor suave y muy cuidado tipográficamente. Nada de estética genérica de plantilla.

## Especificaciones técnicas
- Formato: **1080×1920 px (9:16)**, 30 fps, duración **15–20 s**.
- Exportar **MP4 (H.264)**, listo para subir a IG.
- Herramienta recomendada: **Remotion** (React + TypeScript). Alternativa: HTML/CSS/GSAP con captura a MP4 vía Puppeteer + ffmpeg.
- Zona segura: no colocar texto importante en los 250 px superiores ni los 340 px inferiores (UI de Instagram).
- Loop suave: el último frame debe enlazar visualmente con el primero.

## Assets incluidos (carpeta `assets/`)
- `tina-logo-circle.png` — logo principal: círculo chocolate con aro fino dorado, "TINA" en crema + "café". **Usar siempre este**, nunca redibujarlo.
- `tina-logo.png` / `tina-logo.svg` — versión del logotipo sin círculo.
- `ilustraciones/01-bizcocho.png` — ilustración del personaje Tina.
- No inventar ni dibujar otros logos. Si hacen falta más ilustraciones de Tina, dejar huecos marcados `[ILUSTRACIÓN TINA]` para sustituir.

## Paleta (usar solo estos colores)
| Rol | Nombre | HEX |
|---|---|---|
| Fondo principal | Chocolate | `#5C3A1E` |
| Fondo profundo / sombras | Chocolate oscuro | `#3F2611` |
| Texto sobre chocolate | Crema | `#F2E3C0` |
| Fondo claro | Hueso | `#FAF4E6` |
| Acentos finos (aros, líneas) | Oro | `#B8893E` |
| Acento cálido | Caramelo claro | `#D4A668` |
| Texto secundario sobre claro | Caramelo | `#8B5E3C` |
| Acento puntual (mejillas, corazones) | Terracota | `#C97A5C` |
| Destacado itálico sobre chocolate | Amarillo mantequilla | `#FFDE86` |
| Tinta | Ink | `#2A1B0E` |

Sin degradados agresivos, sin neón y sin colores fuera de la paleta.

## Tipografía (Google Fonts)
- **Fraunces**: titulares. 900 en redonda para impacto ("Invierno", "La final") y 300–400 en *itálica* para frases cálidas ("nuestro horario de", "vívelo con nosotros —").
- **Inter**: textos de apoyo, 400–500.
- **JetBrains Mono**: etiquetas pequeñas en MAYÚSCULAS con tracking amplio (letter-spacing ~3px), por ejemplo "ENTRE SEMANA", "SÁBADO".
- Patrón editorial típico: frase pequeña en itálica (amarillo mantequilla o crema al 75 %) → titular grande en Fraunces 900 → línea fina crema al 40 % → datos.

## Lenguaje visual
- Marco fino de 1.5 px en crema (o chocolate sobre fondo claro), inset ~24 px, radio 4 px. Es la firma de todos los carteles.
- Mucho aire, composición centrada y jerarquía clara.
- Decoración sutil: copos, granos de café o vapor dibujados con línea fina al 8–18 % de opacidad.
- Personaje **Tina**: chica cute de piel morena/canela, estilo ilustración tierna. Aparece metida en una taza de café, empujando un bollo gigante o haciendo un corazón con las manos.
- **Granitos felices**: granos de café con carita kawaii, útiles como elementos animados secundarios.

## Tono de copy
Español de España, cercano, tierno y con guiño. Frases cortas, en minúscula cuando son en itálica. Ejemplos del tono: "vívelo con nosotros —", "¡hasta pronto!", "el café, mejor calentito". Prohibido: emojis, mayúsculas gritonas en titulares, signos de exclamación en exceso.

## Información real del negocio (usar solo esta)
- **Horario de invierno**: entre semana 08:00–20:00 · sábado 10:00–22:00 · domingo 10:00–15:00.
- **Promos**: Hora Reposada (12–14 h, mar–vie), Hora Aperol (14–16 h, mar–vie), Hora del Recreo para estudiantes (pincho + bebida, 3,50 €).
- **Tarjeta de fidelidad**: 10 consumiciones + 1 gratis.

## Guion propuesto (≈18 s)
1. **0–2,5 s · Apertura**: fondo chocolate. El aro dorado del logo se dibuja (stroke animado) y aparece `tina-logo-circle.png` con un pequeño rebote (scale 0.9 → 1.03 → 1). Detrás, vapor de café en línea fina crema.
2. **2,5–5 s · Gancho**: itálica amarillo mantequilla "tu rincón favorito" y debajo "**Tina café**" en Fraunces 900, entrando letra a letra con stagger de 30 ms.
3. **5–9 s · Personaje**: transición a fondo hueso con una ola o barrido circular desde el centro. Tina (ilustración) aparece dentro de una taza con un leve balanceo y granitos felices saltando alrededor. Copy: "café, bollitos y mimos" en itálica caramelo.
4. **9–13 s · Promos**: tres tarjetas con marco fino que se deslizan en vertical, una tras otra: Hora Reposada · Hora Aperol · Hora del Recreo 3,50 €. Etiqueta mono arriba y titular Fraunces.
5. **13–16 s · Horario**: vuelta al chocolate con copos sutiles cayendo despacio. "nuestro horario de / **Invierno**" y las tres franjas horarias apareciendo en cascada.
6. **16–18 s · Cierre**: logo centrado, "te esperamos —" en itálica. Fundido que enlaza con el frame inicial para el loop.

## Animación
- Easing suave: `cubic-bezier(0.22, 1, 0.36, 1)` o springs de Remotion con damping alto. Nada brusco ni demasiado rápido.
- Microinteracciones *cute*: rebotes pequeños, balanceos de ±3°, parpadeos de los granitos y vapor ondulante.
- Ritmo de unos 2–4 s por escena. Texto en pantalla mínimo 1,5 s para que se pueda leer.
- Opcional: hueco para música lo-fi/acústica suave (no incluir audio con copyright).

## Entregables
1. Proyecto Remotion con escenas separadas por componente (`Intro`, `Hook`, `Character`, `Promos`, `Hours`, `Outro`) y un archivo `brand.ts` con colores y fuentes.
2. `out/tina-reel.mp4` a 1080×1920.
3. Una portada `out/cover.png` a 1080×1920 para la miniatura del reel.

## Checklist de calidad
- [ ] Solo colores de la paleta y solo las 3 fuentes.
- [ ] El logo real se usa sin deformar (mantener proporción 1:1).
- [ ] El texto respeta las zonas seguras de IG.
- [ ] Contraste legible: crema sobre chocolate, chocolate sobre hueso.
- [ ] Sin emojis ni ilustraciones genéricas de stock.
- [ ] El loop final enlaza con el inicio.
