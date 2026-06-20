import json
import math
import sys

from modulo_mercado import SabiduriaMercado
from modulo_contexto import ContextoTorneo
from modulo_tactico import ChoqueTactico
from modulo_jugadores import JugadoresEstrella
from modulo_dinamica import DinamicaInPlay
from modulo_noticias import RastreadorNoticias

class OrquestadorPredictivo:
    def __init__(self):
        # DICCIONARIO CENTRAL DE PESOS Y PONDERACIONES
        self.pesos = {
            "GLOBALES": {
                "mercado": 40.0,
                "simulador_ia": 35.0,
                "usuario": 25.0
            },
            "INTERNOS_SIMULADOR": {
                "M4_estrellas": 40.0,
                "M2_contexto": 35.0,
                "M3_tactico": 25.0
            },
            "M1_MERCADO": {
                "casas_tradicionales": 70.0,
                "polymarket": 30.0
            },
            "M5_DINAMICA_PRIMER_GOL": {
                "estadistica_xG": 50.0,
                "cuotas_mercado": 50.0
            },
            "M4_JUGADORES_ESTRELLA": {
                "peso_jugador_1": 15.0,
                "peso_jugador_2": 10.0,
                "peso_jugador_3": 5.0
            }
        }
        self.mod_noticias = RastreadorNoticias()
        
    def inicializar_modulos(self):
        # Inyecta los pesos actualizados a los módulos
        self.mod_mercado = SabiduriaMercado(peso_global=(self.pesos["GLOBALES"]["mercado"]/100))
        # Si tuviéramos que inyectar el peso interno de mercado, modificaríamos SabiduriaMercado aquí.
        
        self.mod_contexto = ContextoTorneo()
        self.mod_tactico = ChoqueTactico()
        
        self.mod_jugadores = JugadoresEstrella()
        # M5 recibe su balance interno
        p5A = self.pesos["M5_DINAMICA_PRIMER_GOL"]["estadistica_xG"] / 100
        p5B = self.pesos["M5_DINAMICA_PRIMER_GOL"]["cuotas_mercado"] / 100
        self.mod_dinamica = DinamicaInPlay(peso_5A=p5A, peso_5B=p5B)
        self.mod_noticias = RastreadorNoticias()

    def menu_interactivo(self):
        print("\n" + "="*70)
        print("  PANEL DE CONTROL Y PONDERACIONES (MODO ENTRENADOR) ")
        print("="*70)
        print("Antes de simular, aquí tienes TODAS las ponderaciones del sistema:\n")
        
        for categoria, valores in self.pesos.items():
            print(f"[{categoria}]")
            for factor, peso in valores.items():
                print(f"  - {factor}: {peso}%")
            print("")
            
        print("="*70)
        opcion = input("¿Deseas modificar alguna ponderación particular? (s/n): ").strip().lower()
        
        if opcion == 's':
            for categoria in self.pesos.keys():
                cambiar = input(f"¿Deseas modificar los valores de [{categoria}]? (s/n): ").strip().lower()
                if cambiar == 's':
                    for factor in self.pesos[categoria].keys():
                        nuevo = input(f"  -> Nuevo valor para '{factor}' (Actual: {self.pesos[categoria][factor]}%): ").strip()
                        if nuevo:
                            try:
                                self.pesos[categoria][factor] = float(nuevo)
                            except ValueError:
                                print("     Valor inválido, se mantiene el anterior.")
                    
                    # Validar que sumen 100% (opcional, pero buena práctica)
                    suma = sum(self.pesos[categoria].values())
                    if suma != 100.0 and categoria not in ["M4_JUGADORES_ESTRELLA"]:
                        print(f"  [!] Advertencia: Los valores en {categoria} suman {suma}%, no 100%.")
            print("\n[✓] Ponderaciones actualizadas.")
        else:
            print("[✓] Manteniendo ponderaciones por defecto.")
            
        self.inicializar_modulos()
        
    def calcular_poisson_y_marcadores(self, prob_L_o_xg, prob_V_o_xg, es_xg=True):
        xg_A = prob_L_o_xg if es_xg else max(0.5, prob_L_o_xg * 3)
        xg_B = prob_V_o_xg if es_xg else max(0.5, prob_V_o_xg * 3)
        
        prob_A = prob_B = prob_E = 0.0
        marcadores = {}
        for goles_A in range(6):
            for goles_B in range(6):
                p_A = ((xg_A ** goles_A) * math.exp(-xg_A)) / math.factorial(goles_A)
                p_B = ((xg_B ** goles_B) * math.exp(-xg_B)) / math.factorial(goles_B)
                prob_resultado = p_A * p_B
                
                marcador_str = f"{goles_A} - {goles_B}"
                marcadores[marcador_str] = prob_resultado
                
                if goles_A > goles_B: prob_A += prob_resultado
                elif goles_B > goles_A: prob_B += prob_resultado
                else: prob_E += prob_resultado
                
        total = prob_A + prob_B + prob_E
        marcadores_ordenados = dict(sorted(marcadores.items(), key=lambda item: item[1], reverse=True))
        return prob_A/total, prob_E/total, prob_B/total, marcadores_ordenados

    def simular_partido(self, partido_config):
        A = partido_config["Equipo_A"]
        B = partido_config["Equipo_B"]
        
        print("\n" + "█"*70)
        print("  [MÓDULO 6] INTELIGENCIA PREVIA (HISTORIAL Y NOTICIAS)  ")
        print("█"*70)
        
        print(f">> ÚLTIMOS PARTIDOS DE {A['nombre'].upper()}:")
        historial_A = self.mod_noticias.obtener_ultimos_partidos(A["nombre"])
        for h in historial_A:
            print(f"   ⚽ {h}")
        
        # Noticias removidas temporalmente
            
        print(f"\n>> ÚLTIMOS PARTIDOS DE {B['nombre'].upper()}:")
        historial_B = self.mod_noticias.obtener_ultimos_partidos(B["nombre"])
        for h in historial_B:
            print(f"   ⚽ {h}")
            
        # Noticias removidas temporalmente
        print("█"*70)

        self.menu_interactivo()
        
        A = partido_config["Equipo_A"]
        B = partido_config["Equipo_B"]
        usr = partido_config.get("Prediccion_Usuario", {"L": 0.33, "E": 0.34, "V": 0.33})
        
        print("\n" + "█"*70)
        print("  REPORTE PREDICTIVO AVANZADO DE FÚTBOL (V4.0)  ")
        print("█"*70 + "\n")
        
        p_mercado = self.pesos["GLOBALES"]["mercado"] / 100
        p_simulador = self.pesos["GLOBALES"]["simulador_ia"] / 100
        p_usuario = self.pesos["GLOBALES"]["usuario"] / 100
        
        print(f">>> 1. ANÁLISIS DEL MERCADO Y CASAS DE APUESTAS (Peso: {p_mercado*100}%)")
        prob_M1_L, prob_M1_E, prob_M1_V = self.mod_mercado.obtener_prediccion_mercado(
            A["cuotas_casas"], A["polymarket_probs"], {}, {}
        )[0]
        
        _, _, _, marc_mercado = self.calcular_poisson_y_marcadores(prob_M1_L, prob_M1_V, es_xg=False)
        
        print(f"  [+] Probabilidades base según el dinero global:")
        print(f"      Victoria {A['nombre']}: {prob_M1_L*100:.1f}%")
        print(f"      Empate: {prob_M1_E*100:.1f}%")
        print(f"      Victoria {B['nombre']}: {prob_M1_V*100:.1f}%")
        print(f"  [+] Top 3 Resultados Exactos según el Mercado:")
        contador = 0
        for m, p in marc_mercado.items():
            if contador < 3:
                print(f"      {A['nombre']} {m} {B['nombre']} ({p*100:.1f}%)")
                contador += 1
        print("-" * 70)

        print(f"\n>>> 2. ANÁLISIS DEL MOTOR ESTADÍSTICO (Peso: {p_simulador*100}%)")
        _, mods_M2_A, mods_M2_B = self.mod_contexto.procesar_contexto_partido(True, A["contexto"], B["contexto"])
        _, mods_M3_A, mods_M3_B = self.mod_tactico.ejecutar_modulo(
            A["nombre"], A["tactica"]["stats"], A["tactica"]["flex"],
            B["nombre"], B["tactica"]["stats"], B["tactica"]["flex"]
        )
        _, mods_M4_A, mods_M4_B = self.mod_jugadores.procesar_jugadores(A["nombre"], A["top3"], B["nombre"], B["top3"])
        
        p_est = self.pesos["INTERNOS_SIMULADOR"]["M4_estrellas"] / 100
        p_ctx = self.pesos["INTERNOS_SIMULADOR"]["M2_contexto"] / 100
        p_tac = self.pesos["INTERNOS_SIMULADOR"]["M3_tactico"] / 100

        atk_final_A = (mods_M4_A["ataque"]*p_est) + (mods_M2_A["ataque"]*p_ctx) + (mods_M3_A[0]*p_tac)
        def_final_A = (mods_M4_A["defensa"]*p_est) + (mods_M2_A["defensa"]*p_ctx) + (mods_M3_A[1]*p_tac)
        
        atk_final_B = (mods_M4_B["ataque"]*p_est) + (mods_M2_B["ataque"]*p_ctx) + (mods_M3_B[0]*p_tac)
        def_final_B = (mods_M4_B["defensa"]*p_est) + (mods_M2_B["defensa"]*p_ctx) + (mods_M3_B[1]*p_tac)

        xg_ajustado_A = (A["xg_base"] * atk_final_A) / def_final_B
        xg_ajustado_B = (B["xg_base"] * atk_final_B) / def_final_A
        
        p5_A, p5_E, p5_B, marc_simulador = self.calcular_poisson_y_marcadores(xg_ajustado_A, xg_ajustado_B)
        
        print(f"  [+] Probabilidades calculadas por la Simulación:")
        print(f"      Victoria {A['nombre']}: {p5_A*100:.1f}%")
        print(f"      Empate: {p5_E*100:.1f}%")
        print(f"      Victoria {B['nombre']}: {p5_B*100:.1f}%")
        print("-" * 70)

        print(f"\n>>> 3. INTUICIÓN DEL MÍSTER [USUARIO] (Peso: {p_usuario*100}%)")
        print(f"  [+] Datos ingresados por el analista principal:")
        print(f"      Victoria {A['nombre']}: {usr['L']*100:.1f}%")
        print(f"      Empate: {usr['E']*100:.1f}%")
        print(f"      Victoria {B['nombre']}: {usr['V']*100:.1f}%")
        print("-" * 70)

        prob_final_A = (prob_M1_L * p_mercado) + (p5_A * p_simulador) + (usr['L'] * p_usuario)
        prob_final_E = (prob_M1_E * p_mercado) + (p5_E * p_simulador) + (usr['E'] * p_usuario)
        prob_final_B = (prob_M1_V * p_mercado) + (p5_B * p_simulador) + (usr['V'] * p_usuario)
        
        print("\n" + "░"*70)
        print("  [✓] CÁLCULO MAESTRO FINAL")
        print("░"*70)
        print(f"  ⚽ VICTORIA {A['nombre'].upper()}:   {prob_final_A*100:.2f}%")
        print(f"  ⚖️ EMPATE:               {prob_final_E*100:.2f}%")
        print(f"  ⚽ VICTORIA {B['nombre'].upper()}:   {prob_final_B*100:.2f}%")
        usr_over25 = partido_config.get("Prediccion_Usuario_Over25", None)
        usr_under25 = partido_config.get("Prediccion_Usuario_Under25", None)
        _, _, _, marc_usuario_base = self.calcular_poisson_y_marcadores(usr['L'], usr['V'], es_xg=False)
        
        todos = set(list(marc_mercado.keys()) + list(marc_simulador.keys()) + list(marc_usuario_base.keys()))
        
        # 1. Matemática Pura sin sesgo
        marc_finales_puros = {}
        for m in todos:
            m_prob = (marc_mercado.get(m, 0) * p_mercado) + (marc_simulador.get(m, 0) * p_simulador) + (marc_usuario_base.get(m, 0) * p_usuario)
            marc_finales_puros[m] = m_prob
            
        print("\n  [!] Top 10 Resultados (Matemática Pura sin Sesgo de Goles):")
        top3_puros = sorted(marc_finales_puros.items(), key=lambda x: x[1], reverse=True)[:10]
        for r, p in top3_puros:
            print(f"      {A['nombre']} {r} {B['nombre']}  ->  {p*100:.2f}%")

        # 2. Con Sesgo de Goles del Usuario
        marc_usuario_final = {}
        if usr_over25 is not None or usr_under25 is not None:
            if usr_under25 is not None:
                usr_over25 = 1.0 - usr_under25
                
            sum_over, sum_under = 0.0, 0.0
            for m, p in marc_usuario_base.items():
                g = sum(map(int, m.split(" - ")))
                if g > 2.5: sum_over += p
                else: sum_under += p
                
            for m, p in marc_usuario_base.items():
                g = sum(map(int, m.split(" - ")))
                if g > 2.5:
                    marc_usuario_final[m] = p * (usr_over25 / sum_over) if sum_over > 0 else 0
                else:
                    marc_usuario_final[m] = p * ((1.0 - usr_over25) / sum_under) if sum_under > 0 else 0
                    
            marc_finales_sesgados = {}
            for m in todos:
                m_prob = (marc_mercado.get(m, 0) * p_mercado) + (marc_simulador.get(m, 0) * p_simulador) + (marc_usuario_final.get(m, 0) * p_usuario)
                marc_finales_sesgados[m] = m_prob
                
            print("\n  [!] Top 10 Resultados (Ponderado con tu Sesgo de Goles):")
            top3_sesgados = sorted(marc_finales_sesgados.items(), key=lambda x: x[1], reverse=True)[:10]
            for r, p in top3_sesgados:
                print(f"      {A['nombre']} {r} {B['nombre']}  ->  {p*100:.2f}%")
        print("█"*70 + "\n")

