from typing import List, Optional, TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langgraph.graph import MessagesState
import operator

class Analyst(TypedDict):
    name: str           # Analyst name.
    affiliation: str    # Analyst affiliation.
    role: str           # Role in research.
    description: str    # Brief description of focus and perspective.

class InterviewState(MessagesState):
    max_num_turns: int                   # Maximum Q&A turns allowed.
    context: Annotated[list, operator.add] # List of context snippets or source documents.
    analyst: Analyst                     # Analyst persona.
    interview: str             # Complete transcript of the interview.
    sections: list       # Final memo sections produced from the interview.
