from io import BytesIO
from gtts import gTTS
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from thefuzz import fuzz

# Configuración de página
st.set_page_config(
    page_title="Português Flutuante - Leções",
    page_icon="🇧🇷",
    layout="centered",
)

# Estilos CSS para convertir la interfaz en tarjetas limpias estilo App
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
        text-align: center;
    }
    .badge-module {
        background-color: #e7f5ff;
        color: #1c7ed6;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 12px;
    }
    .phrase-pt {
        font-size: 26px;
        font-weight: 700;
        color: #212529;
        margin-bottom: 8px;
    }
    .phrase-es {
        font-size: 18px;
        color: #6c757d;
        font-style: italic;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# MOTOR DE AUDIO ESTABLE
# -------------------------------------------------------------------
def generar_audio(texto):
    tts = gTTS(text=texto, lang="pt", tld="com.br")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


# -------------------------------------------------------------------
# BASE DE DATOS DE LECCIONES TEMÁTICAS
# -------------------------------------------------------------------
MODULOS = {
    "🍔 En el Restaurante": [
        {
            "pt": "Uma cerveja bem gelada, por favor.",
            "es": "Una cerveza bien helada, por favor.",
            "tips": "Ojo con 'gelada', la G suena suave como 'yelada'.",
        },
        {
            "pt": "A conta, por favor.",
            "es": "La cuenta, por favor.",
            "tips": "Pronuncia la 'O' final de 'conta' casi como una 'U'.",
        },
        {
            "pt": "Onde fica o banheiro?",
            "es": "¿Dónde queda el baño?",
            "tips": "'Banheiro' suena como 'bañeiro'.",
        },
    ],
    "🧳 Viajes y Servicios": [
        {
            "pt": "Bom dia! Como você está?",
            "es": "¡Buenos días! ¿Cómo estás?",
            "tips": "'Bom' se pronuncia nasalizado, sin cerrar fuerte los labios.",
        },
        {
            "pt": "Muito prazer em conhecê-lo.",
            "es": "Mucho gusto en conocerlo.",
            "tips": "La 'R' inicial de 'prazer' es suave.",
        },
        {
            "pt": "Pode falar mais devagar, por favor?",
            "es": "¿Puede hablar más despacio, por favor?",
            "tips": "'Devagar' acentúa fuerte la última sílaba.",
        },
    ],
}

# -------------------------------------------------------------------
# ESTADO DE LA SESIÓN
# -------------------------------------------------------------------
if "modulo_actual" not in st.session_state:
    st.session_state.modulo_actual = "🍔 En el Restaurante"
if "indice_frase" not in st.session_state:
    st.session_state.indice_frase = 0
if "puntos" not in st.session_state:
    st.session_state.puntos = 0
if "desbloqueado" not in st.session_state:
    st.session_state.desbloqueado = False

frases_modulo = MODULOS[st.session_state.modulo_actual]
frase_actual = frases_modulo[st.session_state.indice_frase]

# -------------------------------------------------------------------
# CABECERA Y GAMIFICACIÓN
# -------------------------------------------------------------------
col_title, col_score = st.columns([3, 1])

with col_title:
    st.title("🇧🇷 Português Rápido")

with col_score:
    st.metric(label="⭐ Experiencia", value=f"{st.session_state.puntos} XP")

# Selector de Lección
modulo_seleccionado = st.selectbox(
    "Selecciona un Módulo de Práctica:",
    list(MODULOS.keys()),
    index=list(MODULOS.keys()).index(st.session_state.modulo_actual),
)

if modulo_seleccionado != st.session_state.modulo_actual:
    st.session_state.modulo_actual = modulo_seleccionado
    st.session_state.indice_frase = 0
    st.session_state.desbloqueado = False
    st.rerun()

# Barra de Progreso del Módulo
progreso_modulo = (st.session_state.indice_frase + 1) / len(frases_modulo)
st.progress(
    progreso_modulo,
    text=f"Lección: Frase {st.session_state.indice_frase + 1} de {len(frases_modulo)}",
)

st.markdown("---")

# -------------------------------------------------------------------
# TARJETA INTERACTIVA DE APRENDIZAJE (FLASHCARD)
# -------------------------------------------------------------------
st.markdown(
    f"""
    <div class="card">
        <div class="badge-module">{st.session_state.modulo_actual}</div>
        <div class="phrase-pt">"{frase_actual['pt']}"</div>
        <div class="phrase-es">{frase_actual['es']}</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Botón para escuchar el modelo
if st.button("🔊 Escuchar Pronunciación Nativa", use_container_width=True):
    audio_file = generar_audio(frase_actual["pt"])
    st.audio(audio_file, format="audio/mp3", autoplay=True)

# Tip del Tutor de IA
with st.expander("💡 Consejo de pronunciación del tutor"):
    st.write(frase_actual["tips"])

st.markdown("---")

# -------------------------------------------------------------------
# PRÁCTICA Y DESAFÍO DE VOZ (DESBLOQUEO AL 90%)
# -------------------------------------------------------------------
st.subheader("🎤 Graba tu voz para evaluar:")

texto_escuchado = speech_to_text(
    language="pt-BR",
    start_prompt="🎙️ Toca para hablar",
    stop_prompt="⏹️ Evaluar mi pronunciación",
    key="grabador_voz",
)

if texto_escuchado:
    st.write(f"**Escuchado:** *\"{texto_escuchado}\"*")

    # Evaluación de precisión por Fuzzy Matching
    score = fuzz.ratio(
        frase_actual["pt"].lower().strip(), texto_escuchado.lower().strip()
    )

    if score >= 90:
        st.success(
            f"🎉 ¡Excelente pronunciación! Precision: **{score}%**. ¡Frase superada!"
        )
        if not st.session_state.desbloqueado:
            st.session_state.puntos += 50
            st.session_state.desbloqueado = True
    else:
        st.error(
            f"🤏 Obtuviste **{score}%**. Necesitas un 90% para avanzar. ¡Ajusta el tono y prueba de nuevo!"
        )
        st.session_state.desbloqueado = False

st.markdown("---")

# -------------------------------------------------------------------
# NAVEGACIÓN Y AVANCE BLOQUEADO
# -------------------------------------------------------------------
col_prev, col_next = st.columns(2)

with col_prev:
    if st.button("⬅️ Anterior Frase", use_container_width=True):
        if st.session_state.indice_frase > 0:
            st.session_state.indice_frase -= 1
            st.session_state.desbloqueado = False
            st.rerun()

with col_next:
    if st.session_state.desbloqueado:
        if st.button("➡️ Siguiente Frase", use_container_width=True):
            if st.session_state.indice_frase < len(frases_modulo) - 1:
                st.session_state.indice_frase += 1
                st.session_state.desbloqueado = False
                st.rerun()
            else:
                st.balloons()
                st.success("🏆 ¡Módulo completado! Selecciona otra lección.")
    else:
        st.button(
            "🔒 Siguiente Frase (Bloqueado)",
            disabled=True,
            use_container_width=True,
            help="Supera el 90% de precisión en tu grabación para avanzar.",
        )
