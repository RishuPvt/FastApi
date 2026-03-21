from fastapi import APIRouter , Depends
from pydantic import BaseModel
from agent.agent import agent
from routes.get_current_user import get_current_user
router = APIRouter()

class Prompt(BaseModel):
    message: str


@router.post("/agent")
def agent_chat(
    prompt: Prompt,
    current_user = Depends(get_current_user)
):
    user_id = current_user.id    

    response = agent.invoke({
        "input": f"{prompt.message}. user_id:{user_id}"
    })

    return {"response": response["output"]}
