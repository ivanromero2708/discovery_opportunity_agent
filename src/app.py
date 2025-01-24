# src/app.py

import sys
import os
import uuid  # Para generar un thread_id único
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

# Importa tu grafo compilado
from market_research_graph.graph import graph
from market_research_graph.state import ResearchGraphState
from utils.report_generator import convert_markdown_to_word

def initialize_session_state():
    """
    Configura el estado inicial de la sesión de Streamlit.
    """
    if 'research_state' not in st.session_state:
        st.session_state.research_state = {
            'company_name': 'IR Consulting',
            'industry': 'Innovation Strategy Consulting',
            'region': 'USA',
            'product_services': 'Technology and Market Research Services',
            'feedback': '',
            'report_generated': False,
            'run_analysis': False,
            'final_report': '',
            'analysts': [],
            # Dejamos un campo para almacenar el thread_id único
            'thread_id': None,
        }

def display_sidebar():
    """Muestra la barra lateral con campos de configuración."""
    with st.sidebar:
        st.header("🔧 Configuración del Análisis")

        st.session_state.research_state['company_name'] = st.text_input(
            "Nombre de la empresa",
            value=st.session_state.research_state['company_name'],
            help="Ej: Amazon, Tesla, Meta..."
        )
        
        st.session_state.research_state['industry'] = st.text_input(
            "Industria Objetivo",
            value=st.session_state.research_state['industry'],
            help="Ej: Tecnología, Agricultura, Manufactura, etc."
        )
        
        st.session_state.research_state['region'] = st.text_input(
            "Región de Estudio", 
            value=st.session_state.research_state['region'],
            help="Ej: América Latina, Sudeste Asiático"
        )
        
        st.session_state.research_state['product_services'] = st.text_input(
            "Productos/Servicios a investigar", 
            value=st.session_state.research_state['product_services'],
            help="Ej:Technology and Market Research Services"
        )
        
        st.session_state.research_state['feedback'] = st.text_area(
            "📝 Feedback del Analista",
            height=120,
            help="Ingrese comentarios para refinar el análisis"
        )
        
        st.markdown("---")

        # Botón que genera un thread nuevo y ejecuta el análisis
        if st.button("🎉 Iniciar Nuevo Reporte", use_container_width=True):
            # Marcamos que se generará un nuevo análisis
            st.session_state.research_state['report_generated'] = False
            # Creamos un nuevo thread_id con uuid
            new_thread = str(uuid.uuid4())
            st.session_state.research_state['thread_id'] = new_thread
            st.session_state.research_state['run_analysis'] = True
            st.rerun()

def generate_research_report():
    """
    Ejecuta el pipeline (graph) en dos fases:
      1) Stream hasta la interrupción en 'human_feedback'.
      2) Inyecta el feedback humano y continúa hasta el final.
      3) Guarda el 'final_report' en session_state.
    """
    try:
        # Construimos el estado inicial
        initial_state: ResearchGraphState = {
            "company_name": st.session_state.research_state['company_name'],
            "industry": st.session_state.research_state['industry'],
            "region": st.session_state.research_state['region'],
            "product_services": st.session_state.research_state['product_services'],
            "mision_vision": "",
            "strategic_goals": "",
            # No asignamos feedback aún, lo haremos en la fase 2
            "human_analyst_feedback": None,
            "analysts": [],
            "sections": [],
            "introduction": "",
            "content": "",
            "conclusion": "",
            "final_report": ""
        }

        # Obtenemos el thread_id guardado en session_state
        thread_id = st.session_state.research_state['thread_id']
        if not thread_id:
            raise ValueError("No se ha definido un thread_id. Presiona 'Iniciar Nuevo Reporte' en la barra lateral.")

        # Creamos la config para el checkpointer
        thread_info = {"configurable": {"thread_id": thread_id}}

        st.write("## 🏁 Fase 1: Generando Analistas (hasta `human_feedback`)")
        st.markdown("A continuación, el grafo se ejecuta hasta que detecta la interrupción para inyectar el feedback humano.")
        
        with st.spinner("Ejecutando primera fase..."):
            # Corre el grafo en modo streaming
            for event in graph.stream(initial_state, thread_info, stream_mode="values"):
                # Si se generan analistas en esta etapa, los mostramos
                if "analysts" in event and event["analysts"]:
                    st.session_state.research_state['analysts'] = event["analysts"]
                    st.write("**Analistas generados:**")
                    for a in event["analysts"]:
                        st.markdown(f"- **{a.name}** - {a.role}\n  {a.description}")
        
        st.markdown("---")
        st.write("## ✏️ Fase 2: Inyectando Feedback Humano y completando el Reporte")

        # Inyectamos el feedback del usuario
        user_feedback = st.session_state.research_state['feedback'] or None
        graph.update_state(thread_info, {"human_analyst_feedback": user_feedback}, as_node="human_feedback")

        with st.spinner("Ejecutando segunda fase..."):
            for event in graph.stream(None, thread_info, stream_mode="updates"):
                # Podrías mostrar el nombre del nodo si deseas, p.ej.:
                # node_name = next(iter(event.keys()))
                # st.write(f"Ejecutando nodo: {node_name}")
                pass

        # Finalmente, obtenemos el estado final
        final_state = graph.get_state(thread_info)
        final_report = final_state.values.get('final_report')
        if not final_report:
            raise ValueError("No se encontró 'final_report' en el estado final del grafo.")

        # Guardamos el reporte en session_state
        st.session_state.research_state['final_report'] = final_report
        st.session_state.research_state['report_generated'] = True

    except Exception as e:
        st.error(f"❌ Error durante la ejecución del análisis: {str(e)}")
        st.session_state.research_state['report_generated'] = False

def display_main_content():
    """Muestra el reporte final y el botón de descarga, si está listo."""
    st.title("📝 AI Market Research Assistant")
    st.markdown("¡Bienvenido! Configura los parámetros en la barra lateral y haz clic en **Iniciar Nuevo Reporte** para comenzar.")
    
    if st.session_state.research_state['report_generated']:
        st.subheader("📄 Reporte Final Generado")
        with st.expander("Ver Reporte Completo", expanded=True):
            st.markdown(st.session_state.research_state['final_report'])

        try:
            output_file = convert_markdown_to_word(
                st.session_state.research_state['final_report'],
                st.session_state.research_state['industry'],
                st.session_state.research_state['region']
            )
            with open(output_file, "rb") as f:
                st.download_button(
                    label="⬇️ Descargar Reporte en Word",
                    data=f,
                    file_name=os.path.basename(output_file),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            st.success("✅ Reporte generado y listo para descargar!")

        except Exception as e:
            st.error(f"❌ Error al generar documento Word: {str(e)}")

    else:
        st.info("👉 Configura los parámetros en la barra lateral y haz clic en 'Iniciar Nuevo Reporte'")

    # Bloque opcional para inspeccionar todo el session_state
    with st.expander("Ver estado interno (debug)"):
        st.json(st.session_state.research_state)

def main():
    """Punto de entrada principal de la aplicación Streamlit."""
    initialize_session_state()
    display_sidebar()

    # Si el usuario presionó "Iniciar Nuevo Reporte"
    if st.session_state.research_state.get('run_analysis', False):
        generate_research_report()
        # Si quieres que, tras terminar, NO siga marcando run_analysis = True, haz:
        # st.session_state.research_state['run_analysis'] = False

    display_main_content()

if __name__ == "__main__":
    main()
