import streamlit as st
from gtts import gTTS
from io import BytesIO
import random

# Configuración de la página
st.set_page_config(
    page_title="Português Rápido - Brasil",
    page_icon="🇧🇷",
    layout="wide"
)

# -------------------------------------------------------------------
# FUNCIÓN DE AUDIO SIMPLE Y DIRECTA
# -------------------------------------------------------------------
def generar_audio(texto):
    # Genera audio en portugués de Brasil
    tts = gTTS(text=texto, lang="pt", tld="com.br")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# -------------------------------------------------------------------
# BASE DE DATOS DE FRASES
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
st.subheader("Aprende frases clave con pronunciación en vivo")

st.markdown("---")

if "frase_actual" not in st.session_state:
    st.session_state.frase_actual = random.choice(FRASES)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 🇧🇷 **{st.session_state.frase_actual['pt']}**")
    st.markdown(f"🇦🇷 *{st.session_state.frase_actual['es']}*")

    if st.button("🔊 Generar Audio"):
        with st.spinner("Cargando voz..."):
            audio_bytes = generar_audio(st.session_state.frase_actual['pt'])
            st.audio(audio_bytes, format="audio/mp3")

with col2:
    if st.button("🔄 Siguiente Frase"):
        st.session_state.frase_actual = random.choice(FRASES)
        st.rerun()

st.markdown("---")

st.markdown("### ✍️ Escribe tu propia frase en portugués:")
texto_usuario = st.text_input("Ingresa el texto a escuchar:", "Tudo bem, meu amigo!")

if st.button("🔊 Pronunciar mi texto"):
    if texto_usuario.strip():
        with st.spinner("Cargando voz..."):
            audio_bytes_user = generar_audio(texto_usuario)
            st.audio(audio_bytes_user, format="audio/mp3")
