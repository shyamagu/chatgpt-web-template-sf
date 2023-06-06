from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from call_ada import encode_content,get_similarity
from logger import logger

router = APIRouter()

class Query(BaseModel):
    word:str
    target:str

@router.post("/embedding")
async def embedding(query: Query):

    embedding_word = encode_content(query.word)
    embedding_target = encode_content(query.target)

    similarity = get_similarity(embedding_word,embedding_target)

    data = {
        "similarity": similarity,
        "embedding" : embedding_target
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)
