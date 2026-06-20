class DinamicaInPlay:
    def __init__(self, peso_5A=0.50, peso_5B=0.50):
        """
        MÓDULO 5: DINÁMICA IN-PLAY (Híbrido)
        Calcula quién anota primero usando un enfoque 50/50 entre Estadística Pura y Sabiduría del Mercado.
        """
        self.peso_5A = peso_5A # Peso de la estadística (xG)
        self.peso_5B = peso_5B # Peso de las apuestas (First Team to Score)

    def probabilidad_primer_gol_hibrida(self, xg_A, xg_B, mercado_A, mercado_B, mercado_0):
        """
        MÓDULO 5A: Estadística Pura (Basada en Goles Esperados)
        MÓDULO 5B: Mercado (Cuotas de Bet365/Polymarket para "Primer equipo en marcar")
        """
        # --- CÁLCULO 5A (Estadística Pura) ---
        total_xg = xg_A + xg_B
        if total_xg == 0:
            prob_5A_A, prob_5A_B, prob_5A_0 = 0.0, 0.0, 1.0
        else:
            prob_5A_0 = 0.25  # Probabilidad histórica de 0-0 al descanso
            prob_5A_A = (xg_A / total_xg) * (1 - prob_5A_0)
            prob_5A_B = (xg_B / total_xg) * (1 - prob_5A_0)

        # --- FUSIÓN DE MÓDULOS (5A y 5B) ---
        prob_final_A = (prob_5A_A * self.peso_5A) + (mercado_A * self.peso_5B)
        prob_final_B = (prob_5A_B * self.peso_5A) + (mercado_B * self.peso_5B)
        prob_final_0 = (prob_5A_0 * self.peso_5A) + (mercado_0 * self.peso_5B)
        
        # Normalización matemática por seguridad (para asegurar que sumen 100%)
        suma_total = prob_final_A + prob_final_B + prob_final_0
        
        return prob_final_A / suma_total, prob_final_B / suma_total, prob_final_0 / suma_total

    def reaccion_psicologica(self, necesidad, recibio_gol):
        """Modifica tácticas según la necesidad en tabla y el golpe emocional del gol."""
        mult_ataque = 1.0
        mult_defensa = 1.0
        
        if necesidad == "eliminatoria":
            if recibio_gol: mult_ataque, mult_defensa = 1.40, 0.85
            else: mult_ataque, mult_defensa = 0.85, 1.20
        elif necesidad == "sirve_empate":
            if recibio_gol: mult_ataque, mult_defensa = 1.10, 0.60
            else: mult_ataque, mult_defensa = 0.40, 1.50
        elif necesidad == "ganar_obligado":
            if recibio_gol: mult_ataque, mult_defensa = 1.80, 0.50
            else: mult_ataque, mult_defensa = 1.00, 1.10
        elif necesidad == "eliminado":
            if recibio_gol: mult_ataque, mult_defensa = 0.70, 0.50
            else: mult_ataque, mult_defensa = 1.10, 0.90
        elif necesidad == "clasificado":
            if recibio_gol: mult_ataque, mult_defensa = 0.50, 0.80
            else: mult_ataque, mult_defensa = 0.60, 1.10
                
        return mult_ataque, mult_defensa

    def simular_dinamica(self, equipo_A, xg_A, nec_A, prob_mercado_A, equipo_B, xg_B, nec_B, prob_mercado_B, prob_mercado_0):
        reporte = ["\n--- [MÓDULO 5] DINÁMICA DEL PRIMER GOL Y REACCIÓN (GAME STATE) ---"]
        
        # Fusión Híbrida 5A + 5B
        pA, pB, p0 = self.probabilidad_primer_gol_hibrida(xg_A, xg_B, prob_mercado_A, prob_mercado_B, prob_mercado_0)
        
        reporte.append(f"-> Probabilidad Híbrida del Primer Gol (50% xG + 50% Mercado):")
        reporte.append(f"   [Cálculo 5A - Estadística] vs [Cálculo 5B - Mercado/Polymarket]")
        reporte.append(f"   - Oportunidad final de {equipo_A}: {pA*100:.1f}%")
        reporte.append(f"   - Oportunidad final de {equipo_B}: {pB*100:.1f}%")
        reporte.append(f"   - Oportunidad de Sin Goles (0-0):  {p0*100:.1f}%")
        
        reporte.append("\n-> MATRIZ DE REACCIÓN PSICOLÓGICA POST-GOL:")
        
        # Si A marca
        atk_A_gana, def_A_gana = self.reaccion_psicologica(nec_A, False)
        atk_B_pierde, def_B_pierde = self.reaccion_psicologica(nec_B, True)
        reporte.append(f"   [Si {equipo_A} pega primero]:")
        reporte.append(f"     > {equipo_A} cambia a: Ataque {atk_A_gana}x, Defensa {def_A_gana}x")
        reporte.append(f"     > {equipo_B} cambia a: Ataque {atk_B_pierde}x, Defensa {def_B_pierde}x")
        
        # Si B marca
        atk_A_pierde, def_A_pierde = self.reaccion_psicologica(nec_A, True)
        atk_B_gana, def_B_gana = self.reaccion_psicologica(nec_B, False)
        reporte.append(f"\n   [Si {equipo_B} pega primero]:")
        reporte.append(f"     > {equipo_A} cambia a: Ataque {atk_A_pierde}x, Defensa {def_A_pierde}x")
        reporte.append(f"     > {equipo_B} cambia a: Ataque {atk_B_gana}x, Defensa {def_B_gana}x")

        return "\n".join(reporte)

# --- ÁREA DE PRUEBA DEL MÓDULO ---
if __name__ == "__main__":
    modulo5 = DinamicaInPlay(peso_5A=0.50, peso_5B=0.50)
    
    # Prueba: Marruecos vs Portugal
    # Estadística Pura (Módulo 5A) asume que Portugal debería marcar primero por su xG alto.
    # Pero el MERCADO (Módulo 5B) dictamina estas cuotas para "Quién anotará primero":
    # Mercado confía un poco más en un batacazo marroquí o un 0-0 cerrado.
    mercado_MAR = 0.35
    mercado_POR = 0.40
    mercado_00 = 0.25
    
    reporte = modulo5.simular_dinamica("Marruecos", 1.2, "sirve_empate", mercado_MAR, 
                                       "Portugal",  2.1, "eliminatoria", mercado_POR, mercado_00)
    print(reporte)
