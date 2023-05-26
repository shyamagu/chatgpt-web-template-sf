from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

import requests

from call_chatgpt import call_chatgpt
from call_bingapi import call_bingapi
from analyze_html import analyze_html

from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/bingsearch")
async def bingsearch(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    messages_for_query = messages.copy()
    messages_for_summary = messages.copy()

    # System Prompt
    system_prompt = """あなたはBing検索クエリ―生成器です。ユーザの入力から、必要となるであろうBing検索クエリを以下の出力フォーマットで返します。
次のステップで処理します。
1. ユーザの入力からユーザが求めている情報について分析する
2. 分析した情報について、必要となるBing検索用のクエリを生成する
**2.で生成した、出力フォーマットの配列文字列のみ回答してください**
**補足や説明は不要です**

出力フォーマット:
["query1","query2","query3"]

サンプル)
入力:「Azureとは?」
出力:["Azure","概要"]

入力:「山田太郎について知りたいです」
出力:["山田太郎","プロフィール"]
"""
    # messagesの先頭に要素を追加
    messages_for_query.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages_for_query)

    # ChatGPTを呼び出す
    answer_query = call_chatgpt([m.dict() for m in messages_for_query])
    # テスト用クエリ answer_query = '["大谷翔平","プロフィール","成績","ニュース"]'

    # answer_queryが配列形式の文字列かどうかをチェックする
    if not answer_query.startswith("[") or not answer_query.endswith("]"):
        data = {
            "message": "検索クエリ―の生成に失敗しました。",
            "query":"",
            "searchResult":[],
        }
        return JSONResponse(content=data)

    bingsearchurl = "https://api.bing.microsoft.com/v7.0/search?q="
    querystring = "%20".join(eval(answer_query))
    option = "&count=5&offset=0"
    #"&count=5&offset=0&mkt=ja-JP"

    logger.debug(answer_query)
 
    bingResult = await call_bingapi(bingsearchurl,querystring,option)

    logger.debug("## bingapi called")

    # bingResult配列を先頭からループ処理し、byteNumの合計が4000になるように配列を作り直す
    analyzeResult = []
    for i in range(len(bingResult)):
        targetUrl = bingResult[i]["url"]
        logger.debug(targetUrl)
        # targetUrlがpdfで終わっている場合は、次のループに移る
        if targetUrl.endswith(".pdf"):
            continue
        try:
            # 例外が発生した場合次のループに移る
            short_title, content_text = analyze_html(targetUrl)
        except:
            continue
        analyzeResult.append({"url":targetUrl,"title":short_title,"content":content_text})

    # analyzeResultの内容を平文テキストに変換する
    analyzeResultText = ""
    for i in range(len(analyzeResult)):
        analyzeResultText += f"""{analyzeResult[i]["title"]}
{analyzeResult[i]["content"]}\n
"""
    # analyzeResultTextを4000バイトに収まるように切り詰める
    b = analyzeResultText.encode('utf-8')
    b = b[:4000]
    analyzeResultText = b.decode('utf-8', 'ignore')

    # System Prompt
    system_prompt = f"""以下の検索結果情報**だけ**をつかって、質問に日本語で回答してください。
検索結果情報に質問の回答が見つからない場合は、決して推測で文章を作成せずに、「Bing検索結果から、私には情報が見つけられませんでした。」という形の回答をして下さい。
**質問の回答は、検索結果情報のみで回答してください。**

###検索結果情報
{analyzeResultText}
"""
    #logger.debug(system_prompt)

    # messagesの先頭に要素を追加
    messages_for_summary.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages_for_summary)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages_for_summary])

    data = {
        "message": answer,
        "query":answer_query,
        "searchResult":analyzeResult,
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)