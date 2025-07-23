from app.models.issue import Issue
from app.graph.l3_engineer_graph import l3_agent
from datetime import datetime

test_issue = Issue(
    title="Application Crash on Launch",
    description="Custom application crashes immediately after starting, possibly due to code-level bug or memory issue",
    created_at=datetime.now()
)

state = l3_agent.invoke(test_issue)
print(state.get("solution")) 