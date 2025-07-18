from pydantic import BaseModel, Field

class ClassifiedTicket(BaseModel):
    title: str = Field(..., description="Title of the issue")
    description: str = Field(..., description="Description of the issue")
    level_label: str = Field(..., description="Level label assigned to the issue (e.g., L1, L2, L3)")
    priority_label: str = Field(..., description="Priority label assigned to the issue (e.g., Low, Medium, High)")
    eta: int = Field(..., description="Estimated time of arrival or resolution for the issue, in days") 