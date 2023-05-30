from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt
from longmemory import saveConvMemory,rememberConvMemory
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/longconv")
async def longconv(messages: List[Message]):

    memoryMessages = rememberConvMemory(messages[-1].content)

    if memoryMessages:
        messages[0:0] = memoryMessages

    # messagesの要素が3以上の場合
    if len(messages) >= 3:
        saveConvMemory(messages[-3:-1])

    # System Prompt
    system_prompt = f"""あなたは聞き上手な会話エキスパートです。
会話に関係する適切な質問をたまに入れてください。
"""
    # messagesの先頭に要素を追加
    messages.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages])

    data = {
        "message": answer
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)