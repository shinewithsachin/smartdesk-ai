from fastapi import APIRouter, HTTPException, Body
from app.models import TicketCreate, TicketResponse
from app.database import ticket_collection, ticket_helper
from app.utils import predict_ticket_info 
from bson import ObjectId
from app.rag import generate_response

router = APIRouter()

@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate):
    ticket_dict = ticket.dict()
    ticket_dict["status"] = "open"
    ticket_dict["solution"] = None  
    
    category, priority = predict_ticket_info(ticket.description)
    ticket_dict["category"] = category
    ticket_dict["priority"] = priority
   
    new_ticket = await ticket_collection.insert_one(ticket_dict)
    
    created_ticket = await ticket_collection.find_one({"_id": new_ticket.inserted_id})
    return ticket_helper(created_ticket)

@router.get("/")
async def get_tickets():
    tickets = []
    async for ticket in ticket_collection.find():
        tickets.append(ticket_helper(ticket))
    return tickets

@router.get("/{id}")
async def get_ticket(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Ticket ID format")
        
    ticket = await ticket_collection.find_one({"_id": ObjectId(id)})
    if ticket:
        return ticket_helper(ticket)
    raise HTTPException(status_code=404, detail="Ticket not found")

@router.post("/{id}/reply")
async def generate_ticket_reply(id: str):
    if not ObjectId.is_valid(id):
         raise HTTPException(status_code=400, detail="Invalid Ticket ID")

    ticket = await ticket_collection.find_one({"_id": ObjectId(id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    ai_reply = generate_response(ticket["description"])
    
    await ticket_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"suggested_reply": ai_reply}}
    )
    
    return {"ticket_id": id, "ai_reply": ai_reply}

@router.patch("/{id}")
async def update_ticket(id: str, payload: dict = Body(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid Ticket ID")

    update_result = await ticket_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": payload}
    )

    if update_result.modified_count == 1:
        return {"message": "Ticket updated successfully", "id": id}
    
    existing_ticket = await ticket_collection.find_one({"_id": ObjectId(id)})
    if existing_ticket:
        return {"message": "No changes needed", "id": id}
        
    raise HTTPException(status_code=404, detail="Ticket not found")