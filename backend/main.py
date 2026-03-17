from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from tools.calendar_tools import create_meeting

app = FastAPI()

# Allow CORS so frontend can access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message.lower()

    # If user wants to schedule a meeting
    if "schedule meeting" in message or "create meeting" in message:
        response = create_meeting(message)
    else:
        response = run_agent(request.message)

    return {"response": response}