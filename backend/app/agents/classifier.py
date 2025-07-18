from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool
from datetime import datetime 
from langchain.schema import SystemMessage
from typing import Dict, Any

from app.agents.prompts.level_prompt import level_template
from app.agents.prompts.priority_prompt import priority_template
from app.agents.prompts.eta_prompt import eta_template
from app.rag.retriever import get_retriever
from app.models.issue import Issue

from typing import TypedDict, List, Union, Literal
from dotenv import load_dotenv

llm = ChatOpenAI(model="gpt-4o", temperature=0)
load_dotenv()

class IssueState(TypedDict, total=False):
    title: str
    description: str
    created_at: datetime
    messages: List[Union[HumanMessage, AIMessage]]
    refined: bool
    level: str
    priority: str
    eta: str

retriever = get_retriever(k=3)
ticket_tool = create_retriever_tool(
    retriever,
    name="retrieve_tickets",
    description="Fetch similar past tickets (title, description)."
)

def receive_issue( issue: Issue) -> IssueState:
    title = issue.title
    desc = issue.description
    created = issue.created_at
    content = f"Title: {title}\nDescription: {desc}\nCreated at: {created}"
    return {
        "title": title,
        "description": desc, 
        "created_at": created,
        "messages": [HumanMessage(content=content)], 
        "refined": False
    }

def retrieve_similar_tickets(state : IssueState) -> IssueState:
    sys_msg = (
        "You are a ticket classification assistant. Your task is to find similar past tickets "
        "that can help classify the current ticket.\n\n"
        "ALWAYS use the 'retrieve_tickets' tool to search for similar tickets. "
        "Create a search query based on the ticket's title and description.\n\n"
        "Guidelines for creating the search query:\n"
        "- Focus on the main problem/issue described\n"
        "- Include key technical terms and error messages\n"
        "- Use relevant keywords from both title and description\n"
        "- Keep the query concise but descriptive\n"
    )
    messages = [SystemMessage(content=sys_msg)] + state["messages"]
    response = llm.bind_tools([ticket_tool]).invoke(messages)
    return {
        "messages": [response],
        "refined": state["refined"]
    }

GRADE_PROMPT = (
    "You are an evaluator determining if a retrieved ticket is relevant to a support request.\n"
    "Here is the ticket excerpt: \n\n {context} \n\n"
    "Here is the user request: {question} \n"
    "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n"
    "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."
)

class GradeDocuments(BaseModel):
    """Grade ticket excerpt using a binary score for relevance check."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )

def grade_relevance(state: IssueState) -> Dict[str, Any]:
    """"Grade the relevance of retrieved tickets to the user request."""
    question = state["messages"][0].content
    context = state["messages"][-1].content

    prompt = GRADE_PROMPT.format(question=question, context=context)
    response = (
        llm
        .with_structured_output(GradeDocuments).invoke(
            [HumanMessage(content=prompt)]
        )
    )
    score = response.binary_score.lower()

    updated_refined = state.get("refined", False)
    if score == "no" and not updated_refined:
        updated_refined = True
        next_stage = "refine_query"
    else:
        next_stage = "classify_level"

    return {
        "messages": state["messages"],
        "refined": updated_refined,
        "next_stage": next_stage  
    }

REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:"
    "\n ------- \n"
    "{question}"
    "\n ------- \n"
    "Formulate an improved question:"
)

def refine_query(state: IssueState) -> IssueState:
    """Rewrite the original ticket."""
    original_question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=original_question)
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [HumanMessage(content=result.content)], "refined": True}

def classify_level(state: IssueState) -> IssueState:
    ticket_content = state["messages"][0].content
    retrieved_context = state["messages"][-1].content if len(state["messages"])>1 else ""
    prompt = level_template.format(question=ticket_content, context=retrieved_context)
    res = llm.invoke([HumanMessage(content=prompt)])
    
    level = res.content.strip()
    if level not in {"L1", "L2", "L3"}:
        raise ValueError(f"Incorrect response: {res.content!r}")
    return {
        "messages": [res], 
        "refined": state["refined"],
        "level": level
    }

def classify_priority(state: IssueState) -> IssueState:
    ticket_content = state["messages"][0].content
    retrieved_context = state["messages"][-1].content
    prompt = priority_template.format(question=ticket_content, context=retrieved_context)
    res = llm.invoke([HumanMessage(content=prompt)])
    
    priority = res.content.strip()
    if priority not in {"Low", "Medium", "High"}:
        raise ValueError(f"Incorrect response: {res.content!r}")
    
    return {
        "messages": [res], 
        "refined": state["refined"],
        "level": state.get("level", "L1"),
        "priority": priority
    }

def estimate_eta(state: IssueState) -> IssueState:
    ticket_content = state["messages"][0].content
    retrieved_context = state["messages"][-1].content
    prompt = eta_template.format(question=ticket_content, context=retrieved_context)
    res = llm.invoke([HumanMessage(content=prompt)])
    if isinstance(int(res.content), int):
        eta = res.content.strip()

    return {
        "messages": [res], 
        "refined": state["refined"],
        "level": state.get("level", "L1"),
        "priority": state.get("priority", "medium"),
        "eta": eta
    }

