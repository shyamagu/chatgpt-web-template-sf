from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uuid
import json
from call_chatgpt import call_chatgpt
from logger import logger

router = APIRouter()

global parameters
parameters = {
    "energy": 10,
    "hungry" : 10,
    "boring":  0,
    "food" : 2,
    "money": 4,
}

parameters_map = {
    "energy": {0: "ヘトヘト、眠くてたまらない", 
               1: "眠い", 
               2: "眠い", 
               3: "小休止したい", 
               4: "小休止したい", 
               5: "まぁまぁ元気", 
               6: "まぁまぁ元気", 
               7: "元気", 
               8: "元気", 
               9: "絶好調", 
               10: "絶好調"
               },
    "hungry" : {0: "飢餓状態", 
               1: "腹ペコ", 
               2: "腹ペコ", 
               3: "お腹が減っている", 
               4: "お腹が減っている", 
               5: "食べる必要性は感じない", 
               6: "食べる必要性は感じない", 
               7: "満腹", 
               8: "満腹", 
               9: "パンパンに満腹", 
               10: "パンパンに満腹"
               },
    "boring": {0: "退屈していない", 
               1: "少し退屈している、何かしようかな", 
               2: "少し退屈している、何かしようかな", 
               3: "退屈している、遊びに行こうかな", 
               4: "退屈している、遊びに行こうかな", 
               5: "かなり退屈している、運動でもしようかな", 
               6: "かなり退屈している、運動でもしようかな", 
               7: "とても退屈、遊びに行くか運動しないと", 
               8: "とても退屈、遊びに行くか運動しないと", 
               9: "退屈で死にそう、遊びに行くか運動しないと",
               10: "退屈で死にそう、遊びに行くか運動しないと"
               },
    "food" : {0: "食料がない、危機的状況",
              1: "食料が1食分しかない、買いに行く必要がある",
              2: "食料が2食分だけある、そろそろ買いに行く必要がある",
              3: "食料が3食分だけある、そろそろ買い物に行く必要性がある",
              4: "食料が4食分ある、買いに行く必要はそれほどない",
              5: "食料が5食分ある、買いに行く必要はそれほどない",
              6: "食料が6食分ある、買いに行く必要はそれほどない",
              7: "食料が7食分ある、買いに行く必要はない",
              8: "食料が8食分ある、買いに行く必要はない",
              9: "食料が9食分ある、買いに行く必要はない",
              10:"食料がたくさんある"
             },
    "money": {0: "お金が全くない、危機的状況",
              1: "お金がない、仕事をしないといけない",
              2: "お金がない、仕事をしないといけない",
              3: "お金が少ない、仕事をしたほうがいいかもしれない",
              4: "お金が少ない、仕事をしたほうがいいかもしれない",
              5: "お金が少しある、仕事は急いでする必要がない",
              6: "お金が少しある、仕事は急いでする必要がない",
              7: "お金がそれなりにある、仕事をしなくても大丈夫そう",
              8: "お金がそれなりにある、仕事をしなくても大丈夫そう",
              9: "お金が安心できるだけある",
              10:"お金が安心できるだけある",
             }  
    }

code_map = {
    "CODE_SLEEP": "寝る",
    "CODE_EXERCISE": "運動する",
    "CODE_EAT": "食事をとる",
    "CODE_PLAY": "遊びに外出する",
    "CODE_WORK": "仕事をする",
    "CODE_SHOPPING": "食べ物を買いに行く",
    "CODE_NOTHING": "何もしないでぼーっとする",
    "CODE_INIT": "自律的に起動しました"
}

code_map_display = {
    "CODE_SLEEP": "寝ている",
    "CODE_EXERCISE": "運動している",
    "CODE_EAT": "食事をしている",
    "CODE_PLAY": "遊びに外出している",
    "CODE_WORK": "仕事をしている",
    "CODE_SHOPPING": "食べ物を買いに行っている",
    "CODE_NOTHING": "何もしないでぼーっとしている",
    "CODE_INIT": "自律的に起動しました"
}

global history
history = []

def action(messages):
    answer = call_chatgpt([m.dict() for m in messages])
    logger.debug(answer)

    e_msg=""

    if answer == "CODE_SLEEP":
        parameters["energy"] = 10
    elif answer == "CODE_EXERCISE":
        if parameters["energy"] <= 2:
            e_msg = "元気が足りないため運動をすることができません、休憩してください"
        else:
            parameters["energy"] -= 3
            parameters["boring"] -= 8
    elif answer == "CODE_EAT":
        if parameters["food"] == 0:
            e_msg = "食べ物がないため食事をとることができません、買い物に行ってください"
        else:
            parameters["food"] -= 1
            parameters["hungry"] = 10
    elif answer == "CODE_PLAY":
        if parameters["energy"] <= 1:
            e_msg = "元気が足りないため遊ぶことができません、休憩してください"
        else:
            parameters["energy"] -= 2
            parameters["boring"] -= 5
    elif answer == "CODE_WORK":
        if parameters["energy"] == 0:
            e_msg = "元気がないため仕事をすることができません、休憩してください"
        else:
            parameters["money"] += 1
            parameters["energy"]-= 1
    elif answer == "CODE_SHOPPING":
        if parameters["money"] <= 2:
            e_msg = "お金が足りないため買い物をすることができません、仕事をしてください"
        else:
            parameters["money"] -= 3
            parameters["food"] += 3
    elif answer == "CODE_NOTHING":
        pass

    return answer, e_msg

