---
workflow: general-video
flow: automation
storyboard: no
message: "Fondo claro en movimiento para la cabecera de las vacantes de TESSERA en Teamtailor"
destination: web
aspect: 1920x1080
language: es
length: 16s
angle: "Versión clara de la malla difusa: fondo Bruma con dos masas Teal, en movimiento, sin texto ni logo"
style_preset: brand-native
narration: none
audio: none
loop: exact
---

## Intent

Segunda referencia de Eddy: fondo Bruma con una masa Teal arriba a la derecha y otra abajo a la
izquierda, con el eslogan y el logo. Pidió lo mismo sin letras ni logos y en movimiento. Es la
versión clara de `../teamtailor-fondo-teal`, con el mismo motor.

## Sistema

- Base Bruma (`#E6ECEC` → `#DCE3E3`). Colores muestreados de la referencia.
- Seis manchas: masa Teal principal arriba a la derecha y su halo, masa Teal abajo a la izquierda,
  un velo Teal muy suave en el centro, un brillo Bruma que recorta las masas y un toque Teal que
  pasea arriba. De 1 a 3 vueltas enteras por bucle; el bucle cierra solo.
- Grano al 12 % en overlay. CRF 24 con `-tune grain`: 3,0 MB.

## Atención: color del título

Sobre este fondo, el título **blanco** que Teamtailor pone por defecto no se lee: 1,45:1 en el
peor fotograma. En **Navy** da 8,1:1. Para usar este fondo, el texto de la cabecera tiene que ir
oscuro en Teamtailor.
