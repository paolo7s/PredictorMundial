import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import csv

class RastreadorNoticias:
    def __init__(self):
        # Usamos el RSS gratuito de Google News en español
        self.base_url = "https://news.google.com/rss/search?q={}&hl=es-419&gl=AR&ceid=AR:es-419"

    def buscar_ultimas_noticias(self, equipo, max_noticias=4):
        # Búsqueda inteligente: Forzamos a buscar novedades médicas, tácticas o escándalos
        query = f'"{equipo}" seleccion futbol AND ("lesión" OR "lesionado" OR "baja" OR "molestia" OR "táctica" OR "alineación" OR "crisis" OR "escándalo")'
        query_encoded = urllib.parse.quote(query)
        url = self.base_url.format(query_encoded)

        noticias = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            
            # Recorremos los ítems del RSS
            for item in root.findall('./channel/item'):
                titulo = item.find('title').text
                fecha = item.find('pubDate').text
                
                # Limpiar el título (Google News suele poner " - Fuente" al final)
                if " - " in titulo:
                    titulo = titulo.rsplit(" - ", 1)[0]
                    
                noticias.append({"titulo": titulo, "fecha": fecha})
                
                if len(noticias) >= max_noticias:
                    break
                    
        except Exception as e:
            noticias.append({"titulo": "No se pudieron obtener noticias en tiempo real. (Error de red/API)", "fecha": ""})
            
        return noticias

    def obtener_ultimos_partidos(self, equipo, max_partidos=4):
        resultados = []
        try:
            with open("historical_results.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["home_team"] == equipo or row["away_team"] == equipo:
                        resultados.append(row)
        except Exception:
            return ["Base de datos histórica no encontrada."]
            
        ultimos = resultados[-max_partidos:]
        lista_formateada = []
        for p in reversed(ultimos):
            lista_formateada.append(f"[{p['date']} | {p['tournament']}] {p['home_team']} {p['home_score']} - {p['away_score']} {p['away_team']}")
            
        return lista_formateada

if __name__ == "__main__":
    rastreador = RastreadorNoticias()
    n = rastreador.buscar_ultimas_noticias("Argentina")
    for i in n:
        print("-", i["titulo"])
