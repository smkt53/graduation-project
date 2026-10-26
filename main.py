print("Hello, World!")

from dotenv import load_dotenv
from google import genai
load_dotenv()

import os
import json

# APIキーを環境変数から取得
KEY_API = os.getenv("KEY_API")
print("KEY_API:", KEY_API)

# interaction IDを環境変数から取得
json_open = open("session.json", "r")
json_load = json.load(json_open)
id_section = json_load["interaction1"]["id"]
json_open.close()
print("interid:", id_section)


# APIキーを使ってクライアントを作成
client = genai.Client(api_key=KEY_API)

# 新規セッションで開始
if id_section == None:
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="トークセッションの保存をテストしたいので、「Hello, World!」のみ出力してください。",
    )
else:
    # 前回のセッションを引き継いで続きから開始
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input="先ほどの出力内容の最後に「!」をもう一つ追加して出力してください。",
        previous_interaction_id=id_section,
    )    

# APIのレスポンスを表示
print(interaction.output_text)

# 保存するIDをいったん表示。後で消す。
print(interaction.id)