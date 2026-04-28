Simulación de Teoría de Colas — Zona de Microondas Universitaria

Este proyecto presenta el análisis y simulación de un sistema de colas en una zona de microondas dentro de un entorno universitario, modelado como un sistema M/M/1 y extendido a diferentes escenarios de mejora, incluyendo un modelo M/M/2.

El objetivo es evaluar el desempeño del sistema real, comparar resultados teóricos y analizar estrategias que reduzcan los tiempos de espera y mejoren la eficiencia operativa.

Descripción del Problema

En horarios cercanos al almuerzo, múltiples estudiantes utilizan un único microondas, generando congestión y tiempos de espera. Este comportamiento se modela como un sistema de colas donde:

Los usuarios llegan de manera aleatoria (proceso de Poisson)
Los tiempos de servicio son variables (distribución exponencial)
Existe un único servidor (microondas)
Objetivos
Analizar el sistema real mediante datos observados
Modelar el sistema como una cola M/M/1
Calcular indicadores de desempeño (λ, μ, ρ, Wq, Lq, etc.)
Comparar resultados teóricos vs observados
Simular escenarios de mejora sin modificar y con modificación de infraestructura
Estructura del Proyecto

El proyecto se divide en dos grandes partes:

1. Análisis del Sistema Real

Incluye:

Procesamiento de datos de dos sesiones experimentales
Cálculo de:
Tasa de llegada (λ)
Tasa de servicio (μ)
Utilización (ρ)
Tiempo promedio de espera (Wq)
Tiempo total en el sistema (W)
Comparación con el modelo teórico M/M/1
2. Simulación de Escenarios

Se implementan diferentes escenarios usando modelos analíticos de teoría de colas:

Escenario 1: Reducción del tiempo de servicio
Disminución del 5% al 20%
Impacto directo en μ
Reduce significativamente Wq
Escenario 2: Control de servicios largos
Imposición de un tiempo máximo de uso
Efectivo solo si el tope es menor al promedio actual
Escenario 3: Distribución de llegadas
Reducción de λ (5%, 10%, 15%)
Simula cambios de comportamiento de usuarios
Escenario 4: Segundo microondas (M/M/2)
Sistema con dos servidores
Reducción drástica de tiempos de espera (>90%)
Escenario 5: Escenario combinado
Reducción simultánea de λ y tiempo de servicio
Mejor relación costo-beneficio sin inversión física
Tecnologías Utilizadas
Python 3
Pandas
NumPy
Matplotlib
Google Colab (ejecución del código)
Resultados Generados

El proyecto genera:

Tablas de indicadores por sesión
Comparaciones entre escenarios
Gráficas:
Tiempo de espera (Wq)
Tiempo total en sistema (W)
Utilización (ρ)
Longitud de cola (Lq)
Reducción porcentual de tiempos
Comparación M/M/1 vs M/M/2

Archivos exportados en formato .png.

Principales Hallazgos
El sistema es estable (λ < μ), pero presenta congestión por llegadas agrupadas
La espera no depende solo del número de usuarios, sino de:
Variabilidad en el servicio
Concentración de llegadas
Reducir el tiempo de servicio tiene un impacto no lineal en la espera
Agregar un segundo microondas elimina casi completamente la cola
El escenario combinado ofrece la mejor solución sin costos adicionales
Cómo Ejecutar
Abrir el código en Google Colab o entorno local
Ejecutar las celdas en orden
Revisar:
Tablas impresas en consola
Gráficas generadas automáticamente
Archivos .png exportados
