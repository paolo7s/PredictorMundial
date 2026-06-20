import math
import random

class SimuladorHibrido:
    def __init__(self, num_simulaciones=10000):
        self.num_simulaciones = num_simulaciones

    def calcular_fuerza_mercado_elo(self, cuotas, elos):
        """Convierte las cuotas y el ELO en una métrica de fuerza comparable."""
        cA, cE, cB = cuotas
        eA, eB = elos
        
        # Probabilidades implícitas del mercado (apuestas)
        margen = (1/cA) + (1/cE) + (1/cB)
        p_mercado_A = (1/cA) / margen
        p_mercado_B = (1/cB) / margen
        
        # Probabilidades implícitas del ELO
        dr = eA - eB
        p_elo_A = 1 / (10 ** (-dr / 400) + 1)
        p_elo_B = 1 - p_elo_A
        
        return p_mercado_A, p_mercado_B, p_elo_A, p_elo_B

    def procesar_factores(self, equipo_A, equipo_B, datos_A, datos_B, conf_pesos):
        xg_ataque_A, xg_defensa_A, fatiga_A, baja_A, nec_A, insaciable_A = datos_A
        xg_ataque_B, xg_defensa_B, fatiga_B, baja_B, nec_B, insaciable_B = datos_B
        cuotas, elos = conf_pesos['datos_externos']
        
        peso_cuotas = conf_pesos['peso_cuotas']
        peso_elo = conf_pesos['peso_elo']
        peso_xg = conf_pesos['peso_xg']

        reporte = []
        reporte.append("=========================================================")
        reporte.append(" 📋 REPORTE DE PONDERACIÓN Y FACTORES (HÍBRIDO) 📋")
        reporte.append("=========================================================")
        
        # 1. Integración de Cuotas y ELO
        pMA, pMB, pEA, pEB = self.calcular_fuerza_mercado_elo(cuotas, elos)
        
        # 2. xG Puro
        xg_base_A = (xg_ataque_A + xg_defensa_B) / 2.0
        xg_base_B = (xg_ataque_B + xg_defensa_A) / 2.0
        
        # 3. PONDERACIÓN MAESTRA (Fusión de xG con Sabiduría del Mercado)
        # Convertimos la probabilidad del mercado/elo a un multiplicador de xG
        # Si el mercado le da un 70% de ganar (muy favorito), su xG base debería subir.
        # Asumimos que 50% de prob = multiplicador 1.0
        mult_mercado_A = (pMA / 0.50) if pMA > 0 else 0.1
        mult_mercado_B = (pMB / 0.50) if pMB > 0 else 0.1
        mult_elo_A = (pEA / 0.50)
        mult_elo_B = (pEB / 0.50)
        
        # El multiplicador final es la suma ponderada
        mult_final_A = (mult_mercado_A * peso_cuotas) + (mult_elo_A * peso_elo) + (1.0 * peso_xg)
        mult_final_B = (mult_mercado_B * peso_cuotas) + (mult_elo_B * peso_elo) + (1.0 * peso_xg)
        
        xg_ponderado_A = xg_base_A * mult_final_A
        xg_ponderado_B = xg_base_B * mult_final_B

        reporte.append(f"[*] PESOS CONFIGURADOS: Cuotas({peso_cuotas*100}%) | ELO({peso_elo*100}%) | Táctica/xG({peso_xg*100}%)")
        reporte.append(f"    - El mercado/ELO modificó el poder de {equipo_A} un {(mult_final_A-1)*100:+.1f}%")
        reporte.append(f"    - El mercado/ELO modificó el poder de {equipo_B} un {(mult_final_B-1)*100:+.1f}%")
        reporte.append(f"    - xG Consolidado Inicial: {equipo_A} [{xg_ponderado_A:.2f}] vs [{xg_ponderado_B:.2f}] {equipo_B}")

        # 4. Fatiga y Bajas
        if fatiga_A < 4: xg_ponderado_A *= (1 - (4 - fatiga_A) * 0.07)
        if fatiga_B < 4: xg_ponderado_B *= (1 - (4 - fatiga_B) * 0.07)
        if baja_A: xg_ponderado_A *= 0.85
        if baja_B: xg_ponderado_B *= 0.85

        # 5. Táctica
        if nec_A == 2: xg_ponderado_A *= 1.15; xg_ponderado_B *= 1.20
        elif nec_A == 3: xg_ponderado_A *= 0.85; xg_ponderado_B *= 0.80
        if nec_B == 2: xg_ponderado_B *= 1.15; xg_ponderado_A *= 1.20
        elif nec_B == 3: xg_ponderado_B *= 0.85; xg_ponderado_A *= 0.80

        # 6. Estilo Insaciable
        if insaciable_A: reporte.append(f"[!] ESTILO SÁDICO: {equipo_A} NO dejará de atacar aunque vaya goleando.")
        if insaciable_B: reporte.append(f"[!] ESTILO SÁDICO: {equipo_B} NO dejará de atacar aunque vaya goleando.")

        underdog_A = xg_ponderado_A < (xg_ponderado_B * 0.70)
        underdog_B = xg_ponderado_B < (xg_ponderado_A * 0.70)
        
        reporte.append("=========================================================\n")
        
        return "\n".join(reporte), xg_ponderado_A, xg_ponderado_B, underdog_A, underdog_B, nec_A, nec_B, insaciable_A, insaciable_B

    def simular(self, xg_A, xg_B, u_A, u_B, nec_A, nec_B, ins_A, ins_B):
        victorias_A = 0; empates = 0; victorias_B = 0; resultados = {}

        for _ in range(self.num_simulaciones):
            goles_A = 0; goles_B = 0
            momentum_A = 0; momentum_B = 0

            for minuto in range(0, 90, 5):
                mult_A = 1.0; mult_B = 1.0

                # Efecto Underdog (Se cuelgan del travesaño si van ganando)
                if goles_A > goles_B and u_A: mult_A *= 0.3; mult_B *= 0.7
                elif goles_B > goles_A and u_B: mult_B *= 0.3; mult_A *= 0.7

                # Kamikaze (Necesita ganar y va perdiendo al min 75+)
                if minuto >= 75:
                    if goles_A <= goles_B and nec_A == 2: mult_A *= 1.8; mult_B *= 1.8
                    if goles_B <= goles_A and nec_B == 2: mult_B *= 1.8; mult_A *= 1.8

                # Control de Daños vs ESTILO INSACIABLE (Diferencia de 2+ goles al min 60+)
                if minuto >= 60 and abs(goles_A - goles_B) >= 2:
                    if goles_A > goles_B:
                        if not ins_A: mult_A *= 0.4 # Se relaja si no es insaciable
                        mult_B *= 0.4 # El perdedor asume la derrota
                    else:
                        if not ins_B: mult_B *= 0.4
                        mult_A *= 0.4

                # Momentum (10 min de euforia tras marcar)
                if momentum_A > 0: mult_A *= 1.4; momentum_A -= 1
                if momentum_B > 0: mult_B *= 1.4; momentum_B -= 1

                prob_5min_A = (xg_A / 18.0) * mult_A
                prob_5min_B = (xg_B / 18.0) * mult_B

                if random.random() < prob_5min_A:
                    goles_A += 1; momentum_A = 2
                if random.random() < prob_5min_B:
                    goles_B += 1; momentum_B = 2

            if goles_A > goles_B: victorias_A += 1
            elif goles_A == goles_B: empates += 1
            else: victorias_B += 1
            
            marcador = f"{goles_A}-{goles_B}"
            resultados[marcador] = resultados.get(marcador, 0) + 1

        p_A = victorias_A / self.num_simulaciones
        p_E = empates / self.num_simulaciones
        p_B = victorias_B / self.num_simulaciones
        marcadores_ordenados = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        
        return p_A, p_E, p_B, marcadores_ordenados

