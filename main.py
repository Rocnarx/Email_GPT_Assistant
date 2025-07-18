from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from AI_utils import generar_respuesta_correo
from AI_utils import clasificar_correo
from logger import guardar_log
import json
from fastapi.responses import JSONResponse
from pydantic import Field
from fastapi import Body
from send_email import enviar_email


app = FastAPI()

class EmailRequest(BaseModel):
    correo: str
    modelo: str = Field(default= "google/gemma-3n-e2b-it:free")

# Ruta POST para enviar el correo y obtener respuesta
@app.post("/responder")
def responder_correo(email_req: EmailRequest):
    try:
        modelo = email_req.modelo
        respuesta = generar_respuesta_correo(email_req.correo, modelo)
        categoria = clasificar_correo(email_req.correo, modelo)
        guardar_log(email_req.correo, respuesta, categoria, modelo)
        return {"respuesta": respuesta, "categoria": categoria}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/historial")
def obtener_historial():
    try:
        with open("log.json", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
        data = sorted(data, key=lambda x: x["timestamp"], reverse=True)
        return JSONResponse(content=data)
    except FileNotFoundError:
        return JSONResponse(content={"historial": []}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enviar")
def enviar_respuesta(payload: dict):
    try:
        destinatario = payload["destinatario"]
        asunto = payload["asunto"]
        mensaje = payload["mensaje"]

        print(f"[INFO] Enviando correo a: {destinatario}")
        print(f"[INFO] Asunto: {asunto}")
        print(f"[INFO] Contenido:\n{mensaje}")

        enviar_email(destinatario, asunto, mensaje)
        print("[INFO] Correo enviado correctamente ✅")
        return {"mensaje": "Correo enviado correctamente"}
    
    except Exception as e:
        print("[ERROR] Fallo al enviar el correo:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
