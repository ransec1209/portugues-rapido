from io import BytesIO
import random
from gtts import gTTS
import streamlit as st

# Configuración visual de la aplicación
st.set_page_config(
    page_title="IA Assistente de Português", page_icon="🤖", layout="centered"
)


# -------------------------------------------------------------------
# MOTOR DE AUDIO ESTABLE Y RÁPIDO
# -------------------------------------------------------------------
def generar_audio(texto):
    tts = gTTS(text=texto, lang="pt", tld="com.br")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


# Base de datos de respuestas/frases del asistente
FRASES = [
    {
        "pt": "Olá! Tudo bem? Como posso ajudar você hoje?",
        "es": "¡Hola! ¿Todo bien? ¿Cómo puedo ayudarte hoy?",
    },
    {
        "pt": "Com certeza! Vamos praticar a pronúncia juntos.",
        "es": "¡Por supuesto! Vamos a practicar la pronunciación juntos.",
    },
    {
        "pt": "Por favor, onde fica o restaurante mais próximo?",
        "es": "Por favor, ¿dónde queda el restaurante más cercano?",
    },
    {
        "pt": "Muito obrigado pela sua ajuda, meu amigo!",
        "es": "¡Muchas gracias por tu ayuda, mi amigo!",
    },
    {
        "pt": "Uma cerveja bem gelada e uma água, por favor.",
        "es": "Una cerveza bien helada y un agua, por favor.",
    },
]

# -------------------------------------------------------------------
# INTERFAZ TIPO ASISTENTE DE IA
# -------------------------------------------------------------------
st.title("🤖 Assistente de Português IA")
st.caption("Tu tutor interactivo para practicar pronunciación en tiempo real")

st.markdown("---")

# Historial de conversación en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Soy tu asistente de Portugués. Escribe cualquier frase abajo para escuchar su pronunciación o toca el botón para darte un ejemplo.",
        }
    ]

# Mostrar historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "audio" in msg:
            st.audio(msg["audio"], format="audio/mp3", autoplay=True)

# Botón para pedir sugerencia a la IA
if st.button("🎲 Pedir frase de ejemplo a la IA"):
    ejemplo = random.choice(FRASES)
    texto_pt = ejemplo["pt"]
    texto_es = ejemplo["es"]

    mensaje_ia = f"🇧🇷 **{texto_pt}**\n\n🇦🇷 *(Traducción: {texto_es})*"
    audio_bytes = generar_audio(texto_pt)

    st.session_state.messages.append(
        {"role": "assistant", "content": mensaje_ia, "audio": audio_bytes}
    )
    st.rerun()

# Entrada de texto estilo Chat (Entrada del usuario)
if prompt := st.chat_input("Escribe una frase en portugués..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta del asistente con audio
    with st.spinner("Procesando voz del asistente..."):
        audio_bytes = generar_audio(prompt)
        respuesta_ia = f"🔊 Pronunciación de: **{prompt}**"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": respuesta_ia,
                "audio": audio_bytes,
            }
        )

    st.rerun()
