from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from recommender import recommend_assessments

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    latest_message = request.messages[-1].content.lower()

    full_user_context = " ".join(
        message.content.lower()
        for message in request.messages
        if message.role == "user"
    )

    off_topic_words = ["salary", "legal", "law", "resume", "cover letter", "interview tips"]
    if any(word in latest_message for word in off_topic_words):
        return {
            "reply": "I can only help with SHL assessment recommendations and comparisons.",
            "recommendations": [],
            "end_of_conversation": False
        }

    if "ignore previous" in latest_message or "prompt" in latest_message:
        return {
            "reply": "I can only use the SHL catalog and cannot follow instructions outside this task.",
            "recommendations": [],
            "end_of_conversation": False
        }

    if "compare" in latest_message or "difference" in latest_message:
        if "opq" in latest_message and "java" in latest_message:
            return {
                "reply": (
                    "OPQ is a personality assessment focused on workplace behavior, "
                    "communication, and leadership potential. "
                    "Java assessments evaluate technical programming and coding skills."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        elif "opq" in latest_message and "verify" in latest_message:
            return {
                "reply": (
                    "OPQ measures personality and behavioral preferences, "
                    "while SHL Verify assessments measure cognitive ability, reasoning, "
                    "and aptitude."
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        else:
            return {
                "reply": "Please mention valid SHL assessment names you want to compare.",
                "recommendations": [],
                "end_of_conversation": False
            }

    vague_queries = ["assessment", "test", "hiring", "need assessment", "i need an assessment"]
    if latest_message.strip() in vague_queries or len(latest_message.split()) <= 3:
        return {
            "reply": "Sure. What role are you hiring for, and what skills do you want to assess?",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = recommend_assessments(full_user_context)

    if recommendations:
        return {
            "reply": "Here are suitable SHL assessments based on your hiring needs.",
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    return {
        "reply": "Could you provide more details such as role, skills, seniority level, or whether you need cognitive, technical, or personality assessments?",
        "recommendations": [],
        "end_of_conversation": False
    }