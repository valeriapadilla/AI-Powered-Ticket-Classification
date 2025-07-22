from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, Header, APIRouter
from sqlalchemy.orm import Session
#from models.schemas import IssueCreate, IssueOut
import json
from ..models.issue import Issue
from ..utils.webhook_security import verify_signature, SECRET
from ..db.db import Base, engine, SessionLocal
from ..models.Issue_db import Issue_db, StatusEnum
from ..graph.test_agent import classify_ticket

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: str | None = Header(None),
    x_hub_signature_256: str | None = Header(None),
    db: Session = Depends(get_db)
):
    raw = await request.body()

    # if verify_signature(raw, x_hub_signature_256):
    #     print("Signature verified")
    # else:
    #     print("Invalid signature")
    #     raise HTTPException(status_code=403, detail="Invalid signature")

    payload = json.loads(raw)

    if "action" not in payload or payload["action"] != "opened":
        raise HTTPException(status_code=400, detail="Not an issue opened event")
    
    issue = payload["issue"]
    github_issue_id = issue["id"]
    title = issue["title"]
    created_at = issue["created_at"]
    created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    created_at = created_at.replace(tzinfo=None)
    body = issue.get("body", "")
    
    input_issue = Issue(
        title       = title,
        description = body,
        created_at   = created_at
    )

    # Run LangGraph classification
    result = classify_ticket(input_issue)
    print(result)

    # Store in DB
    issue_db = Issue_db(
        github_issue_id=github_issue_id,
        title=title,
        body=body,
        level_label=result.level_label,
        priority_label=result.priority_label,
        created_at= created_at,
        eta=result.eta,
        status=StatusEnum.PENDING.value)
    
    db.add(issue_db)
    db.commit()
    db.refresh(issue_db)

    print("Saved:", issue_db.id)
    print(f"EVENT: {x_github_event}")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    return {"ok": True}

