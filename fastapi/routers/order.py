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
async def order(messages: List[Message]):

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
async def summary(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    # System Prompt
    system_prompt = f"""Create a json summary of the previous food order.
The fields should be 1) item_name 2) item_size 3) item_price 4) quantity. 
**Your output must be a JSON ONLY.**

output JSON example:
[
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
]

The menu is following:
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