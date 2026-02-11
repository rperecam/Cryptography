# Changelog - Cryptography Lab

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [2.0] - 2026-02-11

### Añadido

#### Análisis Forense Completo
- **Generador de Dataset**: Sistema automatizado para crear 100 imágenes de ruido con mensaje oculto en una aleatoria
- **Algoritmo de Búsqueda Optimizado**: Implementación con terminación temprana (early termination)
  - Speedup: 13.59x más rápido que fuerza bruta en imágenes 1000×1000
  - Complejidad reducida de O(N×W×H) a O(N)
- **RS Steganalysis**: Análisis Regular-Singular para detectar manipulación LSB
  - Detección de anomalías con diferencia >3% entre Rm y Sm
  - Análisis por canal RGB individual
- **Análisis Chi-Cuadrado**: Prueba estadística para detectar desviaciones en distribución LSB
- **Análisis de Histograma**: Comparación de distribución de valores de píxeles

#### Documentación Ampliada
- **Sección 10**: Análisis Forense y Estegoanálisis
  - Algoritmos de búsqueda (fuerza bruta vs optimizado)
  - Técnicas de estegoanálisis (RS, Chi-cuadrado, histograma)
  - Resultados experimentales con tablas comparativas
  - Recomendaciones de uso seguro
- **Sección 11**: Análisis de Complejidad y Escalabilidad
  - Complejidad teórica O(N×W×H) vs O(N)
  - Análisis de cuellos de botella (I/O vs CPU)
  - Proyecciones para 1 millón de imágenes
  - Estrategias de paralelización
  - Ley de Amdahl aplicada al sistema
- **Anexo G**: Fórmulas de Análisis Forense
- **Anexo H**: Tabla de Complejidad Comparativa
- **Anexo J**: Glosario Ampliado (términos forenses y de complejidad)

#### Notebook Jupyter
- **Parte 2**: Detector Forense con dos implementaciones
  - `search_brute_force()`: Búsqueda exhaustiva O(N×W×H)
  - `search_optimized()`: Búsqueda con terminación temprana O(N)
- **Parte 3**: Análisis de Estegoanálisis
  - `rs_steganalysis_detect()`: Implementación vectorizada
  - `chi_square_analysis()`: Prueba Chi-cuadrado
  - `histogram_analysis()`: Análisis de distribución
- **Parte 4**: Visualización de Tiempos
  - Función `run_complexity_experiments()`
  - Gráficas comparativas de rendimiento
  - Anotaciones de tiempo en gráficos
- **Respuestas a Preguntas de Análisis**:
  - Complejidad teórica de ambos enfoques
  - Identificación de cuellos de botella
  - Análisis de escalabilidad
  - Seguridad de la esteganografía

### Modificado

#### Mejoras en Documentación
- **Resumen Ejecutivo**: Añadidas métricas de speedup (13.59x) y detección RS (3.67%)
- **Índice**: Reorganizado con nuevas secciones 10 y 11
- **Conclusiones**: Actualizadas con logros de análisis forense y complejidad
- **Lecciones Aprendidas**: 
  - Añadida lección sobre I/O como cuello de botella (61% del tiempo)
  - Análisis de complejidad práctica vs teórica
  - Efectividad del estegoanálisis
- **Trabajo Futuro**:
  - Distribución LSB consciente para evitar detección
  - Búsqueda distribuida para datasets masivos
  - Machine Learning para detección automatizada
- **Referencias**: Añadidas 4 referencias nuevas sobre estegoanálisis y análisis de complejidad

#### Métricas Actualizadas
- Tabla de resultados clave incluye ahora speedup y detección RS
- Tabla de métricas finales ampliada con detección forense y escalabilidad
- Resultados experimentales con 3 resoluciones (200×200, 500×500, 1000×1000)

### Información Técnica

**Resultados de Benchmarks:**
```
Resolución 1000×1000, Dataset 100 imágenes:
- Fuerza Bruta:  221.37 segundos
- Optimizado:     16.28 segundos
- Speedup:        13.59x

Análisis RS (imagen con 95% capacidad):
- Imagen Limpia:  Rm=35.33%, Sm=34.00%, Diff=1.33%
- Imagen Stego:   Rm=33.83%, Sm=37.50%, Diff=3.67%

Análisis Chi-cuadrado:
- Imagen Limpia:  χ² = 225.00
- Imagen Stego:   χ² = 324.00 (+44%)
```

**Complejidad Algorítmica:**
```
T_brute(N, W, H) = O(N × W × H)
T_opt(N) = O(N)

Speedup teórico: (W × H × 3) / k
Para 1000×1000 e k=400: 7,500x teórico
Speedup real: 13.59x (limitado por I/O)
```

### Versión
- **Número de versión**: 1.0 → 2.0 → 2.1
- **Páginas de documentación**: 50+ → 70+ → 75+
- **Palabras en README**: ~15,000 → ~20,000 → ~22,000
- **Secciones principales**: 12 → 14 → 14
- **Anexos**: 7 → 11 → 12
- **Imágenes documentadas**: 0 → 0 → 5

---

## [1.0] - 2026-02-09

### Añadido

#### Sistema Base
- **Cifrado AES-256-GCM**: Implementación con autenticación integrada
- **Derivación de claves PBKDF2**: 100,000 iteraciones con SHA-256
- **Posiciones aleatorias**: PRNG determinista para distribución no secuencial
- **Estrategia híbrida**: Header/salt secuencial, payload aleatorio

#### Componentes
- `stego_system.py`: Motor principal con clases `CryptoEngine` y `LSBSteganography`
- `demo.py`: Script de demostración con análisis visual y estadístico
- Análisis de capacidad, visual y estadístico

#### Documentación
- README.md con 12 secciones principales
- 7 anexos con tablas, fórmulas y glosario
- Instrucciones de uso y ejemplos

### Resultados Iniciales
- PSNR: 51.34 - 80.98 dB
- Capacidad máxima probada: 171,831 bytes (95.49%)
- MSE: 0.000519 - 0.477348
- Integridad: 100%

---

## Leyenda

- **Añadido**: Nuevas características
- **Modificado**: Cambios en funcionalidad existente
- **Deprecado**: Características que serán eliminadas
- **Eliminado**: Características eliminadas
- **Corregido**: Corrección de bugs
- **Seguridad**: Cambios relacionados con vulnerabilidades

