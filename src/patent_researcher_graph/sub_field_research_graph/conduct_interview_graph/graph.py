from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from .state import InterviewState

from .nodes import (
    GenerateQuestion,
    SearchWeb,
    GenerateAnswer,
    SaveInterview,
    WriteSection,
    SearchPatents,
    SearchDescriptiveAnalyticResults,
)

from .edges import (
    RouteMessages,    
)

generate_question = GenerateQuestion()
search_web = SearchWeb()
generate_answer = GenerateAnswer()
save_interview = SaveInterview()
write_section = WriteSection()
route_messages = RouteMessages()
search_patents = SearchPatents()
search_descriptive_analytic_results = SearchDescriptiveAnalyticResults()

# Add nodes and edges 
conduct_interview_builder = StateGraph(InterviewState)
conduct_interview_builder.add_node("ask_question", generate_question.run)
conduct_interview_builder.add_node("search_web", search_web.run)
conduct_interview_builder.add_node("search_patents", search_patents.run)
conduct_interview_builder.add_node("search_descriptive_analytic_results", search_descriptive_analytic_results.run)
conduct_interview_builder.add_node("answer_question", generate_answer.run)
conduct_interview_builder.add_node("save_interview", save_interview.run)
conduct_interview_builder.add_node("write_section", write_section.run)

# Flow
conduct_interview_builder.add_edge(START, "ask_question")
conduct_interview_builder.add_edge("ask_question", "search_web")
conduct_interview_builder.add_edge("ask_question", "search_patents")
conduct_interview_builder.add_edge("ask_question", "search_descriptive_analytic_results")
conduct_interview_builder.add_edge(["search_web", "search_patents", "search_descriptive_analytic_results"], "answer_question")
conduct_interview_builder.add_conditional_edges("answer_question", route_messages.run,['ask_question','save_interview'])
conduct_interview_builder.add_edge("save_interview", "write_section")
conduct_interview_builder.add_edge("write_section", END)

# Compile 
conduct_interview_memory = MemorySaver()
conduct_interview_graph = conduct_interview_builder.compile(checkpointer=conduct_interview_memory).with_config(run_name="Conduct Interviews")