/* Modo pabellón para la pizarra G·Madrid: parqué, grada con público que aplaude,
 * panel LED, figuras con volumen y cámara que entra volando y orbita suave.
 * Todo determinista (PRNG con semilla fija) y dentro de la línea de tiempo GSAP.
 */
(function () {
  let seed = 20260722;
  const rnd = () => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  };
  const BRAND = ["#9B3FA6", "#2FA8E0", "#E0303A", "#F2A21B", "#F2DD2A", "#8CC63F"];
  const NEUTRAL = ["#e9edf5", "#1d2b52", "#3b4a6b", "#c7ced9", "#20345f", "#5b6782"];

  // ---------- pista de parqué ----------
  function court(plane, h) {
    const { svgEl, el, OY } = h;
    const H = 800 + OY;
    // suelo del pabellón alrededor de la pista
    const floor = el("div", "arena-floor", plane);
    floor.style.cssText = "position:absolute;left:-520px;top:-260px;width:2040px;height:1500px;";
    const svg = svgEl("svg", { class: "court", width: 1000, height: H, viewBox: `0 0 1000 ${H}` }, plane);
    const defs = svgEl("defs", {}, svg);
    const shine = svgEl("radialGradient", { id: "shine", cx: "50%", cy: "35%", r: "70%" }, defs);
    svgEl("stop", { offset: "0", "stop-color": "rgba(255,255,255,0.22)" }, shine);
    svgEl("stop", { offset: "1", "stop-color": "rgba(255,255,255,0)" }, shine);
    const area = svgEl("linearGradient", { id: "area3d", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    svgEl("stop", { offset: "0", "stop-color": "#2e66c4" }, area);
    svgEl("stop", { offset: "1", "stop-color": "#1f4fa3" }, area);
    // tablas de parqué con tonos variados
    svgEl("rect", { x: 0, y: 0, width: 1000, height: H, fill: "#c88a4c" }, svg);
    const tones = ["#c98b4d", "#c4843f", "#cf9558", "#bf7f3c", "#d39b5f", "#c78846"];
    for (let x = 0; x < 1000; x += 22) {
      let y = -rnd() * 160;
      while (y < H) {
        const len = 120 + rnd() * 140;
        svgEl("rect", {
          x, y, width: 22, height: len, fill: tones[Math.floor(rnd() * tones.length)],
          stroke: "rgba(70,35,10,0.25)", "stroke-width": 1,
        }, svg);
        y += len;
      }
    }
    svgEl("rect", { x: 0, y: 0, width: 1000, height: H, fill: "url(#shine)" }, svg);
    const y0 = OY;
    const D = (r) =>
      `M ${425 - r} ${y0} A ${r} ${r} 0 0 0 425 ${y0 + r} L 575 ${y0 + r} A ${r} ${r} 0 0 0 ${575 + r} ${y0}`;
    svgEl("path", { d: D(300) + " Z", fill: "url(#area3d)" }, svg);
    svgEl("path", { d: D(300), fill: "none", stroke: "#fff", "stroke-width": 6 }, svg);
    svgEl("path", { d: D(450), fill: "none", stroke: "#fff", "stroke-width": 5, "stroke-dasharray": "22 16" }, svg);
    svgEl("line", { x1: 485, y1: y0 + 350, x2: 515, y2: y0 + 350, stroke: "#fff", "stroke-width": 6 }, svg);
    svgEl("line", { x1: 0, y1: y0, x2: 1000, y2: y0, stroke: "#fff", "stroke-width": 6 }, svg);
    svgEl("rect", { x: 3, y: 3, width: 994, height: H - 6, fill: "none", stroke: "#fff", "stroke-width": 6 }, svg);
    // logo del club pintado en el parqué (zona libre, fuera del área)
    const img = svgEl("image", { href: "assets/gmadrid-logo.png", x: 425, y: y0 + 610, width: 150, height: 159, opacity: 0.22 }, svg);
    img.setAttribute("preserveAspectRatio", "xMidYMid meet");
    return svg;
  }

  // ---------- figuras con volumen ----------
  let gid = 0;
  function figureSVG(color, isDef, label) {
    const id = "f" + gid++;
    const base = isDef ? "#4a5470" : color;
    const tag = label
      ? `<rect x="2" y="2" width="66" height="38" rx="19" fill="${color}" stroke="#ffffff" stroke-width="3"/>
         <text x="35" y="29" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="22" fill="#0b1533">${label}</text>`
      : "";
    return `<svg viewBox="-5 -50 70 154" width="70" height="154">
      <defs>
        <linearGradient id="${id}b" x1="0" x2="1" y1="0" y2="0">
          <stop offset="0" stop-color="#ffffff" stop-opacity="0.45"/>
          <stop offset="0.35" stop-color="#ffffff" stop-opacity="0.05"/>
          <stop offset="1" stop-color="#000000" stop-opacity="0.35"/>
        </linearGradient>
        <radialGradient id="${id}h" cx="0.35" cy="0.3" r="0.8">
          <stop offset="0" stop-color="#ffe2c8"/><stop offset="1" stop-color="#b9805a"/>
        </radialGradient>
      </defs>
      <g transform="translate(-5 -42)">${tag}</g>
      <path d="M19 72 L17 100 M41 72 L43 100" stroke="${isDef ? "#2b3147" : "#1b2342"}" stroke-width="10" stroke-linecap="round"/>
      ${isDef
        ? `<path d="M15 40 L4 14 M45 40 L56 14" stroke="${base}" stroke-width="8" stroke-linecap="round"/>`
        : `<path d="M15 40 L8 66 M45 40 L52 66" stroke="${base}" stroke-width="8" stroke-linecap="round"/>`}
      <path d="M13 36 Q30 27 47 36 L45 74 Q30 79 15 74 Z" fill="${base}"/>
      <path d="M13 36 Q30 27 47 36 L45 74 Q30 79 15 74 Z" fill="url(#${id}b)"/>
      <circle cx="30" cy="16" r="12.5" fill="url(#${id}h)"/>
      <path d="M17.5 13 Q30 -1 42.5 13 Q36 7 30 7.5 Q24 7 17.5 13 Z" fill="#2a1d16"/>
    </svg>`;
  }

  // ---------- grada, público y panel LED ----------
  function setup(E, h) {
    const { el, OY } = h;
    const orbit = E.plane;
    // LED justo detrás de la portería
    const ledWrap = el("div", "bb led-bb", orbit);
    ledWrap.style.left = "-300px";
    ledWrap.style.top = OY - 34 + "px";
    const led = el("div", "led", ledWrap);
    const strip = el("div", "led-strip", led);
    let html = "";
    for (let i = 0; i < 14; i++)
      html += `<span><b style="color:${BRAND[i % 6]}">●</b> G·MADRID BALONMANO</span>`;
    strip.innerHTML = html;
    E.led = strip;

    // grada inclinada detrás del fondo
    const standWrap = el("div", "stand-wrap", orbit);
    const stand = el("div", "stand", standWrap);
    const ROWS = 4;
    const COLS = 40;
    E.fans = [];
    for (let r = 0; r < ROWS; r++) {
      const row = el("div", "stand-row", stand);
      row.style.top = (ROWS - 1 - r) * 60 + "px";
      for (let c = 0; c < COLS; c++) {
        if (rnd() < 0.08) continue; // algún asiento libre
        const f = el("div", "fan", row);
        f.style.left = c * 42 + (r % 2) * 21 + Math.round(rnd() * 6) + "px";
        const shirt = rnd() < 0.45 ? BRAND[Math.floor(rnd() * 6)] : NEUTRAL[Math.floor(rnd() * NEUTRAL.length)];
        const skin = ["#f1c7a5", "#d9a37c", "#a8714d", "#7c4f33"][Math.floor(rnd() * 4)];
        const hair = ["#2a1d16", "#5a3a22", "#111", "#c79a5a", "#8a8a8a"][Math.floor(rnd() * 5)];
        f.innerHTML = `<i class="torso" style="background:${shirt}"></i><i class="head" style="background:${skin};box-shadow: inset 0 5px 0 ${hair}"></i>`;
        const hl = el("i", "hand l", f);
        const hr = el("i", "hand r", f);
        hl.style.background = hr.style.background = skin;
        E.fans.push({ f, hl, hr, g: Math.floor(rnd() * 3) });
      }
    }
  }

  // ---------- cámara, aplausos, LED ----------
  function animate(E, M, h) {
    const tl = E.tl;
    const yaws = h.YAWS;
    const end = M.end;
    const orbit = E.plane;

    // cámara: entra volando y luego orbita muy suave (las figuras se compensan para seguir de pie)
    const ang = (v) => [{ el: orbit, v }, { el: yaws, v: -v }];
    const orbitTo = (from, to, t0, dur, ease) => {
      for (const { el, v } of ang(1)) {
        tl.fromTo(el, { rotationZ: from * v }, { rotationZ: to * v, duration: dur, ease, immediateRender: false }, t0);
      }
    };
    tl.set(orbit, { rotationZ: -34 }, 0);
    tl.set(yaws, { rotationZ: 34 }, 0);
    orbitTo(-34, 0, 2.85, 1.9, "power3.out");
    tl.fromTo("#cam", { scale: 0.62, y: 160 }, { scale: 1, y: 0, duration: 1.9, ease: "power3.out" }, 2.85);
    orbitTo(0, 5, 4.75, M.mirror - 4.75, "sine.inOut");
    orbitTo(5, -5, M.mirror, M.outro - M.mirror, "sine.inOut");

    // focos: aparecen con la pista y se apagan en el cierre
    tl.fromTo("#lights", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.9 }, 2.9);
    tl.to("#lights", { autoAlpha: 0, duration: 0.5 }, M.outro);

    // panel LED: el texto corre todo el vídeo
    tl.fromTo(E.led, { x: 0 }, { x: -1500, duration: end, ease: "none" }, 0);

    // aplausos: tres grupos desfasados para que no parezca un metrónomo
    const groups = [0, 1, 2].map((g) => E.fans.filter((f) => f.g === g));
    const period = 0.3;
    groups.forEach((gr, i) => {
      const t0 = 0.05 + i * 0.1;
      const reps = Math.max(0, Math.floor((end - t0) / period) - 1);
      tl.fromTo(gr.map((f) => f.hl), { x: 0 }, { x: 6, duration: period / 2, ease: "power1.in", yoyo: true, repeat: reps * 2 + 1 }, t0);
      tl.fromTo(gr.map((f) => f.hr), { x: 0 }, { x: -6, duration: period / 2, ease: "power1.in", yoyo: true, repeat: reps * 2 + 1 }, t0);
    });
    // momentos de ovación: el público se levanta
    const cheer = (t0, dur) => {
      groups.forEach((gr, i) => {
        const reps = Math.max(1, Math.floor(dur / 0.5) * 2 - 1);
        tl.fromTo(gr.map((f) => f.f), { y: 0 }, { y: -10, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: reps, immediateRender: false }, t0 + i * 0.08);
      });
    };
    cheer(0.1, 3.2);
    cheer(M.decision + 0.6, 2.5);
    cheer(M.key, 2.0);
    cheer(M.outro, end - M.outro - 0.3);
  }

  window.PizarraArena = { court, figureSVG, setup, animate };
})();
