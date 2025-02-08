import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated
from dataclasses import dataclass
import os, getpass
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde .env

@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the chatbot."""
    number_of_queries: int = 2
    number_of_sub_fields: int = 3 
    tavily_topic: str = "general"
    tavily_days: str = None
    planner_model: str = "gpt-4o-mini"
    writer_model: str = "claude-3-5-sonnet-latest"

    @classmethod
    def from_runnable_config(cls, config):
        """Convierte un RunnableConfig en una instancia de Configuration"""
        configurable = config.configurable if hasattr(config, "configurable") else {}
        return cls(**configurable)