from pydantic import BaseModel
from typing import Optional

class TicketOut(BaseModel):
    github_issue_id: int
    title: str
    body: Optional[str]
    level_label: str
    priority_label: str
    response: Optional[str]
    status: str
    eta:int

    class Config:
        orm_mode = True
