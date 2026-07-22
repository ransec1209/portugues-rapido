import streamlit as st
from gtts import gTTS
import io
import random

# Configuración de la página
st.set_page_config(
    page_title="Português Rápido - Brasil",
    page_icon="🇧🇷",
    layout="wide"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (Interfaz & Menú Amigable)
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Encabezado Principal */
    .header-container {
        background: linear-gradient(135deg, #0b6623 0%, #1a365d 100%);
        padding: 22px;
        border-radius: 14px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #f6e05e;
        font-weight: 300;
        margin-top: 4px;
    }

    /* Tarjetas de Diálogo / Vocabulario */
    .dialog-card {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 15px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.03);
    }

    .translation-box {
        background-color: #f0f9ff;
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 8px;
        border: 1px solid #bae6fd;
    }

    .pt-text {
        color: #1e293b;
        font-size: 1.15rem;
        font-weight: 600;
    }
    
    .es-text {
        color: #0369a1;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .pron-text {
        color: #15803d;
        font-size: 0.9rem;
        font-style: italic;
        margin-top: 4px;
    }

    /* Estilos Generales de Botones */
    .stButton>button {
        background-color: #16a34a;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 10px 18px;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #15803d;
        color: #ffffff;
    }

    /* MENÚ LATERAL AMIGABLE Y ESTILIZADO */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sidebar-section-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Principal
st.markdown("""
    <div class="header-container">
        <div class="header-title">🇧🇷 Português Rápido</div>
        <div class="header-subtitle">Plataforma Móvil de Lectura, Pronunciación y Práctica</div>
    </div>
""", unsafe_allow_html=True)

# Función para generar audio
def reproducir_audio(texto, lento=False):
    tts = gTTS(text=texto, lang='pt', tld='com.br', slow=lento)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format='audio/mp3')

# Base de Datos Ampliada
vocabulario_base = [
    # Saludos y Cortesía
    {"pt": "Oi, tudo bem?", "es": "¡Hola! ¿Todo bien?", "pron": "Oi, tu-do bein?", "cat": "Saludos y Cortesía"},
    {"pt": "Bom dia, como você está?", "es": "Buenos días, ¿cómo estás?", "pron": "Bon jí-a, ko-mu vo-se es-ta?", "cat": "Saludos y Cortesía"},
    {"pt": "Muito obrigado! / Obrigada!", "es": "¡Muchas gracias!", "pron": "Mui-tu o-bri-ga-du / o-bri-ga-da", "cat": "Saludos y Cortesía"},
    {"pt": "Com licença / Dá licença", "es": "Con permiso / Permiso", "pron": "Kon li-sen-sa / Da li-sen-sa", "cat": "Saludos y Cortesía"},
    
    # Atención al Cliente
    {"pt": "Seja bem-vindo!", "es": "¡Sea bienvenido!", "pron": "Se-ja bein-vin-du!", "cat": "Atención al Cliente"},
    {"pt": "Em que posso ajudar?", "es": "¿En qué puedo ayudar?", "pron": "Ein ke po-su a-ju-dar?", "cat": "Atención al Cliente"},
    {"pt": "Sente-se por favor, a sua mesa está pronta", "es": "Tome asiento por favor, su mesa está lista", "pron": "Sen-chi-se por fa-vor, a su-a me-sa es-ta pron-ta", "cat": "Atención al Cliente"},
    {"pt": "Tudo esteve do seu agrado?", "es": "¿Todo estuvo de su agrado?", "pron": "Tu-do es-chi-ve du seu a-gra-du?", "cat": "Atención al Cliente"},

    # Gastronomía y Servicio
    {"pt": "A conta, por favor", "es": "La cuenta, por favor", "pron": "A kon-ta, por fa-vor", "cat": "Gastronomía y Servicio"},
    {"pt": "Uma cerveja bem gelada", "es": "Una cerveza bien fría", "pron": "U-ma ser-ve-ja bein je-la-da", "cat": "Gastronomía y Servicio"},
    {"pt": "Qual é o ponto da carne?", "es": "¿Cuál es el punto de la carne?", "pron": "Kual e u pon-tu da kar-ni?", "cat": "Gastronomía y Servicio"},
    {"pt": "Mal passada / Ao ponto / Bem passada", "es": "Jugosa / Al punto / Bien cocida", "pron": "Mal pa-sa-da / Au pon-tu / Bein pa-sa-da", "cat": "Gastronomía y Servicio"},
    {"pt": "Alguém tem alguma alergia alimentar?", "es": "¿Alguien tiene alguna alergia alimentaria?", "pron": "Al-guein tein al-gu-ma a-ler-ji-a a-li-men-tar?", "cat": "Gastronomía y Servicio"},

    # Trabajo y Operaciones
    {"pt": "Vamos fazer o briefing do serviço", "es": "Vamos a hacer el briefing del servicio", "pron": "Va-mus fa-zer u bri-fing du ser-vi-su", "cat": "Trabajo y Operaciones"},
    {"pt": "A mise en place está completa", "es": "La mise en place está completa", "pron": "A miz an plas es-ta kom-ple-ta", "cat": "Trabajo y Operaciones"},
    {"pt": "Bom trabalho a todos!", "es": "¡Buen trabajo a todos!", "pron": "Bon tra-ba-lhu a to-dus!", "cat": "Trabajo y Operaciones"}
]

