# Predictor Mundial V4.0

Un orquestador predictivo avanzado para partidos de fútbol, diseñado específicamente para proyectar resultados de la Copa Mundial 2026. Combina inteligencia artificial, datos del mercado financiero y la intuición humana.

---

## 🚀 Guía Rápida: Cómo Utilizar el Sistema

El sistema fue diseñado para ser utilizado desde la consola de comandos. Como analista o entrenador, tu flujo de trabajo es muy sencillo:

### 1. Ejecutar el Simulador
Abre tu terminal (Termux, Linux o CMD) en la carpeta del proyecto y ejecuta:
```bash
python orquestador.py
```

### 2. Panel Interactivo
El sistema comenzará a descargar las últimas noticias y a leer el historial de partidos. Luego se pausará y te hará una pregunta clave:
> *¿Deseas modificar alguna ponderación particular? (s/n):*

- **Si presionas `n` (No)**: El sistema correrá la simulación inmediatamente utilizando la matemática pura y te arrojará los 3 resultados exactos más probables.
- **Si presionas `s` (Sí)**: Entrarás al "Modo Entrenador". El sistema te preguntará uno por uno si deseas cambiar los porcentajes. Podrás decirle a la máquina que le dé más importancia a tu propia intuición, o modificar tu predicción de victoria (ej. 60% Local) y tu expectativa de goles (ej. 70% menos de 2.5 goles).

### 3. ¿Cómo simular un partido distinto?
Para predecir un partido nuevo, abre el archivo `orquestador.py` con cualquier editor de texto, baja hasta el final del documento (donde dice `config = { ... }`) y cambia los datos de `Equipo_A` y `Equipo_B` por los países que van a jugar. Guarda el archivo y vuelve a ejecutar el comando del paso 1.

---

## 🏗️ Funcionamiento General de la Estructura

El Predictor no confía en una sola fuente de la verdad. Su funcionamiento general se basa en el **consenso de tres grandes cerebros**:

1. **Sabiduría del Mercado (El Dinero)**: Analiza dónde está apostando la gente real.
2. **Motor Estadístico (La Máquina)**: Cruza números fríos, formación táctica y estado de los jugadores.
3. **Intuición del Analista (El Humano)**: Permite que el instinto experto corrija los puntos ciegos de la máquina.

El sistema recolecta la probabilidad de victoria calculada independientemente por cada uno de estos tres cerebros, las multiplica por su nivel de importancia (Ponderación) y las fusiona en un solo **Cálculo Maestro Final**. Con este cálculo, se utiliza una fórmula de **Distribución de Poisson** para transformar la probabilidad de ganar en marcadores exactos (ej. 2-1, 0-0, 3-0).

---

## ⚖️ Sistema de Ponderación (Los Pesos)

El algoritmo toma decisiones basadas en un sistema de pesos jerárquicos. Existen 3 niveles de ponderación que puedes modificar:

### 1. Ponderaciones Globales (La mezcla maestra)
Determinan qué cerebro tiene más voz en la decisión final:
- **Mercado:** `40.0%`
- **Simulador IA:** `35.0%`
- **Usuario (Analista):** `25.0%`

### 2. Ponderaciones del Simulador IA (Subgrupos)
Dentro del 35% que le toca a la máquina, esta divide su análisis en tres sub-criterios:
- **Módulo de Estrellas (M4):** `40.0%` (El peso individual de los mejores jugadores).
- **Módulo de Contexto (M2):** `35.0%` (La presión psicológica del partido).
- **Módulo Táctico (M3):** `25.0%` (Posesión del balón y estilos de juego).

### 3. Ponderaciones Internas de Módulos
Ejemplo en el Módulo de Mercado (M1), el sistema evalúa a las casas tradicionales con un `70%` de peso, pero reserva un `30%` para los mercados predictivos descentralizados (Polymarket), que suelen ser más precisos.

---

## 🧩 Detalle Técnico: Cómo funciona cada Módulo

Si deseas auditar el código, el orquestador se apoya en 6 scripts independientes:

### `modulo_mercado.py` (M1: Dinero)
Extrae las cuotas de las casas de apuestas (ej. 1.20 a favor de España). Dado que las casas inflan las cuotas para tener ganancias (Overround), este módulo utiliza matemáticas financieras para "limpiar" la cuota y extraer la probabilidad estadística real que la casa de apuestas le asigna al equipo.

### `modulo_contexto.py` (M2: Psicología)
Suma o resta décimas de gol a la predicción basándose en:
- **Peso de Camiseta**: (Bajo, Medio, Alto) Equipos históricos reciben un bono en partidos clave.
- **Necesidad**: Si un equipo está "Obligado a ganar" y el otro dice "Sirve el empate", el módulo asume que el segundo se encerrará atrás.

### `modulo_tactico.py` (M3: Pizarra)
Cruza los estilos de juego. Si un equipo juega a la "Posesión" contra un equipo al "Contragolpe", penaliza o premia los Goles Esperados (xG) basándose en qué bloque táctico es más eficiente frente al otro.

### `modulo_jugadores.py` (M4: Estrellas)
Analiza los 3 jugadores más importantes definidos en la configuración. 
- Al Jugador 1 le asigna un `15%` de impacto.
- Al Jugador 2 un `10%`.
- Al Jugador 3 un `5%`.
Si el Jugador 1 está marcado como `"lesionado"`, el sistema restará drásticamente la capacidad goleadora del equipo.

### `modulo_dinamica.py` (M5: Eventos de Partido)
Se encarga de inyectar caos estadístico. Regula qué probabilidades tiene de abrirse el partido basándose en la intensidad de los primeros minutos y calcula qué equipo es más propenso a marcar el "Primer Gol".

### `modulo_noticias.py` (M6: Inteligencia Previa)
Es un módulo de scraping e historia. Busca en la base de datos `historical_results.csv` para imprimir los resultados recientes. Además, puede conectarse a Google News RSS para arrojar los últimos 3 titulares de prensa de cada país, dándole al usuario un pulso sobre lesiones, suspensiones o crisis de última hora antes de que ingrese su intuición.
