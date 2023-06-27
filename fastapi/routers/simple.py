from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt,call_chatgpt_w_token
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/simple")
def message(messages: List[Message]):

    logger.debug(messages)

    # ChatGPTを呼び出す
    answer,input,output,total = call_chatgpt_w_token([m.dict() for m in messages])

    data = {
        "message": answer,
        "input": input,
        "output": output,
        "total": total
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)