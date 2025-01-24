from ..state import InterviewState, SearchQuery
from ..prompts import search_instructions
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import os
from utils.config import TAVILY_API_KEY, TAVILY_MAX_RESULTS, LANGCHAIN_TRACING_V2

class SearchWeb:
    def __init__(self) -> None:
        self.tavily_search = TavilySearchResults(
            max_results=TAVILY_MAX_RESULTS,
            api_key=TAVILY_API_KEY
        )
        self.model = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=OPENAI_TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        
    def search_web(self, state: InterviewState):
    
        """ Retrieve docs from web search """

        # Search query
        structured_llm = self.model.with_structured_output(SearchQuery)
        search_query = structured_llm.invoke([search_instructions]+state['messages'])
        
        # Search
        search_docs = self.tavily_search.invoke(search_query.search_query)

        # Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
                for doc in search_docs
            ]
        )

        return {"context": [formatted_search_docs]}
    
    def run(self, state: InterviewState):
        result = self.search_web(state)
        return result