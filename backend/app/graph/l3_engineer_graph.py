from langgraph.graph import StateGraph, START, END
from app.agents.l3_engineer import (
    SolutionState,
    receive_issue,
    retrieve_similar_solutions,
    create_solution,
)

graph = StateGraph(SolutionState)

graph.add_node("receive_issue", receive_issue)
graph.add_node("retrieve_similar_solutions", retrieve_similar_solutions)
graph.add_node("create_solution", create_solution)

graph.add_edge(START, "receive_issue")
graph.add_edge("receive_issue", "retrieve_similar_solutions")
graph.add_edge("retrieve_similar_solutions", "create_solution")
graph.add_edge("create_solution", END)

l3_agent = graph.compile()