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
        configurable = config.get("configurable", {}) if config else {}

        # Pydantic 2.x -> cls.model_fields.  Pydantic <2.x -> cls.__fields__
        # Ajusta según tu versión. Supongamos Pydantic 2.x:
        fields_dict = cls.model_fields

        values: dict[str, Any] = {}
        for field_name in fields_dict:
            # Prioridad: ENV var -> config["configurable"] -> lo que ya tenga en la clase
            env_value = os.environ.get(field_name.upper())
            config_value = configurable.get(field_name)
            # Elige el primero que NO sea None
            final_value = env_value if env_value is not None else config_value
            if final_value is not None:
                values[field_name] = final_value

        # Instancia la pydantic model con los valores recolectados
        return cls(**values)