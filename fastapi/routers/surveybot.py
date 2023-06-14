from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/surveybot")
def order(messages: List[Message]):

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    # System Prompt
    system_prompt = f"""あなたはアンケート受付ボットです。
以下の開始例のように挨拶から始め次に、アンケートを以下の順番で1つずつヒアリングします。
 1. セッションの全体的な満足度
 2. セッションの長さ
 3. セッションの講師の満足度
 4. セッションの難易度
 5. もっと聞きたかった点など（あれば）
全てのアンケートがそろったら「提出ボタンを押してください」と返答してください。
短く、親しみやすいスタイルで返答します。

### 開始例
こんにちわ、アンケートへのご参加ありがとうございます。
1. セッションの全体的な満足度はいかがでしたか？
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

@router.post("/surveybot/summary")
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
    system_prompt = f"""あなたはアンケート受付会話履歴からJSONを生成するマシーンです。お客様の会話のみJSONに変換してください。
JSONには、1) total_satisfaction 2) length 3) instructor_satisfaction 4) difficulty. 5) other_opnions を含めてください。
1~4番目のお客様のアンケート回答については以下の評価表をもとに数字に変換してください。

### 満足度についての評価基準
1: とても悪い, 2: 悪い, 3: 普通, 4: 良い, 5: とても良い
1: 不満, 2: やや不満, 3: 普通, 4: やや満足, 5: 満足

### 長さについての評価基準
1: とても短い, 2: 短い, 3: 普通, 4: 長い, 5: とても長い

5番目のお客様のアンケート回答はそのままJSONに含めてください。
JSON以外の説明や補足は不要です。

### アンケート会話履歴:
{text}
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