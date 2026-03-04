# Cryptography – Prácticas del Grado en Ingeniería de Datos e Inteligencia Artificial (UAX)

Este repositorio reúne distintas prácticas, ejercicios y pequeños proyectos relacionados con **criptografía**, **esteganografía** y seguridad de la información, desarrollados en el contexto del **Grado en Ingeniería de Datos e Inteligencia Artificial** de la **Universidad Alfonso X el Sabio (UAX)**. La idea es tener en un mismo sitio todo el material técnico que va surgiendo en las asignaturas del grado, de forma ordenada y fácil de consultar, tanto para uso personal como para posibles revisiones en el futuro.

El repositorio está vivo: se irá ampliando a medida que aparezcan nuevas tareas, proyectos o experimentos. Este documento solo pretende dar una visión general y un punto de partida para navegar por las carpetas.

---

## Estructura general del repositorio

El contenido se organiza por carpetas, normalmente una por práctica o tema. Desde aquí puedes hacerte una idea rápida de qué hay en cada sitio y entrar en más detalle cuando lo necesites. A medida que se añadan nuevas prácticas, este índice se actualizará con una breve descripción de cada una.

### `steganography-lsb/` – Esteganografía con bits menos significativos

Esta carpeta recoge una práctica centrada en **esteganografía basada en LSB (Least Significant Bit)** aplicada a imágenes digitales. El proyecto implementa un sistema completo que combina cifrado AES-256-GCM con técnicas avanzadas de ocultación y análisis forense.

**Características principales:**
- **Cifrado robusto:** AES-256-GCM con autenticación integrada
- **Posiciones aleatorias:** Distribución no secuencial mediante PRNG determinista
- **Análisis forense:** Implementación de RS Steganalysis, Chi-cuadrado e histogramas
- **Optimización avanzada:** Algoritmo de búsqueda 13.59x más rápido que fuerza bruta
- **Generación de datasets:** Sistema para crear 100 imágenes con mensaje oculto en una aleatoria
- **Análisis de complejidad:** Evaluación teórica O(N×W×H) vs O(N) con pruebas empíricas
### `pollard_rho/` – Optimización Heurística del Algoritmo Pollard Rho

Esta carpeta recoge un experimento de **optimización del algoritmo Pollard Rho** aplicado al Problema del Logaritmo Discreto (DLP). El objetivo fue superar empíricamente al algoritmo clásico (partición mod 3 con elevación al cuadrado) diseñando una función de iteración alternativa basada en **caminatas multiplicativas de Teske** y un **selector de rama por desplazamiento de bits**.

**Puntos clave:**
- **Grid Search** sobre 40 configuraciones: 5 valores de K × 4 métodos de entropía × 2 estrategias de iteración
- **Métrica:** ratio pasos/√N promediado en primos de 10 a 24 bits
- **Configuración ganadora:** K=8 particiones, `shift_4` como selector de entropía, caminatas aleatorias de Teske
- **Resultado:** reducción de pasos superior al **96 % en todos los espectros** frente al algoritmo clásico
- **Invariante verificado:** $x_k \equiv g^{a_k} \cdot h^{b_k} \pmod{p}$ se mantiene tras cada paso multiplicativo

> Ver [pollard_rho/README.md](pollard_rho/README.md) para la memoria técnica completa con código, análisis y visualizaciones.

---

## Cómo trabajar con este repositorio

La idea es que este repositorio funcione como un cuaderno de trabajo a largo plazo. Lo normal será clonar el repositorio en tu entorno de desarrollo (por ejemplo, DataSpell), entrar en la carpeta de la práctica que quieras revisar y seguir las instrucciones específicas de esa carpeta (si tiene su propio `README.md`) o simplemente abrir los notebooks y scripts relevantes.

En un flujo típico con Python podrías:

1. Crear y activar un entorno virtual en la raíz del repositorio.
2. Instalar las dependencias indicadas por cada práctica (por ejemplo, las de `steganography-lsb/` usando su `requirements.txt`).
3. Abrir el cuaderno Jupyter o ejecutar los scripts que acompañan a la práctica.

Por ejemplo, en PowerShell, situándote en la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\steganography-lsb\requirements.txt
jupyter notebook .\steganography-lsb\LSB_Lab_Notebook.ipynb
```

A partir de ahí, cada carpeta podrá tener sus propias instrucciones adicionales, dependencias concretas o notas técnicas.

---

## Mantener el repositorio al día

Aunque está pensado principalmente para uso personal durante el grado, es útil mantener una mínima estructura para que el repositorio siga siendo claro con el paso del tiempo. Algunas ideas sencillas:

- Cada vez que se cree una nueva práctica o proyecto, añadir una carpeta con un nombre descriptivo y, si es posible, un pequeño `README.md` dentro explicando el objetivo y cómo ejecutar el código.
- Actualizar este `README.md` principal cuando se añadan carpetas nuevas que merezcan aparecer en el índice, sumando una breve descripción similar a la de `steganography-lsb/`.
- Mantener al día los archivos de requisitos (`requirements.txt`, entornos de conda, etc.) para poder reconstruir los entornos sin demasiadas sorpresas cuando se retomen las prácticas más adelante.
- Anotar cualquier decisión técnica relevante o problemas encontrados (versiones conflictivas, librerías que dieron error, mejoras pendientes) para no tener que redescubrirlo todo en el futuro.

Con el tiempo, la intención es que este repositorio se convierta en una especie de resumen práctico de las asignaturas de criptografía y seguridad dentro del **Grado en Ingeniería de Datos e Inteligencia Artificial (UAX)**: un sitio donde vuelvas cuando quieras recordar cómo resolviste una práctica, reutilizar código o enseñar tu trabajo técnico en este ámbito.
