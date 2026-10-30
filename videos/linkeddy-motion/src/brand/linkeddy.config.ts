/**
 * LINKEDDY — identidad de motion en un solo archivo.
 *
 * Cuando llegue el brand kit definitivo, se cambia aquí (colores, familias,
 * curvas, zonas seguras) y todas las piezas se actualizan. Los archivos de
 * fuente viven en ./fonts y se registran en ./fonts.ts.
 */

export const brand = {
  name: 'LinkEddy',

  // ── Paleta provisional ────────────────────────────────────────────
  // Marfil y blanco roto para superficies, carbón para tinta, grises
  // cálidos para lo secundario y un único acento: "tomate" escandinavo.
  colors: {
    paper: '#FBF8F2', // superficie de tarjetas / UI
    ivory: '#F1EBDF', // fondo claro de marca
    ink: '#1B1A17', // tipografía, negro suave
    night: '#141311', // fondo oscuro de marca
    grey: '#8C867B', // texto secundario
    greyLight: '#D9D2C5', // reglas, bordes
    accent: '#F04E23', // acento: con moderación
  },

  // ── Tipografía ────────────────────────────────────────────────────
  // Familjen Grotesk (Familjen, Estocolmo) para titulares y cuerpo,
  // Instrument Serif en cursiva para el comentario irónico y
  // DM Mono para la microtipografía (metadatos, etiquetas, contadores).
  fonts: {
    display: 'Familjen Grotesk',
    serif: 'Instrument Serif',
    mono: 'DM Mono',
  },

  type: {
    tracking: {
      display: '-0.04em',
      title: '-0.025em',
      mono: '0.08em',
    },
  },

  // ── Movimiento ────────────────────────────────────────────────────
  // Curvas cúbicas (x1, y1, x2, y2). Entradas rápidas que frenan largo,
  // salidas que aceleran sin rebote. Nada de springs con overshoot.
  ease: {
    enter: [0.16, 1, 0.3, 1] as const, // expo out: entra con decisión
    settle: [0.22, 1, 0.36, 1] as const, // quint out: asentar detalles
    move: [0.65, 0, 0.35, 1] as const, // in-out: desplazamientos de composición
    exit: [0.7, 0, 0.84, 0] as const, // expo in: salidas limpias
    draw: [0.45, 0, 0.2, 1] as const, // trazos de línea
  },

  // Duraciones base en frames (30 fps).
  beat: {
    micro: 8,
    short: 14,
    base: 20,
    long: 30,
  },

  // ── Formato ───────────────────────────────────────────────────────
  video: { width: 1080, height: 1920, fps: 30 },

  // Zonas seguras aproximadas para Reels y TikTok a 1080×1920 (px).
  // top: barra superior/pestañas · bottom: descripción, audio, CTA ·
  // right: columna de botones (like, comentar, compartir).
  safe: { top: 220, bottom: 440, left: 64, right: 150 },
} as const;

export type Brand = typeof brand;
export type Bezier = readonly [number, number, number, number];
