from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from ..state import SubFieldResearchGraphState, PatentSearchEquation
from ...configuration import Configuration
from ..prompts import PROMPT_CREATE_SEARCH_EQUATION


class CreateSearchEquation:
    def __init__(self):
        self.configurable = None
    
    def create_search_equation(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        
        research_plan = state["research_plan"]
        industry_context = research_plan.industry_context
        technology_domain = research_plan.technology_domain
        key_applications = research_plan.key_applications
        research_objective = research_plan.research_objective
        supporting_questions = research_plan.supporting_questions
        
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model = configurable.planner_model, temperature = 0)
        number_of_core_terms = configurable.number_of_core_terms
        number_of_related_terms = configurable.number_of_related_terms
        number_of_exclusion_terms = configurable.number_of_exclusion_terms        
        
        system_instructions = PROMPT_CREATE_SEARCH_EQUATION.format(
            industry_context = industry_context,
            technology_domain = technology_domain,
            key_applications = key_applications,
            research_objective = research_objective,
            supporting_questions = supporting_questions,
            number_of_core_terms = number_of_core_terms,
            number_of_related_terms= number_of_related_terms,
            number_of_exclusion_terms = number_of_exclusion_terms,
        )
        
        system_msg = SystemMessage(content=system_instructions)
        human_msg = HumanMessage(
            content="Using the research plan provided above, first analyze and extract key patent terms by breaking down the research objective and supporting questions. Identify at least three core keywords, three related synonyms or technical terms, and two exclusion terms. Then, construct a Boolean query that combines these terms using AND, OR, and NOT operators, with proper grouping (parentheses) and exact phrase matching (quotes). Ensure that the final query is logically sound, follows Google Patents’ advanced search syntax, and does not include any field-specific tags (TI, AB, CL)."
        )
        
        structured_llm = llm.with_structured_output(PatentSearchEquation)
        result = structured_llm.invoke([system_msg, human_msg])
        
        return {"search_equation": result.search_equation}
    
    def run(self, state, config):
        return self.create_search_equation(state, config)