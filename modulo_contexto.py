class ContextoTorneo:
    def __init__(self):
        """
        MÓDULO 2 (Actualizado): CONTEXTO, JERARQUÍA Y ESTILO DE JUEGO
        Genera multiplicadores tácticos y morales basados en la necesidad del equipo,
        su historia (peso de la camiseta) y su estilo futbolístico natural.
        """
        pass

    def evaluar_equipo(self, equipo, posicion, necesidad, peso_camiseta, estilo):
        """
        necesidad: ganar_obligado, sirve_empate, clasificado, diferencia_goles, eliminado
        peso_camiseta: alto, medio, bajo
        estilo: ofensivo, defensivo, posesion
        """
        # 1. VALORES BASE SEGÚN NECESIDAD
        mult_ataque = 1.0
        mult_defensa = 1.0  # Mayor a 1.0 = más difícil hacerle gol
        moral = 1.0
        
        if necesidad == "ganar_obligado":
            mult_ataque = 1.25; mult_defensa = 0.80; moral = 1.15
        elif necesidad == "sirve_empate":
            mult_ataque = 0.70; mult_defensa = 1.30; moral = 1.05
        elif necesidad == "clasificado":
            mult_ataque = 0.80; mult_defensa = 0.85; moral = 0.70
        elif necesidad == "diferencia_goles":
            mult_ataque = 1.40; mult_defensa = 0.60; moral = 1.25
        elif necesidad == "eliminado":
            mult_ataque = 1.05; mult_defensa = 0.75; moral = 0.60
            
        # 2. AJUSTE POR JERARQUÍA (PESO DE LA CAMISETA)
        # Los equipos grandes juegan mejor bajo presión extrema, los chicos se asustan.
        if necesidad in ["ganar_obligado", "diferencia_goles"]:
            if peso_camiseta == "alto":
                moral *= 1.25         # Saca a relucir su historia
                mult_ataque *= 1.10   # Efectividad "clutch"
            elif peso_camiseta == "bajo":
                moral *= 0.80         # Pánico escénico
                mult_defensa *= 0.80  # Errores defensivos por nervios

        # 3. AJUSTE POR ESTILO DE JUEGO (Últimos 10 partidos)
        if estilo == "defensivo":
            if necesidad in ["ganar_obligado", "diferencia_goles"]:
                # Un equipo defensivo obligado a atacar sufre muchísimo
                mult_ataque *= 0.85   # Falta de creatividad
                mult_defensa *= 0.85  # Quedan brutalmente expuestos a contras
            elif necesidad == "sirve_empate":
                mult_defensa *= 1.25  # Están en su ecosistema ideal
                
        elif estilo == "ofensivo":
            if necesidad == "sirve_empate":
                # No saben echarse atrás, si lo intentan fracasan
                mult_defensa *= 0.85  
                mult_ataque *= 1.15   # Su mejor defensa sigue siendo atacar
                
        elif estilo == "posesion":
            # La posesión neutraliza el ritmo del partido
            if necesidad == "sirve_empate":
                mult_defensa *= 1.20  # Se defienden durmiendo la pelota
                mult_ataque *= 0.90
            elif necesidad in ["ganar_obligado", "diferencia_goles"]:
                mult_ataque *= 1.10   # Asfixian al rival metiéndolo en su área

        # Redondear para estética
        return {
            "ataque": round(mult_ataque, 3),
            "defensa": round(mult_defensa, 3),
            "moral": round(moral, 3)
        }

    def procesar_contexto_partido(self, es_fase_grupos, datos_A, datos_B):
        """
        Ejemplo estructura de datos_A:
        {'equipo': 'Italia', 'posicion': 2, 'necesidad': 'sirve_empate', 'peso_camiseta': 'alto', 'estilo': 'defensivo'}
        """
        reporte = []
        reporte.append("\n--- [MÓDULO 2] CONTEXTO, JERARQUÍA Y ESTILO TÁCTICO ---")
        
        if not es_fase_grupos:
            reporte.append("-> Partido de Eliminatoria Directa (Mata-Mata).")
            # En eliminatorias, la presión siempre es máxima. Asumimos 'ganar_obligado'.
            mods_A = self.evaluar_equipo(datos_A['equipo'], 0, "ganar_obligado", datos_A['peso_camiseta'], datos_A['estilo'])
            mods_B = self.evaluar_equipo(datos_B['equipo'], 0, "ganar_obligado", datos_B['peso_camiseta'], datos_B['estilo'])
        else:
            mods_A = self.evaluar_equipo(datos_A['equipo'], datos_A['posicion'], datos_A['necesidad'], datos_A['peso_camiseta'], datos_A['estilo'])
            mods_B = self.evaluar_equipo(datos_B['equipo'], datos_B['posicion'], datos_B['necesidad'], datos_B['peso_camiseta'], datos_B['estilo'])
        
        for dt, md in [(datos_A, mods_A), (datos_B, mods_B)]:
            nec_txt = dt.get('necesidad', 'MATA-MATA').upper()
            reporte.append(f"-> [{dt['equipo']}] | Estilo: {dt['estilo'].upper()} | Jerarquía: {dt['peso_camiseta'].upper()}")
            if es_fase_grupos:
                reporte.append(f"   Tabla: Necesidad -> {nec_txt}")
            reporte.append(f"   [Impacto Final] Ataque: {md['ataque']}x | Defensa: {md['defensa']}x | Moral: {md['moral']}x")
            
        return "\n".join(reporte), mods_A, mods_B

# --- ÁREA DE PRUEBA DEL MÓDULO ---
if __name__ == "__main__":
    modulo2 = ContextoTorneo()
    
    # Prueba: Italia necesita un empate. Tienen jerarquía alta y estilo defensivo.
    info_A = {'equipo': 'Italia', 'posicion': 2, 'necesidad': 'sirve_empate', 'peso_camiseta': 'alto', 'estilo': 'defensivo'}
    
    # Prueba: Japón necesita ganar sí o sí. Jerarquía media, estilo ofensivo (transiciones rápidas).
    info_B = {'equipo': 'Japón', 'posicion': 3, 'necesidad': 'ganar_obligado', 'peso_camiseta': 'medio', 'estilo': 'ofensivo'}
    
    txt_reporte, mods_A, mods_B = modulo2.procesar_contexto_partido(True, info_A, info_B)
    print(txt_reporte)