# ---------------------------------------------------------
# MENÚ LATERAL AMIGABLE Y CORREGIDO
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧭 Menú Principal</div>', unsafe_allow_html=True)
    st.caption("Selecciona el módulo que deseas practicar hoy")
    
    st.markdown('<div class="sidebar-section-label">📚 Estudio & Búsqueda</div>', unsafe_allow_html=True)
    
    # Opciones con íconos grandes e intuitivos
    opciones_menu = {
        "📖 Lectura y Pronunciación": "Módulo de Lectura y Audio",
        "🔍 Buscador Inteligente": "Buscador Rápido",
        "🎴 Tarjetas de Repaso": "Flashcards Interactivas",
        "🧩 Juego de Emparejar": "Juego: Emparejar Palabras",
        "🎙️ Desafío Auditivo": "Quiz Auditivo"
    }
    
    seleccion = st.radio(
        label="Navegación",
        options=list(opciones_menu.keys()),
        label_visibility="collapsed"
    )
    
    opcion = opciones_menu[seleccion]
    
    st.divider()
    
    st.markdown('<div class="sidebar-section-label">🔊 Ajustes de Voz</div>', unsafe_allow_html=True)
    velocidad_lenta = st.toggle("🐌 Reproducir audio despacio", value=False)

lista_categorias = ["Todas"] + sorted(list(set(item["cat"] for item in vocabulario_base)))

