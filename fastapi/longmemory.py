
from pydantic import BaseSettings
class Settings(BaseSettings):
    AOAI_API_KEY :str
    AOAI_ENDPOINT :str
    AOAI_EMB_MODEL :str

settings = Settings(_env_file=".env")

from logger import logger

import openai
openai.api_type = "azure"
openai.api_base = settings.AOAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = settings.AOAI_API_KEY

from openai.embeddings_utils import get_embedding, cosine_similarity
from fastapi.encoders import jsonable_encoder
import json


def saveConvSummaryMemory (summary):

    global chatgpt_summary_memory
    if not "chatgpt_summary_memory" in globals():
        chatgpt_summary_memory = []

    embedding = get_embedding(summary, settings.AOAI_EMB_MODEL)
    chatgpt_summary_memory.append({"id":len(chatgpt_summary_memory),"content":summary,"embedding":embedding})

def rememberConvSummaryMemory (message):

    global chatgpt_summary_memory
    if not "chatgpt_summary_memory" in globals():
        chatgpt_summary_memory = []

    embedding = get_embedding(message, settings.AOAI_EMB_MODEL)

    if len(chatgpt_summary_memory) == 0:
        return []

    # chatgpt_memoryの各要素にsimilarityを追加
    for i in range(len(chatgpt_summary_memory)):
        chatgpt_summary_memory[i]["similarity"] = cosine_similarity(embedding, chatgpt_summary_memory[i]["embedding"])

    # similarityでソートした上で、先頭の3要素を取得
    top3_memory = sorted(chatgpt_summary_memory, key=lambda x: x["similarity"], reverse=True)
    top3_memory = top3_memory[:3]

    remember_memory = []
    for i in range(len(top3_memory)):
        remember_memory.append(top3_memory[i]["content"])

    return remember_memory


def saveConvMemory (messages):

    global chatgpt_memory

    embedding = get_embedding(json.dumps(jsonable_encoder(messages),ensure_ascii=False), settings.AOAI_EMB_MODEL)
    chatgpt_memory.append({"id":len(chatgpt_memory),"content":messages.copy(),"embedding":embedding})

def rememberConvMemory (message):

    global chatgpt_memory

    #chatgpt_memoryが定義されていなければ空の配列を定義
    if not "chatgpt_memory" in globals():
        chatgpt_memory = []

    embedding = get_embedding(message, settings.AOAI_EMB_MODEL)

    # chatgpt_memoryの各要素にsimilarityを追加
    for i in range(len(chatgpt_memory)):
        chatgpt_memory[i]["similarity"] = cosine_similarity(embedding, chatgpt_memory[i]["embedding"])

    # similarityでソートした上で、先頭の3要素を取得
    top3_memory = sorted(chatgpt_memory, key=lambda x: x["similarity"], reverse=True)
    top3_memory = top3_memory[:3]

    remember_memory = []
    for i in range(len(top3_memory)):
        remember_memory.extend(top3_memory[i]["content"])
        # top3_memory[i]["id"]がリストの最後の要素でなければ
        if top3_memory[i]["id"] != len(chatgpt_memory)-1:
            remember_memory.extend(chatgpt_memory[top3_memory[i]["id"]+1]["content"])

    return remember_memory
