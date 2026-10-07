---
workflow: general-video
flow: automation
storyboard: no
message: "En Tessera somos capaces de tenerlo todo bajo control: hemos construido nuestro propio CRM."
destination: linkedin
aspect: 1080x1350
language: es
audience: "Clientes, candidatos y red de Tessera en LinkedIn"
length: 33.4s
angle: "Orgullo de capacidad propia: lo que gestionamos → la herramienta que hemos creado → control total"
style_preset: brand-native
capture: client-supplied
narration: es-female
---

## Intent

Versión para publicar en LinkedIn del promo del CRM (`videos/tessera-crm`). Encargo, en palabras
de Eddy: "promocionando nuestro propio CRM… como somos capaces de tenerlo todo bajo control".

## Customizations

- 4:5 vertical (1080×1350): el formato que más pantalla ocupa en el feed móvil de LinkedIn.
- Mirada hacia fuera: abre con lo que gestionamos (Clientes. Vacantes. Candidatos. Equipo.) y
  cierra el gancho con "Todo bajo control."; luego "Hemos construido nuestro propio CRM.",
  "Todo el negocio, en un solo sitio.", "Al momento.", "100% interno. 100% nuestro." y el lema.
- Todo el mensaje va en pantalla, para que funcione sin sonido (LinkedIn reproduce en silencio).
- Mismas reglas que el 16:9: cero cifras, cero nombres de clientes, candidatos o compañeros.

## Voz (versión con locución)

- Voz femenina en español: Kokoro `ef_dora`, generada en local (`assets/vo/`). Guion:
  "Clientes. Vacantes. Candidatos. Equipo. Todo, bajo control." · "Por eso, en Tessera, hemos
  construido nuestro propio CRM. Hecho en casa, a nuestra medida." · "Todo el negocio, en un
  solo sitio. Cada proceso, a un clic." · "Y al momento: cada cambio lo ve todo el equipo, al
  instante." · "Cien por cien interno. Cien por cien nuestro." · "Diseñado y controlado por
  nuestro equipo." · "Tessera." · "Better decisions, together." (esta última con fonética inglesa).
- Cada frase arranca con su escena. La música se agacha sola bajo la voz (sidechain) y todo
  queda en `assets/bgm/soundtrack.wav`; el vídeo final mide −16,4 LUFS.
- `renders/video-linkedin.mp4` es la versión sin voz; `renders/video-linkedin-voz.mp4`, la nueva.
