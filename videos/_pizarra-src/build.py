"""Genera los tres proyectos de jugada a partir de la plantilla y el motor común.

Uso:  python3 videos/_pizarra-src/build.py
Coordenadas de pista: x 0..1000 (20 m de ancho), y = distancia a la línea de gol
(50 px = 1 m). Posiciones de salida en pizarra.js (START).
"""
import json, os, shutil, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(HERE)

PLAYS = {
    "poni": {
        "num": "01",
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
            {"cap": "Al pasar, el central {CE} se va <em>hacia atrás</em>, al lado contrario del pase.",
             "acts": [{"move": "CE", "pts": [[430, 680], [310, 700], [215, 600]], "dur": 1.7}]},
            {"cap": "El lateral izquierdo {LI}, en <em>trayectoria amplia</em>, ocupa el puesto de central.",
             "acts": [{"move": "LI", "pts": [[300, 455], [420, 520], [495, 650]], "dur": 1.7}]},
            {"cap": "El lateral derecho {LD} <em>aguanta el balón</em> y fija a su defensor.",
             "acts": [{"move": "LD", "pts": [[760, 450], [785, 500]], "dur": 1.2, "arrow": False},
                      {"call": "LD", "text": "¡AGUANTA!", "at": 0.1, "hold": 1.5}]},
            {"cap": "El nuevo central {LI} <em>entra en carrera</em> y recibe de {LD}.",
             "acts": [{"move": "LI", "pts": [[500, 540], [508, 430]], "dur": 1.3, "ease": "power1.in"},
                      {"pass": ["LD", "LI"], "at": 0.35, "dur": 0.55}]},
            {"cap": "Decide: <em>tira</em>… o, si le defienden, la pasa a uno u otro lateral: {CE} o {LD}.",
             "acts": [{"opts": "LI", "to": ["goal", "CE", "LD"], "at": 0, "hold": 1.6},
                      {"shot": "LI", "at": 1.6, "dur": 0.45}],
             "after": 1.0},
        ],
        "key": "Tres cosas: pase al lateral, el central sale <em>por detrás</em> al otro lado y el lateral <em>entra en carrera</em> por el centro.",
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
        "intro": "La inicia el lateral. Es una permuta entre lateral {LI} y central {CE}.",
        "steps": [
            {"cap": "El central {CE} pasa el balón al lateral izquierdo {LI}.",
             "acts": [{"pass": ["CE", "LI"], "at": 0.1, "dur": 0.55}]},
            {"cap": "El lateral {LI} se la pasa al extremo {EI}.",
             "acts": [{"pass": ["LI", "EI"], "at": 0.1, "dur": 0.6}]},
            {"cap": "Tras pasar, el lateral {LI} ocupa la posición <em>por delante</em> del central.",
             "acts": [{"move": "LI", "pts": [[330, 455], [470, 470]], "dur": 1.4}]},
            {"cap": "El central {CE} hace una <em>trayectoria amplia</em> y ocupa el puesto de lateral.",
             "acts": [{"move": "CE", "pts": [[450, 700], [320, 700], [225, 610]], "dur": 1.8}]},
            {"cap": "El extremo {EI} retiene el balón… y se la da a {CE}, ahora lateral, que <em>entra en carrera</em>.",
             "acts": [{"call": "EI", "text": "¡RETIENE!", "at": 0, "hold": 1.0},
                      {"move": "CE", "pts": [[262, 520], [318, 430]], "at": 0.8, "dur": 1.3, "ease": "power1.in"},
                      {"pass": ["EI", "CE"], "at": 1.15, "dur": 0.55}]},
            {"cap": "Y finaliza con <em>tiro en carrera</em>.",
             "acts": [{"shot": "CE", "at": 0.1, "dur": 0.45}],
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
        "intro": "El central {CE} tiene el balón y canta la jugada.",
        "steps": [
            {"cap": "El central {CE} marca quién inicia: uno u otro lateral. Aquí, {LI}.",
             "acts": [{"call": "CE", "text": "¡LONG CHICKEN!", "at": 0, "hold": 1.8}]},
            {"cap": "El lateral {LI} va a ocupar el puesto de central y {CE} se la pasa.",
             "acts": [{"move": "LI", "pts": [[320, 460], [430, 480]], "dur": 1.3},
                      {"pass": ["CE", "LI"], "at": 0.85, "dur": 0.5}]},
            {"cap": "El central {CE} ocupa el puesto del lateral que se ha desplazado.",
             "acts": [{"move": "CE", "pts": [[420, 680], [300, 680], [220, 585]], "dur": 1.7}]},
            {"cap": "El otro lateral {LD} viene <em>por detrás</em> y hace un <em>cruce</em> con {LI}.",
             "acts": [{"move": "LI", "pts": [[560, 465], [700, 470], [785, 505]], "at": 0.1, "dur": 2.0},
                      {"move": "LD", "pts": [[770, 640], [640, 650], [520, 560], [480, 470]], "dur": 2.2},
                      {"pass": ["LI", "LD"], "at": 1.15, "dur": 0.45}]},
            {"cap": "{LD}, ahora central, decide: <em>tira</em> o se la pasa a {CE}, que ahora es lateral.",
             "acts": [{"opts": "LD", "to": ["goal", "CE"], "at": 0, "hold": 1.4},
                      {"shot": "LD", "at": 1.4, "dur": 0.45}],
             "after": 1.0},
        ],
        "key": "El central canta el lado. Ese lateral entra al centro, el central ocupa su hueco y el otro lateral <em>cruza por detrás</em>.",
        "mirrorCap": "Si el central marca el otro lado, inicia {LD} y cruza {LI}. Misma idea, en espejo.",
    },
}


def main():
    tpl = open(os.path.join(HERE, "template.html")).read()
    engine = os.path.join(HERE, "pizarra.js")
    for key, cfg in PLAYS.items():
        proj = os.path.join(VIDEOS, "gmadrid-" + key)
        os.makedirs(os.path.join(proj, "assets"), exist_ok=True)
        shutil.copy(engine, os.path.join(proj, "assets", "pizarra.js"))
        os.makedirs(os.path.join(proj, "assets", "vendor"), exist_ok=True)
        shutil.copy(os.path.join(HERE, "gsap.min.js"), os.path.join(proj, "assets", "vendor", "gsap.min.js"))
        words = "".join(
            f'<span class="m"><span class="w{" acc" if i == cfg["accent"] else ""}">{w}</span></span>'
            for i, w in enumerate(cfg["title"])
        )
        dur_file = os.path.join(proj, ".duration")
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
        open(os.path.join(proj, "index.html"), "w").write(html)
        # música (Brisk Beat, aportada por el club): recorte a la duración del vídeo + fundido final
        mdir = os.path.join(proj, "assets", "music")
        os.makedirs(mdir, exist_ok=True)
        for old in os.listdir(mdir):
            os.remove(os.path.join(mdir, old))
        d = float(duration)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(HERE, "brisk-beat.m4a"), "-t", duration,
                        "-af", f"afade=t=out:st={d - 2.5:.2f}:d=2.5,loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k",
                        os.path.join(mdir, "brisk-beat.mp3")], check=True)
        print("ok", key, duration)


if __name__ == "__main__":
    main()
