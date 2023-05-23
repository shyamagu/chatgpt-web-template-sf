
from pydantic import BaseSettings
class Settings(BaseSettings):
    AOAI_API_KEY :str
    AOAI_ENDPOINT :str
    AOAI_MODEL :str

settings = Settings(_env_file=".env")

from logger import logger

import openai
openai.api_type = "azure"
openai.api_base = settings.AOAI_ENDPOINT
openai.api_version = "2023-05-15"
openai.api_key = settings.AOAI_API_KEY

def call_chatgpt (messages):

    response = openai.ChatCompletion.create(
        engine=settings.AOAI_MODEL, # engine = "deployment_name".
        messages=messages
    )

    return response['choices'][0]['message']['content']
