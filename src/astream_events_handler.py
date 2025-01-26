import streamlit as st
from literature_research_graph.graph import workflow

async def execute_research_flow(messages, placeholder, thread_id, llm_model, llm_temperature, max_research_cycles):
    """
    Maneja el flujo de investigación asíncrono, procesando eventos de herramientas y tokens del modelo.

    Args:
        messages (list): Lista de mensajes (AIMessage, HumanMessage) para enviar al grafo.
        placeholder (st.empty): Placeholder de Streamlit para mostrar el progreso.

    Returns:
        str: Respuesta final generada por el modelo.
    """
    container = placeholder
    thoughts_placeholder = container.container()  # Para mostrar estados y herramientas
    token_placeholder = container.empty()  # Para mostrar tokens progresivos
    final_text = ""  # Acumula la respuesta final

    config = {
        "configurable": {
            "thread_id": thread_id,
            "llm_model": llm_model,  # Selecciona un modelo específico
            "llm_temperature": llm_temperature,  # Personaliza el comportamiento del asistente
            "max_research_cycles": max_research_cycles  # Limita el número de ciclos de investigación
        }
    }
    
    # Flujo de eventos del grafo
    async for event in workflow.astream_events({"messages": messages}, config = config, version="v2"):
        event_type = event["event"]

        if event_type == "on_chat_model_stream":
            # Nuevo token generado por el modelo
            token = event["data"]["chunk"].content
            final_text += token
            if token:
                token_placeholder.write(final_text)  # Muestra el texto progresivo

        elif event_type == "on_tool_start":
            # Inicio de una llamada a herramienta
            with thoughts_placeholder:
                status_placeholder = st.empty()
                with status_placeholder.status("Llamando herramienta...", expanded=True) as status:
                    st.write(f"Herramienta: {event['name']}")
                    st.write("Input de la herramienta:")
                    st.code(event['data'].get('input'))  # Muestra el input de la herramienta
                    st.write("Output de la herramienta:")
                    output_placeholder = st.empty()  # Placeholder para el output
                    status.update(label="Llamada completada!", expanded=False)

        elif event_type == "on_tool_end":
            # Finalización de una llamada a herramienta
            with thoughts_placeholder:
                if 'output_placeholder' in locals():
                    output_placeholder.code(event['data'].get('output').content)  # Muestra el output

    return final_text