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
  title.innerHTML = TX.title.map((w) => `<span class="w">${w}</span>`).join("");
  document.getElementById("season").textContent = TX.season;
  const words = [...document.querySelectorAll(".word")];
  words.forEach((el, i) => {
    el.textContent = TX.words[i];
    el.style.color = cfg.color.words[i];
  });
  const sig = document.getElementById("signature");
  sig.innerHTML = `${TX.signature[0]} <span class="slash">/</span> <span class="sub">${TX.signature[1]}</span>`;

  // ---- canvas ----
  const canvas = document.getElementById("forest");
  canvas.width = W;
  canvas.height = H;
  const forest = window.createForest(canvas, cfg);
  sig.style.top = forest.LOGO_Y + forest.LOGO_SIZE * 0.5 + (H > W ? 70 : 46) + "px";
  const textLayer = document.getElementById("textLayer");

  const state = { t: 0 };
  const draw = () => {
    const cam = forest.render(state.t);
    textLayer.style.transform = `scale(${cam})`;
  };

  const tl = gsap.timeline({ paused: true });
  // reloj del bosque: un único tween lineal que dibuja el canvas en cada seek
  tl.to(state, { t: T.total, duration: T.total, ease: "none", onUpdate: draw }, 0);

  // ---- escena 3: FOREST EDITION / TEMPORADA 26/27 ----
  tl.fromTo("#titleBox", { yPercent: -50 }, { yPercent: -50, duration: 0.01 }, 0);
  tl.fromTo(
    "#title .w",
    { opacity: 0, y: 70, scale: 1.08, filter: "blur(16px)" },
    { opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 1.2, ease: "expo.out", stagger: 0.14 },
    T.title
  );
  tl.fromTo(
    "#season",
    { opacity: 0, y: 24, scaleX: 1.25, filter: "blur(6px)" },
    { opacity: 1, y: 0, scaleX: 1, filter: "blur(0px)", duration: 1.1, ease: "power3.out" },
    T.title + 0.5
  );
  tl.to("#titleBox", { opacity: 0, scale: 1.06, filter: "blur(10px)", duration: 0.3, ease: "power2.in" }, T.words[0] - 0.3);

  // ---- escena 4: tres palabras con corte rítmico ----
  words.forEach((el, i) => {
    const at = T.words[i];
    tl.fromTo(
      el,
      { opacity: 0, yPercent: -50, scale: 1.18, filter: "blur(18px)" },
      { opacity: 1, yPercent: -50, scale: 1, filter: "blur(0px)", duration: 0.42, ease: "expo.out", immediateRender: false },
      at
    );
    // corte seco antes de la siguiente
    const end = i < words.length - 1 ? T.words[i + 1] : T.open - 0.05;
    // ligero empuje mientras se sostiene
    const holdEnd = i < words.length - 1 ? end : end - 0.22;
    tl.to(el, { scale: 1.035, duration: holdEnd - (at + 0.42), ease: "none" }, at + 0.42);
    if (i < words.length - 1) tl.set(el, { opacity: 0 }, end);
    else tl.to(el, { opacity: 0, scale: 1.12, filter: "blur(12px)", duration: 0.22, ease: "power2.in" }, end - 0.22);
  });

  // ---- escena 5: firma bajo el logo ----
  tl.fromTo(
    "#signature",
    { opacity: 0, y: 16, scaleX: 1.3, filter: "blur(6px)" },
    { opacity: 1, y: 0, scaleX: 1, filter: "blur(0px)", duration: 1.0, ease: "power3.out" },
    T.open + 0.55
  );
  // fundido final
  tl.fromTo("#fade", { opacity: 0 }, { opacity: 1, duration: T.total - T.fade, ease: "power1.in" }, T.fade);

  draw();
  window.__timelines[compId] = tl;
  tl.seek(0);
  return tl;
};
