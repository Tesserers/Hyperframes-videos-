/* ============================================================
   FOREST ENGINE — G·Madrid Balonmano "Forest Edition"
   Dibuja todo el bosque en un <canvas> como función pura del tiempo:
   render(t) siempre produce el mismo fotograma para el mismo t.
   Nada de Math.random sin semilla, nada de relojes.
   ============================================================ */
(function () {
  "use strict";

  // ---------- utilidades ----------
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const prog = (t, start, dur) => clamp((t - start) / dur);
  const easeOutCubic = (k) => 1 - Math.pow(1 - k, 3);
  const easeInCubic = (k) => k * k * k;
  const easeInOutCubic = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  const easeOutExpo = (k) => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k));
  const easeInOutSine = (k) => -(Math.cos(Math.PI * k) - 1) / 2;
  // muelle amortiguado: 0 -> 1 con un leve rebote
  const spring = (k, damp = 5.2, freq = 9) => (k <= 0 ? 0 : 1 - Math.exp(-damp * k) * Math.cos(freq * k));
  const angDiff = (a, b) => {
    let d = (b - a) % (Math.PI * 2);
    if (d > Math.PI) d -= Math.PI * 2;
    if (d < -Math.PI) d += Math.PI * 2;
    return d;
  };
  function hexToRgb(h) {
    const n = parseInt(h.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function mix(h1, h2, k) {
    const a = hexToRgb(h1), b = hexToRgb(h2);
    return `rgb(${Math.round(lerp(a[0], b[0], k))},${Math.round(lerp(a[1], b[1], k))},${Math.round(lerp(a[2], b[2], k))})`;
  }
  function rgba(h, a) {
    const c = hexToRgb(h);
    return `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  }
  function bez(p0, p1, p2, p3, s) {
    const u = 1 - s;
    return [
      u * u * u * p0[0] + 3 * u * u * s * p1[0] + 3 * u * s * s * p2[0] + s * s * s * p3[0],
      u * u * u * p0[1] + 3 * u * u * s * p1[1] + 3 * u * s * s * p2[1] + s * s * s * p3[1],
    ];
  }
  function bezTan(p0, p1, p2, p3, s) {
    const u = 1 - s;
    const dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * s * (p2[0] - p1[0]) + 3 * s * s * (p3[0] - p2[0]);
    const dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * s * (p2[1] - p1[1]) + 3 * s * s * (p3[1] - p2[1]);
    return Math.atan2(dy, dx);
  }

  // ---------- forma de hoja ----------
  // Hoja dibujada a lo largo de +x desde la base (0,0). shape: 0 lanceolada, 1 ovalada, 2 tropical curvada
  function leafPath(ctx, len, wid, shape, bend) {
    const w = wid;
    const tipY = bend * len * 0.12;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    if (shape === 1) {
      ctx.bezierCurveTo(len * 0.18, -w * 1.1, len * 0.7, -w * 1.05, len, tipY);
      ctx.bezierCurveTo(len * 0.7, w * 0.95, len * 0.18, w * 1.0, 0, 0);
    } else if (shape === 2) {
      ctx.bezierCurveTo(len * 0.25, -w * 0.9, len * 0.62, -w * 0.95 + tipY * 0.5, len, tipY);
      ctx.bezierCurveTo(len * 0.66, w * 0.55 + tipY * 0.6, len * 0.3, w * 0.8, 0, 0);
    } else {
      ctx.bezierCurveTo(len * 0.3, -w * 0.85, len * 0.72, -w * 0.6, len, tipY);
      ctx.bezierCurveTo(len * 0.72, w * 0.6, len * 0.3, w * 0.85, 0, 0);
    }
    ctx.closePath();
  }

  function drawLeaf(ctx, L, x, y, ang, scale, widK, alpha, light) {
    if (scale <= 0.002 || alpha <= 0.002) return;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(ang);
    ctx.scale(scale, scale);
    ctx.globalAlpha = alpha;
    const len = L.len, wid = L.wid * widK;
    leafPath(ctx, len, wid, L.shape, L.bend);
    ctx.fillStyle = L.c1;
    ctx.fill();
    // mitad iluminada (estilo ilustrado de la camiseta)
    ctx.beginPath();
    ctx.moveTo(0, 0);
    if (L.shape === 1) ctx.bezierCurveTo(len * 0.18, -wid * 1.1, len * 0.7, -wid * 1.05, len, L.bend * len * 0.12);
    else if (L.shape === 2) ctx.bezierCurveTo(len * 0.25, -wid * 0.9, len * 0.62, -wid * 0.95, len, L.bend * len * 0.12);
    else ctx.bezierCurveTo(len * 0.3, -wid * 0.85, len * 0.72, -wid * 0.6, len, L.bend * len * 0.12);
    ctx.quadraticCurveTo(len * 0.5, L.bend * len * 0.04, 0, 0);
    ctx.closePath();
    ctx.fillStyle = L.c2;
    ctx.fill();
    // nervio central
    ctx.beginPath();
    ctx.moveTo(len * 0.04, 0);
    ctx.quadraticCurveTo(len * 0.5, L.bend * len * 0.04, len * 0.92, L.bend * len * 0.11);
    ctx.lineWidth = Math.max(0.8, len * 0.018);
    ctx.strokeStyle = L.vein;
    ctx.stroke();
    if (light > 0.01) {
      // destello al nacer
      leafPath(ctx, len, wid, L.shape, L.bend);
      ctx.globalCompositeOperation = "lighter";
      ctx.globalAlpha = alpha * light;
      ctx.fillStyle = "#C4E64D";
      ctx.fill();
      ctx.globalCompositeOperation = "source-over";
    }
    ctx.restore();
  }

  // ============================================================
  function createForest(canvas, cfg) {
    const W = canvas.width, H = canvas.height;
    const ctx = canvas.getContext("2d");
    const C = cfg.color, T = cfg.time;
    const rnd = mulberry32(cfg.seed);
    const R = (a, b) => a + (b - a) * rnd();
    const pick = (arr) => arr[Math.floor(rnd() * arr.length)];
    const cx = W / 2, cy = H / 2;
    const U = Math.min(W, H) / 1080;          // unidad de escala
    const portrait = H > W;

    // capas desenfocadas (fondo y primer plano)
    const backC = document.createElement("canvas"); backC.width = W; backC.height = H;
    const frontC = document.createElement("canvas"); frontC.width = W; frontC.height = H;
    const bctx = backC.getContext("2d"), fctx = frontC.getContext("2d");

    // ---------- paletas de hoja ----------
    const prideKeys = ["red", "orange", "yellow", "green", "blue", "purple"];
    const greens = C.greens;
    function leafColors(base) {
      return {
        c1: base,
        c2: mix(base, "#FFFFFF", 0.16),
        vein: rgba("#071F1B", 0.28),
      };
    }

    // ---------- árbol ----------
    const branches = [];
    const leaves = [];
    let prideCounter = 0;

    function makeLeaf(opt) {
      let base, kind = "green", prideKey = null;
      if (opt.forcePride) {
        prideKey = prideKeys[prideCounter++ % 6];
        base = C.pride[prideKey]; kind = "pride";
      } else {
        const r = rnd();
        if (r < 0.035) { base = C.pink; kind = "accent"; }
        else if (r < 0.06) { base = C.blue; kind = "accent"; }
        else if (r < 0.09) { base = C.teal; kind = "accent"; }
        else base = greens[2 + Math.floor(rnd() * (greens.length - 2))];
      }
      const L = Object.assign(
        {
          len: opt.len, wid: opt.len * R(0.2, 0.32),
          shape: Math.floor(rnd() * 3), bend: R(-0.8, 0.8),
          kind, prideKey, phase: R(0, 6.28),
        },
        leafColors(base),
        opt
      );
      leaves.push(L);
      return L;
    }

    function addBranch(p0, ang, len, birth, dur, depth, width, curl) {
      const a1 = ang + curl * 0.35, a2 = ang + curl;
      const p3 = [p0[0] + Math.cos(ang + curl * 0.6) * len, p0[1] + Math.sin(ang + curl * 0.6) * len];
      const p1 = [p0[0] + Math.cos(a1) * len * 0.35, p0[1] + Math.sin(a1) * len * 0.35];
      const p2 = [p3[0] - Math.cos(a2) * len * 0.3, p3[1] - Math.sin(a2) * len * 0.3];
      const B = { p0, p1, p2, p3, birth, dur, depth, width };
      branches.push(B);
      // hojas a lo largo de la rama
      const nLeaves = depth === 0 ? 0 : Math.round(len / ((depth === 1 ? 52 : 44) * U));
      for (let i = 0; i < nLeaves; i++) {
        const s = 0.25 + (0.75 * (i + R(0.1, 0.9))) / nLeaves;
        const side = i % 2 === 0 ? 1 : -1;
        const pt = bez(p0, p1, p2, p3, s);
        const tan = bezTan(p0, p1, p2, p3, s);
        makeLeaf({
          x: pt[0], y: pt[1],
          ang: tan + side * R(0.6, 1.1),
          side,
          birth: birth + dur * s + R(0.02, 0.18),
          len: R(62, 112) * U * (depth === 1 ? 1.12 : 1),
          layer: "mid",
          forcePride: rnd() < 0.075,
        });
      }
      // hoja final en la punta
      if (depth > 0) {
        const tan = bezTan(p0, p1, p2, p3, 1);
        makeLeaf({ x: p3[0], y: p3[1], ang: tan + R(-0.2, 0.2), side: 1, birth: birth + dur + 0.05, len: R(80, 120) * U, layer: "mid" });
      }
      // ramificaciones
      if (depth < 3) {
        const nKids = depth === 0 ? 0 : depth === 1 ? 4 : 2;
        for (let k = 0; k < nKids; k++) {
          const s = 0.3 + (0.6 * (k + R(0.2, 0.8))) / nKids;
          const pt = bez(p0, p1, p2, p3, s);
          const tan = bezTan(p0, p1, p2, p3, s);
          const side = k % 2 === 0 ? 1 : -1;
          addBranch(pt, tan + side * R(0.45, 0.95), len * R(0.42, 0.62), birth + dur * s, dur * 0.8, depth + 1, width * 0.6, side * R(0.2, 0.6));
        }
      }
      return B;
    }

    // Tallo principal: de abajo al centro (escena 1) y sigue subiendo
    const stemTop = portrait ? H * 0.2 : H * 0.12;
    const stem = {
      p0: [cx + 10 * U, H + 30 * U],
      p1: [cx - 70 * U, H * 0.72],
      p2: [cx + 60 * U, H * 0.42],
      p3: [cx - 8 * U, stemTop],
      depth: 0, width: 4.2 * U,
    };
    branches.push(stem);
    // crecimiento del tallo: hasta el centro en 2s, y luego hasta arriba a los 4.6s
    function stemProgress(t) {
      // s=0.62 aprox. queda en el centro de la pantalla
      if (t < 0.25) return 0;
      if (t < 2.0) return 0.62 * easeInOutSine(prog(t, 0.25, 1.75));
      return 0.62 + 0.38 * easeOutCubic(prog(t, 2.0, 2.6));
    }
    const stemTime = (s) => (s <= 0.62 ? 0.25 + 1.75 * (s / 0.62) : 2.0 + 2.6 * ((s - 0.62) / 0.38) * 0.55);
    stem.custom = stemProgress;

    // ramas principales desde el tallo (alternas, hacia ambos lados)
    const mainCount = portrait ? 11 : 11;
    for (let i = 0; i < mainCount; i++) {
      const s = 0.22 + (0.76 * (i + 0.5)) / mainCount;
      const pt = bez(stem.p0, stem.p1, stem.p2, stem.p3, s);
      const tan = bezTan(stem.p0, stem.p1, stem.p2, stem.p3, s);
      const side = i % 2 === 0 ? -1 : 1;
      const reach = portrait ? W * R(0.42, 0.55) : W * R(0.3, 0.42);
      const birth = Math.max(T.sprout, stemTime(s)) + R(0, 0.15) + (s < 0.42 ? 0.35 : 0);
      addBranch(pt, tan + side * R(0.7, 1.2) + (s < 0.42 ? side * 0.25 : 0), reach, birth, R(1.3, 1.8), 1, 2.6 * U, -side * R(0.35, 0.75));
    }
    // dos tallos laterales que nacen desde abajo para llenar la pantalla
    for (const side of [-1, 1]) {
      const x0 = cx + side * W * (portrait ? 0.3 : 0.33);
      const p0 = [x0, H + 20 * U];
      addBranch(p0, -Math.PI / 2 + side * 0.25, H * (portrait ? 0.55 : 0.7), 2.4, 1.6, 1, 3 * U, side * 0.35);
    }
    // en horizontal, dos tallos bajos más para que la parte de abajo también se llene
    if (!portrait) {
      for (const side of [-1, 1]) {
        const p0 = [cx + side * W * 0.15, H + 20 * U];
        addBranch(p0, -Math.PI / 2 + side * 0.55, H * 0.5, 2.9, 1.5, 1, 2.6 * U, side * 0.5);
      }
    }
    // hojas directamente sobre el tallo (los primeros brotes, a partir de 2s)
    for (let i = 0; i < 9; i++) {
      const s = 0.3 + i * 0.075;
      const pt = bez(stem.p0, stem.p1, stem.p2, stem.p3, s);
      const tan = bezTan(stem.p0, stem.p1, stem.p2, stem.p3, s);
      const side = i % 2 === 0 ? 1 : -1;
      makeLeaf({ x: pt[0], y: pt[1], ang: tan + side * R(0.7, 1.0), side, birth: Math.max(T.sprout, stemTime(s)) + i * 0.06, len: R(85, 120) * U, layer: "mid", forcePride: i === 4 });
    }

    // ---------- capa de fondo: hojas pequeñas y oscuras que nacen en ola ----------
    const nBack = portrait ? 190 : 210;
    for (let i = 0; i < nBack; i++) {
      const x = R(-0.05, 1.05) * W, y = R(-0.05, 1.05) * H;
      const d = Math.hypot(x - cx, y - (cy + H * 0.1)) / Math.hypot(W, H);
      makeLeaf({
        x, y, ang: R(0, Math.PI * 2), side: rnd() < 0.5 ? 1 : -1,
        birth: 2.3 + d * 4.4 + R(0, 0.5),
        len: R(55, 105) * U, layer: "back",
        forcePride: rnd() < 0.04,
      });
    }
    // ---------- primer plano: hojas grandes y desenfocadas que entran por los bordes ----------
    const nFront = 16;
    for (let i = 0; i < nFront; i++) {
      const a = (i / nFront) * Math.PI * 2 + R(-0.15, 0.15);
      const rx = W * 0.56, ry = H * 0.56;
      const x = cx + Math.cos(a) * rx * R(0.9, 1.08);
      const y = cy + Math.sin(a) * ry * R(0.9, 1.08);
      makeLeaf({
        x, y, ang: a + Math.PI + R(-0.5, 0.5), side: 1,
        birth: R(3.0, 5.4), len: R(230, 330) * U, layer: "front",
        forcePride: i % 7 === 3,
      });
    }

    // ---------- formación (escena 3): anillos que evocan la estrella ----------
    const RING = 392 * U;
    const mids = leaves.filter((l) => l.layer === "mid");
    // ángulos de los colores de la estrella del club (rojo arriba, sentido horario)
    const sectorAng = { red: -Math.PI / 2, orange: -Math.PI / 6, yellow: Math.PI / 6, green: Math.PI / 2, blue: (5 * Math.PI) / 6, purple: (7 * Math.PI) / 6 };
    const prideLeaves = mids.filter((l) => l.kind === "pride");
    const greenLeaves = mids.filter((l) => l.kind !== "pride");
    const SWIRL = 0.9; // giro adicional durante la formación
    const polar = (l) => Math.atan2(l.y - cy, l.x - cx);

    // verdes -> 3 anillos tangenciales (corona de laurel)
    const ringSlots = [];
    const rings = [{ r: 0.78, n: 30 }, { r: 0.92, n: 36 }, { r: 1.06, n: 42 }];
    rings.forEach((rg, ri) => {
      for (let j = 0; j < rg.n; j++) ringSlots.push({ th: (j / rg.n) * Math.PI * 2 + ri * 0.07, r: RING * rg.r, ring: ri });
    });
    const formGreens = greenLeaves.slice().sort((a, b) => a.birth - b.birth).slice(0, ringSlots.length);
    // asignación por ángulo para que no se crucen
    formGreens.sort((a, b) => polar(a) - polar(b));
    const slotsSorted = ringSlots.slice().sort((a, b) => a.th - b.th);
    // repartir slots ordenados entre hojas ordenadas (si hay menos hojas, se salta)
    formGreens.forEach((l, i) => {
      const sl = slotsSorted[Math.floor((i * slotsSorted.length) / formGreens.length)];
      l.form = { th: sl.th, r: sl.r, ang: sl.th + Math.PI / 2 + (sl.ring - 1) * 0.25, scale: (0.85 + sl.ring * 0.12) * (84 * U) / l.len, delay: 0 };
    });
    // pride -> 6 abanicos en la posición de cada color de la estrella
    for (const key of prideKeys) {
      const grp = prideLeaves.filter((l) => l.prideKey === key).slice(0, 7);
      grp.sort((a, b) => polar(a) - polar(b));
      grp.forEach((l, j) => {
        const n = grp.length;
        const off = n > 1 ? (j / (n - 1) - 0.5) : 0;
        // se resta el giro para que, al asentarse la corona, el rojo quede arriba como en el logo
        const th = sectorAng[key] - SWIRL - 0.12 + off * 0.34;
        l.form = { th, r: RING * (1.2 + Math.abs(off) * -0.12 + (j % 2) * 0.05), ang: th + off * 0.9, scale: (100 * U) / l.len * (1 - Math.abs(off) * 0.3), delay: 0.1 };
      });
    }
    leaves.forEach((l, i) => {
      if (l.form) {
        l.form.delay += (i % 17) / 17 * 0.55;
        // giro coherente: destino siempre "por delante" en sentido antihorario visual
        const th0 = polar(l);
        let target = l.form.th + SWIRL;
        l.form.dTh = angDiff(th0, target);
        l.form.th0 = th0;
        l.form.r0 = Math.hypot(l.x - cx, l.y - cy);
      }
    });

    // ---------- polen ----------
    const pollen = [];
    for (let i = 0; i < 90; i++) {
      pollen.push({ x: R(0, W), y: R(0, H), sp: R(14, 42) * U, amp: R(6, 26) * U, f: R(0.4, 1.2), ph: R(0, 6.28), r: R(1.0, 3.2) * U, tw: R(0, 6.28) });
    }
    const sprite = document.createElement("canvas");
    sprite.width = sprite.height = 64;
    {
      const s = sprite.getContext("2d");
      const g = s.createRadialGradient(32, 32, 0, 32, 32, 32);
      g.addColorStop(0, "rgba(255,255,240,1)");
      g.addColorStop(0.18, rgba(C.pollen, 0.85));
      g.addColorStop(0.45, rgba(C.lime, 0.22));
      g.addColorStop(1, rgba(C.lime, 0));
      s.fillStyle = g;
      s.fillRect(0, 0, 64, 64);
    }

    // ---------- logo (estrella vectorizada) ----------
    const starPieces = [];
    (window.GMADRID_STAR || []).forEach((sh) => {
      sh.d.split("Z").map((s) => s.trim()).filter(Boolean).forEach((d, i) => {
        const nums = d.replace(/[ML]/g, " ").trim().split(/\s+/).map(Number);
        let sx = 0, sy = 0, n = 0;
        for (let k = 0; k < nums.length; k += 2) { sx += nums[k]; sy += nums[k + 1]; n++; }
        const pcx = sx / n - 0.5, pcy = sy / n - 0.5;
        starPieces.push({ path: new Path2D(d + "Z"), color: sh.color, cx: pcx, cy: pcy, a: Math.atan2(pcy, pcx), name: sh.name });
      });
    });
    // orden de aparición: en sentido horario desde arriba
    starPieces.forEach((p) => { p.order = ((p.a + Math.PI / 2 + Math.PI * 4) % (Math.PI * 2)) / (Math.PI * 2); });
    const LOGO_SIZE = (portrait ? 600 : 540) * U;
    const LOGO_Y = cy - (portrait ? 70 : 60) * U;

    // ============================================================
    // cámara global (empuje lento durante el crecimiento, zoom out final)
    function camera(t) {
      let s = 1 + 0.07 * easeInOutSine(prog(t, 0, 6.2));
      s = lerp(s, 1, easeInOutCubic(prog(t, 6.0, 2.2)));
      s *= 1 - 0.06 * easeInOutSine(prog(t, T.zoomOut, T.total - T.zoomOut));
      return s;
    }

    function drawBackground(t) {
      ctx.globalCompositeOperation = "source-over";
      ctx.globalAlpha = 1;
      ctx.fillStyle = C.bgDeep;
      ctx.fillRect(0, 0, W, H);
      // casi negro al principio
      const k = 0.18 + 0.82 * easeInOutSine(prog(t, 0.4, 3.2));
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.hypot(W, H) * 0.55);
      g.addColorStop(0, rgba(C.bgCenter, k));
      g.addColorStop(0.55, rgba(C.bgCenter, k * 0.35));
      g.addColorStop(1, rgba(C.bgCenter, 0));
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
      // oscurecer al principio
      const dark = 0.55 * (1 - easeInOutSine(prog(t, 0, 2.6)));
      if (dark > 0) { ctx.fillStyle = `rgba(2,10,8,${dark})`; ctx.fillRect(0, 0, W, H); }
    }

    function strokeBranch(c, B, g, t, glow) {
      const N = 30;
      const steps = Math.max(2, Math.ceil(N * g));
      c.beginPath();
      for (let i = 0; i <= steps; i++) {
        const s = (g * i) / steps;
        const p = bez(B.p0, B.p1, B.p2, B.p3, s);
        if (i === 0) c.moveTo(p[0], p[1]); else c.lineTo(p[0], p[1]);
      }
      c.lineCap = "round";
      c.lineJoin = "round";
      // de luz lima a verde rama a medida que madura
      const age = B.depth === 0 ? prog(t, 3.0, 2.5) : prog(t, B.birth + B.dur, 1.6);
      c.strokeStyle = mix(C.lime, C.branch, age * 0.75);
      c.lineWidth = B.width * (B.depth === 0 ? 1 : 1.25);
      c.shadowColor = C.lime;
      c.shadowBlur = glow * (1 - age * 0.7) * 22 * U;
      c.stroke();
      c.shadowBlur = 0;
      // punta luminosa mientras crece
      if (g > 0 && g < 1) {
        const p = bez(B.p0, B.p1, B.p2, B.p3, g);
        const rr = (B.depth === 0 ? 46 : 22) * U;
        c.globalCompositeOperation = "lighter";
        c.globalAlpha = B.depth === 0 ? 0.95 : 0.6;
        c.drawImage(sprite, p[0] - rr, p[1] - rr, rr * 2, rr * 2);
        c.globalAlpha = 1;
        c.globalCompositeOperation = "source-over";
      }
    }

    // posición/estado de una hoja en el tiempo t
    function leafState(L, t) {
      const k = (t - L.birth) / 0.75;
      if (k <= 0) return null;
      let sc = spring(k, 5.0, 9.5);
      const unfold = easeOutCubic(clamp(k * 1.25));
      let ang = L.ang - L.side * 1.0 * (1 - easeOutCubic(clamp(k)));
      // brisa muy leve
      ang += Math.sin(t * 1.1 + L.phase) * 0.035;
      let x = L.x, y = L.y, alpha = 1, scale = sc, light = Math.max(0, 1 - k * 1.6) * 0.55;

      if (L.layer === "mid") {
        if (L.form) {
          // escena 3: giran hacia el centro
          const f = L.form;
          const m = easeInOutCubic(prog(t, T.gather + f.delay, 1.7));
          const th = f.th0 + f.dTh * m + 0.06 * Math.max(0, t - (T.gather + 2.2)); // rotación lenta continua
          let r = lerp(f.r0, f.r, m);
          // respiración en cada palabra
          for (const wt of T.words) {
            const q = t - wt;
            if (q > 0) r *= 1 + 0.045 * Math.exp(-5 * q) * Math.sin(q * 14) ;
          }
          // escena 5: se abren hacia fuera
          const o = prog(t, T.open + (f.delay * 0.12), 0.85);
          const oe = o * o;
          r += oe * Math.hypot(W, H) * 0.75;
          x = cx + Math.cos(th) * r;
          y = cy + Math.sin(th) * r;
          const fAng = f.ang + (th - (f.th0 + f.dTh));
          ang = lerp(ang, ang + angDiff(ang, fAng + SWIRL * 0), m) + oe * 1.6;
          scale = sc * lerp(1, f.scale, m) * (1 + oe * 1.4);
          alpha = 1 - easeInCubic(prog(t, T.open + 0.2, 0.6));
        } else {
          // las que no forman la corona se apartan hacia fuera y se apagan
          const m = easeInOutCubic(prog(t, T.gather, 1.4));
          const dx = L.x - cx, dy = L.y - cy, dd = Math.hypot(dx, dy) || 1;
          x += (dx / dd) * m * 260 * U;
          y += (dy / dd) * m * 260 * U;
          alpha = 1 - m;
          ang += m * 0.8 * L.side;
        }
      } else if (L.layer === "back") {
        const dim = lerp(1, 0.45, easeInOutCubic(prog(t, T.gather, 1.5)));
        const out = prog(t, T.open, 0.8);
        alpha = dim * (1 - out);
        const dx = L.x - cx, dy = L.y - cy;
        x += dx * 0.25 * easeInCubic(out);
        y += dy * 0.25 * easeInCubic(out);
      } else if (L.layer === "front") {
        // entran desde fuera, y en la escena 3 salen de plano
        const enter = easeOutCubic(clamp(k));
        const dx = L.x - cx, dy = L.y - cy;
        const ex = 1 + 0.35 * (1 - enter);
        const leave = easeInCubic(prog(t, T.gather - 0.2, 1.3));
        x = cx + dx * (ex + leave * 0.9);
        y = cy + dy * (ex + leave * 0.9);
        scale = sc * (1 + leave * 0.6);
        alpha = 1 - leave;
      }
      return { x, y, ang, scale, unfold, alpha, light };
    }

    function drawPollen(t) {
      const a = 0.85 * easeInOutSine(prog(t, 2.2, 1.8)) * (1 - 0.5 * prog(t, T.open, 1.2));
      if (a <= 0) return;
      ctx.globalCompositeOperation = "lighter";
      for (const p of pollen) {
        let y = (p.y - p.sp * t) % (H + 40 * U);
        if (y < -20 * U) y += H + 40 * U;
        const x = p.x + Math.sin(t * p.f + p.ph) * p.amp;
        const tw = 0.55 + 0.45 * Math.sin(t * 2.3 + p.tw);
        ctx.globalAlpha = a * tw;
        const rr = p.r * 6;
        ctx.drawImage(sprite, x - rr, y - rr, rr * 2, rr * 2);
      }
      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = "source-over";
    }

    function drawLogo(t) {
      const k0 = T.open + 0.12;
      if (t < k0) return;
      ctx.save();
      ctx.translate(cx, LOGO_Y);
      for (const p of starPieces) {
        const k = (t - k0 - p.order * 0.45 - (p.name === "grey" ? 0.12 : 0)) / 1.15;
        if (k <= 0) continue;
        const e = spring(k, 5.5, 8.5);
        const s = LOGO_SIZE;
        // cada pieza brota desde el centro hacia su sitio
        const px = p.cx * s * e, py = p.cy * s * e;
        ctx.save();
        ctx.translate(px, py);
        ctx.rotate((1 - easeOutExpo(clamp(k))) * -0.6);
        const sc = 0.35 + 0.65 * e;
        ctx.scale(sc, sc);
        ctx.translate(-p.cx * s, -p.cy * s);
        ctx.scale(s, s);
        ctx.translate(-0.5, -0.5);
        ctx.globalAlpha = clamp(k * 3);
        ctx.fillStyle = p.color;
        ctx.fill(p.path);
        ctx.restore();
      }
      ctx.restore();
    }

    function drawBloom(t) {
      // destello de luz al abrirse
      const k = prog(t, T.open - 0.1, 1.4);
      if (k <= 0 || k >= 1) return;
      const a = Math.sin(Math.PI * Math.pow(k, 0.5)) * 0.55;
      const g = ctx.createRadialGradient(cx, LOGO_Y, 0, cx, LOGO_Y, 520 * U * (0.6 + k));
      g.addColorStop(0, `rgba(255,255,235,${a})`);
      g.addColorStop(0.25, rgba(C.lime, a * 0.45));
      g.addColorStop(1, rgba(C.lime, 0));
      ctx.globalCompositeOperation = "lighter";
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = "source-over";
    }

    function drawScrim(t) {
      // velo oscuro en el centro para que se lean los textos
      const a = 0.72 * easeInOutSine(prog(t, T.title - 0.4, 0.9)) * (1 - easeInOutSine(prog(t, T.open - 0.2, 0.6)));
      if (a <= 0) return;
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, RING * 1.25);
      g.addColorStop(0, rgba(C.bgDeep, a));
      g.addColorStop(0.6, rgba(C.bgDeep, a * 0.75));
      g.addColorStop(1, rgba(C.bgDeep, 0));
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
    }

    function drawSeedGlow(t) {
      // la semilla: un pulso de luz en la base antes de que nazca el tallo
      const a = 0.9 * Math.sin(Math.PI * clamp(t / 2.4)) * (t < 2.4 ? 1 : 0);
      if (a <= 0) return;
      const g = ctx.createRadialGradient(cx, H, 0, cx, H, 420 * U);
      g.addColorStop(0, rgba(C.lime, 0.35 * a));
      g.addColorStop(1, rgba(C.lime, 0));
      ctx.globalCompositeOperation = "lighter";
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
      ctx.globalCompositeOperation = "source-over";
    }

    function render(t) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      drawBackground(t);
      const cam = camera(t);
      const camT = (c, f = 1) => {
        const s = 1 + (cam - 1) * f;
        c.setTransform(s, 0, 0, s, cx - cx * s, cy - cy * s);
      };

      // ---- capa de fondo (desenfocada) ----
      bctx.setTransform(1, 0, 0, 1, 0, 0);
      bctx.clearRect(0, 0, W, H);
      camT(bctx, 0.6);
      for (const L of leaves) {
        if (L.layer !== "back") continue;
        const s = leafState(L, t);
        if (!s) continue;
        drawLeaf(bctx, L, s.x, s.y, s.ang, s.scale, s.unfold, s.alpha * 0.8, s.light * 0.5);
      }
      ctx.save();
      ctx.filter = `blur(${3 * U}px) brightness(0.62) saturate(0.85)`;
      ctx.drawImage(backC, 0, 0);
      ctx.restore();

      drawSeedGlow(t);

      // ---- capa media: ramas y hojas nítidas ----
      camT(ctx, 1);
      const branchFade = 1 - easeInOutCubic(prog(t, T.gather, 1.2));
      if (branchFade > 0) {
        ctx.globalAlpha = branchFade;
        for (const B of branches) {
          const g = B.depth === 0 ? stemProgress(t) : easeOutCubic(prog(t, B.birth, B.dur));
          if (g <= 0) continue;
          ctx.globalAlpha = branchFade;
          strokeBranch(ctx, B, g, t, 1);
        }
        ctx.globalAlpha = 1;
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      drawScrim(t);
      camT(ctx, 1);
      for (const L of leaves) {
        if (L.layer !== "mid") continue;
        const s = leafState(L, t);
        if (!s) continue;
        drawLeaf(ctx, L, s.x, s.y, s.ang, s.scale, s.unfold, s.alpha, s.light);
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      drawPollen(t);
      drawBloom(t);
      camT(ctx, 1);
      drawLogo(t);
      ctx.setTransform(1, 0, 0, 1, 0, 0);

      // ---- primer plano (grande y desenfocado) ----
      fctx.setTransform(1, 0, 0, 1, 0, 0);
      fctx.clearRect(0, 0, W, H);
      camT(fctx, 1.6);
      let anyFront = false;
      for (const L of leaves) {
        if (L.layer !== "front") continue;
        const s = leafState(L, t);
        if (!s || s.alpha <= 0) continue;
        anyFront = true;
        drawLeaf(fctx, L, s.x, s.y, s.ang, s.scale, s.unfold, s.alpha * 0.92, 0);
      }
      if (anyFront) {
        ctx.save();
        ctx.filter = `blur(${12 * U}px)`;
        ctx.drawImage(frontC, 0, 0);
        ctx.restore();
      }
      // viñeta
      const v = ctx.createRadialGradient(cx, cy, Math.min(W, H) * 0.35, cx, cy, Math.hypot(W, H) * 0.6);
      v.addColorStop(0, "rgba(0,0,0,0)");
      v.addColorStop(1, "rgba(2,10,8,0.55)");
      ctx.fillStyle = v;
      ctx.fillRect(0, 0, W, H);
      return cam;
    }

    return { render, camera, LOGO_Y, LOGO_SIZE, RING };
  }

  window.createForest = createForest;
})();