def menu_interactivo():
    print("=====================================================")
    print(" 🎲 SIMULADOR DEFINITIVO: CUOTAS + ELO + MONTECARLO ")
    print("=====================================================")
    equipo_A = input("Equipo Local (A): ")
    equipo_B = input("Equipo Visitante (B): ")
    
    print("\n--- 1. SABIDURÍA DEL MERCADO (CUOTAS) ---")
    cA = float(input(f"Cuota victoria {equipo_A} (ej. 1.80): "))
    cE = float(input("Cuota Empate (ej. 3.50): "))
    cB = float(input(f"Cuota victoria {equipo_B} (ej. 4.50): "))
    
    print("\n--- 2. RANKING HISTÓRICO (ELO) ---")
    eA = float(input(f"Puntos ELO {equipo_A} (ej. 1900): "))
    eB = float(input(f"Puntos ELO {equipo_B} (ej. 1750): "))
    
    print("\n--- 3. MÉTRICAS xG (FÚTBOL PURO) ---")
    xg_A = float(input(f"xG a favor de {equipo_A} (ej. 1.8): "))
    xga_A = float(input(f"xGA en contra de {equipo_A} (ej. 0.9): "))
    xg_B = float(input(f"xG a favor de {equipo_B} (ej. 1.4): "))
    xga_B = float(input(f"xGA en contra de {equipo_B} (ej. 1.2): "))
    
    print("\n--- 4. CONTEXTO FÍSICO Y NECESIDAD ---")
    dias_A = float(input(f"Descanso {equipo_A} (días): "))
    dias_B = float(input(f"Descanso {equipo_B} (días): "))
    baja_A = input(f"¿Falta estrella en {equipo_A}? (s/n): ").lower() == 's'
    baja_B = input(f"¿Falta estrella en {equipo_B}? (s/n): ").lower() == 's'
    nec_A = int(input(f"Necesidad {equipo_A} (1=Normal, 2=Ganar, 3=Empate, 4=Clasificado): "))
    nec_B = int(input(f"Necesidad {equipo_B} (1=Normal, 2=Ganar, 3=Empate, 4=Clasificado): "))
    
    print("\n--- 5. FILOSOFÍA DE GOLEADA (ESTILO INSACIABLE) ---")
    print("¿Es un equipo que NO se conforma con ir 3-0 y seguirá atacando brutalmente? (ej. Alemania 2014)")
    ins_A = input(f"¿{equipo_A} es insaciable? (s/n): ").lower() == 's'
    ins_B = input(f"¿{equipo_B} es insaciable? (s/n): ").lower() == 's'

    print("\n--- 6. CONFIGURACIÓN DE PONDERACIÓN ---")
    print("Elige en qué confías más para darle más peso en el algoritmo:")
    print(" 1 = Confío ciegamente en las Casas de Apuestas (40% Cuotas, 20% ELO, 40% xG)")
    print(" 2 = Confío en la estadística pura de cancha (20% Cuotas, 10% ELO, 70% xG)")
    print(" 3 = Equilibrio total (33% a cada uno)")
    opcion_peso = int(input("Tu elección (1-3): "))
    
    if opcion_peso == 1: p_c, p_e, p_x = 0.40, 0.20, 0.40
    elif opcion_peso == 2: p_c, p_e, p_x = 0.20, 0.10, 0.70
    else: p_c, p_e, p_x = 0.33, 0.33, 0.34

    datos_A = (xg_A, xga_A, dias_A, baja_A, nec_A, ins_A)
    datos_B = (xg_B, xga_B, dias_B, baja_B, nec_B, ins_B)
    conf_pesos = {
        'datos_externos': ((cA, cE, cB), (eA, eB)),
        'peso_cuotas': p_c, 'peso_elo': p_e, 'peso_xg': p_x
    }

    # Ejecutar
    simulador = SimuladorHibrido(10000)
    reporte_txt, xg_A_fin, xg_B_fin, u_A, u_B, n_A, n_B, i_A, i_B = simulador.procesar_factores(equipo_A, equipo_B, datos_A, datos_B, conf_pesos)
    print("\n" + reporte_txt)
    
    p_A, p_E, p_B, marcadores = simulador.simular(xg_A_fin, xg_B_fin, u_A, u_B, n_A, n_B, i_A, i_B)

    # Resultados
    print("=====================================================")
    print(" 🏆 RESULTADOS FINALES (10,000 SIMULACIONES) 🏆 ")
    print("=====================================================")
    print(f"Victorias {equipo_A}: {p_A*100:.1f}%")
    print(f"Empates:           {p_E*100:.1f}%")
    print(f"Victorias {equipo_B}: {p_B*100:.1f}%")
    print("-----------------------------------------------------")
    print("Top 5 Marcadores más probables:")
    for i in range(min(5, len(marcadores))):
        marcador, cantidad = marcadores[i]
        print(f" [{marcador}] -> {(cantidad/10000.0)*100:.1f}%")
    print("=====================================================")

if __name__ == "__main__":
    menu_interactivo()
