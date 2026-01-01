from fastapi import FastAPI
from app.routes import tickets

app = FastAPI(title="AI Support Ticket System")

app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])

@app.get("/")
def read_root():
    return {"status": "System is running", "db": "MongoDB Connected"}