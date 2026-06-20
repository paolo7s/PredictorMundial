class JugadoresEstrella:
    def __init__(self):
        """
        MÓDULO 4: IMPACTO DE JUGADORES CLAVE (TOP 3)
        Analiza el estado de forma y disponibilidad de las 3 estrellas principales de cada equipo.
        Aplica bonificaciones o penalizaciones focalizadas (ataque o defensa) según la posición del jugador.
        """
        pass

    def evaluar_top3(self, equipo, lista_top3):
        """
        lista_top3 es una lista de 3 diccionarios ordenados por importancia (1 al 3).
        Ejemplo de un jugador: {"nombre": "Messi", "posicion": "delantero", "estado": "bueno"}
        
        posiciones validas: "delantero", "medio", "defensa_portero"
        estados validos: "bueno" (al 100%), "malo" (fatigado/tocado), "lesionado" (no juega)
        """
        mult_ataque = 1.0
        mult_defensa = 1.0 # Mayor a 1.0 es mejor defensa
        
        # El jugador 1 tiene mayor impacto (15%), el 2 un 10%, el 3 un 5%
        impacto_base = [0.15, 0.10, 0.05]
        
        reporte = [f"-> Análisis de Estrellas: {equipo}"]
        
        for i, jugador in enumerate(lista_top3):
            if i >= 3: break # Solo evaluamos al Top 3
            
            base = impacto_base[i]
            pos = jugador['posicion']
            estado = jugador['estado']
            nombre = jugador.get('nombre', f"Estrella {i+1}")
            
            # --- JUGADOR EN BUEN ESTADO ---
            if estado == "bueno":
                if pos == "delantero":
                    mult_ataque += base
                elif pos == "defensa_portero":
                    mult_defensa += base
                elif pos == "medio":
                    mult_ataque += (base / 2)
                    mult_defensa += (base / 2)
                reporte.append(f"   [+] {nombre} (Rank {i+1} | {pos.upper()}): En forma. Aporta su máximo potencial.")
            
            # --- JUGADOR AUSENTE (Lesionado/Suspendido) ---
            elif estado == "lesionado":
                # La penalización por ausencia duele más (1.5x) que el beneficio de estar presente
                penalidad = base * 1.5 
                if pos == "delantero":
                    mult_ataque -= penalidad
                elif pos == "defensa_portero":
                    mult_defensa -= penalidad
                elif pos == "medio":
                    mult_ataque -= (penalidad / 2)
                    mult_defensa -= (penalidad / 2)
                reporte.append(f"   [!] {nombre} (Rank {i+1} | {pos.upper()}): LESIONADO. Penalidad crítica aplicada.")
            
            # --- JUGADOR EN MAL ESTADO (Fatiga/Infiltrado) ---
            elif estado == "malo":
                # Resta un poco porque no rinde al 100% y ocupa el lugar de alguien sano
                penalidad = base * 0.5
                if pos == "delantero":
                    mult_ataque -= penalidad
                elif pos == "defensa_portero":
                    mult_defensa -= penalidad
                elif pos == "medio":
                    mult_ataque -= (penalidad / 2)
                    mult_defensa -= (penalidad / 2)
                reporte.append(f"   [-] {nombre} (Rank {i+1} | {pos.upper()}): Condición baja (tocado). Penalidad leve aplicada.")

        # Límites para evitar que el multiplicador colapse a 0 o números negativos
        mult_ataque = max(0.4, round(mult_ataque, 3))
        mult_defensa = max(0.4, round(mult_defensa, 3))
        
        reporte.append(f"   >> Modificadores {equipo}: Ataque {mult_ataque}x | Defensa {mult_defensa}x")
        
        return "\n".join(reporte), {"ataque": mult_ataque, "defensa": mult_defensa}

    def procesar_jugadores(self, equipo_A, top3_A, equipo_B, top3_B):
        reporte_A, mods_A = self.evaluar_top3(equipo_A, top3_A)
        reporte_B, mods_B = self.evaluar_top3(equipo_B, top3_B)
        
        reporte_final = "\n--- [MÓDULO 4] IMPACTO DEL TOP 3 DE JUGADORES ESTRELLA ---\n"
        reporte_final += reporte_A + "\n" + reporte_B + "\n"
        reporte_final += "-> Este módulo afectará asimétricamente el ataque o la defensa según la posición del talento.\n"
        
        return reporte_final, mods_A, mods_B

# --- ÁREA DE PRUEBA DEL MÓDULO ---
if __name__ == "__main__":
    modulo4 = JugadoresEstrella()
    
    # Prueba: Argentina 
    # Messi (Delantero Rank 1) está bien. 
    # Dibu Martinez (Portero Rank 2) está lesionado (penalidad fuerte en defensa).
    # De Paul (Medio Rank 3) está fatigado.
    estrellas_ARG = [
        {"nombre": "Messi", "posicion": "delantero", "estado": "bueno"},
        {"nombre": "Dibu Martínez", "posicion": "defensa_portero", "estado": "lesionado"},
        {"nombre": "De Paul", "posicion": "medio", "estado": "malo"}
    ]
    
    # Prueba: Francia
    # Mbappé (Delantero Rank 1) está bien.
    # Griezmann (Medio Rank 2) está bien.
    # Saliba (Defensa Rank 3) está bien.
    estrellas_FRA = [
        {"nombre": "Mbappé", "posicion": "delantero", "estado": "bueno"},
        {"nombre": "Griezmann", "posicion": "medio", "estado": "bueno"},
        {"nombre": "Saliba", "posicion": "defensa_portero", "estado": "bueno"}
    ]
    
    reporte, mods_A, mods_B = modulo4.procesar_jugadores("Argentina", estrellas_ARG, "Francia", estrellas_FRA)
    print(reporte)
