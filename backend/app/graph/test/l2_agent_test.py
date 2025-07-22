from app.models.issue import Issue
from app.graph.l2_engineer_graph import l2_agent
from datetime import datetime

test_issue = Issue(
    title="Email Sync Failure",
    description="User's Outlook is not syncing emails due to server or configuration error",
    created_at=datetime.now()
)

state = l2_agent.invoke(test_issue)
print(state.get("solution")) 