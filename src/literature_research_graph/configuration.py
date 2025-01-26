from pydantic import (
    BaseModel,
    Field,
)


class AgentConfiguration:
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
    api_key: str = Field(
        description="The API key to use for the OpenAI API",
    )