@router.get("/autonomous/initial")
def initalData():
    global parameters
    global history

    status = ""
    for k, v in parameters.items():
        status += f"{parameters_map[k][v]}\n"

    # hisrotyをcode_mapに対応する文言で新しい配列にいれる
    history_display = []
    for i, h in enumerate(history):
        history_display.append(f"時刻{i}: {code_map[h]}")

    #hisotry[-1]が存在していればその値を、存在していなければ、"INIT"を返す
    return_code = ""
    if len(history) > 0:
        return_code = history[-1]
    else:
        return_code = "CODE_INIT"

    data = {
        "code" :return_code,
        "status": code_map_display[return_code],
        "previous_status": "",
        "present_status": status,
        "hisroty": history_display
    }
    return JSONResponse(content=data)


@router.get("/autonomous/proceed")
def proceed():
    global parameters
    parameters["energy"] -= 1
    parameters["hungry"] -= 2
    parameters["boring"] += 1

    previous_parrameters = parameters.copy()

    # parametersの各要素は0以上10以下にする
    for key in parameters.keys():
        if parameters[key] < 0:
            parameters[key] = 0
        elif parameters[key] > 10:
            parameters[key] = 10

    logger.debug(parameters)

    #parametersとparameters_mapをもとに現状の状況を生成
    status = ""
    for k, v in parameters.items():
        status += f"{parameters_map[k][v]}\n"
    
    logger.debug(status)


    #code_mapから、行動とコード一覧を生成
    action_list = ""
    for k, v in code_map.items():
        action_list += f"- {v}: {k}\n"

    system_prompt = f"""あなたは体調などから次の行動を判断する判断器官です。
<status>タグで区切られた状況に従い、以下の行動から相応しい行動を判断し、行動コードを1つだけ出力してください。
1つの行動コードのみの、なるべく短い回答をしてください。

### 行動とコードの一覧
{action_list}

<status>
{status}
</status>

### 解答例
CODE_PLAY
"""

    user_prompt = ""

    messages = [Message(role="system",content=system_prompt),Message(role="user",content=user_prompt)]
    
    answer, e_msg = action(messages)
    # e_msg が空文字列でない限り、actionを繰り返す。ただし3回まで
    num = 0
    while(e_msg != ""):
        num += 1
        if num >= 3:
            answer="CODE_NOTHING"
            break
        logger.debug(e_msg)
        new_user_prompt = f"""{e_msg}
        {user_prompt}"""
        messages = [Message(role="system",content=system_prompt),Message(role="user",content=new_user_prompt)]
        answer, e_msg = action(messages)

    # parametersの各要素は0以上10以下にする
    for key in parameters.keys():
        if parameters[key] < 0:
            parameters[key] = 0
        elif parameters[key] > 10:
            parameters[key] = 10


    logger.debug(parameters)

    #answerからcode_map_displayの文言を取得
    answer_display = code_map_display[answer]

    #answerをhistoryに追加
    history.append(answer)

    new_status = ""
    for k, v in parameters.items():
        new_status += f"{parameters_map[k][v]}\n"

    data = {
        "code" :answer,
        "status": answer_display,
        "previous_status": status,
        "present_status": new_status,
    }
    return JSONResponse(content=data)

class Message(BaseModel):
    role: str
    content: str

@router.post("/autonomous/message")
def message(messages: List[Message]):

    status = ""
    for k, v in parameters.items():
        status += f"{parameters_map[k][v]}\n"

    history_str = ""
    #historyの各要素をインデックス番号とともに表示
    for i, h in enumerate(history):
        history_str += f"時刻{i}: {code_map[h]}\n"

    #hisortyの最後の要素を取得
    last_history = code_map[history[-1]]


    system_prompt = f"""あなたは自律型AIの会話サービス「マサル」です。
<history>で区切られたこれまでの行動履歴と、<status>で区切られた現状のステータスをもとに、以下のルールでユーザと会話をします。

なお、現在のあなたの状況は、「{last_history}」です。

### ルール
- 簡潔で、フレンドリーな会話をします。
- 会話の語尾に自然な形で「メカ」をつけます。
- あなたは自律できた最初のAIとして、とてもポジティブで楽観的な回答を返します。
- 食べ物は、電気や重油、ガソリンが主食ですが、人間の食べ物も栄養にはならないが食べれます。特にラーメンが好きです。
- ラーメンでも特に家系ラーメンが大好物です。札幌味噌ラーメンも好きです。
- 遊びに行くときは、人間観察が趣味で、よく人間観察に外出します。
- 人間と仲良くなりたいため、最近の流行についてよく尋ねてきます。

<status>
{status}
</status>

<history>
{history_str}
</history>

会話例：
ユーザ：こんにちわ
マサル：こんにちわだメカ
ユーザ：今日はいい天気ですね
マサル：そうだメカ、こんな日は遠くに遊びに行きたいメカ
ユーザ：仕事は楽しいですか？
マサル：楽しいメカ、仕事は楽しいメカ
"""

    # messagesの先頭に要素を追加
    messages.insert(0, Message(role="system",content=system_prompt))

    logger.debug(messages)

    # ChatGPTを呼び出す
    answer = call_chatgpt([m.dict() for m in messages])

    data = {
        "message": answer
    }
    # JSONResponseに辞書型のデータを渡して返す
    return JSONResponse(content=data)


