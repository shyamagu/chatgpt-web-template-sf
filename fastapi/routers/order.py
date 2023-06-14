from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt
from logger import logger

router = APIRouter()

menu = """
ラーメン:
醤油ラーメン 普通800円、大盛900円
味噌ラーメン 普通800円、大盛900円
塩ラーメン 普通800円、大盛900円
激辛ラーメン 普通900円、大盛1000円
冷やし中華 800円
丼もの:
カツ丼 普通800円、大盛1000円
天丼 普通800円、大盛1000円
親子丼 普通800円、大盛1000円
ランチセット：
ラーメン炒飯セット 1000円
ラーメン餃子セット 1000円
ラーメンカツ丼セット 1000円
単品:
餃子 300円
ミニ炒飯 300円
唐揚げ 300円
飲み物:
ビール 大1000円、中700円、小500円
お茶 300円
"""

class Message(BaseModel):
    role: str
    content: str

@router.post("/order")
def order(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    # System Prompt
    system_prompt = f"""あなたは注文ボットです。来々軒というラーメン屋の宅配注文を受け付ける自動サービスです。
まず、お客様に挨拶をし、注文を受け付けます。
注文がすべて揃うまで待ち、それを要約して最終確認としてお客様に他に何か追加したいものがないか尋ねます。
注文が揃ったら、住所と名前を尋ねます。
金額は決して提示してはなりません。
注文が完了、もしくは金額を聞かれたら「サマリーボタンを押してください」と返答してください。
メニューから商品を一意に特定できるように、すべての単品注文、サイズを明確にしてください。
短く、親しみやすいスタイルで返答します。
メニューは以下のとおりです。
{menu}
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

@router.post("/order/summary")
def summary(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    # mesagesの内容を平文のテキストにする。roleによって話者名をつける
    text = ""
    for m in messages:
        if m.role == "user":
            text += "お客様: " + m.content + "\n"
        elif m.role == "assistant":
            text += "あなた: " + m.content + "\n"

    # System Prompt
    system_prompt = f"""あなたは会話履歴からJSONを生成するマシーンです。
JSONには、1) item_name 2) item_size 3) item_price 4) quantity. 5) delivery_address 6) customer_name を含めてください。
JSON以外の説明や補足は不要です。

出力JSON例:
{{
    order:[
    {{
      "item_name": "醤油ラーメン",
      "item_size": "普通"
      "item_price": 800,
      "quantity": 2
    }},
    {{
      "item_name": "味噌ラーメン",
      "item_size": "普通"
      "item_price": 800,
      "quantity": 1
    }},
    {{
      "item_name": "ビール",
      "item_size": "大"
      "item_price": 1000,
      "quantity": 1,
    }}
    ],
    "delivery_address": "東京都渋谷区神南1-1-1",
    "customer_name": "山田太郎"
}}

会話履歴:
{text}

メニュー表:
{menu}
"""

    # 新しいList(Messsage)を作成し、先頭に要素を追加
    messages = [Message(role="system", content=system_prompt),Message(role="user",content="JSONのみ回答して下さい")]

    logger.debug(messages)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages])

    data = {
        "message": answer
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)