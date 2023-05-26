
from pydantic import BaseSettings
import requests
from requests.exceptions import Timeout

class Settings(BaseSettings):
    BING_API_KEY :str

settings = Settings(_env_file=".env")

from logger import logger

async def call_bingapi (url,query,option):

    bingurl = url+query+option

    logger.debug(bingurl)

    #bingurlにHeaderつきのGETリクエストを送り結果を取得する
    try:
        result = requests.get(bingurl,headers={'Ocp-Apim-Subscription-Key': settings.BING_API_KEY},timeout=5)
    except Timeout:
        return []

    result.raise_for_status()
    #result からJSONを取得する
    result = result.json()

    return result["webPages"]["value"]
