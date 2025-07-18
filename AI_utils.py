from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generar_respuesta_correo(correo_entrada, modelo: str):
    prompt = f"""
Actúa como un asistente de correo que redacta respuestas claras y útiles para mensajes importantes.

Para este caso, escribe la respuesta con un tono profesional.

Mensaje recibido:
\"\"\"
{correo_entrada}
\"\"\"

Respuesta:
"""


    chat_response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1.2
    )

    return chat_response.choices[0].message.content.strip()

def clasificar_correo(correo_entrada: str, modelo: str):
    prompt = f"""
Tu tarea es clasificar correos electrónicos según su intención principal.

Categorías posibles (elige SOLO una):
- cancelación
- reclamo
- consulta
- agradecimiento
- solicitud
- otra

Correo recibido:
\"\"\"
{correo_entrada}
\"\"\"

Responde SOLO con la categoría correspondiente, sin explicaciones adicionales.
    """

    chat_response = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return chat_response.choices[0].message.content.strip()



    
