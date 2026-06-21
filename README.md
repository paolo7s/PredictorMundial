# Predictor Mundial V4.0

Un orquestador predictivo avanzado para partidos de fútbol, diseñado específicamente para proyectar resultados de la Copa Mundial 2026.

## 🧠 Arquitectura de Ponderaciones
El sistema fusiona tres grandes cerebros predictivos:

1. **Sabiduría del Mercado (40%)**: Extrae y pondera las cuotas de casas de apuestas tradicionales y mercados predictivos.
2. **Motor Estadístico de IA (35%)**: Simula el partido cruzando múltiples variables internas.
3. **Intuición del Usuario (25%)**: Permite inyectar sesgos humanos (probabilidades de victoria y predicción de goles Over/Under 2.5) para alterar el cálculo matemático puro y corregir desviaciones algorítmicas.

---

## ⚙️ Configuración de Partidos (`orquestador.py`)

El núcleo del sistema reside en el bloque `if __name__ == "__main__":` dentro del archivo `orquestador.py`. Aquí se definen los parámetros exactos del partido a simular mediante un diccionario maestro de configuración.

### 1. Variables del Usuario (El Sesgo del Analista)
El usuario puede definir su pronóstico base que afectará el 25% del peso final de la simulación:
```python
"Prediccion_Usuario": {"L": 0.55, "E": 0.30, "V": 0.15},
"Prediccion_Usuario_Under25": 0.60, # 60% de probabilidades de que haya menos de 2.5 goles
```
*El sistema calculará automáticamente el "Efecto Rebote" al contrastar este sesgo de goles con las estadísticas puras de Poisson.*

### 2. Configuración del Equipo A y B
Debes definir a cada equipo de forma exhaustiva para alimentar los submódulos. Ejemplo de estructura:

```python
"Equipo_A": {
    "nombre": "Spain",
    "xg_base": 2.4, # Goles esperados (Expected Goals) base del equipo
    
    # Módulo 1: Sabiduría del Mercado
    "cuotas_casas": [(1.20, 5.50, 12.00), (1.18, 6.00, 13.50)], # (Local, Empate, Visitante)
    "polymarket_probs": (0.80, 0.15, 0.05), # Probabilidades en el mercado de predicción descentralizado
    
    # Módulo 2: Contexto y Psicología
    "contexto": {
        "equipo": "Spain", 
        "posicion": 1, # Posición actual en el grupo/ranking
        "necesidad": "ganar_obligado", # Opciones: ganar_obligado, sirve_empate, sin_presion
        "peso_camiseta": "alto", # Opciones: alto, medio, bajo
        "estilo": "posesion" # Opciones: posesion, contragolpe, defensivo
    },
    
    # Módulo 3: Táctica y Control
    "tactica": {
        "stats": (70.0, 8.0, 5.0, 10.0), # (Posesión %, Llegadas/Ataques, Tiros a Puerta, Córners)
        "flex": "flexible" # Opciones: flexible (se adapta si va perdiendo) o inflexible
    },
    
    # Módulo 4: Impacto de Jugadores Estrella
    "top3": [
        {"nombre": "Rodri", "posicion": "medio", "estado": "bueno"},
        {"nombre": "Lamine Yamal", "posicion": "delantero", "estado": "bueno"},
        {"nombre": "Pedri", "posicion": "medio", "estado": "lesionado"} # El motor penalizará xG si hay lesiones
    ]
}
```

---

## 📊 Submódulos del Motor Estadístico
- **`modulo_mercado.py`**: Traduce las cuotas europeas a probabilidades porcentuales reales eliminando el margen de ganancia de las casas (Overround).
- **`modulo_tactico.py`**: Evalúa si el estilo de un equipo neutraliza al otro (Ej: Posesión vs Muro Defensivo).
- **`modulo_jugadores.py`**: Evalúa el "estado" de los 3 jugadores clave y suma/resta décimas de xG en consecuencia.
- **`modulo_noticias.py`**: Cruza la base de datos local `historical_results.csv` para mostrar resultados recientes.
- **`modulo_dinamica.py`**: Regula cómo el tiempo restante o un "Primer Gol" afectan las probabilidades en vivo (uso futuro para Live Betting).

## 🚀 Uso del Panel Interactivo
Ejecuta el orquestador principal desde la terminal:
```bash
python orquestador.py
```
El script imprimirá la historia de los equipos y luego pausará la ejecución:
`¿Deseas modificar alguna ponderación particular? (s/n):`
- Si respondes **`n`**: El partido se simulará de inmediato usando la configuración en el archivo `orquestador.py`.
- Si respondes **`s`**: Entrarás al Panel de Entrenador, donde podrás modificar en consola los porcentajes globales y submódulos (ej. bajar la importancia del Mercado y subir la del Analista).
