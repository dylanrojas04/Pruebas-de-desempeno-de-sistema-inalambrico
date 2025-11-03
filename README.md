# 📡 Menú Interactivo – Configuración del Transmisor NRF24L01

Este apartado describe el **menú de configuración interactivo** desarrollado para el transmisor basado en **Raspberry Pi Pico 2W + módulo NRF24L01**, el cual permite seleccionar la **potencia de transmisión** y la **velocidad de datos (data rate)** antes de iniciar la comunicación inalámbrica.

Los códigos completos se encuentran en el repositorio principal del proyecto.

---

## 🎯 Propósito

Este menú fue diseñado para facilitar las **pruebas experimentales de alcance y rendimiento** del enlace inalámbrico punto a punto, cumpliendo con los objetivos de la práctica:

> “Evaluar el desempeño del enlace según la potencia de transmisión y la velocidad de datos configurada.”

---

## 🧭 Funcionamiento general

Al ejecutar el transmisor (TX), el usuario es recibido con un **menú en consola** que permite elegir:

| Parámetro | Opciones disponibles |
|------------|----------------------|
| **Potencia de transmisión** | -18 dBm, -12 dBm, -6 dBm, 0 dBm |
| **Velocidad de transmisión** | 250 kbps, 1 Mbps, 2 Mbps |

Una vez seleccionadas las opciones, el sistema muestra la configuración activa y comienza el envío de datos con dichas condiciones.  
El **receptor (RX)**, a su vez, recibe los valores y los muestra en su pantalla OLED, junto con las lecturas del acelerómetro y la posición del servomotor.

---

## 🧩 Interfaz de usuario

El menú se presenta en formato de texto dentro de **Thonny** o cualquier consola serial compatible:
===== CONFIGURACIÓN TX =====
Seleccione potencia de transmisión:
0: -18 dBm | 1: -12 dBm | 2: -6 dBm | 3: 0 dBm

Seleccione tasa de datos:
0: 250 kbps | 1: 1 Mbps | 2: 2 Mbps


Tras la selección, se muestra un resumen de la configuración elegida:



📡 Configuración seleccionada:
Potencia: -6 dBm | Velocidad: 1 Mbps
🚀 Transmisor listo. Enviando datos cada 100 ms...


---

## 🔍 En el receptor (RX)

En la **pantalla OLED** del receptor se visualiza:



📡 RX - Datos
Ax: +0.12

Ay: -0.45

Az: +0.98

Servo: 120°

Potencia: -6 dBm

Velocidad: 1 Mbps

Esto permite verificar visualmente los parámetros de transmisión durante las pruebas de campo.

---

## 🧪 Aplicación práctica

El menú es utilizado en la etapa de **Prueba outdoor con baterías**, donde se compara el **alcance máximo del enlace** para cada combinación de potencia y tasa de datos.

> ✅ Ejemplo de variables de prueba:
>
> - Potencia de transmisión: 0 dBm  
> - Velocidad de datos: 1 Mbps  
> - Distancia alcanzada: 35 metros  
> - Estado de recepción: estable, sin pérdida de paquetes

---

## 📊 Registro de resultados


---

## 🧪 Resultados experimentales esperados

Durante las pruebas *outdoor*, se evalúa la **distancia máxima alcanzada** y la **estabilidad del enlace** para cada combinación de potencia y velocidad.

| Potencia (dBm) | Velocidad | Alcance estimado (m) | Observaciones |
|----------------|------------|----------------------|----------------|
| **-18 dBm** | 250 kbps | 5 | Comunicación débil, frecuentes pérdidas |
| **-18 dBm** | 1 Mbps | 5.4 | Bajo alcance, sensible a interferencias |
| **-18 dBm** | 2 Mbps | 4.8 | Inestable, pérdidas continuas |
| **-12 dBm** | 250 kbps | 5.8 | Enlace más estable, leve retardo |
| **-12 dBm** | 1 Mbps | 6.28 | Fluido, ocasionales errores de recepción |
| **-12 dBm** | 2 Mbps | 5.9 | Intermitente, dependiente del entorno |
| **-6 dBm** | 250 kbps | 6.8 | Estable, buena sincronización |
| **-6 dBm** | 1 Mbps | 7.1 | Desempeño óptimo en línea de vista |
| **-6 dBm** | 2 Mbps | 7.37  | Correcto, con algunas pérdidas |
| **0 dBm** | 250 kbps | 8.01 | Excelente estabilidad y alcance |
| **0 dBm** | 1 Mbps | 9.53 | Muy estable, sin errores visibles |
| **0 dBm** | 2 Mbps | 15.18 | Buen desempeño, leve reducción de rango |

> 🧾 *Estos valores son referenciales y pueden variar según condiciones ambientales, obstáculos e interferencias en la banda de 2.4 GHz.*
---
