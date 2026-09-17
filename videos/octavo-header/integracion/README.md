# Cómo montarlo en el hero

## El cambio

En `#inicio` hay hoy dos capas encima del fondo: la foto y el velo. **Solo se toca la primera.**

```html
<!-- ANTES -->
<img src="1d418382-…" alt="Casa Octavo frente al mar al amanecer"
     style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:octZoom 28s …">

<!-- DESPUÉS -->
<video poster="/media/octavo-header-poster.jpg"
       autoplay muted loop playsinline preload="metadata" aria-hidden="true"
       style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <source src="/media/octavo-header.webm" type="video/webm">
  <source src="/media/octavo-header.mp4"  type="video/mp4">
</video>
```

La segunda capa —el `<img>` del degradado `035b6d4f`— **se queda como está**. El vídeo viene
sin ese degradado justamente para que no se duplique.

Y sobra el `animation: octZoom` de la foto: el movimiento ya va dentro del vídeo.

### Por qué cada atributo

- `muted` — sin él ningún navegador autorreproduce. Los ficheros además no llevan pista de
  audio, así que no hay nada que silenciar ni que descargar.
- `playsinline` — sin él, Safari en iPhone abre el vídeo a pantalla completa.
- `loop` — el bucle es exacto: el último fotograma empalma con el primero sin salto.
- `poster` — lo que se ve mientras carga. Es el fotograma 0, así que no hay parpadeo al entrar.
- `preload="metadata"` — no descarga los 2,9 MB hasta que hace falta.
- `aria-hidden="true"` — es decoración; el mensaje lo ponen el `h1` y el párrafo.

## Qué fichero usar

| Fichero | Para qué |
|---|---|
| `octavo-header.mp4` · 2,9 MB | El principal. 1920×1080, H.264, `faststart`. |
| `octavo-header.webm` · 2,4 MB | El mismo en VP9. Ponlo **primero** en el `<source>`: pesa medio mega menos y lo entienden Chrome, Firefox y Edge. Safari cae al MP4. |
| `octavo-header-720.mp4` · 1,4 MB | 1280×720, para servir por `media` en móvil. |
| `octavo-header-aa.mp4` / `.webm` | Igual, pero con el velo subido hasta que el hero **pasa WCAG AA**. Ver más abajo. |
| `octavo-header-velo.mp4` · 2,2 MB | Con el degradado ya incrustado, para usarlo donde ese velo no exista. **No** en el hero actual. |
| `octavo-header-poster.jpg` | El `poster`. |

Para servir el ligero solo en móvil, sin JavaScript:

```html
<video poster="/media/octavo-header-poster.jpg" autoplay muted loop playsinline
       preload="metadata" aria-hidden="true"
       style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <source src="/media/octavo-header.webm"    type="video/webm" media="(min-width: 900px)">
  <source src="/media/octavo-header.mp4"     type="video/mp4"  media="(min-width: 900px)">
  <source src="/media/octavo-header-720.mp4" type="video/mp4">
</video>
```

Y respetar a quien pide menos movimiento —son 16 s de cámara continua detrás de un titular—:

```css
@media (prefers-reduced-motion: reduce) {
  #inicio video { display: none; }
  #inicio { background: url(/media/octavo-header-poster.jpg) center/cover; }
}
```

## Lo del contraste, que conviene leer

El hero de hoy ya va justo. Medido sobre vuestro propio marcado, con vuestra foto y vuestro
degradado, tomando el percentil 5 de luminancia bajo cada bloque de texto:

| Texto | Hoy | Exige WCAG AA |
|---|---|---|
| `h1` primera línea, basalto 104 px | 9,79:1 | 3:1 ✅ |
| `la casa de tu vida.`, almagre 104 px | **2,78:1** | 3:1 ❌ |
| Párrafo, `#383D42` 21 px | **4,00:1** | 4,5:1 ❌ |

Eso es anterior al vídeo. Lo que sí era mío: los planos 3 y 4 son fotos más oscuras justo donde
cae el texto, y sin corregir hundían la itálica a 1,58:1 y el párrafo a 1,83:1. Por eso cada
plano lleva su propio velo de yeso, con la forma del bloque de texto —plano hasta x=940 y
cayendo a cero en x=1460, porque vuestro degradado ya ha bajado al 7 % en x=1267 y el texto
termina en x=1014—. Con eso, el vídeo **no empeora nada**:

| Texto | Hoy | Plano 1 | Plano 2 | Plano 3 | Plano 4 |
|---|---|---|---|---|---|
| `h1` | 9,79 | 9,79 | 8,03 | 7,49 | 7,40 |
| itálica | 2,78 | 2,78 | 2,91 | 2,81 | 2,85 |
| párrafo | 4,00 | 3,95 | 4,00 | 4,00 | 3,95 |

Si queréis además **corregir lo que ya venía de antes**, usad `octavo-header-aa.mp4`: sube el
velo lo justo y deja itálica ≥ 3,12:1 y párrafo ≥ 4,51:1 en los cuatro planos. Cuesta algo de
foto en la mitad izquierda; es una decisión vuestra y por eso va aparte y no como principal.

Arreglarlo del todo sin tocar el vídeo es más limpio y son dos líneas de CSS vuestras: subir el
peso del párrafo de 400 a 500, o pasar su color de `#383D42` a `#2A2E33` (grafito, que sí está
en vuestro brandkit). Cualquiera de las dos os mete en AA sin velar la fotografía.

## Comprobarlo

`hero-preview.html` es vuestro hero real con el vídeo ya montado. Ábrelo en un navegador:
lo que se ve ahí es lo que se verá en producción.
