# Cryptography – Prácticas del Grado en Ingeniería de Datos e Inteligencia Artificial (UAX)

Este repositorio reúne distintas prácticas, ejercicios y pequeños proyectos relacionados con **criptografía**, **esteganografía** y seguridad de la información, desarrollados en el contexto del **Grado en Ingeniería de Datos e Inteligencia Artificial** de la **Universidad Alfonso X el Sabio (UAX)**. La idea es tener en un mismo sitio todo el material técnico que va surgiendo en las asignaturas del grado, de forma ordenada y fácil de consultar, tanto para uso personal como para posibles revisiones en el futuro.

El repositorio está vivo: se irá ampliando a medida que aparezcan nuevas tareas, proyectos o experimentos. Este documento solo pretende dar una visión general y un punto de partida para navegar por las carpetas.

---

## Estructura general del repositorio

El contenido se organiza por carpetas, normalmente una por práctica o tema. Desde aquí puedes hacerte una idea rápida de qué hay en cada sitio y entrar en más detalle cuando lo necesites. A medida que se añadan nuevas prácticas, este índice se actualizará con una breve descripción de cada una.

### `steganography-lsb/` – Esteganografía con bits menos significativos

Esta carpeta recoge una práctica centrada en **esteganografía basada en LSB (Least Significant Bit)** aplicada a imágenes digitales. El objetivo es explorar cómo ocultar y recuperar mensajes dentro de imágenes, ver el efecto que tiene sobre la calidad visual y entender las limitaciones de este enfoque.

En `steganography-lsb/` encontrarás principalmente:

- Un cuaderno Jupyter (`LSB_Lab_Notebook.ipynb`) donde se explica paso a paso el método, se ilustran los conceptos básicos y se prueban distintos ejemplos de inserción y extracción de mensajes.
- Un conjunto de imágenes de ejemplo en `dataset_images/`, usadas como imágenes portadoras (cover) para incrustar la información.
- Una carpeta de pruebas `test/` con scripts en `scripts/` que automatizan el proceso de ocultar texto en imágenes, generar las imágenes estego y recuperar el mensaje oculto.
- Una carpeta `test/stego-results/` con resultados de ejemplo: la imagen original, la imagen con información oculta, el mensaje recuperado y un pequeño informe sobre lo ocurrido en la prueba.
- Un archivo `requirements.txt` con las dependencias de Python necesarias para ejecutar el notebook y los scripts.

La práctica está planteada para ejecutarse en un entorno Python estándar. La forma habitual de trabajar consiste en crear un entorno virtual, instalar las dependencias y abrir el cuaderno o los scripts para ir experimentando con otras imágenes o mensajes.

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
