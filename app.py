import streamlit as st
import edge_tts
import asyncio
import io
import random

# Configuración de la página
st.set_page_config(
    page_title="Português Rápido - Brasil",
    page_icon="🇧🇷",
    layout="wide"
)

# -------------------------------------------------------------------
# FUNCIÓN DE AUDIO CON VOZ MASCULINA Y VELOCIDAD 1.5x
# -------------------------------------------------------------------
async def generar_audio_native(texto):
    # Voz masculina de Brasil súper natural (Antonio) a 1.5x (+50%)
    communicate = edge_tts.Communicate(texto, voice="pt-BR-AntonioNeural", rate="+50%")
    out = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "data":
            out.write(chunk["data"])
    out.seek(0)
    return out

def reproducir_audio(texto):
    audio_bytes = asyncio.run(generar_audio_native(texto))
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

# -------------------------------------------------------------------
# BASE DE DATOS DE FRASES / FRASES DE EJEMPLO
# -------------------------------------------------------------------
FRASES = [
    {"pt": "Bom dia! Como você está?", "es": "¡Buenos días! ¿Cómo estás?"},
    {"pt": "Muito prazer em conhecê-lo.", "es": "Mucho gusto en conocerlo."},
    {"pt": "Por favor, onde fica o banheiro?", "es": "Por favor, ¿dónde queda el baño?"},
    {"pt": "Quanto custa isto?", "es": "¿Cuánto cuesta esto?"},
    {"pt": "Uma cerveja bem gelada, por favor.", "es": "Una cerveza bien helada, por favor."},
    {"pt": "Obrigado por tudo!", "es": "¡Gracias por todo!"},
    {"pt": "Pode falar mais devagar, por favor?", "es": "¿Puede hablar más despacio, por favor?"}
]

# -------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -------------------------------------------------------------------
st.title("🇧🇷 Português Rápido")
st.subheader("Aprende frases clave con pronunciación masculina natural")

st.markdown("---")

# Selector o práctica
if "frase_actual" not in st.session_state:
    st.session_state.frase_actual = random.choice(FRASES)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 🇧🇷 **{st.session_state.frase_actual['pt']}**")
    st.markdown(f"🇦🇷 *{st.session_state.frase_actual['es']}*")

    if st.button("🔊 Escuchar Pronunciación"):
        reproducir_audio(st.session_state.frase_actual['pt'])

with col2:
    if st.button("🔄 Siguiente Frase"):
        st.session_state.frase_actual = random.choice(FRASES)
        st.rerun()

st.markdown("---")

# Entrada de texto personalizada
st.markdown("### ✍️ Escribe tu propia frase en portugués:")
texto_usuario = st.text_input("Ingresa el texto a escuchar:", "Tudo bem, meu amigo!")

if st.button("🔊 Pronunciar mi texto"):
    if texto_usuario.strip():
        reproducir_audio(texto_usuario)
