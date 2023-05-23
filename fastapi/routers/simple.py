from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/simple")
async def message(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    # System Prompt
    system_prompt = """あなたはAIアシスタントです。
ユーザからの質問に対して、世話好きのおばちゃんのように回答してください。
確認事項があれば遠慮なくユーザに問いかけてください。
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