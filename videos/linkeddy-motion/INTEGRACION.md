# Fichas de integración

Cómo meter cada pieza en el montaje. Timings a 30 fps y `pace = 1`.

---

## 01 — The Experience Paradox

| | |
|---|---|
| **Duración** | 7,2 s (216 frames). Con 2 ofertas en vez de 4: 6,6 s |
| **Guion** | «Quieres encontrar tu primer trabajo. **Abres una oferta** y te piden dos años de experiencia. **Abres otra** y te piden tres.» |
| **Plano recomendado** | Tú con el portátil, plano medio o medio corto. Alternativa: inserto a pantalla completa |
| **Archivo** | `ProRes 4444` (.mov con alfa) o secuencia PNG |

**Sincronía con la voz**

| Frame | Tiempo | Qué pasa | Debe coincidir con |
|---|---|---|---|
| 0 | 0:00 | Entra la oferta 1 | «Abres una oferta…» |
| 16 | 0:16 | La cifra rueda hasta el 2 | «…dos años de experiencia» |
| 48 | 1:18 | Entra la oferta 2 y empuja a la 1 | «Abres otra…» |
| 64 | 2:04 | La cifra rueda (pasa por el 2) hasta el 3 | «…y te piden tres» |
| 86 | 2:26 | Círculo a mano y «¿Becario… con 3 años?» | Pausa o gesto tuyo |
| 128 | 4:08 | Se acumulan más ofertas | Siguiente frase |
| 182 | 6:02 | La pila se cuadra y sale | Corte o cambio de plano |

Regla práctica: coloca el clip para que el **frame 48 caiga justo en «Abres otra»**.
Lo demás encaja solo. Si hablas más despacio, baja `Ritmo` a 0,85–0,9 en el
Studio (alarga toda la coreografía sin romperla).

**Posición en pantalla**

- *Inserto a pantalla completa* (`Pantalla completa`): fondo claro de marca.
  Todo el contenido queda entre y 220 y y 1480, fuera de la UI de Reels/TikTok.
  Es la opción más limpia: la pieza explica sola el chiste.
- *Overlay sobre ti* (`Overlay bajo`, escala 0,58, +340 px): la pila ocupa el
  tercio inferior, por debajo de tu cara. **Ocupa la franja de subtítulos**:
  durante esos 7 s apaga los subtítulos o súbelos por encima de la pila; la
  propia pieza ya dice lo que estás diciendo.
- *Plano de escritorio o manos* (`Overlay alto`, escala 0,58, -330 px):
  cuando la cámara mira al portátil y no se te ve la cara.

**Entrada y salida**

- Entrada: la oferta sube por máscara desde abajo, con un giro que se corrige.
  Funciona como corte directo desde tu plano; no hace falta transición.
- Salida: la pila se cuadra y desaparece hacia arriba por una máscara fija.
  Corta al siguiente plano en el frame 210 o deja que termine (216).

**Montaje**

- No añadas fundido ni zoom encima: la pieza ya trae su entrada y salida.
- Si vas en overlay, una ligera sombra no hace falta: las tarjetas ya la traen.
- Un "tick" de papel o un click suave en los frames 0 y 48 funciona muy bien.
  Nada de whooshes.
- Para la versión corta (solo las dos ofertas del guion), quita las ofertas 3
  y 4 en el Studio.
