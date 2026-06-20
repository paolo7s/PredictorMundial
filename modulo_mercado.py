class SabiduriaMercado:
    def __init__(self, peso_global=0.40):
        self.peso_global = peso_global
        
    def quitar_margen_casas(self, cuota_L, cuota_E, cuota_V):
        impl_L = 1 / cuota_L
        impl_E = 1 / cuota_E
        impl_V = 1 / cuota_V
        margen = impl_L + impl_E + impl_V
        return (impl_L / margen), (impl_E / margen), (impl_V / margen)

    def calcular_consenso_tradicional(self, lista_cuotas_10_casas):
        if not lista_cuotas_10_casas:
            return 0.33, 0.34, 0.33
        sum_L = sum_E = sum_V = 0.0
        for cL, cE, cV in lista_cuotas_10_casas:
            pL, pE, pV = self.quitar_margen_casas(cL, cE, cV)
            sum_L += pL; sum_E += pE; sum_V += pV
        n = len(lista_cuotas_10_casas)
        return (sum_L / n), (sum_E / n), (sum_V / n)

    def integrar_polymarket(self, prob_casas, prob_polymarket, peso_polymarket=0.30):
        cL, cE, cV = prob_casas
        pL, pE, pV = prob_polymarket
        peso_casas = 1.0 - peso_polymarket
        final_L = (cL * peso_casas) + (pL * peso_polymarket)
        final_E = (cE * peso_casas) + (pE * peso_polymarket)
        final_V = (cV * peso_casas) + (pV * peso_polymarket)
        return final_L, final_E, final_V

    def calcular_marcadores_exactos(self, marcadores_casas, marcadores_poly, peso_poly=0.30):
        """
        Recibe diccionarios con las probabilidades de Resultados Exactos (Correct Score).
        Ejemplo: marcadores_casas = {'1-0': 0.12, '1-1': 0.15, '2-1': 0.08...}
        """
        marcadores_finales = {}
        todos_los_marcadores = set(marcadores_casas.keys()).union(set(marcadores_poly.keys()))
        
        peso_casas = 1.0 - peso_poly
        for m in todos_los_marcadores:
            prob_c = marcadores_casas.get(m, 0.0)
            prob_p = marcadores_poly.get(m, 0.0)
            
            # Fusión híbrida del mercado para este marcador específico
            prob_final = (prob_c * peso_casas) + (prob_p * peso_poly)
            marcadores_finales[m] = prob_final
            
        # Retorna el diccionario ordenado de mayor a menor probabilidad
        return dict(sorted(marcadores_finales.items(), key=lambda item: item[1], reverse=True))

    def obtener_prediccion_mercado(self, cuotas_10_casas, polymarket_probs, marcadores_casas, marcadores_poly):
        prob_casas = self.calcular_consenso_tradicional(cuotas_10_casas)
        prob_final = self.integrar_polymarket(prob_casas, polymarket_probs)
        
        # Nuevo: Análisis de Resultados Exactos
        marcadores_consenso = self.calcular_marcadores_exactos(marcadores_casas, marcadores_poly)
        
        print("\n--- [MÓDULO 1] SABIDURÍA DEL MERCADO ---")
        print(f"Probabilidades de Consenso (10 Casas + Polymarket):")
        print(f"Victoria Local: {prob_final[0]*100:.2f}%")
        print(f"Empate:         {prob_final[1]*100:.2f}%")
        print(f"Victoria Visit: {prob_final[2]*100:.2f}%")
        
        print(f"\nPredicción de Marcador Exacto según el Mercado:")
        contador = 0
        for marcador, prob in marcadores_consenso.items():
            if contador < 5: # Mostrar top 5
                print(f" -> Resultado {marcador}: {prob*100:.2f}%")
                contador += 1
                
        print(f"-> Este módulo aportará su peso dinámico a la decisión final.\n")
        
        return prob_final, marcadores_consenso
