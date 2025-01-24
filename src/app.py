# src/app.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from market_research_graph.graph import graph
from market_research_graph.state import ResearchGraphState
from utils.report_generator import convert_markdown_to_word
from utils.config import OPENAI_API_KEY, TAVILY_API_KEY, LANGCHAIN_TRACING_V2

def initialize_session_state():
    """Configura el estado inicial de la sesión"""
    if 'research_state' not in st.session_state:
        st.session_state.research_state = {
            'industry': 'Tecnología',
            'region': 'América Latina',
            'feedback': '',
            'report_generated': False
        }

def display_sidebar():
    """Muestra la barra lateral con controles de entrada"""
    with st.sidebar:
        st.header("🚀 Configuración del Análisis")
        
        st.session_state.research_state['industry'] = st.text_input(
            "Industria Objetivo",
            value=st.session_state.research_state['industry'],
            help="Ej: Tecnología, Agricultura, Manufactura"
        )
        
        st.session_state.research_state['region'] = st.text_input(
            "Región de Estudio", 
            value=st.session_state.research_state['region'],
            help="Ej: América Latina, Sudeste Asiático"
        )
        
        st.session_state.research_state['feedback'] = st.text_area(
            "📝 Feedback del Analista",
            height=150,
            help="Ingrese comentarios para refinar el análisis"
        )
        
        if st.button("🔍 Ejecutar Análisis", use_container_width=True):
            st.session_state.research_state['report_generated'] = False
            st.rerun()

def generate_research_report():
    """Ejecuta el pipeline de investigación y genera el reporte"""
    try:
        initial_state: ResearchGraphState = {
            "company_name": "AI Research Corp",
            "industry": st.session_state.research_state['industry'],
            "region": st.session_state.research_state['region'],
            "product_services": "Servicios de Investigación de Mercado",
            "mision_vision": "Proveer insights accionables mediante IA avanzada",
            "strategic_goals": "Entregar reportes de máxima calidad",
            "human_analyst_feedback": st.session_state.research_state['feedback'],
            "analysts": [],
            "sections": [],
            "introduction": "",
            "content": "",
            "conclusion": "",
            "final_report": ""
        }
        
        with st.spinner("🚀 Ejecutando análisis completo..."):
            final_state = graph.invoke(initial_state)
            st.session_state.research_state['final_report'] = final_state["final_report"]
            st.session_state.research_state['report_generated'] = True

    except Exception as e:
        st.error(f"❌ Error en el proceso de investigación: {str(e)}")

def display_main_content():
    """Muestra el contenido principal de la aplicación"""
    st.title("🔍 AI Market Research Assistant")
    
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
                    file_name=output_file.split("/")[-1],
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
            st.success("✅ Reporte generado y listo para descargar!")
            
        except Exception as e:
            st.error(f"❌ Error al generar documento Word: {str(e)}")
    else:
        st.info("👉 Configura los parámetros en la barra lateral y haz clic en 'Ejecutar Análisis'")

def main():
    initialize_session_state()
    display_sidebar()
    
    if st.session_state.research_state.get('run_analysis', False):
        generate_research_report()
        
    display_main_content()

if __name__ == "__main__":
    main()