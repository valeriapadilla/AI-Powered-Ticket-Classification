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
from app.agents.prompts.retrieve_tickets_sysmsg import retrieve_tickets_sysmsg
from app.agents.prompts.grade_prompt import grade_prompt
from app.agents.prompts.rewrite_prompt import rewrite_prompt
 
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
 
retriever = get_retriever("vector_store/it_tickets_vector_store", k=3)
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
    messages = [SystemMessage(content=retrieve_tickets_sysmsg)] + state["messages"]
    response = llm.bind_tools([ticket_tool]).invoke(messages)
    return {
         **state,
        "messages": state["messages"] + [response],
        "refined": state["refined"]
    }
 
class GradeDocuments(BaseModel):
    """Grade ticket excerpt using a binary score for relevance check."""
 
    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, or 'no' if not relevant"
    )
 
def grade_relevance(state: IssueState) -> Dict[str, Any]:
    """"Grade the relevance of retrieved tickets to the user request."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
 
    prompt = grade_prompt.format(question=question, context=context)
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
        **state,
        "refined": updated_refined,
        "next_stage": next_stage  
    }
 
def refine_query(state: IssueState) -> IssueState:
    """Rewrite the original ticket."""
    original_question = state["messages"][0].content
    prompt = rewrite_prompt.format(question=original_question)
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
        **state,
        "messages": state["messages"] + [res],
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
        **state,
        "messages": state["messages"] + [res],
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
        **state,
        "messages": state["messages"] + [res],
        "refined": state["refined"],
        "level": state.get("level", "L1"),
        "priority": state.get("priority", "medium"),
        "eta": eta
    }
 