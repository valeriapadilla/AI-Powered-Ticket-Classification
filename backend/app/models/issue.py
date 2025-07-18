from pydantic import BaseModel, Field
from datetime import datetime

class Issue(BaseModel):
    title: str = Field(..., description="Title of the issue")
    description: str = Field(..., description="Description of the issue")
    created_at: datetime = Field(..., description="Date the issue was created") 