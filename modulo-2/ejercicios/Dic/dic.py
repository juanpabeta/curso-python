import requests
import random 
import html

URL = "https://opentdb.com"

def obtener_preguntas():
    respuesta = requests.get(URL)
    
    if respuesta.status_code == 200:
        return respuesta.json()["results"]
    else:
        print("Error al obtener preguntas")