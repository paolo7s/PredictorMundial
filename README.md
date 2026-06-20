# Predictor Mundial V4.0

Un orquestador predictivo avanzado para partidos de fútbol, diseñado específicamente para proyectar resultados de la Copa Mundial 2026.

## Arquitectura
El sistema fusiona tres grandes cerebros predictivos:
1. **Sabiduría del Mercado (40%)**: Extrae y pondera las cuotas de casas de apuestas tradicionales y mercados predictivos (Polymarket).
2. **Motor Estadístico de IA (35%)**: Simula el partido cruzando:
   - **Módulo de Contexto**: Presión, peso de la camiseta y necesidad de puntos.
   - **Módulo Táctico**: Choques de estilos (Posesión vs Contragolpe) y estadísticas de control de balón.
   - **Módulo de Jugadores Estrella**: Impacto individual de los top 3 jugadores de cada equipo.
3. **Intuición del Míster (Usuario) (25%)**: Permite inyectar sesgos humanos (probabilidades de victoria y predicción de goles Over/Under 2.5) para alterar y guiar el cálculo matemático puro.

## Funcionalidades
- **Modo Interactivo**: Panel de control en consola para modificar ponderaciones y sesgos en tiempo real antes de simular un partido.
- **Predicción de Marcadores Exactos**: Calcula la distribución probabilística de resultados exactos utilizando la fórmula matemática de Distribución de Poisson.
- **Módulo de Inteligencia Previa**: Rastrea el historial de partidos recientes de los equipos y busca noticias o novedades tácticas de último momento a través del feed de Google News.

## Uso
Ejecuta el orquestador principal desde la terminal:
```bash
python orquestador.py
```
Sigue las instrucciones en pantalla para ajustar los pesos o simplemente presiona 'n' para correr la simulación con las ponderaciones por defecto.
