import json
from datetime import datetime
import os
from dotenv import load_dotenv

LOG_PATH = "log.json"

EMAIL_OWNER = os.getenv("EMAIL_OWNER")

def guardar_log(correo_entrada: str, respuesta: str, categoria: str, modelo: str):
    nueva_entrada = {
       "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "input_correo": correo_entrada,
        "respuesta_modelo": respuesta,
        "categoria": categoria,
        "modelo" : modelo,
        "email_origen": EMAIL_OWNER
    }

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
    else:
        data = []

    data.append(nueva_entrada)

    with open(LOG_PATH, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)
