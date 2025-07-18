from langgraph.graph import StateGraph, START, END
from app.agents.classifier import (
    IssueState,
    receive_issue,
    retrieve_similar_tickets,
    grade_relevance,
    refine_query,
    classify_level,
    classify_priority,
    estimate_eta,
)

graph = StateGraph(IssueState)

graph.add_node("receive_issue", receive_issue)
graph.add_node("retrieve_similar_tickets", retrieve_similar_tickets)
graph.add_node("grade_relevance", grade_relevance)
graph.add_node("refine_query", refine_query)
graph.add_node("classify_level", classify_level)
graph.add_node("classify_priority", classify_priority)
graph.add_node("estimate_eta", estimate_eta)

graph.add_edge(START, "receive_issue")
graph.add_edge("receive_issue", "retrieve_similar_tickets")
graph.add_edge("retrieve_similar_tickets", "grade_relevance")
graph.add_conditional_edges(
    "grade_relevance",
    lambda state: state["next_stage"],
    {
        "classify_level": "classify_level",
        "refine_query": "refine_query"
    }
)
graph.add_edge("refine_query", "retrieve_similar_tickets")
graph.add_edge("classify_level", "classify_priority")
graph.add_edge("classify_priority", "estimate_eta")
graph.add_edge("estimate_eta", END)

agent = graph.compile()