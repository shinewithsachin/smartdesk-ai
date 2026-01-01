import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
ticket_collection = db.get_collection("tickets")

def ticket_helper(ticket) -> dict:
    return {
        "id": str(ticket["_id"]),
        "subject": ticket["subject"],
        "description": ticket["description"],
        "priority": ticket.get("priority", "medium"),
        "category": ticket.get("category", "general"),
        "status": ticket.get("status", "open"),
        # ✅ NEW FIELDS (These were missing!)
        "solution": ticket.get("solution"), 
        "suggested_reply": ticket.get("suggested_reply")
    }