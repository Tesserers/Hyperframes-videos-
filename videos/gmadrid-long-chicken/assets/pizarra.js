/* Pizarra G·Madrid — motor de jugadas de balonmano para HyperFrames.
 * Todo se calcula de forma analítica (posición = f(tiempo)) y se vuelca a la
 * línea de tiempo GSAP como keyframes muestreados: determinista y seekable.
 * Coordenadas de pista: x 0..1000 (ancho, 20 m), y 0..800 (distancia a la
 * línea de gol). 50 px = 1 m. La portería está en (500, 0).
 */
(function () {
  const TILT = 50; // grados de inclinación de la pista
  const OY = 90; // margen del plano por detrás de la línea de gol
  const FPS = 25; // muestras por segundo para los keyframes
  const NS = "http://www.w3.org/2000/svg";

  const ROLES = {
    EI: { name: "Extremo izq.", color: "#9B3FA6" },
    LI: { name: "Lateral izq.", color: "#2FA8E0" },
    CE: { name: "Central", color: "#E0303A" },
    LD: { name: "Lateral der.", color: "#F2A21B" },
    ED: { name: "Extremo der.", color: "#F2DD2A" },
    PI: { name: "Pivote", color: "#8CC63F" },
  };
  const MIRROR_ID = { LI: "LD", LD: "LI", EI: "ED", ED: "EI" };
  const START = {
    EI: [55, 95],
    LI: [215, 505],
    CE: [500, 575],
    LD: [785, 505],
    ED: [945, 95],
    PI: [500, 300],
  };
  const DEF = {
    D1: [118, 250],
    D2: [252, 332],
    D3: [418, 352],
    D4: [582, 352],
    D5: [748, 332],
    D6: [882, 250],
  };
  const HAND = [18, 0];

  const el = (tag, cls, parent, html) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    if (parent) parent.appendChild(n);
    return n;
  };
  const svgEl = (tag, attrs, parent) => {
    const n = document.createElementNS(NS, tag);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };
  const lerp = (a, b, u) => a + (b - a) * u;
  const PX = (x) => x;
  const PY = (y) => y + OY;

  // ---------- curvas ----------
  function catmull(pts) {
    // devuelve una función f(u) u∈[0,1] sobre la spline de Catmull-Rom
    if (pts.length === 2) return (u) => [lerp(pts[0][0], pts[1][0], u), lerp(pts[0][1], pts[1][1], u)];
    const P = [pts[0], ...pts, pts[pts.length - 1]];
    const n = pts.length - 1;
    return (u) => {
      const s = Math.min(n - 1e-9, Math.max(0, u * n));
      const i = Math.floor(s);
      const t = s - i;
      const p0 = P[i], p1 = P[i + 1], p2 = P[i + 2], p3 = P[i + 3];
      const f = (a, b, c, d) =>
        0.5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t * t * t);
      return [f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1])];
    };
  }
  function resample(pts, n) {
    // muestras equiespaciadas por longitud de arco
    const f = catmull(pts);
    const dense = [];
    const D = 300;
    for (let i = 0; i <= D; i++) dense.push(f(i / D));
    const cum = [0];
    for (let i = 1; i < dense.length; i++)
      cum.push(cum[i - 1] + Math.hypot(dense[i][0] - dense[i - 1][0], dense[i][1] - dense[i - 1][1]));
    const L = cum[cum.length - 1] || 1;
    const out = [];
    let j = 0;
    for (let k = 0; k <= n; k++) {
      const target = (k / n) * L;
      while (j < cum.length - 2 && cum[j + 1] < target) j++;
      const seg = cum[j + 1] - cum[j] || 1;
      const u = (target - cum[j]) / seg;
      out.push([lerp(dense[j][0], dense[j + 1][0], u), lerp(dense[j][1], dense[j + 1][1], u)]);
    }
    return { pts: out, len: L };
  }
  function samplePoly(s, p) {
    const n = s.length - 1;
    const x = Math.min(n, Math.max(0, p * n));
    const i = Math.min(n - 1, Math.floor(x));
    const u = x - i;
    return [lerp(s[i][0], s[i + 1][0], u), lerp(s[i][1], s[i + 1][1], u)];
  }
  function pathD(s) {
    return s.map((p, i) => (i ? "L" : "M") + PX(p[0]).toFixed(1) + " " + PY(p[1]).toFixed(1)).join(" ");
  }

  // ---------- escena estática ----------
  function buildCourt(plane) {
    const svg = svgEl("svg", { class: "court", width: 1000, height: 800 + OY, viewBox: `0 0 1000 ${800 + OY}` }, plane);
    const defs = svgEl("defs", {}, svg);
    const g = svgEl("linearGradient", { id: "floorG", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    svgEl("stop", { offset: "0", "stop-color": "#1a2c5c" }, g);
    svgEl("stop", { offset: "1", "stop-color": "#22396f" }, g);
    const g2 = svgEl("linearGradient", { id: "areaG", x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    svgEl("stop", { offset: "0", "stop-color": "#2f6fc0" }, g2);
    svgEl("stop", { offset: "1", "stop-color": "#2a5ea8" }, g2);
    svgEl("rect", { x: 0, y: 0, width: 1000, height: 800 + OY, fill: "url(#floorG)" }, svg);
    // tablas del parqué
    for (let x = 0; x <= 1000; x += 50)
      svgEl("line", { x1: x, y1: 0, x2: x, y2: 800 + OY, stroke: "rgba(255,255,255,0.035)", "stroke-width": 2 }, svg);
    const y0 = PY(0);
    const D = (r) =>
      `M ${425 - r} ${y0} A ${r} ${r} 0 0 0 425 ${y0 + r} L 575 ${y0 + r} A ${r} ${r} 0 0 0 ${575 + r} ${y0}`;
    svgEl("path", { d: D(300) + " Z", fill: "url(#areaG)" }, svg);
    svgEl("path", { d: D(300), fill: "none", stroke: "#fff", "stroke-width": 5 }, svg);
    svgEl("path", { d: D(450), fill: "none", stroke: "rgba(255,255,255,0.75)", "stroke-width": 4, "stroke-dasharray": "22 16" }, svg);
    svgEl("line", { x1: 485, y1: y0 + 350, x2: 515, y2: y0 + 350, stroke: "#fff", "stroke-width": 5 }, svg); // 7 m
    svgEl("line", { x1: 0, y1: y0, x2: 1000, y2: y0, stroke: "#fff", "stroke-width": 5 }, svg);
    svgEl("rect", { x: 3, y: 3, width: 994, height: 800 + OY - 6, fill: "none", stroke: "rgba(255,255,255,0.9)", "stroke-width": 5 }, svg);
    // zona detrás de la portería
    svgEl("rect", { x: 0, y: 0, width: 1000, height: y0, fill: "rgba(8,14,34,0.55)" }, svg);
    return svg;
  }

  function billboard(plane, x, y, cls) {
    const wrap = el("div", "bb " + (cls || ""), plane);
    wrap.style.left = PX(x) + "px";
    wrap.style.top = PY(y) + "px";
    const fig = el("div", "bb-up", wrap);
    return { wrap, fig };
  }

  function figureSVG(color, isDef, label) {
    const body = isDef ? "#8a93a6" : color;
    const stroke = isDef ? "rgba(255,255,255,0.35)" : "#ffffff";
    const tag = label
      ? `<rect x="2" y="2" width="66" height="38" rx="19" fill="${color}" stroke="#ffffff" stroke-width="3"/>
         <text x="35" y="29" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="22" fill="#0b1533">${label}</text>`
      : "";
    return `<svg viewBox="-5 -50 70 154" width="70" height="154">
      <g transform="translate(-5 -42)">${tag}</g>
      <circle cx="30" cy="16" r="12" fill="${body}" stroke="${stroke}" stroke-width="3"/>
      <path d="M14 36 Q30 28 46 36 L44 72 Q30 76 16 72 Z" fill="${body}" stroke="${stroke}" stroke-width="3" stroke-linejoin="round"/>
      <path d="M19 72 L17 100 M41 72 L43 100" stroke="${body}" stroke-width="9" stroke-linecap="round"/>
      ${isDef ? `<path d="M15 40 L4 14 M45 40 L56 14" stroke="${body}" stroke-width="7" stroke-linecap="round"/>` : `<path d="M15 40 L8 66 M45 40 L52 66" stroke="${body}" stroke-width="7" stroke-linecap="round"/>`}
    </svg>`;
  }

  // ---------- motor ----------
  function Engine(root) {
    this.root = root;
    this.plane = root.querySelector("#plane");
    this.capBox = root.querySelector("#caps");
    this.tl = gsap.timeline({ paused: true });
    this.moves = {}; // id -> [{t0,dur,s,ease}]
    this.base = {};
    this.ents = {};
    this.arrowSvg = null;
    this.maskN = 0;
  }

  Engine.prototype.setup = function () {
    buildCourt(this.plane);
    // portería
    const goal = billboard(this.plane, 500, 0, "goal");
    goal.fig.innerHTML = `<svg viewBox="0 0 170 110" width="170" height="110">
      <defs><pattern id="net" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M0 0 L10 10 M10 0 L0 10" stroke="rgba(255,255,255,0.28)" stroke-width="1"/></pattern></defs>
      <rect x="10" y="8" width="150" height="100" fill="url(#net)"/>
      <path d="M10 108 L10 8 L160 8 L160 108" fill="none" stroke="#ffffff" stroke-width="9"/>
      <path d="M10 108 L10 8 L160 8 L160 108" fill="none" stroke="#E0303A" stroke-width="9" stroke-dasharray="14 14"/>
    </svg>`;
    this.goalFlash = el("div", "goal-flash", goal.fig);
    // capa de flechas en el suelo
    this.arrowSvg = svgEl("svg", { class: "arrows", width: 1000, height: 800 + OY, viewBox: `0 0 1000 ${800 + OY}` }, this.plane);
    this.arrowDefs = svgEl("defs", {}, this.arrowSvg);
    // defensores
    for (const id in DEF) this.makeEnt(id, DEF[id], null, true);
    for (const id in START) this.makeEnt(id, START[id], ROLES[id], false);
    // balón
    const b = el("div", "ent ball-ent", this.plane);
    const shadow = el("div", "shadow ball-shadow", b);
    const up = el("div", "bb-up", b);
    const lift = el("div", "lift", up);
    const ballDot = el("div", "ball", lift);
    this.ball = { node: b, lift, shadow, fade: [ballDot, shadow] };
  };

  Engine.prototype.makeEnt = function (id, pos, role, isDef) {
    const n = el("div", "ent " + (isDef ? "def" : "att"), this.plane);
    n.id = "e-" + id;
    el("div", "shadow", n);
    const up = el("div", "bb-up", n);
    const pop = el("div", "pop", up);
    pop.innerHTML = figureSVG(role ? role.color : null, isDef, role ? id : null);
    this.ents[id] = { node: n, pop, isDef };
    this.base[id] = pos.slice();
  };

  // posición analítica de una entidad en el tiempo t
  Engine.prototype.posAt = function (id, t) {
    const ms = this.moves[id] || [];
    let p = this.runStart[id] || this.base[id];
    for (const m of ms) {
      if (m.t0 > t) break;
      if (t >= m.t0 + m.dur) p = m.s[m.s.length - 1];
      else {
        const u = m.ease((t - m.t0) / m.dur);
        p = samplePoly(m.s, u);
      }
    }
    return p;
  };

  Engine.prototype.addMove = function (id, t0, dur, pts, ease) {
    const from = this.posAt(id, t0);
    const all = [from, ...pts];
    const { pts: s } = resample(all, 40);
    (this.moves[id] = this.moves[id] || []).push({ t0, dur, s, ease: gsap.parseEase(ease || "power1.inOut") });
    this.moves[id].sort((a, b) => a.t0 - b.t0);
    return s;
  };

  // ---------- flechas ----------
  Engine.prototype.drawPath = function (s, t0, dur, color, opts) {
    opts = opts || {};
    const tl = this.tl;
    const g = svgEl("g", { class: "arrow" }, this.arrowSvg);
    const d = pathD(s);
    const len = resample(s, 2).len + 2;
    let line;
    if (opts.dashed) {
      const id = "m" + this.maskN++;
      const mask = svgEl("mask", { id, maskUnits: "userSpaceOnUse", x: 0, y: 0, width: 1000, height: 800 + OY }, this.arrowDefs);
      const mp = svgEl("path", { d, fill: "none", stroke: "#fff", "stroke-width": 14, "stroke-linecap": "round" }, mask);
      line = svgEl("path", {
        d, fill: "none", stroke: color, "stroke-width": opts.width || 6, "stroke-dasharray": "14 12",
        "stroke-linecap": "round", mask: `url(#${id})`, opacity: opts.opacity || 1,
      }, g);
      mp.style.strokeDasharray = `${len} ${len + 60}`;
      tl.fromTo(mp, { strokeDashoffset: len + 30 }, { strokeDashoffset: 0, duration: dur, ease: "none" }, t0);
    } else {
      const glow = svgEl("path", { d, fill: "none", stroke: color, "stroke-width": 18, "stroke-linecap": "round", opacity: 0.22 }, g);
      line = svgEl("path", { d, fill: "none", stroke: color, "stroke-width": 7, "stroke-linecap": "round" }, g);
      for (const p of [glow, line]) {
        p.style.strokeDasharray = `${len} ${len + 60}`;
        tl.fromTo(p, { strokeDashoffset: len + 30 }, { strokeDashoffset: 0, duration: dur, ease: opts.ease || "power1.inOut" }, t0);
      }
    }
    if (opts.head !== false) {
      const a = s[s.length - 1];
      const b = s[Math.max(0, s.length - 4)];
      const ang = (Math.atan2(a[1] - b[1], a[0] - b[0]) * 180) / Math.PI;
      const head = svgEl("path", {
        d: "M 6 0 L -16 -12 L -10 0 L -16 12 Z", fill: color,
        transform: `translate(${PX(a[0])} ${PY(a[1])}) rotate(${ang})`,
      }, g);
      tl.fromTo(head, { opacity: 0 }, { opacity: opts.opacity || 1, duration: 0.15 }, t0 + dur - 0.12);
    }
    this.stepArrows.push(g);
    this.runArrows.push(g);
    return g;
  };

  // ---------- etiquetas flotantes ----------
  Engine.prototype.callout = function (x, y, text, color, t0, dur, cls) {
    const b = billboard(this.plane, x, y, "callout-bb");
    const pos = el("div", "callout-pos " + (cls || ""), b.fig);
    const c = el("div", "callout " + (cls || ""), pos, text);
    c.style.setProperty("--c", color || "#ffffff");
    this.tl.fromTo(c, { autoAlpha: 0, scale: 0.4, y: 20 }, { autoAlpha: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2.2)" }, t0);
    if (dur != null) this.tl.to(c, { autoAlpha: 0, scale: 0.8, duration: 0.25, ease: "power2.in" }, t0 + dur);
    this.runCallouts.push(c);
    return c;
  };

  // ---------- volcado de keyframes ----------
  Engine.prototype.bake = function (node, t0, t1, fn) {
    const n = Math.max(2, Math.round((t1 - t0) * FPS));
    const kf = {};
    for (let i = 0; i <= n; i++) {
      const t = t0 + ((t1 - t0) * i) / n;
      const v = fn(t);
      kf[((i / n) * 100).toFixed(3) + "%"] = v;
    }
    kf.easeEach = "none";
    this.tl.to(node, { keyframes: kf, duration: t1 - t0, ease: "none" }, t0);
  };

  // ---------- ejecución de un guion ----------
  // run = { t0, steps, mirror, speed, captions:true|false, ball:'CE' }
  Engine.prototype.runScript = function (run) {
    const tl = this.tl;
    const mirror = !!run.mirror;
    const sp = run.speed || 1;
    const mid = (id) => (mirror && MIRROR_ID[id]) || id;
    const mpt = (p) => (mirror ? [1000 - p[0], p[1]] : p);
    this.moves = {};
    this.runStart = {};
    for (const id in START) this.runStart[id] = START[id].slice();
    for (const id in DEF) this.runStart[id] = DEF[id].slice();
    this.runArrows = [];
    this.runCallouts = [];
    const passes = [];
    const extras = [];
    let t = run.t0;
    const stepTimes = [];

    run.steps.forEach((step, si) => {
      this.stepArrows = [];
      const T = t;
      stepTimes.push(T);
      const lead = (run.lead != null ? run.lead : 0.55) * sp;
      let end = T + lead;
      const acts = step.acts.slice().sort((a, b) => (a.move ? 0 : 1) - (b.move ? 0 : 1));
      for (const a of acts) {
        const at = T + lead + (a.at || 0) * sp;
        const dur = (a.dur || 1) * sp;
        if (a.move) {
          const id = mid(a.move);
          const s = this.addMove(id, at, dur, a.pts.map(mpt), a.ease);
          if (a.arrow !== false) this.drawPath(s, at, dur, ROLES[id].color, { ease: a.ease });
          end = Math.max(end, at + dur);
        } else if (a.pass) {
          passes.push({ from: mid(a.pass[0]), to: mid(a.pass[1]), t0: at, t1: at + (a.dur || 0.5) * sp });
          end = Math.max(end, at + (a.dur || 0.5) * sp);
        } else if (a.shot) {
          passes.push({ from: mid(a.shot), shot: true, t0: at, t1: at + (a.dur || 0.45) * sp });
          end = Math.max(end, at + (a.dur || 0.45) * sp + 0.4);
        } else {
          extras.push({ a, at, dur, mid, mpt });
          end = Math.max(end, at + (a.hold || 1.1) * sp);
        }
      }
      // atenuar flechas de pasos anteriores
      const prev = this.runArrows.filter((g) => this.stepArrows.indexOf(g) < 0);
      if (si > 0 && prev.length) tl.to(prev, { opacity: 0.32, duration: 0.4 }, T);
      t = end + (step.after != null ? step.after : 0.75) * sp;
      if (run.readable) t = Math.max(t, T + readTime(step.cap));
    });

    const dimLater = (g, tt) => {
      const nx = stepTimes.find((st) => st > tt + 0.05);
      if (nx != null) tl.to(g, { opacity: 0.32, duration: 0.4 }, nx);
    };
    // reacción defensiva: tras cada pase, la defensa bascula y sale el más cercano
    const ballX = (p) => p[0];
    passes.forEach((ps) => {
      if (ps.shot) return;
      const tgt = this.posAt(ps.to, ps.t1);
      let best = null, bd = 1e9;
      for (const id in DEF) {
        const p = this.posAt(id, ps.t0);
        const d = Math.hypot(p[0] - tgt[0], p[1] - tgt[1]);
        if (d < bd) { bd = d; best = id; }
      }
      for (const id in DEF) {
        const b = DEF[id];
        let x = b[0] + 0.1 * (ballX(tgt) - 500);
        let y = b[1];
        if (id === best) {
          const v = [tgt[0] - x, tgt[1] - y];
          const L = Math.hypot(v[0], v[1]) || 1;
          x += (v[0] / L) * 55;
          y += (v[1] / L) * 55;
        }
        this.addMove(id, ps.t0 + 0.1, 0.7 * sp, [[x, y]], "power2.out");
      }
    });

    // pases dibujados + trayectoria del balón
    passes.sort((a, b) => a.t0 - b.t0);
    const flights = passes.map((ps) => {
      const a = this.posAt(ps.from, ps.t0);
      const from = [a[0] + HAND[0], a[1] + HAND[1]];
      let to;
      if (ps.shot) to = [from[0] > 500 ? 470 : 530, -6];
      else {
        const b = this.posAt(ps.to, ps.t1);
        to = [b[0] + HAND[0], b[1] + HAND[1]];
      }
      const s = resample([from, to], 12).pts;
      this.stepArrows = [];
      const pg = this.drawPath(s, ps.t0, ps.t1 - ps.t0, "#ffffff", { dashed: true, ease: "none", head: true, width: 5 });
      dimLater(pg, ps.t1);
      if (ps.shot) {
        tl.fromTo(this.goalFlash, { opacity: 0 }, { opacity: 1, duration: 0.12 }, ps.t1);
        tl.to(this.goalFlash, { opacity: 0, duration: 0.6 }, ps.t1 + 0.25);
      }
      return { ...ps, fromP: from, toP: to };
    });

    // extras (llamadas, opciones)
    for (const { a, at, mid: m, mpt: mp } of extras) {
      if (a.call) {
        const id = m(a.call);
        const p = this.posAt(id, at);
        this.callout(p[0], p[1], a.text, ROLES[id].color, at, Math.max(1.0, (a.hold || 1.1) * sp));
      } else if (a.opts) {
        const id = m(a.opts);
        const p = this.posAt(id, at);
        const from = [p[0] + HAND[0], p[1]];
        this.stepArrows = [];
        a.to.forEach((o, k) => {
          const isGoal = o === "goal";
          const q = isGoal ? [from[0] > 500 ? 470 : 530, 10] : this.posAt(m(o), at);
          const s = resample([from, q], 10).pts;
          const ta = at + k * 0.25 * sp;
          const og = this.drawPath(s, ta, 0.4 * sp, isGoal ? "#ffffff" : ROLES[m(o)].color, { dashed: true, ease: "none", opacity: 0.9, width: 5 });
          const lbl = isGoal ? "TIRO" : "PASE";
          const lp = isGoal ? [q[0], 40] : q;
          dimLater(og, ta + 0.4 * sp);
          this.callout(lp[0], lp[1], lbl, isGoal ? "#ffffff" : ROLES[m(o)].color, ta + 0.3 * sp, null, isGoal ? "small low" : "small");
        });
      }
    }

    const tEnd = t;
    // volcar posiciones de todas las entidades en esta ventana
    const from = run.bakeFrom != null ? run.bakeFrom : run.t0 - 0.02;
    for (const id in this.ents) {
      const node = this.ents[id].node;
      this.bake(node, from, tEnd, (tt) => {
        const p = this.posAt(id, tt);
        return { x: PX(p[0]), y: PY(p[1]) };
      });
    }
    // balón
    let owner = mid(run.ball || "CE");
    const ballAt = (tt) => {
      let own = owner;
      for (const f of flights) {
        if (tt < f.t0) break;
        if (tt <= f.t1) {
          const u = (tt - f.t0) / (f.t1 - f.t0);
          const lift = f.shot ? lerp(58, 92, u) + Math.sin(Math.PI * u) * 30 : 58 + Math.sin(Math.PI * u) * 34;
          return { x: PX(lerp(f.fromP[0], f.toP[0], u)), y: PY(lerp(f.fromP[1], f.toP[1], u)), lift };
        }
        if (f.shot) return { x: PX(f.toP[0]), y: PY(f.toP[1]), lift: 70 };
        own = f.to;
      }
      const p = this.posAt(own, tt);
      return { x: PX(p[0] + HAND[0]), y: PY(p[1] + HAND[1]), lift: 58 };
    };
    this.bake(this.ball.node, from, tEnd, (tt) => {
      const b = ballAt(tt);
      return { x: b.x, y: b.y };
    });
    this.bake(this.ball.lift, from, tEnd, (tt) => ({ y: -ballAt(tt).lift }));
    const lastShot = flights.filter((f) => f.shot).pop();
    if (lastShot) tl.to(this.ball.fade, { opacity: 0, duration: 0.3 }, lastShot.t1 + 0.35);

    return { tEnd, stepTimes };
  };

  function readTime(html) {
    const words = html.replace(/<[^>]+>/g, " ").replace(/\{\w+\}/g, "X").split(/\s+/).filter(Boolean).length;
    return 0.9 + 0.3 * words;
  }

  // ---------- capa de texto ----------
  function chips(html) {
    return html.replace(/\{(EI|LI|CE|LD|ED|PI)\}/g, (m, id) =>
      `<span class="chip" style="--c:${ROLES[id].color}">${id}</span>`);
  }

  Engine.prototype.caption = function (label, html, t0, t1) {
    const c = el("div", "cap", this.capBox);
    el("div", "cap-label", c, label);
    el("div", "cap-text", c, chips(html));
    this.tl.fromTo(c, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: "power3.out" }, t0);
    this.tl.to(c, { autoAlpha: 0, y: -24, duration: 0.3, ease: "power2.in" }, t1 - 0.3);
    return c;
  };

  // ---------- montaje completo de una jugada ----------
  window.Pizarra = {
    ROLES,
    build(cfg) {
      const root = document.getElementById("root");
      const E = new Engine(root);
      const tl = E.tl;
      E.setup();
      const q = (s) => root.querySelector(s);

      // INTRO 0 → 3.4
      tl.fromTo("#intro-badge", { scale: 0.86, rotation: -8 }, { scale: 1, rotation: 0, duration: 0.9, ease: "back.out(1.8)" }, 0);
      tl.fromTo("#intro-kicker", { y: 16 }, { y: 0, duration: 0.6, ease: "power3.out" }, 0);
      const IS = cfg.introScale || 1.25;
      tl.fromTo("#head-title", { y: 760, scale: IS * 0.94 }, { y: 760, scale: IS, duration: 2.5, ease: "power1.out" }, 0);
      tl.to(["#intro-badge", "#intro-kicker"], { autoAlpha: 0, y: -40, duration: 0.4, ease: "power2.in" }, 2.5);
      tl.to("#head-title", { y: 0, scale: 1, duration: 0.8, ease: "power3.inOut" }, 2.6);
      tl.fromTo("#head-kicker", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: "power3.out" }, 3.1);
      tl.fromTo("#side-pill", { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: 0.45, ease: "power3.out" }, 3.2);
      tl.fromTo("#stage", { autoAlpha: 0, y: 140 }, { autoAlpha: 1, y: 0, duration: 0.9, ease: "power3.out" }, 2.9);
      tl.fromTo("#hud-top", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 2.9);
      tl.fromTo("#legend", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.5 }, 3.6);

      const pops = Object.keys(E.ents).map((k) => E.ents[k].pop);
      tl.fromTo(pops, { scale: 0, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 0.4, ease: "back.out(2)", stagger: 0.05 }, 3.4);
      tl.fromTo(E.ball.fade, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, 4.0);

      // presentación de posiciones
      let t = 4.1;
      const ti = Math.max(2.6, readTime(cfg.intro));
      E.caption("POSICIÓN INICIAL", cfg.intro, t, t + ti);
      t += ti;

      // CARRERA PRINCIPAL
      const steps = cfg.steps;
      const r1 = E.runScript({ t0: t, steps, ball: cfg.ball, bakeFrom: 0, readable: true });
      r1.stepTimes.forEach((st, i) => {
        const nx = i + 1 < r1.stepTimes.length ? r1.stepTimes[i + 1] : r1.tEnd;
        E.caption(`PASO ${i + 1} / ${steps.length}`, steps[i].cap, st, nx);
      });
      t = r1.tEnd;

      // CLAVES: todo el dibujo a la vista
      tl.to(E.runArrows, { opacity: 1, duration: 0.4 }, t);
      const tk = readTime(cfg.key);
      E.caption("LA CLAVE", cfg.key, t, t + tk);
      t += tk;

      // ESPEJO
      const fadeOut = [...E.runArrows, ...E.runCallouts, ...pops, ...E.ball.fade];
      tl.to(fadeOut, { autoAlpha: 0, duration: 0.35, ease: "power2.in" }, t);
      tl.to("#side-pill", { autoAlpha: 0, x: 30, duration: 0.3 }, t);
      t += 0.45;
      q("#side-pill-2").innerHTML = cfg.sideMirror;
      tl.fromTo("#side-pill-2", { autoAlpha: 0, x: -30 }, { autoAlpha: 1, x: 0, duration: 0.45, ease: "power3.out" }, t);
      tl.fromTo("#mirror-flash", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.25 }, t);
      tl.to("#mirror-flash", { autoAlpha: 0, duration: 0.5 }, t + 1.1);
      tl.to(pops, { autoAlpha: 1, scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.03 }, t + 0.2);
      tl.to(E.ball.fade, { autoAlpha: 1, duration: 0.3 }, t + 0.5);
      const t2 = t + 0.9;
      const r2 = E.runScript({ t0: t2, steps, mirror: true, speed: 0.62, lead: 0.3, ball: cfg.ball, bakeFrom: t });
      t = Math.max(r2.tEnd + 0.8, t + readTime(cfg.mirrorCap));
      E.caption("EN ESPEJO", cfg.mirrorCap, t2 - 0.9, t);

      // OUTRO
      tl.to(["#stage", "#legend", "#hud-top", "#head"], { autoAlpha: 0, y: -60, duration: 0.5, ease: "power2.in" }, t);
      tl.fromTo("#outro", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.4 }, t + 0.35);
      tl.fromTo("#outro-badge", { scale: 0.6, rotation: 10 }, { scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.8)" }, t + 0.35);
      tl.fromTo("#outro .o-line", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.12 }, t + 0.6);
      t += 3.4;

      // barra de progreso
      tl.fromTo("#progress-fill", { scaleX: 0 }, { scaleX: 1, duration: t, ease: "none" }, 0);
      window.__playLength = t;
      return tl;
    },
  };
})();
