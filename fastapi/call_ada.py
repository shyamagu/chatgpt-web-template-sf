
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

def encode_contents (contents):

    # contentをループ処理
    for i in range(len(contents)):
        embedding = get_embedding(contents[i]["content"], settings.AOAI_EMB_MODEL)
        contents[i]["embedding"] = embedding
        logger.debug(str(i+1)+"/"+str(len(contents))+": embedded")

    return contents

def search_contents (message,embedding_data):

    embedding = get_embedding(message, settings.AOAI_EMB_MODEL)
    for i in range(len(embedding_data)):
        embedding_data[i]["similarity"] = cosine_similarity(embedding, embedding_data[i]["embedding"])
    
    # similarityでソート
    embedding_data = sorted(embedding_data, key=lambda x: x["similarity"], reverse=True)

    # embedding_dataの上位5件のidを配列として取得
    top5ids = [embedding_data[i]["id"] for i in range(5)]

    return top5ids
