import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Asistente GPT para Correos", page_icon="✉️")
st.title("📬 Asistente de Respuesta Automática con GPT")

# --- Input del usuario
correo = st.text_area("✉️ Escribe aquí el correo recibido:", height=200)

modelo_seleccionado = st.selectbox(
    "📦 Modelo a utilizar:",
    options=[
        "google/gemma-3n-e2b-it:free",
        "deepseek/deepseek-chat-v3-0324:free",
        "moonshotai/kimi-k2:free",
        "google/gemini-2.0-flash-exp:free"
    ],
    index=0
)

if st.button("Generar respuesta"):
    if not correo.strip():
        st.warning("Por favor, escribe un correo.")
    else:
        with st.spinner("Generando respuesta..."):
            respuesta = requests.post(
                "http://127.0.0.1:8001/responder",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"correo": correo, "modelo": modelo_seleccionado})
            )

            if respuesta.status_code == 200:
                data = respuesta.json()
                st.success("✅ Respuesta generada:")
                st.text_area("✉️ Respuesta:", data["respuesta"], height=200)
            else:
                st.error("❌ Error al generar la respuesta.")

# --- Tabs
st.markdown("---")
tab1, tab2 = st.tabs(["📂 Historial", "📊 Estadísticas"])

# --- Historial
with tab1:
    st.subheader("📂 Historial de correos")

    historial_response = requests.get("http://127.0.0.1:8001/historial")
    if historial_response.status_code == 200:
        historial_data = historial_response.json()

        if historial_data:
            categorias = sorted(set([item.get("categoria", "sin clasificar") for item in historial_data]))
            categoria_seleccionada = st.selectbox("📎 Filtrar por categoría:", ["Todas"] + categorias)

            if categoria_seleccionada != "Todas":
                historial_data = [item for item in historial_data if item.get("categoria") == categoria_seleccionada]

            for i, entry in enumerate(historial_data):

                timestamp = entry["timestamp"]
                correo = entry["input_correo"]
                respuesta = entry["respuesta_modelo"]
                categoria = entry.get("categoria", "sin clasificar")
                modelo = entry.get("modelo", "no especificado")
                email_origen = entry.get("email_origen", "")




                if email_origen and isinstance(email_origen, str):
                    if st.button(f"📧 Enviar respuesta a {email_origen}", key=f"enviar_{i}"):
                        try:
                            send_result = requests.post(
                            "http://127.0.0.1:8001/enviar",
                            json={
                            "destinatario": email_origen,
                            "asunto": "Re: tu consulta",
                            "mensaje": entry.get("respuesta_modelo", "")
                            }
                            )
                            if send_result.ok:
                                st.success(f"✅ Correo enviado a {email_origen}")
                            else:
                                            st.error(f"❌ Error al enviar el correo: {send_result.text}")
                        except Exception as e:
                            st.error(f"❌ Error al conectar con el servidor: {e}")

                st.markdown(
                    f"""
                    <div style="background-color:#ffe9cc;padding:6px 12px;border-radius:5px;margin-bottom:5px;width:fit-content;display:inline-block;color:black;">
                        📎 <strong>Categoría:</strong> {categoria.capitalize()}
                    </div>
                    """, unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <div style="background-color:#e6f0ff;padding:8px 16px;border-radius:5px;display:inline-block;color:black;">
                            🕒 <strong>{timestamp}</strong>
                        </div>
                        <div style="background-color:#e8e8e8;padding:6px 12px;border-radius:5px;display:inline-block;color:black;">
                            📦 <strong>{modelo}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div style="background-color:#f8f8f8;padding:16px;border-radius:8px;margin-bottom:10px;border:1px solid #ccc;color:black;">
                        <strong>📥 Correo recibido:</strong><br>
                        <pre style="white-space:pre-wrap;word-break:break-word;margin:0;color:black;">{correo}</pre>
                    </div>
                    """, unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div style="background-color:#eef9f0;padding:16px;border-radius:8px;margin-bottom:20px;border:1px solid #b0e6c1;color:black;">
                        <strong>📤 Respuesta generada:</strong><br>
                        <pre style="white-space:pre-wrap;word-break:break-word;margin:0;color:black;">{respuesta}</pre>
                    </div>
                    """, unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <hr style="border: none; border-top: 2px dashed #ccc; margin: 30px 0;">
                    """, unsafe_allow_html=True
                )

            

        else:
            st.info("Todavía no hay historial.")
    else:
        st.error("❌ No se pudo cargar el historial.")

# --- Estadísticas
with tab2:
    st.subheader("📈 Estadísticas de correos")

    if historial_response.status_code == 200 and historial_data:
        df = pd.DataFrame(historial_data)

        fig_cat = px.pie(
            df,
            names="categoria",
            title="Distribución por categoría",
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        fig_mod = px.bar(
            df,
            x="modelo",
            title="Cantidad de respuestas por modelo",
            color="modelo",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(fig_mod, use_container_width=True)
    else:
        st.info("Todavía no hay suficientes datos para mostrar estadísticas.")
