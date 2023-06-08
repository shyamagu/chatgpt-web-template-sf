from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

import requests

from call_chatgpt import call_chatgpt
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/booksearch")
async def booksearch(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-1:]

    messages_for_query = messages.copy()
    messages_for_summary = messages.copy()

    # System Prompt
    system_prompt = """あなたは書籍検索クエリ作成マシーンです。ユーザからのリクエストに対して、書籍に含まれそうな単語を2個から5個、以下のフォーマットに従って回答してください。なお、順序は関連度順です。

出力フォーマット）
["単語1","単語2","単語3","単語4","単語5"]
例えば、
ユーザ）エベレストで遭難する話
あなた）["エベレスト","遭難","登山"]
"""
    # messagesの先頭に要素を追加
    messages_for_query.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages_for_query)

    # ChatGPTを呼び出す
    answer_query = call_chatgpt([m.dict() for m in messages_for_query])

    # array配列を+で連結した文字列を作成する
    querystring = "+".join(eval(answer_query))

    googlebooksapi = "https://www.googleapis.com/books/v1/volumes?q="

    option = "&maxResults=5&printType=books&langRestrict=ja&country=JP"

    # GoogleBooksAPIのURLを生成する(googlebooksapi + querystring + test)
    url = googlebooksapi + querystring + option

    # urlにGETリクエストを送り結果をJSONで取得する
    result = requests.get(url).json()

    total_num = result["totalItems"]

    # bookresult用の配列を用意する
    bookresult = []

    # result.itemsでループする。要素が無い場合は空を入れる
    for item in result.get("items", []):
        # itemのvolumeInfoを取得する
        volumeInfo = item.get("volumeInfo", {})
        # volumeInfoのtitleを取得する
        title = volumeInfo.get("title", "")
        # vlumeInfoのinfolinkを取得する
        infolink = volumeInfo.get("infoLink", "")
        # volumeInfoのauthorsを取得する
        authors = volumeInfo.get("authors", [])
        # volumeInfoのdescriptionを取得する
        description = volumeInfo.get("description", "")
        # volumeInfoのimageLinksのthumbnailを取得する
        imageLinks = volumeInfo.get("imageLinks", {})
        thumbnail = imageLinks.get("smallThumbnail", "")

        # bookresultに辞書型で追加する
        bookresult.append({"title": title, "authors": ",".join(authors), "infolink":infolink,"description": description, "smallThumbnail": thumbnail})

    # bookresultの各要素について、descriptionが空、もしくは20文字以下の場合は、リストから除外する
    bookresult  = [book for book in bookresult if len(book["description"]) > 20]

    # bookresultの要素を先頭から3つに絞る
    bookresult = bookresult[:3]

    # bookresultのtitleとauthorsとdescriptionを改行で連結した文字列を作成する
    bookinfo = "\n".join([f"タイトル:{book['title']}\n著者:{book['authors']}\nあらすじ:{book['description']}\n" for book in bookresult])

    # System Prompt
    system_prompt = f"""あなたは本のコンシェルジュです。以下の書籍情報のみを使って、ユーザからのリクエストに回答してください。
ユーザからのリクエストにどうマッチしているか、また、ユーザが読みたくなるような推薦文書を簡潔に書いてください。
**1冊のみおススメしてください**
**書籍情報以外の情報は使用してはなりません。**

### 書籍情報
{bookinfo}
"""
    logger.debug(system_prompt)

    # messagesの先頭に要素を追加
    messages_for_summary.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages_for_summary)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages_for_summary])

    data = {
        "message": answer,
        "bookresult": bookresult,
        "totalnum":total_num,
        "query":answer_query
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)