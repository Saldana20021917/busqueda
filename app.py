from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import requests
from os import getenv
from dotenv import load_dotenv
from flask_cors import CORS  # Importamos CORS

load_dotenv()
app = Flask(__name__)
CORS(app)  # Habilitamos CORS en toda la aplicación

API_KEY = getenv("NEWS_API_KEY")

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
        print(f"Error: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    if request.method == 'POST':
        temas = request.form.get('temas', '').lower().split(',')
        idioma = request.form.get('idioma', 'es')
        limite = int(request.form.get('limite', 10))
        resultados = buscar_noticias(API_KEY, temas, idioma, limite)
    return render_template('index.html', resultados=resultados)

@app.route('/buscar_noticias', methods=['POST'])
def buscar_noticias_post():
    # Obtener datos enviados desde el frontend
    datos = request.get_json()
    temas = datos.get('temas', [])
    idioma = datos.get('idioma', 'es')
    limite = int(datos.get('limite', 10))
    
    # Buscar noticias con la función que ya tienes
    resultados = buscar_noticias(API_KEY, temas, idioma, limite)
    
    # Devolver los resultados como JSON
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)

print(f"API_KEY: {API_KEY}")




