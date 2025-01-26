import os
import asyncio
import logging
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from contextlib import contextmanager
from datetime import datetime
import re
import uuid  # Para generar un thread_id único

# Importar el manejador de eventos
from astream_events_handler import execute_research_flow

# Configuración inicial de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("research_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# Configuración inicial de la página
st.set_page_config(
    page_title="Investigador Científico IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def setup_api_key():
    """Configuración segura de API Keys con validación."""
    st.sidebar.header("🔑 Configuración de API Keys")
    
    openai_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Obtén tu clave en https://platform.openai.com/account/api-keys"
    )
    
    if st.sidebar.button("💾 Guardar Clave", type="primary"):
        if not openai_key:
            st.error("OpenAI API Key es requerida")
        else:
            os.environ["OPENAI_API_KEY"] = openai_key
            st.session_state.api_keys_set = True
            logger.info("API Key configurada correctamente")
            st.success("✅ Clave configurada correctamente")
            st.rerun()

def initialize_chat():
    """Inicializa el estado del chat con valores por defecto."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            AIMessage(content="¡Hola! Soy tu asistente de investigación. ¿En qué tema deseas profundizar hoy?")
        ]
        st.session_state.processing = False
        logger.info("Sesión de chat inicializada")

import streamlit as st
import uuid

def display_sidebar():
    """Muestra la barra lateral con campos de configuración."""
    with st.sidebar:
        st.header("🔧 Configuración del Análisis")
        
        # Campo para seleccionar el modelo LLM
        st.session_state.research_state['llm_model'] = st.text_input(
            "Modelo LLM",
            value="gpt-4o-mini",
            help="Ejemplos: gpt-4, gpt-4o, gpt-3.5-turbo"
        )
        
        # Campo para configurar la temperatura del modelo
        st.session_state.research_state['temperature'] = st.number_input(
            "Temperatura del Modelo",
            min_value=0.0,
            max_value=2.0,
            value=0,
            step=0.1,
            help="Controla la creatividad del modelo (0.0 = determinístico, 2.0 = muy creativo)"
        )
        
        st.markdown("---")

        # Botón que genera un nuevo thread y ejecuta el análisis
        if st.button("🎉 Iniciar Nueva Conversación", use_container_width=True):
            # Creamos un nuevo thread_id con uuid
            new_thread = str(uuid.uuid4())
            st.session_state.research_state['thread_id'] = new_thread
            st.success(f"Nuevo thread iniciado: {new_thread}")

def render_chat_history():
    """Renderiza el historial del chat con formato mejorado."""
    for msg in st.session_state.messages:
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🔬"):
                st.markdown(msg.content)
        elif isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg.content)

def main():
    st.title("🔍 Investigador Científico Asistido por IA")
    
    setup_api_key()
    
    if not st.session_state.get("api_keys_set", False):
        st.info("⚠️ Configura tu API Key en la barra lateral")
        return

    initialize_chat()
    render_chat_history()
    thread_id = st.session_state.research_state['thread_id']
    config = {"configurable": {"thread_id": thread_id}, }
    
    
    if prompt := st.chat_input("Escribe tu pregunta de investigación..."):
        if st.session_state.processing:
            st.warning("Espera a que termine la operación actual")
            return

        st.session_state.processing = True
        st.session_state.messages.append(HumanMessage(content=prompt))
        logger.info(f"Nueva consulta: {prompt[:100]}...")
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🔬"):
            placeholder = st.empty()
            
            with handle_async_errors(), st.spinner("🔍 Analizando consulta..."):
                try:
                    response = asyncio.run(
                        execute_research_flow(
                            st.session_state.messages,
                            placeholder,
                            st.session_state.research_state['thread_id'],
                            st.session_state.research_state['llm_model'],
                            st.session_state.research_state['temperature']
                        )
                    )
                    
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