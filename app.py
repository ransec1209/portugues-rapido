import urllib.parse
import random
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Português Rápido - Brasil",
    page_icon="🇧🇷",
    layout="wide"
)

# -------------------------------------------------------------------
# FUNCIÓN DE AUDIO RÁPIDO Y DIRECTO
# -------------------------------------------------------------------
def obtener_url_audio(texto):
    texto_encoded = urllib.parse.quote(texto)
    # Usa el motor de voz TTS de Google optimizado
    return f"https://translate.google.com/translate_tts?ie=UTF-8&q={texto_encoded}&tl=pt-BR&client=tw-ob"

def reproducir_audio(texto):
    url_audio = obtener_url_audio(texto)
    # Genera el reproductor HTML con autoplay y acelerador a 1.5x
    audio_html = f"""
        <audio autoplay controls style="width: 100%;">
            <source src="{url_audio}" type="audio/mpeg">
            Tu navegador no soporta el reproductor de audio.
        </audio>
        <script>
            var audio = document.querySelector('audio');
            if (audio) {{
                audio.playbackRate = 1.5;
            }}
        </script>
    """
    st.components.v1.html(audio_html, height=80)

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
st.subheader("Aprende frases clave con pronunciación rápida y fluida")

st.markdown("---")

if "frase_actual" not in st.session_state:
    st.session_state.frase_actual = random.choice(FRASES)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 🇧🇷 **{st.session_state.frase_actual['pt']}**")
    st.markdown(f"🇦🇷 *{st.session_state.frase_actual['es']}*")

    if st.button("🔊 Escuchar Pronunciación"):
        reproducir_audio(st.session_state.frase_actual["pt"])

with col2:
    if st.button("🔄 Siguiente Frase"):
        st.session_state.frase_actual = random.choice(FRASES)
        st.rerun()

st.markdown("---")

st.markdown("### ✍️ Escribe tu propia frase en portugués:")
texto_usuario = st.text_input("Ingresa el texto a escuchar:", "Tudo bem, meu amigo!")

if st.button("🔊 Pronunciar mi texto"):
    if texto_usuario.strip():
        reproducir_audio(texto_usuario)
