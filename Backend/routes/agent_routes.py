from fastapi import APIRouter
from pydantic import BaseModel
from agent.agent import agent

router = APIRouter()

class Prompt(BaseModel):
    message: str


@router.post("/agent")
def chat_agent(prompt: Prompt):

    response = agent.invoke(
        {"input": prompt.message}
    )

    return {"response": response}

