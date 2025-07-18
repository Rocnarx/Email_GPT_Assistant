import requests
import time
import random

correos_demo = [
    "Hola, quiero cancelar mi suscripción al boletín mensual.",
    "Tengo problemas para iniciar sesión en mi cuenta, ¿pueden ayudarme?",
    "¿Cuál es el precio actual del plan premium?",
    "Me gustaría cambiar mi dirección de envío para futuras entregas.",
    "¿Tienen descuentos para estudiantes?",
    "El producto llegó dañado, quiero solicitar un reembolso.",
    "Gracias por el excelente servicio, ¡estoy feliz con su atención!",
    "Necesito una factura con mi RUT para este mes.",
    "¿Pueden explicarme cómo funciona la renovación automática?",
    "Mi tarjeta fue rechazada, ¿qué debo hacer?"
]

modelos_demo = [
    "google/gemma-3n-e2b-it:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "moonshotai/kimi-k2:free",
    "google/gemini-2.0-flash-exp:free"
]

def enviar_con_reintento(payload, intentos=3):
    for intento in range(intentos):
        res = requests.post(
            "http://127.0.0.1:8001/responder",
            headers={"Content-Type": "application/json"},
            json=payload
        )

        if res.status_code == 200:
            return res

        elif res.status_code == 429:
            print("⏳ Límite de requests alcanzado. Esperando 60 segundos...")
            time.sleep(60)
        else:
            print(f"❌ Error desconocido ({res.status_code}):")
            print(res.text)
            return res

    return res

# --- Envío con espera para respetar límites ---
for i, correo in enumerate(correos_demo, 1):
    modelo = random.choice(modelos_demo)
    payload = {"correo": correo, "modelo": modelo}

    print(f"📤 [{i}] Enviando correo: {correo[:40]}... | Modelo: {modelo}")

    res = enviar_con_reintento(payload)

    if res.status_code == 200:
        print(f"✅ [{i}] OK\n")
    else:
        print(f"❌ [{i}] Falló\n")

    time.sleep(4)  # ← Seguridad entre llamadas
