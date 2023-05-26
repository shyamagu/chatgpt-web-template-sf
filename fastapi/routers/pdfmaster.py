from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from call_chatgpt import call_chatgpt
from analyze_pdf import analyze_pdf
from call_ada import encode_contents,search_contents
from logger import logger

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str

class PdfUrl(BaseModel):
    url: str

@router.post("/pdfanalyze")
async def pdfanalyze(pdfUrl: PdfUrl):
    logger.debug(pdfUrl.url)

    analyze_result = analyze_pdf(pdfUrl.url)

    global embedding_data
    embedding_data = encode_contents(analyze_result)

    data = {
        "message": "Embeddings Done"
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)

@router.post("/pdfsearch")
async def pdfsearch(messages: List[Message]):
    global embedding_data

    # messagesの最後から10要素のみにする
    messages = messages[-10:]

    latest_message = messages[-1].copy()

    top5ids = search_contents(latest_message.content, embedding_data)

    # System Prompt
    system_prompt = f"""あなたはドキュメントの執筆者です。以下のベクトル検索結果のみを使って、ユーザからの質問に回答してください。
**ベクトル検索結果以外の情報は使用してはなりません。**
**情報が足りない場合や不明な場合は、ユーザにどういう質問をすればいいかを回答してください。**

### ベクトル検索結果
{embedding_data[top5ids[0]]["content"]}
{embedding_data[top5ids[0]+1]["content"]}
{embedding_data[top5ids[0]+2]["content"]}

{embedding_data[top5ids[1]]["content"]}
{embedding_data[top5ids[1]+1]["content"]}

{embedding_data[top5ids[2]]["content"]}

{embedding_data[top5ids[3]]["content"]}

{embedding_data[top5ids[4]]["content"]}
"""
    # messagesの先頭に要素を追加
    messages.insert(0, Message(role="system", content=system_prompt))

    logger.debug(messages)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages])

    data = {
        "message": answer,
        "matched5": [embedding_data[top5ids[0]]["content"]+"\n"+embedding_data[top5ids[0]+1]["content"]+"\n"+embedding_data[top5ids[0]+2]["content"],
                    embedding_data[top5ids[1]]["content"]+"\n"+embedding_data[top5ids[1]+1]["content"],
                    embedding_data[top5ids[2]]["content"],
                    embedding_data[top5ids[3]]["content"],
                    embedding_data[top5ids[4]]["content"]]
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)