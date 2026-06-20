class ChoqueTactico:
    def __init__(self):
        """
        MÓDULO 3 (Actualizado): MATRIZ TÁCTICA + ADAPTABILIDAD DEL DT
        Evalúa el estilo base mediante métricas, pero permite que entrenadores "Flexibles"
        muten su sistema para contrarrestar la debilidad del rival.
        """
        # Diccionario de Kriptonitas (El mejor counter para cada estilo)
        self.kriptonita = {
            "posesion": "bloque_bajo",       # A la posesión se le anula cerrándose atrás y contragolpeando
            "gegenpressing": "juego_directo", # A la presión alta se la salta con pelotazos largos
            "bloque_bajo": "gegenpressing",   # Al bloque bajo se le asfixia para forzar el error en salida
            "bloque_medio": "bloque_medio",   # Contra un equipo pragmático, hay que ser pragmático (ajedrez)
            "juego_directo": "posesion"       # Al juego directo se le anula teniendo el balón y durmiendo el partido
        }

    def determinar_estilo_base(self, posesion, ppda, pases_largos_pct, recuperaciones_altas):
        """Traduce métricas puras en el Estilo Predeterminado del equipo."""
        if ppda < 9.5 and recuperaciones_altas > 5.0: return "gegenpressing"
        elif posesion > 58.0: return "posesion"
        elif pases_largos_pct > 15.0: return "juego_directo"
        elif posesion < 45.0 and ppda > 13.5: return "bloque_bajo"
        else: return "bloque_medio"

    def enfrentar_estilos(self, estilo_A, estilo_B):
        """La Matriz de Multiplicadores (Ataque, Defensa) base."""
        if estilo_A == "posesion":
            if estilo_B == "bloque_bajo": return (0.85, 1.10), (1.15, 1.20)
            elif estilo_B == "gegenpressing": return (1.20, 0.70), (1.25, 0.80)
            elif estilo_B == "bloque_medio": return (0.75, 1.25), (0.80, 1.25)
            elif estilo_B == "juego_directo": return (1.10, 1.00), (1.00, 0.90)
            elif estilo_B == "posesion": return (0.90, 0.90), (0.90, 0.90)

        elif estilo_A == "gegenpressing":
            if estilo_B == "posesion": return (1.25, 0.80), (1.20, 0.70)
            elif estilo_B == "juego_directo": return (0.75, 0.90), (1.20, 1.10)
            elif estilo_B == "bloque_bajo": return (0.90, 1.10), (0.85, 1.20)
            elif estilo_B == "bloque_medio": return (1.05, 1.00), (0.95, 1.00)
            elif estilo_B == "gegenpressing": return (1.30, 0.70), (1.30, 0.70)

        elif estilo_A == "bloque_bajo":
            if estilo_B == "posesion": return (1.15, 1.20), (0.85, 1.10)
            elif estilo_B == "gegenpressing": return (0.85, 1.20), (0.90, 1.10)
            elif estilo_B == "bloque_bajo": return (0.60, 1.40), (0.60, 1.40)
            elif estilo_B == "bloque_medio": return (0.80, 1.15), (0.90, 1.15)
            elif estilo_B == "juego_directo": return (0.95, 1.05), (1.05, 0.95)

        elif estilo_A == "bloque_medio":
            if estilo_B == "posesion": return (0.80, 1.25), (0.75, 1.25)
            elif estilo_B == "gegenpressing": return (0.95, 1.00), (1.05, 1.00)
            elif estilo_B == "bloque_bajo": return (0.90, 1.15), (0.80, 1.15)
            elif estilo_B == "bloque_medio": return (0.70, 1.30), (0.70, 1.30)
            elif estilo_B == "juego_directo": return (0.90, 1.10), (0.90, 1.10)

        elif estilo_A == "juego_directo":
            if estilo_B == "gegenpressing": return (1.20, 1.10), (0.75, 0.90)
            elif estilo_B == "posesion": return (1.00, 0.90), (1.10, 1.00)
            elif estilo_B == "bloque_bajo": return (1.05, 0.95), (0.95, 1.05)
            elif estilo_B == "bloque_medio": return (0.90, 1.10), (0.90, 1.10)
            elif estilo_B == "juego_directo": return (1.15, 0.85), (1.15, 0.85)

        return (1.0, 1.0), (1.0, 1.0)

    def ejecutar_modulo(self, equipo_A, stats_A, flex_A, equipo_B, stats_B, flex_B):
        """
        Evalúa y adapta los estilos si los DTs son flexibles.
        flex = "inflexible" (fiel a su estilo), "flexible" (se adapta para ganar).
        """
        reporte = []
        reporte.append("\n--- [MÓDULO 3] CHOQUE TÁCTICO DIRECTO Y MENTE DEL DT ---")
        
        # 1. Estilos Base
        estilo_A_base = self.determinar_estilo_base(*stats_A)
        estilo_B_base = self.determinar_estilo_base(*stats_B)
        
        estilo_A_final = estilo_A_base
        estilo_B_final = estilo_B_base

        reporte.append(f"-> ADN Táctico Detectado (Estadísticas):")
        reporte.append(f"   [{equipo_A}] Naturalmente juega a: {estilo_A_base.upper()}")
        reporte.append(f"   [{equipo_B}] Naturalmente juega a: {estilo_B_base.upper()}")

        # 2. ADAPTABILIDAD DEL DT
        if flex_A == "flexible" and flex_B == "flexible":
            reporte.append("-> Ambos DTs son FLEXIBLES. Es un partido de ajedrez donde ambos se anulan.")
            estilo_A_final = "bloque_medio"
            estilo_B_final = "bloque_medio"
        
        elif flex_A == "flexible" and flex_B == "inflexible":
            # B no va a cambiar. A adopta la Kriptonita perfecta contra B.
            estilo_A_final = self.kriptonita[estilo_B_base]
            if estilo_A_final != estilo_A_base:
                reporte.append(f"-> [!] El DT de {equipo_A} es FLEXIBLE. Lee el esquema rígido de {equipo_B} y muta su estilo a {estilo_A_final.upper()} para contrarrestarlo.")
                
        elif flex_B == "flexible" and flex_A == "inflexible":
            estilo_B_final = self.kriptonita[estilo_A_base]
            if estilo_B_final != estilo_B_base:
                reporte.append(f"-> [!] El DT de {equipo_B} es FLEXIBLE. Lee el esquema rígido de {equipo_A} y muta su estilo a {estilo_B_final.upper()} para contrarrestarlo.")
        else:
            reporte.append("-> Ambos DTs son INFLEXIBLES (Doctrinarios). Habrá choque frontal de estilos.")

        # 3. Cruce Final
        mods_A, mods_B = self.enfrentar_estilos(estilo_A_final, estilo_B_final)

        reporte.append("----------------------------------------------------------------------")
        reporte.append(f"Resultado del Machup Táctico en cancha:")
        reporte.append(f"[{equipo_A}] (Jugando a {estilo_A_final.upper()}) -> Eficacia Ataque: {mods_A[0]}x | Defensa: {mods_A[1]}x")
        reporte.append(f"[{equipo_B}] (Jugando a {estilo_B_final.upper()}) -> Eficacia Ataque: {mods_B[0]}x | Defensa: {mods_B[1]}x")
        reporte.append("-> Este módulo multiplicará la probabilidad final de goles.\n")

        return "\n".join(reporte), mods_A, mods_B

# --- ÁREA DE PRUEBA DEL MÓDULO ---
if __name__ == "__main__":
    modulo3 = ChoqueTactico()
    
    # España: Muchísima posesión. Inflexible (siempre quieren la pelota).
    stats_Espana = (75.0, 10.0, 5.0, 3.0)
    flex_Espana = "inflexible"
    
    # Marruecos (Mundial 2022): DT Inteligente (Regragui). Sabe que no puede jugarle de tú a tú a España.
    # Naturalmente son un equipo de bloque medio, pero se adaptarán.
    stats_Marruecos = (45.0, 12.0, 12.0, 2.0)
    flex_Marruecos = "flexible"
    
    reporte, mod_A, mod_B = modulo3.ejecutar_modulo("España", stats_Espana, flex_Espana, "Marruecos", stats_Marruecos, flex_Marruecos)
    print(reporte)
