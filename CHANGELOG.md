# Changelog - Cryptography Lab

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [3.0] - 2026-03-04

### Añadido

#### Nuevo Módulo: Optimización Heurística de Pollard Rho (`pollard_rho/`)
- **Notebook Jupyter** `pollard_rho_challenge.ipynb`: implementación completa del experimento de optimización
  - Grid Search sobre 40 configuraciones únicas (5 valores de K × 4 métodos de entropía × 2 estrategias)
  - Evaluación en 5 tamaños de primo: 10, 14, 18, 22 y 24 bits
  - Algoritmo de Floyd (tortuga y liebre) como detector de ciclos
  - Algoritmo clásico (mod 3 + elevación al cuadrado) como referencia comparativa
- **Caminatas de Teske Aleatorias**: sustitución de la elevación al cuadrado por multiplicadores precalculados $M_i \equiv g^{c_i} \cdot h^{d_i} \pmod{p}$
- **Selector de Entropía por Desplazamiento de Bits**: extracción de bits intermedios (`shift_4`) para elegir la rama de iteración con mayor dispersión geométrica
- **Métrica de Score Normalizada**: ratio pasos/√N que pondera por igual todos los tamaños de primo evaluados

#### Documentación Técnica `pollard_rho/README.md`
- **Sección 7**: Extractos clave del código extraídos directamente del notebook
  - §7.1 Generación de parámetros DLP (`generar_parametros_dlp`)
  - §7.2 Preparación de multiplicadores Teske (`preparar_multiplicadores`)
  - §7.3 Función de paso optimizada con selector de entropía (`step_optimizado`)
  - §7.4 Algoritmo clásico de referencia (`pollard_rho_classico_steps`)
  - §7.5 Espacio de búsqueda Grid Search (`ESPACIO_BUSQUEDA`)
- **Sección 8**: Galería completa de resultados visuales (8 gráficas)
  - §8.1 Comparación directa de pasos (clásico vs mejor configuración)
  - §8.2 Ratio de pasos mejor configuración / clásico
  - §8.3 Mejoras porcentuales por tamaño de primo
  - §8.4 Distribución de scores de las 40 configuraciones
  - §8.5 Scores por método de entropía (boxplot)
  - §8.6 Scores por estrategia iterativa (boxplot)
  - §8.7 Heatmap K × método de entropía
  - §8.8 Comparación de las 5 mejores configuraciones

### Resultados Clave

**Configuración ganadora:**
```
K = 8 particiones
Entropía: shift_4  (x >> 4) % K
Estrategia: teske_aleatorio
Score: 0.4019  (pasos / √N)
```

**Mejoras sobre el algoritmo clásico:**
```
10 bits:  390  → 14  pasos  (96.4% de mejora)
14 bits:  1830 → 51  pasos  (97.2% de mejora)
18 bits:  6390 → 256 pasos  (96.0% de mejora)
22 bits: 29265 → 560 pasos  (98.1% de mejora)
24 bits: 60030 → 1638 pasos (97.3% de mejora)
```

### Información Técnica
- **Módulos añadidos**: `pollard_rho/`
- **Archivos de imagen generados**: 8 (`img/*.png`)
- **Configuraciones evaluadas**: 40
- **Reducción media de pasos**: > 96 % en todos los espectros

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

