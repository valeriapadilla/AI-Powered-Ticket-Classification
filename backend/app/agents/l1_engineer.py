from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool
from datetime import datetime 
from langchain.schema import SystemMessage
from typing import Dict, Any
from typing import TypedDict, List, Union
from dotenv import load_dotenv
from app.models.issue import Issue
from app.rag.retriever import get_retriever 
from app.agents.prompts.l1_create_solution_prompts import CREATE_SOLUTION_PROMPT

llm = ChatOpenAI(model="gpt-4o", temperature=0)
load_dotenv()

class SolutionState(TypedDict, total=False):
    title: str                      
    description: str 
    solution: list[str]
    messages: List[Union[HumanMessage, AIMessage]]
    retrieved_context: str  

retriever = get_retriever("vector_store/solutions_vector_store", k=3)
ticket_tool = create_retriever_tool(
    retriever,
    name="solutions_retriever",
    description="Fetch similar past solutions."
)


def receive_issue(issue: Issue) -> SolutionState:
    title = issue.title
    description = issue.description
    content = f"Title: {title}\nDescription: {description}"
    return {
        "title": title,
        "description": description,
        "messages": [HumanMessage(content=content)]
    }

def retrieve_similar_solutions(state: SolutionState) -> SolutionState:
    query = f"{state['title']}\n{state['description']}"
    retrieved_docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    return {
        **state,
        "retrieved_context": context
    }

def create_solution(state: SolutionState) -> SolutionState:
    issue = f"Title: {state['title']}\nDescription: {state['description']}"
    context = state.get("retrieved_context") or (state["messages"][-1].content if state["messages"] else "")
    prompt = CREATE_SOLUTION_PROMPT.format(issue=issue, context=context)
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        **state,
        "messages": state["messages"] + [response],
        "solution": response.content
    }
    