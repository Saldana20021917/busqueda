from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests
from os import getenv
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Crear app Flask
app = Flask(__name__)

# Obtener clave desde entorno
API_KEY = getenv("NEWS_API_KEY")

# Función para obtener noticias desde NewsAPI
def buscar_noticias(api_key, palabras_clave, idioma="es", max_noticias=20):
    fecha_hasta = datetime.now()
    fecha_desde = fecha_hasta - timedelta(days=7)
    fecha_hasta_str = fecha_hasta.strftime('%Y-%m-%d')
    fecha_desde_str = fecha_desde.strftime('%Y-%m-%d')

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": " OR ".join(palabras_clave),
        "language": idioma,
        "from": fecha_desde_str,
        "to": fecha_hasta_str,
        "sortBy": "relevancy",
        "pageSize": max_noticias,
    }
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        articulos = response.json().get("articles", [])
        return [{
            "titulo": a.get('title', 'Sin título'),
            "fuente": a.get('source', {}).get('name', 'Desconocida'),
            "descripcion": a.get('description', 'Sin descripción'),
            "enlace": a.get('url', '#'),
            "fecha": a.get('publishedAt', 'Sin fecha')
        } for a in articulos]
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar NewsAPI: {e}")
        return []

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    if request.method == 'POST':
        temas = request.form.get('temas', '').lower().split(',')
        idioma = request.form.get('idioma', 'es')
        limite = int(request.form.get('limite', 10))
        resultados = buscar_noticias(API_KEY, temas, idioma, limite)
    return render_template('index.html', resultados=resultados)

# 🚀 Punto de entrada con soporte para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)