# ---------------------------------------------------------
# SECCIÓN 1: LECTURA Y AUDIO
# ---------------------------------------------------------
if opcion == "Módulo de Lectura y Audio":
    st.markdown("### 📖 Lectura y Pronunciación Guía")
    categoria_sel = st.selectbox("📂 Selecciona una categoría:", lista_categorias)
    
    datos_filtrados = vocabulario_base if categoria_sel == "Todas" else [d for d in vocabulario_base if d["cat"] == categoria_sel]
    
    st.divider()

    for item in datos_filtrados:
        col_card, col_audio = st.columns([3, 1.2])
        with col_card:
            st.markdown(f"""
                <div class="dialog-card">
                    <div class="pt-text">🇧🇷 {item['pt']}</div>
                    <div class="pron-text">🗣️ Pronunciación: {item['pron']}</div>
                    <div class="translation-box">
                        <span class="es-text">🇪🇸 {item['es']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col_audio:
            st.write("")
            reproducir_audio(item["pt"], lento=velocidad_lenta)

# ---------------------------------------------------------
# SECCIÓN 2: BUSCADOR
# ---------------------------------------------------------
elif opcion == "Buscador Rápido":
    st.markdown("### 🔍 Buscador de Palabras y Frases")
    busqueda = st.text_input("Escribe cualquier término en español o portugués:")
    
    if busqueda:
        resultados = [
            d for d in vocabulario_base 
            if busqueda.lower() in d["pt"].lower() or busqueda.lower() in d["es"].lower()
        ]
        
        if resultados:
            st.success(f"Se encontraron {len(resultados)} resultado(s):")
            for item in resultados:
                col_card, col_audio = st.columns([3, 1.2])
                with col_card:
                    st.markdown(f"""
                        <div class="dialog-card">
                            <div class="pt-text">🇧🇷 {item['pt']}</div>
                            <div class="pron-text">🗣️ Pronunciación: {item['pron']}</div>
                            <div class="translation-box">
                                <span class="es-text">🇪🇸 {item['es']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_audio:
                    st.write("")
                    reproducir_audio(item["pt"], lento=velocidad_lenta)
        else:
            st.warning("No se encontraron coincidencias.")

# ---------------------------------------------------------
# SECCIÓN 3: FLASHCARDS
# ---------------------------------------------------------
elif opcion == "Flashcards Interactivas":
    st.markdown("### 🎴 Tarjetas de Memorización")
    
    if "indice" not in st.session_state:
        st.session_state.indice = 0
        
    item_actual = vocabulario_base[st.session_state.indice]
    
    st.markdown(f"""
        <div class="dialog-card" style="text-align: center; padding: 25px;">
            <span style="color: #64748b; font-size: 0.85rem;">Categoría: {item_actual['cat']}</span>
            <h2 style="color: #1e293b; margin: 10px 0;">🇧🇷 {item_actual['pt']}</h2>
            <p class="pron-text" style="font-size: 1rem;">🗣️ {item_actual['pron']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    reproducir_audio(item_actual["pt"], lento=velocidad_lenta)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("👁️ Revelar Traducción"):
            st.markdown(f"""
                <div class="translation-box" style="text-align: center; padding: 12px;">
                    <span class="es-text" style="font-size: 1.1rem;">🇪🇸 {item_actual['es']}</span>
                </div>
            """, unsafe_allow_html=True)
    with col_btn2:
        if st.button("➡️ Siguiente Tarjeta"):
            st.session_state.indice = (st.session_state.indice + 1) % len(vocabulario_base)
            st.rerun()

# ---------------------------------------------------------
# SECCIÓN 4: JUEGO DE EMPAREJAR
# ---------------------------------------------------------
elif opcion == "Juego: Emparejar Palabras":
    st.markdown("### 🧩 Desafío: Empareja las Frases")
    st.write("Relaciona la traducción correcta en español:")

    if "juego_items" not in st.session_state:
        st.session_state.juego_items = random.sample(vocabulario_base, 4)

    correctas = 0
    for idx, item in enumerate(st.session_state.juego_items):
        st.markdown(f"**{idx + 1}. 🇧🇷 {item['pt']}**")
        
        opciones = [item["es"]] + [
            x["es"] for x in vocabulario_base if x["es"] != item["es"]
        ][:2]
        random.seed(idx)
        random.shuffle(opciones)
        
        eleccion = st.radio(f"Opción para la frase {idx + 1}:", opciones, key=f"juego_{idx}")
        
        if eleccion == item["es"]:
            correctas += 1
        st.divider()

    if st.button("🏆 Verificar Puntaje"):
        if correctas == 4:
            st.balloons()
            st.success("¡Puntaje Perfecto! 4/4 respuestas correctas. 🔥")
        else:
            st.info(f"Lograste {correctas} de 4 aciertos. ¡A seguir practicando!")

# ---------------------------------------------------------
# SECCIÓN 5: QUIZ AUDITIVO
# ---------------------------------------------------------
elif opcion == "Quiz Auditivo":
    st.markdown("### 🎙️ Desafío Auditivo Nativo")
    
    if "quiz_item" not in st.session_state:
        st.session_state.quiz_item = random.choice(vocabulario_base)

    item_q = st.session_state.quiz_item
    
    st.write("Escucha atentamente el audio:")
    reproducir_audio(item_q["pt"], lento=velocidad_lenta)
    
    opciones_incorrectas = [x["es"] for x in vocabulario_base if x["es"] != item_q["es"]]
    opciones_quiz = random.sample(opciones_incorrectas, 2) + [item_q["es"]]
    random.shuffle(opciones_quiz)

    eleccion_quiz = st.radio("¿Qué significa la frase escuchada?", opciones_quiz)
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button("Comprobar Respuesta"):
            if eleccion_quiz == item_q["es"]:
                st.balloons()
                st.success(f"¡Excelente! Significa: **{item_q['es']}**")
            else:
                st.error("Respuesta incorrecta. Escucha nuevamente.")
    with col_q2:
        if st.button("🎲 Siguiente Pregunta"):
            st.session_state.quiz_item = random.choice(vocabulario_base)
            st.rerun()
