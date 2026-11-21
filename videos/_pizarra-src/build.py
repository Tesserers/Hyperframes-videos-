"""Genera los tres proyectos de jugada a partir de la plantilla y el motor común.

Uso:  python3 videos/_pizarra-src/build.py
Coordenadas de pista: x 0..1000 (20 m de ancho), y = distancia a la línea de gol
(50 px = 1 m). Posiciones de salida en pizarra.js (START).
"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)

PLAYS = {
    "poni": {
        "num": "01",
        "music": "poniclub.mp3",
        "title": ["LA", "PONI"],
        "accent": 1,
        "titleSize": 150,
        "subtitle": "PERMUTA CENTRAL–LATERAL",
        "sideMain": "▶ POR LA <b>DERECHA</b>",
        "sideMirror": "◀ POR LA <b>IZQUIERDA</b>",
        "next": "PRÓXIMA: <b>LA PROHIBIDA</b>",
        "ball": "CE",
        "intro": "Ataque en 6:0. El balón lo tiene el central {CE}.",
        "steps": [
            {"cap": "El central {CE} pasa el balón al lateral derecho {LD}.",
             "acts": [{"pass": ["CE", "LD"], "at": 0.1, "dur": 0.55}]},
            {"cap": "Permuta: el central {CE} cambia de lado <em>por dentro</em>, cerca de la defensa, y el lateral {LI} va <em>por fuera</em>, por detrás, hasta el centro.",
             "acts": [{"move": "CE", "pts": [[410, 505], [305, 490], [225, 520]], "dur": 1.9},
                      {"move": "LI", "at": 0.25, "pts": [[255, 640], [375, 725], [495, 655]], "dur": 2.1}]},
            {"cap": "Mientras, el lateral derecho {LD} <em>aguanta el balón</em>.",
             "acts": [{"move": "LD", "pts": [[760, 450], [785, 500]], "dur": 1.2, "arrow": False},
                      {"call": "LD", "text": "¡AGUANTA!", "at": 0.1, "hold": 1.5}]},
            {"cap": "El nuevo central {LI} <em>entra en carrera</em> y recibe de {LD}.",
             "acts": [{"move": "LI", "pts": [[500, 540], [508, 430]], "dur": 1.3, "ease": "power1.in"},
                      {"pass": ["LD", "LI"], "at": 0.35, "dur": 0.55}]},
            {"cap": "Decide: si el pivote {PI} le abre hueco, <em>tira</em>. Si no, la pasa: al pivote, a un lateral ({CE} o {LD}) o a un extremo ({EI} o {ED}).",
             "acts": [{"opts": "LI", "to": ["goal", "PI", "CE", "LD", "EI", "ED"], "at": 0, "hold": 3.0}],
             "after": 1.0},
        ],
        "key": "Pase al lateral; el central cambia de lado <em>por dentro</em> y el lateral va <em>por fuera</em>, por detrás, para <em>entrar en carrera</em> por el centro.",
        "mirrorCap": "Poni por la izquierda: lo mismo, cambiando el lado. Pase a {LI} y el que entra es {LD}.",
    },
    "prohibida": {
        "num": "02",
        "title": ["LA", "PROHIBIDA"],
        "accent": 1,
        "titleSize": 116,
        "introScale": 1.0,
        "subtitle": "O «ESCÁNDALO»",
        "sideMain": "◀ POR LA <b>IZQUIERDA</b>",
        "sideMirror": "▶ POR LA <b>DERECHA</b>",
        "next": "PRÓXIMA: <b>LONG CHICKEN</b>",
        "ball": "CE",
        "start": {"PI": [232, 292]},
        "intro": "La inicia el lateral: permuta entre lateral {LI} y central {CE}. El pivote {PI} se coloca sobre el 2 de ese lado.",
        "steps": [
            {"cap": "El central {CE} pasa el balón al lateral izquierdo {LI}.",
             "acts": [{"pass": ["CE", "LI"], "at": 0.1, "dur": 0.55}]},
            {"cap": "El lateral {LI} se la pasa al extremo {EI}, que <em>sale un poco hacia delante</em> para recibir.",
             "acts": [{"move": "EI", "pts": [[118, 212]], "at": 0, "dur": 0.9, "ease": "power2.out"},
                      {"pass": ["LI", "EI"], "at": 0.2, "dur": 0.6}]},
            {"cap": "Tras pasar, el lateral {LI} ocupa la posición <em>por delante</em> del central.",
             "acts": [{"move": "LI", "pts": [[330, 455], [470, 470]], "dur": 1.4}]},
            {"cap": "El central {CE} hace una <em>trayectoria amplia</em> y ocupa el puesto de lateral.",
             "acts": [{"move": "CE", "pts": [[450, 700], [320, 700], [225, 610]], "dur": 1.8}]},
            {"cap": "El extremo {EI} retiene el balón… y se la da a {CE}, ahora lateral, que <em>entra en carrera</em>.",
             "acts": [{"call": "EI", "text": "¡RETIENE!", "at": 0, "hold": 1.0},
                      {"move": "CE", "pts": [[262, 520], [318, 430]], "at": 0.8, "dur": 1.3, "ease": "power1.in"},
                      {"pass": ["EI", "CE"], "at": 1.15, "dur": 0.55}]},
            {"cap": "{CE} decide: si el pivote {PI} le abre hueco, <em>tira</em>. Si no, se la pasa al pivote, al central {LI} o al extremo {EI}.",
             "acts": [{"opts": "CE", "to": ["goal", "PI", "LI", "EI"], "at": 0, "hold": 2.6}],
             "after": 1.0},
        ],
        "key": "La inicia el lateral: pasa al extremo, se mete <em>por delante</em> del central y el central <em>sale amplio</em> para entrar de lateral.",
        "mirrorCap": "Prohibida por la derecha: misma jugada en espejo. Inicia {LD} con el extremo {ED}.",
    },
    "long-chicken": {
        "num": "03",
        "title": ["LONG", "CHICKEN"],
        "accent": 1,
        "titleSize": 108,
        "introScale": 0.98,
        "subtitle": "EL CENTRAL MARCA QUIÉN INICIA",
        "sideMain": "◀ INICIA EL <b>LATERAL IZQ.</b>",
        "sideMirror": "▶ INICIA EL <b>LATERAL DER.</b>",
        "next": "¡A PROBARLA EN EL <b>ENTRENO</b>!",
        "ball": "CE",
        "start": {"PI": [335, 312]},
        "intro": "El central {CE} tiene el balón y canta la jugada. El pivote {PI} está entre el 2 y el 3 del lado que inicia.",
        "steps": [
            {"cap": "El central {CE} marca quién inicia: uno u otro lateral. Aquí, {LI}.",
             "acts": [{"call": "CE", "text": "¡LONG CHICKEN!", "at": 0, "hold": 1.8}]},
            {"cap": "El lateral {LI} va a ocupar el puesto de central y {CE} se la pasa. El pivote {PI} sale un poco hacia delante.",
             "acts": [{"move": "LI", "pts": [[320, 460], [430, 480]], "dur": 1.3},
                      {"move": "PI", "pts": [[340, 385]], "at": 0.3, "dur": 0.9},
                      {"pass": ["CE", "LI"], "at": 0.85, "dur": 0.5}]},
            {"cap": "El central {CE} ocupa el puesto del lateral que se ha desplazado.",
             "acts": [{"move": "CE", "pts": [[420, 680], [300, 680], [220, 585]], "dur": 1.7}]},
            {"cap": "El otro lateral {LD} viene <em>por detrás</em> y hace un <em>cruce</em> con {LI}.",
             "acts": [{"move": "LI", "pts": [[560, 465], [700, 470], [785, 505]], "at": 0.1, "dur": 2.0},
                      {"move": "LD", "pts": [[770, 640], [640, 650], [520, 560], [480, 470]], "dur": 2.2},
                      {"pass": ["LI", "LD"], "at": 1.15, "dur": 0.45}]},
            {"cap": "{LD}, ahora central, decide: si el pivote {PI} le abre hueco, <em>tira</em>. Si no, la pasa: al pivote, a un lateral ({CE} o {LI}) o a un extremo ({EI} o {ED}).",
             "acts": [{"opts": "LD", "to": ["goal", "PI", "CE", "LI", "EI", "ED"], "at": 0, "hold": 3.0}],
             "after": 1.0},
        ],
        "key": "El central canta el lado. Ese lateral entra al centro, el central ocupa su hueco y el otro lateral <em>cruza por detrás</em>.",
        "mirrorCap": "Si el central marca el otro lado, inicia {LD} y cruza {LI}. Misma idea, en espejo.",
    },
}


ARENA_CSS = """
      /* ---- modo pabellón ---- */
      #head, #hud-top { z-index: 6; }
      #head-bg { position: absolute; left: 0; top: 0; width: 1080px; height: 455px; z-index: 5;
        background: linear-gradient(180deg, #142a5c 0%, #142a5c 88%, rgba(20,42,92,0) 100%); }
      #cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1100px; transform-style: preserve-3d; transform-origin: 50% 62%; }
      #orbit { position: absolute; left: 0; top: 0; width: 1000px; height: 890px; transform-style: preserve-3d; transform-origin: 500px 600px; }
      .yaw { position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }
      .arena-floor { background: radial-gradient(ellipse at 50% 45%, #22397a 0%, #101d45 55%, #0a1430 100%); }
      .court { box-shadow: 0 0 0 10px #0d1a3e, 0 0 0 13px rgba(47,168,224,0.55), 0 50px 140px rgba(0,0,0,0.7); }
      .ring { position: absolute; left: -40px; top: -17px; width: 80px; height: 34px; border-radius: 50%;
        border: 4px solid var(--c); box-shadow: 0 0 22px var(--c), inset 0 0 12px var(--c); opacity: 0.9; }
      .stand-wrap { position: absolute; left: -420px; top: 0; width: 1840px; height: 0; transform-style: preserve-3d; }
      .stand { position: absolute; left: 0; bottom: 0; width: 1840px; height: 250px; transform-origin: 50% 100%;
        transform: rotateX(-62deg); background: repeating-linear-gradient(180deg, #14224a 0 32px, #1a2b5a 32px 62px); }
      .stand-row { position: absolute; left: 20px; width: 1800px; height: 62px; }
      .fan { position: absolute; bottom: 4px; width: 34px; height: 56px; }
      .fan i { position: absolute; display: block; }
      .fan .torso { left: 3px; bottom: 0; width: 28px; height: 30px; border-radius: 12px 12px 4px 4px; }
      .fan .head { left: 8px; bottom: 28px; width: 18px; height: 18px; border-radius: 50%; }
      .fan .hand { bottom: 30px; width: 9px; height: 9px; border-radius: 50%; }
      .fan .hand.l { left: 2px; }
      .fan .hand.r { left: 23px; }
      .led-bb { position: absolute; width: 1600px; height: 0; transform-style: preserve-3d; }
      .led { position: absolute; left: 0; bottom: 0; width: 1600px; height: 48px; transform-origin: 50% 100%; transform: rotateX(-90deg);
        background: #050a1a; border-top: 3px solid #2fa8e0; border-bottom: 3px solid #2fa8e0; overflow: hidden; box-shadow: 0 0 34px rgba(47,168,224,0.45); }
      .led-strip { display: flex; gap: 70px; width: 9000px; white-space: nowrap; font: 400 30px/48px var(--display); color: #fff; padding-left: 40px; }
      .led-strip b { font-weight: 400; margin-right: 14px; }
      #lights { position: absolute; left: 0; top: 280px; width: 1080px; height: 1100px; pointer-events: none; mix-blend-mode: screen;
        background: radial-gradient(520px 340px at 22% 18%, rgba(190,220,255,0.16), rgba(0,0,0,0) 70%),
          radial-gradient(520px 340px at 78% 18%, rgba(190,220,255,0.16), rgba(0,0,0,0) 70%),
          radial-gradient(700px 420px at 50% 62%, rgba(255,240,210,0.08), rgba(0,0,0,0) 70%); }
"""


def arena_html(html, duration):
    """Convierte la plantilla plana en la versión pabellón."""
    html = html.replace("      /* Intro / outro */", ARENA_CSS + "\n      /* Intro / outro */", 1)
    html = html.replace('<div id="stage" data-layout-ignore><div id="plane"></div></div>',
                        '<div id="stage" data-layout-ignore><div id="cam"><div id="plane"><div id="orbit"></div></div></div></div>\n'
                        '        <div id="lights" data-layout-ignore></div>\n        <div id="head-bg"></div>', 1)
    html = html.replace('<script src="assets/pizarra.js"></script>',
                        '<script src="assets/arena.js"></script>\n    <script src="assets/pizarra.js"></script>', 1)
    html = html.replace('data-track-index="1" data-volume="0.9"></audio>',
                        'data-track-index="1" data-volume="0.9"></audio>\n'
                        f'      <audio id="crowd" src="assets/music/crowd.mp3" data-start="0" data-duration="{duration}" data-track-index="2" data-volume="1"></audio>', 1)
    assert 'id="orbit"' in html and "arena.js" in html and 'id="crowd"' in html
    return html


def write_if_changed(path, data):
    if os.path.exists(path) and open(path, "rb").read() == data:
        return
    open(path, "wb").write(data)


def make(key, cfg, tpl, arena):
    name = "gmadrid-" + key + ("-3d" if arena else "")
    proj = os.path.join(VIDEOS, name)
    os.makedirs(os.path.join(proj, "assets", "vendor"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "pizarra.js"), os.path.join(proj, "assets", "pizarra.js"))
    shutil.copy(os.path.join(HERE, "gsap.min.js"), os.path.join(proj, "assets", "vendor", "gsap.min.js"))
    if arena:
        shutil.copy(os.path.join(HERE, "arena.js"), os.path.join(proj, "assets", "arena.js"))
        logo = os.path.join(VIDEOS, "gmadrid-" + key, "assets", "gmadrid-logo.png")
        shutil.copy(logo, os.path.join(proj, "assets", "gmadrid-logo.png"))
        cfg = dict(cfg, arena=True)
    words = "".join(
        f'<span class="m"><span class="w{" acc" if i == cfg["accent"] else ""}">{w}</span></span>'
        for i, w in enumerate(cfg["title"])
    )
    # la versión pabellón dura lo mismo que la plana: misma jugada, mismos tiempos
    dur_file = os.path.join(VIDEOS, "gmadrid-" + key, ".duration")
    duration = open(dur_file).read().strip() if os.path.exists(dur_file) else "60"
    html = (
        tpl.replace("__TITLE_PLAIN__", " ".join(cfg["title"]))
        .replace("__TITLE_WORDS__", words)
        .replace("__TITLE_SIZE__", str(cfg["titleSize"]))
        .replace("__NUM__", cfg["num"])
        .replace("__SUBTITLE__", cfg["subtitle"])
        .replace("__SIDE_MAIN__", cfg["sideMain"])
        .replace("__NEXT__", cfg["next"])
        .replace("__DURATION__", duration)
        .replace("__PLAY_JSON__", json.dumps(cfg, ensure_ascii=False))
    )
    if arena:
        html = arena_html(html, duration)
    write_if_changed(os.path.join(proj, "index.html"), html.encode())
    # música: Brisk Beat por defecto; una jugada puede llevar su propio tema ("music").
    # Si el tema es algo más corto que el vídeo, se estira (sin cambiar el tono) para que
    # termine con el vídeo; si es más largo, se recorta con fundido final.
    mdir = os.path.join(proj, "assets", "music")
    os.makedirs(mdir, exist_ok=True)
    d = float(duration)
    src = os.path.join(HERE, cfg.get("music", "brisk-beat.m4a"))
    sdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", src], capture_output=True, text=True, check=True).stdout)
    chain = []
    if sdur < d:
        chain.append(f"atempo={sdur / d:.5f}")
    chain += [f"afade=t=out:st={d - 2.5:.2f}:d=2.5", "loudnorm=I=-16:TP=-1.5:LRA=11"]
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "bgm.mp3")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-t", duration, "-af", ",".join(chain),
                        "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", "-map_metadata", "-1", out], check=True)
        write_if_changed(os.path.join(mdir, "bgm.mp3"), open(out, "rb").read())
    if arena:
        # aplausos del público sincronizados con los momentos de la jugada
        marks = subprocess.run(["node", os.path.join(HERE, "marks.cjs"), os.path.join(proj, "index.html")],
                               capture_output=True, text=True, check=True).stdout.strip()
        with tempfile.TemporaryDirectory() as td:
            wav = os.path.join(td, "crowd.wav")
            out = os.path.join(td, "crowd.mp3")
            subprocess.run(["python3", os.path.join(HERE, "crowd.py"), wav, duration, marks], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "loudnorm=I=-25:TP=-3:LRA=15", "-ar", "44100", "-c:a", "libmp3lame",
                            "-b:a", "160k", "-map_metadata", "-1", out], check=True)
            write_if_changed(os.path.join(mdir, "crowd.mp3"), open(out, "rb").read())
    print("ok", name, duration)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    tpl = open(os.path.join(HERE, "template.html")).read()
    for key, cfg in PLAYS.items():
        if only in ("all", "2d"):
            make(key, cfg, tpl, arena=False)
        if only in ("all", "3d"):
            make(key, cfg, tpl, arena=True)


if __name__ == "__main__":
    main()
