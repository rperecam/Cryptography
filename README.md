# Cryptography – Grado en Ingeniería de Datos e Inteligencia Artificial (UAX)

Este repositorio reúne prácticas, ejercicios y proyectos desarrollados en el marco del **Grado en Ingeniería de Datos e Inteligencia Artificial** de la **Universidad Alfonso X el Sabio (UAX)**. Su objetivo es servir como base de trabajo, referencia y documentación de las distintas actividades relacionadas con **criptografía**, **esteganografía** y seguridad de la información, entre otros contenidos afines.

> **Nota:** El repositorio está vivo y se irá actualizando a medida que se incorporen nuevas asignaturas, prácticas y materiales.

---

## Estructura del repositorio

A continuación se describen las carpetas principales del repositorio. Este índice se irá ampliando conforme se añadan nuevos módulos y proyectos.

### 1. `lsb/`

Carpeta dedicada a un proyecto/práctica de **esteganografía basada en el método LSB (Least Significant Bit)** aplicado a imágenes.

**Contenido destacado:**

- `LSB_Lab_Notebook.ipynb`  
  Cuaderno Jupyter con el desarrollo experimental del sistema de esteganografía LSB. Suele incluir:
  - Explicación teórica del método LSB.
  - Pruebas de inserción y extracción de mensajes en imágenes.
  - Análisis de calidad visual y posibles artefactos.

- `MEMORIA_TECNICA_PROYECTO_LSB.md`  
  Memoria técnica del proyecto LSB, con la descripción formal de:
  - Objetivos del proyecto.
  - Metodología empleada.
  - Diseño del sistema y decisiones técnicas.
  - Resultados, conclusiones y posibles mejoras.

- `requirements.txt`  
  Lista de dependencias de Python necesarias para ejecutar los notebooks y scripts de la carpeta `lsb/`. Útil para reproducir el entorno de trabajo en otros equipos.

- `dataset_images/`  
  Conjunto de imágenes de ejemplo utilizadas como **covers** (imágenes portadoras) para las pruebas de inserción de mensajes mediante LSB.

- `test/scripts/`  
  Scripts de prueba y demostración del sistema de esteganografía:
  - `demo.py`: suele contener un flujo de ejemplo para esconder y recuperar mensajes desde una imagen, generando salidas ilustrativas.
  - `stego_system.py`: posibles implementaciones de las funciones o clases que encapsulan la lógica de inserción y extracción de datos mediante LSB.

- `test/scripts/resultados_stego/`  
  Carpeta donde se guardan resultados generados por los scripts de prueba, por ejemplo:
  - Imágenes de entrada (cover).
  - Imágenes con información oculta.
  - Diferencias visuales entre imágenes.
  - Informes de resultados y mensajes recuperados.

---

## Cómo usar este repositorio

1. **Clonar el repositorio** (desde GitHub u otra plataforma donde esté alojado).
2. **Crear y activar un entorno virtual de Python** (recomendado) para aislar dependencias.
3. **Instalar dependencias específicas de cada proyecto** (por ejemplo, las de `lsb/` usando su `requirements.txt`).
4. Ejecutar los **notebooks** o **scripts** correspondientes según la práctica que se desee revisar.

Ejemplo para la carpeta `lsb/` (en PowerShell, situándote en la raíz del repositorio):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\lsb\requirements.txt
jupyter notebook .\lsb\LSB_Lab_Notebook.ipynb
```

---

## Lineas futuras y ampliaciones

Este repositorio se ampliará progresivamente con:

- Nuevas prácticas de **criptografía clásica y moderna**.
- Ejercicios de **seguridad de la información**, **esteganografía avanzada** y **ciberseguridad** aplicada a datos.
- Proyectos integradores que combinen **Inteligencia Artificial**, **procesamiento de datos** y **métodos criptográficos**.

Se recomienda consultar periódicamente este `README.md`, ya que se actualizará para reflejar la estructura más reciente del repositorio y facilitar la navegación por las distintas carpetas y proyectos.

