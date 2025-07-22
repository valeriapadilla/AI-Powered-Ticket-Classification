import sys
from pathlib import Path
from datetime import datetime, timezone

backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.models.issue        import Issue
from app.models.classification import ClassifiedTicket
from .classification_graph     import agent  

def classify_ticket(issue: Issue) -> ClassifiedTicket:
    payload = issue.model_dump()  

    final_state = agent.invoke(payload)

    return ClassifiedTicket(
        title          = issue.title,
        description    = issue.description,
        level_label    = final_state.get("level", ""),
        priority_label = final_state.get("priority", ""),
        eta            = final_state.get("eta", "")
    )

if __name__ == "__main__":
    dummy_issue = Issue(
        title       = "Password Reset Request",
        description = "User unable to access account due to forgotten password",
        created_at   = datetime.now(timezone.utc)
    )

    result = classify_ticket(dummy_issue)
    print("Resultado de clasificación:")
    print(result)
