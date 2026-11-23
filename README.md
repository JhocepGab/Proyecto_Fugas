# Sistema de priorización de reparaciones de fugas de agua en Cajamarca
Proyecto final – Análisis de Algoritmos y Estrategias de Programación (UPN 2026-2)

Comparación entre **programación dinámica** y **algoritmo voraz** para decidir qué fugas reparar
con S/ 10 000, 48 horas-persona y 4 trabajadores, dando prioridad a las fugas críticas.

## Archivo
Todo el sistema está en **`proyecto_fugas.py`**, ordenado por secciones:

| Sección | Funciones |
|---|---|
| Apoyo | `preparar_fugas`, `suma_recursiva`, `calcular_totales`, `contar_por_riesgo` |
| Semana 4 y 5 | `ordenamiento_burbuja`, `busqueda_binaria` |
| Paso 1 (las dos estrategias) | `reparar_emergencias` con `heapq` |
| **Estrategia 01** | `alg_voraz` |
| **Estrategia 02** | `prog_dinamica` |
| Comprobación | `fuerza_bruta` |
| Sistema | `resolver`, `comparar`, `prueba_tiempos`, datos de las 12 fugas y menú |

## Cómo ejecutar (Python 3.10 o superior, no hay que instalar nada)
Desde la TERMINAL de VS Code, dentro de la carpeta del proyecto:

    python proyecto_fugas.py

## Menú
1. Ver fugas detectadas
2. Ver fugas ordenadas por prioridad (burbuja)
3. Buscar una fuga por código (búsqueda binaria)
4. Resolver con algoritmo voraz
5. Resolver con programación dinámica
6. Comprobar con fuerza bruta
7. Comparar las estrategias (beneficio, costo, horas, agua, tiempo y memoria)
8. Prueba de tiempos con 6 a 60 fugas (análisis empírico y prueba de estrés)

## Qué semana del curso usa cada parte
| Semana | Tema | Dónde se usa |
|---|---|---|
| 1 | Variables, tipos y operaciones (`//`, `%`, `round`) | Datos del caso, bloques de S/ 50, porcentajes |
| 2 | Funciones, listas y `match` | Todo el programa y el menú |
| 3 | Diccionarios y fuerza bruta (viajero) | Cada fuga es un diccionario; fuerza bruta con `combinations` |
| 4 | Ordenamiento burbuja | Opción 2 |
| 5 | Búsqueda binaria | Opción 3 |
| 7 | Voraz (monedas) y `heapq` | `reparar_emergencias` y `alg_voraz` |
| 8 | Recursividad | `suma_recursiva` y `prog_dinamica` |
| 9 | Divide y vencerás, conteo con diccionario | `prog_dinamica` y `contar_por_riesgo` |

## Resultado con los datos del caso
Voraz = 475, programación dinámica = 484 y fuerza bruta = 484 (la PD encuentra el óptimo).
