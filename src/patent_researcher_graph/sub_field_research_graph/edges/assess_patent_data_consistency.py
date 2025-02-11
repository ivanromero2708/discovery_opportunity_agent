from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from ..state import SubFieldResearchGraphState
from ...configuration import Configuration
from ..prompts import PROMPT_PATENT_CONTENT_ASSESSMENT, PROMPT_IMPROVE_SEARCH_EQUATION
from datetime import datetime, MINYEAR
from pydantic import BaseModel, Field
from typing import Literal




class AsessPatentDataConsistency:
    def __init__(self):
        self.configurable = None
        
    def assess_patent_data_consistency(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        
        class PatentAssessment(BaseModel):
            is_relevant: Literal["Y", "N"] = Field(..., description="Final assessment of the relevancy of patent content repsect to the field of study. It is a Y or N")
            rationale: str = Field(..., description="Rationale behind the relevancy assesment for the patent content")

        class SuggestionsSearchEquation(BaseModel):
            suggestions_search_equation: str = Field(
                ...,
                description = "Consolidated suggestions regarding core terms, related terms, and exclusion terms to consider for assembling the search equation"
            )
        
        patents = state["initial_patent_documents"]
        research_plan = state["research_plan"]
        industry_context = research_plan.industry_context
        technology_domain = research_plan.technology_domain
        key_applications = research_plan.key_applications
        research_objective = research_plan.research_objective
        supporting_questions = research_plan.supporting_questions
        
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model = configurable.planner_model, temperature = 0)
                
        minimum_consistency_score = configurable.minimum_consistency_score
        base_consistency_score = configurable.base_consistency_score
        
        # Sort patents by priority date (handle None values)
        sorted_patents = sorted(
            patents, key=lambda x: x["priority_date"] if x["priority_date"] else datetime(MINYEAR, 1, 1), reverse=True
        )
        
        consistency_score = 0
        rationales = ""

        # Analyze retrieved patents for relevance
        total_patents = len(sorted_patents[:base_consistency_score])
        if total_patents == 0:
            state["improve_search_equation"] = "Please widen up the search equation because there werent any patent related results."
            return "re_search"
        
        for index, patent in enumerate(sorted_patents[:base_consistency_score], start=1):
            title = patent["title"]
            snippet = patent["snippet"]
            text = f"Title: {title}\nSnippet: {snippet}"
            
            system_instructions = PROMPT_PATENT_CONTENT_ASSESSMENT.format(
                patent_text=text,
                industry_context = industry_context,
                technology_domain = technology_domain,
                key_applications = key_applications,
                research_objective = research_objective,
                supporting_questions = supporting_questions,
            )            
            system_msg = SystemMessage(content= system_instructions)
            human_msg = HumanMessage(
                content = """
                Perform rigorous relevance assessment of this patent document. 
                Consider both explicit content and implicit connections to the research framework. 
                Highlight any potential indirect relevance through enabling technologies.
                """
            ) 
            
            structured_llm = llm.with_structured_output(PatentAssessment)
            result = structured_llm.invoke([system_msg, human_msg])
            
            # Update consistency score based on relevance
            if result.is_relevant == "Y":
                consistency_score += 1
            
            rationales += f"\n{result.rationale}"
            
        consistency_index = consistency_score / total_patents
        
        search_equation = state["search_equation"]
        
        system_instructions_2 = PROMPT_IMPROVE_SEARCH_EQUATION.format(
            rationale = rationales,
            search_equation = search_equation,
        )
        
        system_msg_2 = SystemMessage(content=system_instructions_2)
        human_msg_2 = HumanMessage(
            content="""
            Generate evolutionary improvements rather than complete overhauls. 
            Prioritize modifications that address multiple rationale points simultaneously. 
            """
        )
        structured_llm_2 = llm.with_structured_output(SuggestionsSearchEquation)
        result_2 = structured_llm_2.invoke([system_msg_2, human_msg_2])
        
        state["improve_search_equation"] = result_2.suggestions_search_equation
        
        return "continue" if (consistency_index >= minimum_consistency_score) else "re_search"
    
    def run(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        return self.assess_patent_data_consistency(state, config)
    
    
    
    """
    from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from ..state import SubFieldResearchGraphState
from ...configuration import Configuration
from ..prompts import PROMPT_PATENT_CONTENT_ASSESSMENT, PROMPT_IMPROVE_SEARCH_EQUATION
from datetime import datetime, MINYEAR
from pydantic import BaseModel, Field
from typing import Literal
import concurrent.futures

class PatentAssessment(BaseModel):
    is_relevant: Literal["Y", "N"] = Field(
        ..., 
        description="Final assessment of the relevancy of patent content repsect to the field of study. It is a Y or N"
    )
    rationale: str = Field(
        ..., 
        description="Rationale behind the relevancy assesment for the patent content"
    )

class SuggestionsSearchEquation(BaseModel):
    suggestions_search_equation: str = Field(
        ...,
        description="Consolidated suggestions regarding core terms, related terms, and exclusion terms to consider for assembling the search equation"
    )

class AsessPatentDataConsistency:
    def __init__(self):
        self.configurable = None
        
    def assess_patent_data_consistency(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        # Retrieve the initial patent documents and research plan details
        patents = state["initial_patent_documents"]
        research_plan = state["research_plan"]
        industry_context = research_plan.industry_context
        technology_domain = research_plan.technology_domain
        key_applications = research_plan.key_applications
        research_objective = research_plan.research_objective
        supporting_questions = research_plan.supporting_questions
        
        configurable = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(model=configurable.planner_model, temperature=0)
                
        minimum_consistency_score = configurable.minimum_consistency_score
        base_consistency_score = configurable.base_consistency_score
        
        # Sort patents by priority date (handle None values)
        sorted_patents = sorted(
            patents, 
            key=lambda x: x["priority_date"] if x["priority_date"] else datetime(MINYEAR, 1, 1), 
            reverse=True
        )
        
        consistency_score = 0
        rationales = ""

        # Analyze retrieved patents for relevance (limit to base_consistency_score)
        total_patents = len(sorted_patents[:base_consistency_score])
        if total_patents == 0:
            state["improve_search_equation"] = (
                "Please widen up the search equation because there werent any patent related results."
            )
            return "re_search"
        
        # Helper function to assess a single patent
        def assess_single_patent(index, patent):
            title = patent["title"]
            snippet = patent["snippet"]
            text = f"Title: {title}\nSnippet: {snippet}"
            
            system_instructions = PROMPT_PATENT_CONTENT_ASSESSMENT.format(
                patent_text=text,
                industry_context=industry_context,
                technology_domain=technology_domain,
                key_applications=key_applications,
                research_objective=research_objective,
                supporting_questions=supporting_questions,
            )            
            system_msg = SystemMessage(content=system_instructions)
            human_msg = HumanMessage(
                content="
                Perform rigorous relevance assessment of this patent document. Consider both explicit content and implicit connections to the research framework. Highlight any potential indirect relevance through enabling technologies.
                "
            ) 
            
            structured_llm = llm.with_structured_output(PatentAssessment)
            result = structured_llm.invoke([system_msg, human_msg])
            
            # Optional: print for debugging/logging purposes
            print(f"Patent {index}: {title}")
            print(f"Rationale: {result.rationale}")
            
            return result.is_relevant, result.rationale

        # Parallelize the for-loop using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(assess_single_patent, index, patent)
                for index, patent in enumerate(sorted_patents[:base_consistency_score], start=1)
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    is_relevant, rationale = future.result()
                    if is_relevant == "Y":
                        consistency_score += 1
                    rationales += f"\n{rationale}"
                except Exception as exc:
                    print(f"Error during patent assessment: {exc}")
            
        consistency_index = consistency_score / total_patents
        
        # Improve search equation based on rationales
        search_equation = state["search_equation"]
        
        system_instructions_2 = PROMPT_IMPROVE_SEARCH_EQUATION.format(
            rationale=rationales,
            search_equation=search_equation,
        )
        
        system_msg_2 = SystemMessage(content=system_instructions_2)
        human_msg_2 = HumanMessage(
            content="Generate evolutionary improvements rather than complete overhauls. Prioritize modifications that address multiple rationale points simultaneously."
        )
        structured_llm_2 = llm.with_structured_output(SuggestionsSearchEquation)
        result_2 = structured_llm_2.invoke([system_msg_2, human_msg_2])
        
        state["improve_search_equation"] = result_2.suggestions_search_equation
        
        return "continue" if (consistency_index >= minimum_consistency_score) else "re_search"
    
    def run(self, state: SubFieldResearchGraphState, config: RunnableConfig):
        return self.assess_patent_data_consistency(state, config)

    
    """