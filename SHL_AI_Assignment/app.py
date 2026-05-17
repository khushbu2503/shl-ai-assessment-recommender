from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -----------------------------
# Request Models
# -----------------------------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# -----------------------------
# Health Endpoint
# -----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    latest_message = request.messages[-1].content.lower()

    # vague query handling
    if "assessment" in latest_message and len(latest_message.split()) < 4:
        return {
            "reply": "Sure. What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # java developer recommendation
    elif "java" in latest_message:
        return {
            "reply": "Here are some SHL assessments suitable for a Java developer.",
            "recommendations": [
                {
                    "name": "Java 8 (New)",
                    "url": "https://www.shl.com",
                    "test_type": "Technical"
                },
                {
                    "name": "OPQ32r",
                    "url": "https://www.shl.com",
                    "test_type": "Personality"
                }
            ],
            "end_of_conversation": False
        }

    # default response
    return {
        "reply": "Could you provide more hiring details?",
        "recommendations": [],
        "end_of_conversation": False
    }