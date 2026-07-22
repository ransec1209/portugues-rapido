from io import BytesIO
import random
from gtts import gTTS
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from thefuzz import fuzz

# Configuración de la página
st.set_page_config(
    page_title="Desafío de Pronúncia - IA", page_icon="🎯", layout="centered"
)


# -------------------------------------------------------------------
# FUNCIÓN DE AUDIO SINTETIZADO
# -------------------------------------------------------------------
def generar_audio(texto):
    tts = gTTS(text=texto, lang="pt", tld="com.br")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


# Base de datos de frases
FRASES = [
    {"pt": "Bom dia! Como você está?", "es": "¡Buenos días! ¿Cómo estás?"},
    {"pt": "Muito prazer em conhecê-lo.", "es": "Mucho gusto en conocerlo."},
    {
        "pt": "Por favor, onde fica o banheiro?",
        "es": "Por favor, ¿dónde queda el baño?",
    },
    {"pt": "Quanto custa isto?", "es": "¿Cuánto cuesta esto?"},
    {"pt": "Obrigado por tudo!", "es": "¡Gracias por todo!"},
]

# -------------------------------------------------------------------
# ESTADO DE LA SESIÓN
# -------------------------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "precision" not in st.session_state:
    st.session_state.precision = 0
if "desbloqueado" not in st.session_state:
    st.session_state.desbloqueado = False

frase_actual = FRASES[st.session_state.indice]

# -------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -------------------------------------------------------------------
st.title("🎯 Desafío de Pronunciación (Examen 90%)")
st.caption(
    "Escucha la frase, presiona el micrófono para pronunciarla. La app calculará tu precisión y solo te dejará avanzar si alcanzas el 90%."
)

st.markdown("---")

st.subheader(f"Frase #{st.session_state.indice + 1} de {len(FRASES)}")
st.markdown(f"### 🇧🇷 **{frase_actual['pt']}**")
st.markdown(f"🇦🇷 *{frase_actual['es']}*")

# Escuchar modelo
if st.button("🔊 Escuchar pronunciación correcta"):
    audio_bytes = generar_audio(frase_actual["pt"])
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

st.markdown("---")

# -------------------------------------------------------------------
# RECONOCIMIENTO Y EVALUACIÓN DE VOZ
# -------------------------------------------------------------------
st.markdown("### 🎤 Tu turno de hablar:")

# Componente de grabación con reconocimiento de voz en portugués
texto_escuchado = speech_to_text(
    language="pt-BR",
    start_prompt="🔴 Presiona para Grabar",
    stop_prompt="⏹️ Detener y Evaluar",
    key="reconocedor_voz",
)

if texto_escuchado:
    st.write(f"**Lo que la IA escuchó:** *\"{texto_escuchado}\"*")

    # Comparación de precisión usando Fuzzy Logic
    score = fuzz.ratio(
        frase_actual["pt"].lower().strip(), texto_escuchado.lower().strip()
    )
    st.session_state.precision = score

    # Evaluación según el 90%
    if score >= 90:
        st.success(
            f"🎉 ¡Excelente pronunciación! Precisión obtenida: **{score}%**"
        )
        st.session_state.desbloqueado = True
    else:
        st.error(
            f"❌ Precisión obtenida: **{score}%**. Necesitas al menos 90% para avanzar. ¡Inténtalo de nuevo!"
        )
        st.session_state.desbloqueado = False

# Metric de progreso
st.progress(
    st.session_state.precision / 100,
    text=f"Precisión actual: {st.session_state.precision}% / Meta: 90%",
)

st.markdown("---")

# -------------------------------------------------------------------
# BOTÓN DE AVANCE CONDICIONAL
# -------------------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🔄 Reiniciar nivel"):
        st.session_state.precision = 0
        st.session_state.desbloqueado = False
        st.rerun()

with col2:
    # Solo habilita el botón si superó el 90%
    if st.session_state.desbloqueado:
        if st.button("➡️ Siguiente Frase (Desbloqueado)"):
            if st.session_state.indice < len(FRASES) - 1:
                st.session_state.indice += 1
                st.session_state.precision = 0
                st.session_state.desbloqueado = False
                st.rerun()
            else:
                st.balloons()
                st.success(
                    "🏆 ¡Felicitaciones! Has completado todo el módulo con pronunciación perfecta."
                )
    else:
        st.button(
            "🔒 Siguiente Frase (Bloqueado)",
            disabled=True,
            help="Alcanza el 90% de precisión para desbloquear esta opción.",
        )