if __name__ == "__main__":
    config = {
        "Prediccion_Usuario": {"L": 0.50, "E": 0.20, "V": 0.30},
        "Prediccion_Usuario_Under25": 0.55,
        "Equipo_A": {
            "nombre": "Bélgica",
            "xg_base": 1.9,
            "cuotas_casas": [(1.45, 4.50, 7.50), (1.48, 4.30, 7.00)],
            "polymarket_probs": (0.65, 0.23, 0.12),
            "contexto": {"equipo": "Bélgica", "posicion": 1, "necesidad": "ganar_obligado", "peso_camiseta": "alto", "estilo": "posesion"},
            "tactica": {"stats": (65.0, 6.0, 6.0, 8.0), "flex": "flexible"},
            "top3": [
                {"nombre": "Kevin De Bruyne", "posicion": "medio", "estado": "bueno"},
                {"nombre": "Romelu Lukaku", "posicion": "delantero", "estado": "bueno"},
                {"nombre": "Jeremy Doku", "posicion": "delantero", "estado": "bueno"}
            ]
        },
        "Equipo_B": {
            "nombre": "Irán",
            "xg_base": 0.8,
            "contexto": {"equipo": "Irán", "posicion": 3, "necesidad": "sirve_empate", "peso_camiseta": "bajo", "estilo": "contragolpe"},
            "tactica": {"stats": (35.0, 10.0, 18.0, 3.0), "flex": "inflexible"},
            "top3": [
                {"nombre": "Mehdi Taremi", "posicion": "delantero", "estado": "bueno"},
                {"nombre": "Sardar Azmoun", "posicion": "delantero", "estado": "bueno"},
                {"nombre": "Alireza Jahanbakhsh", "posicion": "medio", "estado": "bueno"}
            ]
        }
    }
    orquestador = OrquestadorPredictivo()
    orquestador.simular_partido(config)
