from app.models.issue import Issue
from app.graph.l1_engineer_graph import l1_agent
from datetime import datetime

test_issue = Issue(
    title="VPN Connection Issue",
    description="User cannot connect to VPN due to configuration error",
    created_at=datetime.now()
)

state = l1_agent.invoke(test_issue)
print(state.get("solution"))

