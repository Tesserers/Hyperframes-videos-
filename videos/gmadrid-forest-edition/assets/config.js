/* ============================================================
   G·MADRID BALONMANO — FOREST EDITION
   Configuración editable: textos, colores y tiempos.
   Los dos formatos (index.html = 1920×1080, compositions/vertical.html = 1080×1920)
   leen este mismo archivo. Cambia aquí y vuelve a renderizar.
   ============================================================ */
window.FOREST_CONFIG = {
  // ---------- Textos ----------
  text: {
    title: ["FOREST", "EDITION"],          // escena 3 (en horizontal va en una línea)
    season: "TEMPORADA 26/27",             // debajo del título, en lima
    words: ["NATURALEZA", "CRECIMIENTO", "DIVERSIDAD"], // escena 4, una a una
    signature: ["G·MADRID", "BALONMANO"],  // cierre, debajo del logo
  },

  // ---------- Colores ----------
  color: {
    bgDeep: "#071F1B",     // fondo
    bgCenter: "#123C34",   // degradado suave en el centro
    lime: "#C4E64D",       // acento principal
    pink: "#F14C9A",
    blue: "#36A9E8",
    white: "#FFFFFF",
    grey: "#A7B9B1",       // texto secundario
    // Colores de cada palabra de la escena 4 (mismo orden que text.words)
    words: ["#C4E64D", "#F14C9A", "#36A9E8"],
    // Pride de la estrella del club
    pride: {
      red: "#E30613",
      orange: "#F39200",
      yellow: "#FFDD00",
      green: "#95C11F",
      blue: "#009FE3",
      purple: "#8E1E7E",
    },
    // Tonos de hoja (la mayoría verdes)
    greens: ["#0B3D2E", "#14533C", "#1F6B45", "#2E8B4A", "#4FA83D", "#7EC242", "#A6D63F", "#C4E64D"],
    teal: "#00A7B5",
    branch: "#2F6B3A",
    pollen: "#EEF8C4",
  },

  // ---------- Producto ----------
  // Las imágenes están en assets/product (recortadas de las fichas oficiales con tools/extract_product.py).
  // Para cambiarlas, sustituye esos archivos manteniendo el nombre.

  // ---------- Tiempos (segundos) ----------
  time: {
    total: 15,
    sprout: 2.0,      // empiezan a brotar hojas
    gather: 4.5,      // las hojas giran hacia el centro y forman la corona
    title: 4.85,      // aparece FOREST EDITION
    reveal: 6.35,     // la corona se abre y nace la camiseta
    flip: 7.55,       // la camiseta gira y enseña la espalda
    words: [8.6, 9.6, 10.6], // palabra + detalle
    duo: 11.6,        // oficial + portería
    open: 12.8,       // las hojas se abren y aparece el logo
    zoomOut: 13.6,
    fade: 14.3,
  },
  growthSpeed: 1.6,   // velocidad del crecimiento tras el brote

  // Semilla del bosque: cambia el número para otra distribución de ramas y hojas
  seed: 2627,
};
