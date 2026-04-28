# Simulación de Teoría de Colas — Microondas Universitario

Sistema de análisis y simulación basado en teoría de colas (modelos M/M/1 y M/M/2) aplicado a una zona de microondas en un entorno universitario.

El proyecto integra datos reales, modelado matemático y simulación computacional para evaluar el desempeño del sistema y proponer mejoras operativas.

---

## Descripción

En horarios de alta demanda, múltiples usuarios utilizan un único microondas, generando filas y tiempos de espera. Este comportamiento se modela como un sistema de colas con las siguientes características:

- Llegadas aleatorias (proceso de Poisson, λ)  
- Tiempos de servicio variables (distribución exponencial, μ)  
- Un único servidor (microondas)  

---

## Objetivos

- Analizar el comportamiento real del sistema mediante datos observados  
- Calcular indicadores de desempeño (λ, μ, ρ, Wq, W, Lq, L)  
- Comparar resultados teóricos con datos reales  
- Simular escenarios de mejora  
- Evaluar alternativas para reducir tiempos de espera  

---

## Modelos Utilizados

### M/M/1 (Sistema actual)
- Un servidor  
- Llegadas aleatorias  
- Servicio exponencial  

### M/M/2 (Escenario mejorado)
- Dos servidores  
- Misma tasa de llegada  
- Reducción significativa de congestión  

---

## Estructura del Proyecto

El proyecto se divide en dos componentes principales:

### 1. Análisis del sistema real

Incluye:

- Procesamiento de datos de dos sesiones experimentales  
- Cálculo de:
  - Tasa de llegada (λ)  
  - Tasa de servicio (μ)  
  - Utilización (ρ)  
  - Tiempo promedio de espera (Wq)  
  - Tiempo total en el sistema (W)  
  - Longitud promedio de cola (Lq)  
  - Número promedio de usuarios en el sistema (L)  
- Comparación entre valores observados y teóricos del modelo M/M/1  

---

### 2. Simulación de escenarios

Se implementan cinco escenarios utilizando modelos analíticos de teoría de colas:

#### Escenario 1: Reducción del tiempo de servicio
- Disminución entre 5% y 20%  
- Incremento de la tasa de servicio (μ)  
- Reducción no lineal del tiempo de espera (Wq)  

#### Escenario 2: Control de servicios largos
- Imposición de un tiempo máximo de uso  
- Solo genera impacto si el tope es menor al promedio observado  
- Reduce la variabilidad del sistema  

#### Escenario 3: Distribución de llegadas
- Reducción de la tasa de llegada (λ) entre 5% y 15%  
- Simula cambios en el comportamiento de los usuarios  
- Disminuye la congestión en horas pico  

#### Escenario 4: Segundo microondas (M/M/2)
- Sistema con dos servidores  
- Aplicación del modelo Erlang-C  
- Reducción de más del 90% en el tiempo de espera  

#### Escenario 5: Escenario combinado
- Reducción simultánea del 10% en λ y en el tiempo de servicio  
- Efecto conjunto no lineal  
- Mejor relación costo-beneficio sin inversión en infraestructura  

---

## Tecnologías Utilizadas

- Python 3  
- Pandas  
- NumPy  
- Matplotlib  
- Google Colab  

---

## Resultados Generados

El sistema produce:

- Tablas de indicadores por sesión  
- Comparación completa entre escenarios  
- Evaluación de desempeño del sistema  
- Gráficas exportadas en formato PNG:
  - Tiempo de espera en cola (Wq)  
  - Tiempo total en el sistema (W)  
  - Factor de utilización (ρ)  
  - Longitud de cola (Lq)  
  - Reducción porcentual de tiempos  
  - Comparación entre modelos M/M/1 y M/M/2  

---

## Ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
