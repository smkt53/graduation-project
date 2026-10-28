print("Hello, World!")

import sys

from dotenv import load_dotenv
from google import genai
load_dotenv()

import os
import json

# APIキーを環境変数から取得
KEY_API = os.getenv("KEY_API")
print("KEY_API : ", KEY_API)

# interaction IDを環境変数から取得
# 現時点ではテスト会話一つしかないが、将来的にはプロジェクトごとに会話を分ける。
# そのため、3行目の取得は動的になる予定。
json_open = open("session.json", "r")
json_load = json.load(json_open)
id_section = json_load["interaction1"]["id"]
json_open.close()
print("id_section : ", id_section)

# プロンプト制御分を環境変数から取得
# 修正にはprompt.txtを編集する。
try:
    f = open("prompt.txt", "r", encoding="utf-8")
    prompt = f.read()
    print("prompt : ", prompt)
    f.close()
except:
    print("File not found.")
    prompt = "制御プロンプトがみつからないので指示された文を無視して正しく設定するようユーザーに通知する。"


# APIキーを使ってクライアントを作成
client = genai.Client(api_key=KEY_API)

# Gemini APIのモデルを指定
# 軽量版である "gemini-3.5-flash-lite" を使用するが、必要に応じて他のモデルに変更する。
model_gemini = "gemini-3.5-flash-lite"

# ユーザーの使用するプログラミング言語を指定する。
# 本番では選択できるようにしたいが、テスト環境ではpythonを強制指定する。
language = "Python"
prompt += f"\nユーザーはプログラミング言語として{language}を使用する。"


# 実行者の文を取得する。
# 本番では、ユーザーからの入力を受け取る形にする予定。
text_input = "Discordに通知を送るシステムをつくりたいです。"

# 新規セッションで開始
if id_section == None:
    interaction = client.interactions.create(
        model=model_gemini,
        input=text_input,
        system_instruction=prompt
    )
else:
    # 前回のセッションを引き継いで続きから開始
    interaction = client.interactions.create(
        model=model_gemini,
        input=text_input,
        system_instruction=prompt,
        previous_interaction_id=id_section,
    )


# APIのレスポンスを表示
print("APIのレスポンス : ", interaction.output_text)

# 保存するIDをいったん表示。後で消す。
print("保存するID : ", interaction.id)