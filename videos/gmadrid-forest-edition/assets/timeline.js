/* Construye la línea de tiempo (una sola, pausada) para cualquiera de los dos formatos.
   Uso: buildForestFilm("main")  — el id debe coincidir con data-composition-id del root. */
window.buildForestFilm = function (compId) {
  const cfg = window.FOREST_CONFIG;
  const T = cfg.time, TX = cfg.text;
  const root = document.getElementById("root");
  const W = +root.dataset.width, H = +root.dataset.height;
  root.style.width = W + "px";
  root.style.height = H + "px";
  root.classList.add(H > W ? "portrait" : "landscape");

  // ---- textos desde la configuración ----
  const title = document.getElementById("title");
  const chars = (str) => [...str].map((c) => `<span class="ch">${c === " " ? "&nbsp;" : c}</span>`).join("");
  title.innerHTML = TX.title.map((w) => `<span class="w">${chars(w)}</span>`).join("");
  document.getElementById("seasonTxt").textContent = TX.season;
  const words = [...document.querySelectorAll(".word")];
  words.forEach((el, i) => {
    el.innerHTML = chars(TX.words[i]);
    el.style.color = cfg.color.words[i];
  });

  // ---- canvas ----
  const canvas = document.getElementById("forest");
  canvas.width = W;
  canvas.height = H;
  const forest = window.createForest(canvas, cfg);
  const textLayer = document.getElementById("textLayer");

  const state = { t: 0 };
  const draw = () => {
    const cam = forest.render(state.t);
    textLayer.style.transform = `scale(${cam})`;
  };

  const tl = gsap.timeline({ paused: true });
  // reloj del bosque: un único tween lineal que dibuja el canvas en cada seek
  tl.to(state, { t: T.total, duration: T.total, ease: "none", onUpdate: draw }, 0);

  // ---- escena 3: FOREST EDITION + etiqueta 26/27 ----
  // cada palabra entra letra a letra: FOREST desde abajo, EDITION desde arriba
  tl.fromTo("#titleBox", { yPercent: -50 }, { yPercent: -50, duration: 0.01 }, 0);
  tl.set("#titleBox", { opacity: 0 }, 0);
  tl.set("#titleBox", { opacity: 1 }, T.title);
  tl.set("#titleBox", { opacity: 0 }, T.reveal - 0.05);
  document.querySelectorAll("#title .w, .word").forEach((el) => el.setAttribute("data-layout-allow-overflow", "true"));
  const tw = [...document.querySelectorAll("#title .w")];
  tw.forEach((w, wi) => {
    const dir = wi % 2 === 0 ? 1 : -1;
    tl.fromTo(w.querySelectorAll(".ch"), { yPercent: 115 * dir, rotation: 6 * dir },
      { yPercent: 0, rotation: 0, duration: 0.7, ease: "expo.out", stagger: { each: 0.035, from: dir > 0 ? "start" : "end" } },
      T.title + wi * 0.12);
    tl.to(w.querySelectorAll(".ch"), { yPercent: -115 * dir, duration: 0.24, ease: "power3.in", stagger: 0.012 }, T.reveal - 0.42 + wi * 0.04);
  });
  tl.fromTo("#title", { scale: 1 }, { scale: 1.05, duration: T.reveal - T.title, ease: "none" }, T.title);
  // etiqueta inclinada: se despliega de izquierda a derecha y entra el texto
  tl.fromTo("#seasonWrap", { scaleX: 0, opacity: 1 }, { scaleX: 1, opacity: 1, duration: 0.5, ease: "expo.out" }, T.title + 0.35);
  tl.fromTo("#seasonTxt", { xPercent: -40, opacity: 0 }, { xPercent: 0, opacity: 1, duration: 0.5, ease: "expo.out" }, T.title + 0.5);
  tl.to("#seasonWrap", { scaleX: 0, duration: 0.22, ease: "power3.in" }, T.reveal - 0.32);

  // ---- la camiseta nace en el centro ----
  const P = H > W;
  const heroH = P ? 960 : 840;
  gsap.set(["#heroFront", "#heroBack"], { height: heroH, width: "auto" });
  const glowS = P ? 1400 : 1250;
  gsap.set("#heroGlow", { width: glowS, height: glowS });
  gsap.set("#heroStage", { y: P ? -40 : 10 });
  tl.fromTo("#heroGlow", { xPercent: -50, yPercent: -50, opacity: 0, scale: 0.4 },
    { xPercent: -50, yPercent: -50, opacity: 1, scale: 1, duration: 1.2, ease: "expo.out" }, T.reveal - 0.05);
  tl.fromTo("#heroFront", { xPercent: -50, yPercent: -50, opacity: 0, scale: 0.8, y: 70, filter: "blur(22px) brightness(1.8)" },
    { xPercent: -50, yPercent: -50, opacity: 1, scale: 1, y: 0, filter: "blur(0px) brightness(1)", duration: 1.1, ease: "expo.out" }, T.reveal);
  // empuje lento de cámara sobre la camiseta
  tl.fromTo("#heroStage", { scale: 1, x: P ? -30 : -60, rotation: -1.5 },
    { scale: 1.09, x: P ? 30 : 60, rotation: 1.5, duration: T.words[0] - T.reveal, ease: "none" }, T.reveal);
  // giro: frontal -> espalda
  tl.to("#heroFront", { scaleX: 0, filter: "blur(6px)", duration: 0.13, ease: "power2.in" }, T.flip);
  tl.set("#heroFront", { opacity: 0 }, T.flip + 0.13);
  tl.fromTo("#heroBack", { xPercent: -50, yPercent: -50, opacity: 1, scaleX: 0, filter: "blur(6px)" },
    { xPercent: -50, yPercent: -50, opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.22, ease: "power2.out", immediateRender: false }, T.flip + 0.13);
  tl.set("#heroBack", { opacity: 0 }, 0);
  tl.set("#heroBack", { opacity: 1 }, T.flip + 0.13);
  // salida antes de las palabras
  tl.to(["#heroBack", "#heroGlow"], { opacity: 0, filter: "blur(14px)", duration: 0.25, ease: "power2.in" }, T.words[0] - 0.25);

  // ---- escena 4: tres palabras, letra a letra, cada una con su detalle ----
  words.forEach((el, i) => {
    const at = T.words[i];
    const next = i < words.length - 1 ? T.words[i + 1] : T.duo;
    const d = i % 2 === 0 ? 1 : -1;   // alterna el sentido del movimiento
    const chs = el.querySelectorAll(".ch");
    tl.set(el, { opacity: 1, yPercent: -50 }, at);
    tl.fromTo(el, { x: 70 * d }, { x: -70 * d, duration: next - at, ease: "none", immediateRender: false }, at);
    tl.fromTo(chs, { yPercent: 115, rotation: 8 * d }, { yPercent: 0, rotation: 0, duration: 0.5, ease: "expo.out", stagger: 0.028, immediateRender: false }, at);
    tl.to(chs, { yPercent: -115, duration: 0.14, ease: "power3.in", stagger: 0.006 }, next - 0.21);
    tl.set(el, { opacity: 0 }, next);
    // detalle: entra desde un lado, deriva y sale disparado hacia el otro
    const card = document.getElementById("card" + (i + 1));
    const img = card.querySelector("img");
    tl.fromTo(card, { opacity: 0, x: 260 * d, rotation: 5 * d, filter: "blur(14px)" },
      { opacity: 1, x: 24 * d, rotation: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out", immediateRender: false }, at);
    tl.to(card, { x: -24 * d, duration: next - at - 0.72, ease: "none" }, at + 0.5);
    tl.to(card, { x: -320 * d, rotation: -4 * d, opacity: 0, filter: "blur(12px)", duration: 0.22, ease: "power3.in" }, next - 0.22);
    tl.fromTo(img, { scale: 1.0 }, { scale: 1.14, duration: next - at, ease: "none", immediateRender: false }, at);
  });

  // ---- oficial + portería ----
  const duoH = P ? 600 : 780, duoX = P ? 220 : 300;
  gsap.set(["#duoHome", "#duoGk"], { height: duoH, width: "auto" });
  gsap.set("#duoStage", { y: P ? -40 : 0 });
  tl.fromTo("#duoHome", { xPercent: -50, yPercent: -50, x: -duoX - 520, opacity: 0, rotation: -10, filter: "blur(16px)" },
    { xPercent: -50, yPercent: -50, x: -duoX, opacity: 1, rotation: 0, filter: "blur(0px)", duration: 0.75, ease: "expo.out" }, T.duo);
  tl.fromTo("#duoGk", { xPercent: -50, yPercent: -50, x: duoX + 520, opacity: 0, rotation: 10, filter: "blur(16px)" },
    { xPercent: -50, yPercent: -50, x: duoX, opacity: 1, rotation: 0, filter: "blur(0px)", duration: 0.75, ease: "expo.out" }, T.duo + 0.1);
  tl.fromTo("#duoStage", { scale: 0.94, rotation: 1.5 }, { scale: 1.06, rotation: -1.5, duration: T.open - T.duo, ease: "none" }, T.duo);
  tl.to(["#duoHome", "#duoGk"], { opacity: 0, scale: 1.12, filter: "blur(16px)", duration: 0.3, ease: "power2.in" }, T.open - 0.15);

  // ---- escena 5: logo original (sin fondo) naciendo de un halo de luz ----
  // logo-star 680x664, logo-text 844x221 (texto 664 px por debajo del borde superior de la estrella)
  const k = P ? 0.92 : 0.78;
  const starW = 680 * k, starH = 664 * k, textW = 844 * k, textH = 221 * k;
  const totalH = (664 + 221 + 10) * k;
  gsap.set("#logoStage", { y: -18 });
  gsap.set("#logoStar", { width: starW, height: starH, x: -starW / 2 - 24 * k, y: -totalH / 2 }); // la estrella va 24 px a la izquierda del centro, como en el original
  gsap.set("#logoText", { width: textW, height: textH, x: -textW / 2, y: -totalH / 2 + (664 + 10) * k });
  const plateS = totalH * 2.05;
  gsap.set("#logoPlate", { width: plateS, height: plateS, x: -plateS / 2, y: -plateS / 2 });
  tl.fromTo("#logoPlate", { opacity: 0, scale: 0.25 }, { opacity: 1, scale: 1, duration: 1.0, ease: "expo.out" }, T.open + 0.05);
  tl.fromTo("#logoStar", { opacity: 0, scale: 0.55, rotation: -28, filter: "blur(16px)" },
    { opacity: 1, scale: 1, rotation: 0, filter: "blur(0px)", duration: 1.25, ease: "expo.out" }, T.open + 0.15);
  tl.fromTo("#logoText", { opacity: 0, yPercent: 0, filter: "blur(10px)" },
    { opacity: 1, filter: "blur(0px)", duration: 0.9, ease: "power3.out" }, T.open + 0.55);
  tl.fromTo("#logoText", { scale: 0.92 }, { scale: 1, duration: 0.9, ease: "power3.out" }, T.open + 0.55);
  // fundido final
  tl.fromTo("#fade", { opacity: 0 }, { opacity: 1, duration: T.total - T.fade, ease: "power1.in" }, T.fade);

  draw();
  window.__timelines[compId] = tl;
  tl.seek(0);
  return tl;
};
