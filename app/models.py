from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    priority: Optional[str] = "pending" 
    category: Optional[str] = "pending"

class TicketResponse(TicketCreate):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    status: str = "open"
    solution: Optional[str] = None 
    suggested_reply: Optional[str] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "65b123...",
                "subject": "VPN Error",
                "description": "Cannot connect...",
                "priority": "High",
                "status": "closed",
                "solution": "Please restart your router."
            }
        }