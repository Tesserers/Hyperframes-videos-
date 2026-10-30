# LinkEddy Motion

Sistema de animaciones para el canal LinkEddy. React + Remotion, 1080×1920,
30 fps. Cada pieza es una composición independiente con textos, colores,
encuadre y ritmo editables.

- `MOTION.md`: lenguaje visual (paleta, tipografía, curvas, reglas).
- `INTEGRACION.md`: fichas de montaje de cada pieza.

## Arrancar

Necesitas Node 18+ y ffmpeg no hace falta (Remotion trae el suyo).

```bash
cd videos/linkeddy-motion
npm install
npm run studio        # LinkEddy Motion Studio → http://localhost:5180
```

El Studio permite elegir pieza, reproducir, pausar, moverte frame a frame
(espacio, ← →, Mayús + ← → para saltar 1 s), editar textos y colores, ver la
pieza sobre fondo claro, oscuro, transparente o encima de tu propio clip, con
las zonas seguras de Reels/TikTok. **En local, los botones de Exportar
renderizan de verdad** y te dan el archivo para descargar.

También está el Studio oficial de Remotion, con editor de props:

```bash
npm run remotion
```

## Exportar desde terminal

```bash
node scripts/render.mjs ExperienceParadox prores   # .mov ProRes 4444 con alfa
node scripts/render.mjs ExperienceParadox png      # secuencia PNG con alfa (+ .zip)
node scripts/render.mjs ExperienceParadox webm     # VP9 con alfa
node scripts/render.mjs ExperienceParadox mp4      # preview sin alfa
```

Con tus ajustes del Studio (botón "Copiar ajustes", pegados en un .json):

```bash
node scripts/render.mjs ExperienceParadox prores --props ExperienceParadox.props.json
```

Los archivos salen en `renders/`.

| Formato | Alfa | Para |
|---|---|---|
| ProRes 4444 `.mov` | Sí | Premiere, Final Cut, DaVinci. El bueno para montar |
| Secuencia PNG | Sí | Cualquier editor; también CapCut de escritorio vía import de imágenes |
| WebM VP9 | Sí | Web, After Effects con plugin. CapCut no respeta su alfa |
| MP4 H.264 | **No** | Previsualizar o usar como inserto a pantalla completa |

Un MP4 nunca lleva transparencia: si eliges "Transparente" y exportas MP4, se
renderiza sobre el fondo oscuro.

## Cambiar la identidad

Todo sale de `src/brand/linkeddy.config.ts` (colores, familias, curvas,
duraciones base, zonas seguras). Para cambiar una tipografía: deja los
`.woff2` en `src/brand/fonts/`, actualiza los imports en `src/brand/fonts.ts`
y el nombre de familia en el config.

## Estructura

```
src/
  brand/            linkeddy.config.ts · fonts.ts · fonts/
  motion/           curvas (ease.ts) y ritmo global (frame.tsx)
  components/       Stage y primitivas (MaskReveal, RollingNumber, DrawPath…)
  compositions/     una pieza por archivo + registry.ts (catálogo único)
studio/             LinkEddy Motion Studio (Vite + @remotion/player)
scripts/render.mjs  render programático
renders/            previews MP4 (los masters con alfa no se versionan)
```

Para dar de alta una pieza nueva: crea el componente en `compositions/` y
añádelo a `registry.ts`. Aparece sola en Remotion, en el Studio y en el script.

## Licencia de Remotion

Remotion es gratis para uso individual y empresas de hasta 3 personas. Para
LinkEddy como marca personal no hay problema. Si algún día lo usa una empresa
más grande (Tessera, por ejemplo), necesita licencia de empresa.
