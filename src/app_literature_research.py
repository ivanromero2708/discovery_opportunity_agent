# app_literature_research.py

import os
import asyncio
import logging
import streamlit as st
from dotenv import load_dotenv
from contextlib import contextmanager
from datetime import datetime
import re
import uuid  # Para generar un thread_id único

# Módulos de langchain_core que usas en el chat
from langchain_core.messages import AIMessage, HumanMessage

# Importar el manejador de eventos
from astream_events_handler import execute_research_flow

# ------------------------------------------------------
# 1) Configuración inicial
# ------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("research_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cargamos las variables de entorno del archivo .env
load_dotenv()

# Configuración inicial de la página Streamlit
st.set_page_config(
    page_title="Investigador Científico IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------
# 2) Manejo de errores asíncronos
# ------------------------------------------------------
@contextmanager
def handle_async_errors():
    """Maneja errores asíncronos y muestra mensajes en la UI."""
    try:
        yield
    except Exception as e:
        logger.exception(f"Error crítico: {str(e)}")
        st.error(f"🚨 Error crítico: {str(e)}")
        st.session_state.processing = False
        st.rerun()

# ------------------------------------------------------
# 3) Inicializa estados de la aplicación
# ------------------------------------------------------
def initialize_chat():
    """Inicializa el historial de chat en session_state."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            AIMessage(content="¡Hola! Soy tu asistente de investigación. ¿En qué tema deseas profundizar hoy?")
        ]
        st.session_state.processing = False
        logger.info("Sesión de chat inicializada")

def initialize_research_state():
    """
    Inicializa el diccionario research_state en session_state
    para manejar configuración de la conversación: 
    - thread_id
    - modelo LLM
    - temperatura
    - max_research_cycles, etc.
    """
    if "research_state" not in st.session_state:
        st.session_state["research_state"] = {
            "thread_id": None,  
            "llm_model": "gpt-4o-mini",  
            "temperature": 0.0,
            "max_research_cycles": 3,
        }

# ------------------------------------------------------
# 4) Sidebar con controles de configuración (opcional)
# ------------------------------------------------------
def display_sidebar():
    """Muestra la barra lateral con campos de configuración."""
    with st.sidebar:
        st.header("🔧 Configuración del Análisis")
        
        # Campo para seleccionar el modelo LLM
        st.session_state.research_state['llm_model'] = st.text_input(
            "Modelo LLM",
            value=st.session_state.research_state['llm_model'],
            help="Ejemplos: gpt-4, gpt-3.5-turbo"
        )
        
        # Campo para configurar la temperatura del modelo
        st.session_state.research_state['temperature'] = st.number_input(
            "Temperatura del Modelo",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.research_state['temperature'],
            step=0.1,
            help="Controla la creatividad del modelo (0.0 = determinístico, 2.0 = muy creativo)"
        )
        
        # Campo para configurar max_research_cycles
        st.session_state.research_state['max_research_cycles'] = st.number_input(
            "Máximo de research cycles",
            min_value=1,
            max_value=20,
            value=st.session_state.research_state['max_research_cycles'],
            step=1,
            help="Número máximo de iteraciones de investigación antes de terminar"
        )
        
        st.markdown("---")

        # Botón que genera un nuevo thread y ejecuta el análisis
        if st.button("🎉 Iniciar Nueva Conversación", use_container_width=True):
            # Creamos un nuevo thread_id con uuid
            new_thread = str(uuid.uuid4())
            st.session_state.research_state['thread_id'] = new_thread
            st.success(f"Nuevo thread iniciado: {new_thread}")

# ------------------------------------------------------
# 5) Renderizar el historial de chat
# ------------------------------------------------------
def render_chat_history():
    """Renderiza el historial del chat con formato mejorado."""
    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🔬"):
                st.markdown(msg.content)
        elif isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg.content)

# ------------------------------------------------------
# 6) Lógica principal de la app
# ------------------------------------------------------
def main():
    st.title("🔍 Investigador Científico Asistido por IA")
    
    # 1) Inicializar estados
    initialize_research_state()  
    initialize_chat()

    # 2) Muestra sidebar (puedes comentar si no lo necesitas)
    display_sidebar()

    # 3) Renderizar historial
    render_chat_history()

    # 4) Capturar una nueva pregunta de investigación
    if prompt := st.chat_input("Escribe tu pregunta de investigación..."):
        # Evita que se envíen preguntas mientras se procesa
        if st.session_state.processing:
            st.warning("Espera a que termine la operación actual")
            return

        st.session_state.processing = True
        st.session_state.messages.append(HumanMessage(content=prompt))
        logger.info(f"Nueva consulta: {prompt[:100]}...")  # Loggea un snippet

        st.chat_message("user", avatar="👤").write(prompt)

        # 5) Llamar a la función que ejecuta el flow
        with st.chat_message("assistant", avatar="🔬"):
            placeholder = st.container()
            
            with handle_async_errors(), st.spinner("🔍 Analizando consulta..."):
                try:
                    thread_id = st.session_state.research_state['thread_id']
                    llm_model = st.session_state.research_state['llm_model']
                    llm_temperature = st.session_state.research_state['temperature']
                    max_cycles = st.session_state.research_state['max_research_cycles']

                    # Llamada a tu astream pipeline
                    response = asyncio.run(
                        execute_research_flow(
                            st.session_state.messages,
                            placeholder,
                            thread_id,
                            llm_model,
                            llm_temperature,
                            max_cycles
                        )
                    )
                    
                    # Mostrar la respuesta final (limpia markdown)
                    if response:
                        clean_response = re.sub(r"```markdown\n|\n```", "", response)
                        final_message = AIMessage(content=clean_response)
                        st.session_state.messages.append(final_message)
                        logger.info("Respuesta generada exitosamente")
                finally:
                    st.session_state.processing = False
                    logger.info("Proceso completado")


if __name__ == "__main__":
    main()
