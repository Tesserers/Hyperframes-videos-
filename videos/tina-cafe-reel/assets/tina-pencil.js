/* El lápiz de Tina: todo lo que en el reel se dibuja, se escribe o se borra pasa
   por aquí. Funciones puras sobre una línea de tiempo GSAP en pausa: nada de
   relojes ni azar, así que cada fotograma sale igual en preview y en render.

   - make(parent, id, mode)      crea un lápiz ("draw" = punta, "erase" = goma)
   - move(tl, pen, pts, t, dur)  lo lleva por una polilínea a velocidad constante
   - scribble(tl, o)             colorea (o borra) una zona a trazos en zigzag
   - trace(tl, path, o)          repasa un contorno SVG con el lápiz encima
   - write(tl, el, o)            «escribe» un texto de izquierda a derecha
   - box(el, root)               caja de un elemento en coordenadas del cuadro */
(function () {
  const NS = "http://www.w3.org/2000/svg";

  // Lápiz dibujado en horizontal, punta en (0,0) y cuerpo hacia +x; luego se
  // inclina como si lo sujetase una mano derecha.
  const BODY =
    '<path d="M40 -22 L250 -22 L250 22 L40 22 Z" fill="#FFDE86" stroke="#2A1B0E" stroke-width="3"/>' +
    '<path d="M40 -7 L250 -7 M40 8 L250 8" stroke="#D4A668" stroke-width="3"/>' +
    '<path d="M0 0 L40 -22 L40 22 Z" fill="#F2E3C0" stroke="#2A1B0E" stroke-width="3" stroke-linejoin="round"/>' +
    '<path d="M0 0 L13 -7 L13 7 Z" fill="#2A1B0E"/>' +
    '<rect x="250" y="-23" width="26" height="46" fill="#B8893E" stroke="#2A1B0E" stroke-width="3"/>' +
    '<path d="M276 -23 L306 -23 Q320 -23 320 -9 L320 9 Q320 23 306 23 L276 23 Z" fill="#C97A5C" stroke="#2A1B0E" stroke-width="3"/>';

  function make(parent, id, mode) {
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("id", id);
    svg.setAttribute("width", "1");
    svg.setAttribute("height", "1");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("data-layout-allow-overflow", ""); // entra y sale por fuera de cuadro a propósito
    svg.setAttribute("style", "position:absolute;left:0;top:0;overflow:visible;z-index:50;opacity:0;visibility:hidden");
    const tf = mode === "erase" ? "rotate(-50) translate(320 0) scale(-1 1)" : "rotate(-50)";
    svg.innerHTML =
      '<g transform="' + tf + '"><g transform="translate(6 10)" opacity="0.18">' + BODY.replace(/fill="#[0-9A-F]+"/g, 'fill="#2A1B0E"') +
      '</g>' + BODY + "</g>";
    parent.appendChild(svg);
    return svg;
  }

  function lengths(pts) {
    const seg = [];
    let total = 0;
    for (let i = 1; i < pts.length; i++) {
      const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      seg.push(d);
      total += d;
    }
    return { seg, total };
  }

  // Velocidad constante sobre la polilínea, con un leve cabeceo en cada tramo.
  function move(tl, pen, pts, t, dur, wiggle) {
    const { seg, total } = lengths(pts);
    tl.set(pen, { x: pts[0][0], y: pts[0][1], autoAlpha: 1, transformOrigin: "0px 0px" }, t);
    let at = t;
    const w = wiggle === undefined ? 4 : wiggle;
    seg.forEach((d, i) => {
      const dd = total ? (dur * d) / total : dur / seg.length;
      tl.to(pen, { x: pts[i + 1][0], y: pts[i + 1][1], rotation: i % 2 ? w : -w, duration: dd, ease: "none" }, at);
      at += dd;
    });
    return at;
  }

  // Entrada o salida del lápiz desde fuera de cuadro, con algo de inercia.
  function fly(tl, pen, from, to, t, dur, out) {
    tl.fromTo(pen, { x: from[0], y: from[1], autoAlpha: 1 },
      { x: to[0], y: to[1], rotation: 0, duration: dur, ease: out ? "power2.in" : "power3.out", transformOrigin: "0px 0px" }, t);
    if (out) tl.set(pen, { autoAlpha: 0 }, t + dur);
  }

  function zigzag(x0, y0, x1, y1, w) {
    const m = w * 0.5;
    const step = w * 0.62;
    const pts = [];
    let y = y0 - m * 0.4;
    let left = true;
    while (y < y1 + m) {
      pts.push([left ? x0 - m : x1 + m, y]);
      y += step * 0.5;
      left = !left;
    }
    pts.push([left ? x0 - m : x1 + m, y]);
    return pts;
  }

  /* Colorea a zigzag la caja (x0,y0)-(x1,y1) con trazo de ancho w. Si el color
     es el del fondo, se lee como goma de borrar. Devuelve el path. */
  function scribble(tl, o) {
    const pts = zigzag(o.x0, o.y0, o.x1, o.y1, o.w);
    const { total } = lengths(pts);
    const path = document.createElementNS(NS, "path");
    path.setAttribute("d", "M" + pts.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" L"));
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", o.color);
    path.setAttribute("stroke-width", String(o.w));
    path.setAttribute("stroke-linecap", "round");
    path.setAttribute("stroke-linejoin", "round");
    if (o.filter) path.setAttribute("filter", "url(#" + o.filter + ")");
    if (o.id) path.setAttribute("id", o.id);
    o.svg.appendChild(path);
    // escondido hasta su turno: con punta redonda, un trazo «vacío» deja un punto
    gsap.set(path, { autoAlpha: 0 });
    tl.set(path, { autoAlpha: 1 }, o.t);
    tl.fromTo(path, { strokeDasharray: total + 2, strokeDashoffset: total + 2 },
      { strokeDashoffset: 0, duration: o.dur, ease: "none" }, o.t);
    if (o.pen) move(tl, o.pen, pts, o.t, o.dur, 7);
    if (o.hideAt !== undefined) tl.set(path, { autoAlpha: 0 }, o.hideAt);
    return path;
  }

  /* Repasa un path SVG: el trazo aparece bajo la punta del lápiz. o.ox/o.oy/o.s
     pasan de coordenadas del SVG a coordenadas del cuadro. */
  function trace(tl, path, o) {
    const len = path.getTotalLength();
    gsap.set(path, { autoAlpha: 0 });
    tl.set(path, { autoAlpha: 1 }, o.t);
    tl.fromTo(path, { strokeDasharray: len + 1, strokeDashoffset: len + 1 },
      { strokeDashoffset: 0, duration: o.dur, ease: o.ease || "none" }, o.t);
    if (!o.pen) return;
    const n = o.samples || 18;
    const pts = [];
    for (let i = 0; i <= n; i++) {
      const p = path.getPointAtLength((len * i) / n);
      pts.push([o.ox + p.x * o.s, o.oy + p.y * o.s]);
    }
    move(tl, o.pen, pts, o.t, o.dur, 3);
  }

  function box(el, root) {
    const r = el.getBoundingClientRect();
    const rr = root.getBoundingClientRect();
    const k = rr.width / 1080 || 1;
    return { x: (r.left - rr.left) / k, y: (r.top - rr.top) / k, w: r.width / k, h: r.height / k };
  }

  /* Escribe un texto: se destapa de izquierda a derecha mientras la punta del
     lápiz va dando saltitos sobre la línea. b = box() medido antes de animar. */
  function write(tl, el, o) {
    const b = o.box;
    // escondido del todo hasta su turno (la itálica sobresale de su caja)
    gsap.set(el, { autoAlpha: 0 });
    tl.set(el, { autoAlpha: 1 }, o.t);
    tl.fromTo(el, { clipPath: "inset(-20% 104% -20% -4%)" },
      { clipPath: "inset(-20% -4% -20% -4%)", duration: o.dur, ease: "none" }, o.t);
    if (!o.pen) return;
    const steps = Math.max(4, Math.round(b.w / 46));
    const pts = [];
    for (let i = 0; i <= steps; i++) {
      const x = b.x + (b.w * i) / steps;
      const y = b.y + b.h * (i % 2 ? 0.42 : 0.72);
      pts.push([x, y]);
    }
    move(tl, o.pen, pts, o.t, o.dur, 5);
  }

  window.TinaPencil = { make, move, fly, scribble, trace, write, box, zigzag };
})();
