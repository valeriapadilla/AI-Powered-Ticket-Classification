from enum import Enum
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from ..db.db import Base

class StatusEnum(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In-progress"
    RESOLVED = "Resolved"

class Issue_db(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    github_issue_id = Column(Integer, unique=True, index=True)
    title = Column(String)
    body = Column(String)
    level_label = Column(String)
    priority_label = Column(String, nullable=True)
    response = Column(String, nullable=True)
    eta = Column(Integer, nullable=True)
    status = Column(String, default=StatusEnum.PENDING.value)
    created_at = Column(DateTime, nullable=False)