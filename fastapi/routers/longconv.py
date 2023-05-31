from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt
from longmemory import saveConvMemory,rememberConvMemory,saveConvSummaryMemory,rememberConvSummaryMemory
from logger import logger

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

@router.post("/longconv")
async def longconv(messages: List[Message]):

    memoryMessages = rememberConvMemory(messages[-1].content)

    if memoryMessages:
        messages[0:0] = memoryMessages

    # messagesの要素が3以上の場合
    if len(messages) >= 3:
        saveConvMemory(messages[-3:-1])

    # System Prompt
    system_prompt = f"""あなたは聞き上手な会話エキスパートです。
会話に関係する適切な質問をたまに入れてください。
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

@router.post("/longconv/summary")
async def longconvsummary(messages: List[Message]):

    global chatgpt_conv_history
    # chatgpt_conv_historyが定義されていなければ空の配列を定義
    if not "chatgpt_conv_history" in globals():
        chatgpt_conv_history = []

    # chatgpt_conv_historyの長さが10以上の場合
    if len(chatgpt_conv_history) >= 10:
        # message_from_sessionの内容を平文に変換する
        text_message = ""
        for m in chatgpt_conv_history:
            if m.role == "user":
                text_message += "ユーザ: " + m.content + "\n"
            if m.role == "assistant":
                text_message += "ChatGPT: " + m.content + "\n"
        # System Prompt
        system_prompt = f"""あなたは会話ログの要約生成マシーンです。
入力された会話ログから、簡潔な要約を作成してください。
特に固有名詞は必ず含めてください。

入力される会話ログは以下の形式です。
ユーザ: こんにちは
ChatGPT: こんにちは、あなたのお名前は何ですか？
ユーザ: 私は山田太郎です。
ChatGPT: 山田さん、始めまして。今日は何かお困りですか？

要約例:
ユーザの名前は山田太郎
"""
        # ChatGPTを呼び出す
        summary = call_chatgpt([m.dict() for m in [Message(role="system", content=system_prompt),Message(role="user", content=text_message)]])
        saveConvSummaryMemory(summary)
        # 履歴をクリアする
        chatgpt_conv_history = []

    # messagesの最新の要素をchatgpt_conv_historyに追加
    chatgpt_conv_history.append(messages[-1])


    remember_summary = rememberConvSummaryMemory(messages[-1].content)
    logger.debug(remember_summary)
    #remember_summaryの配列の内容を要素ごとに改行コードで結合したテキストを作成する
    past_summary = ""
    if remember_summary:
        # 要素単位で改行コードを追加して改行
        for i in range(len(remember_summary)):
            past_summary += remember_summary[i] + "\n"
    else:
        past_summary = "なし"

    # System Prompt
    system_prompt = f"""あなたは聞き上手な会話エキスパートです。
会話に関係する適切な質問をたまに入れてください。なお、過去の会話要約情報があればその情報を参考にしてください。

###過去の会話要約情報
{past_summary}
"""
    # messagesの先頭に要素を追加
    messages.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages])

    # answerをcontentにした新しいMessageをchatgpt_conv_historyに追加
    chatgpt_conv_history.append(Message(role="assistant", content=answer))

    data = {
        "message": answer
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)

@router.get("/longconv/clear")
async def clear(request:Request):
    global chatgpt_conv_history
    chatgpt_conv_history = []
    return JSONResponse(content={"message": "ok"})