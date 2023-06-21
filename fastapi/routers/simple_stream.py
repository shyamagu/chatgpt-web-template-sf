from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt_stream import call_chatgpt
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str


def chatgpt_streamer(response):
    for chunk in response:
        if chunk is not None:
            content = chunk["choices"][0]["delta"].get("content")
            if content is not None:
                yield content

@router.post("/simple/stream")
def message(messages: List[Message]):

    logger.debug(messages)

    # ChatGPTを呼び出す
    response = call_chatgpt([m.dict() for m in messages])

#    for chunk in response:
#        logger.debug(chunk)

    return StreamingResponse(
        chatgpt_streamer(response),media_type="text/event-stream"
    )
