from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketUpdate(BaseModel):
    level: Optional[str] = None
    priority: Optional[str] = None
    eta: Optional[int] = None
