from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Issue(BaseModel):
    title: str = Field(..., description="Title of the issue")
    description: str = Field(..., description="Description of the issue")
    created_at: Optional[datetime] = None