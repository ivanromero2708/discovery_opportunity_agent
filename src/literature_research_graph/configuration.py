from pydantic import (
    BaseModel,
    Field,
)
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from dataclasses import dataclass, fields
from typing import Any, Optional

# Cargar variables del entorno
load_dotenv()

class AgentConfiguration(BaseModel):
    "Configuration for the Agent in the literature research workflow"
    max_research_cycles: int = Field(
        description = "The maximum number of research cycles to perform before ending the workflow.",
    )
    llm_model: str = Field(
        description="The selected LLM model"
    )
    llm_temperature: float = Field(
        description="The temperature to use in the LLM model",
    )
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    core_api_key: str = os.getenv("CORE_API_KEY")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")  # Opcional para LangSmith
    
    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "AgentConfiguration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})