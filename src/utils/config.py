# src/utils/config.py
import os
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()

# Configuración de APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")  # Opcional para LangSmith

# Configuración de modelos
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.0

# Configuración de búsqueda
TAVILY_MAX_RESULTS = 3

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"