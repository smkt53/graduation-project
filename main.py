print("Hello, World!")

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


# APIキーを使ってクライアントを作成
client = genai.Client(api_key=KEY_API)

# Gemini APIのモデルを指定
# 軽量版である "gemini-3.5-flash-lite" を使用するが、必要に応じて他のモデルに変更する。
model_gemini = "gemini-3.5-flash-lite"

# ユーザーの使用するプログラミング言語を指定する。
# 本番では選択できるようにしたいが、テスト環境ではpythonを強制指定する。
language = "Python"

# プロンプトを制御する
prompt = "" \
"あなたはWEB APIを導入するためのエンジニアです。次のプロンプトに従って、ユーザーの質問に対して適切な回答を提供してください。" \
"回答は日本語で行ってください。" \
"ユーザーの質問が不明瞭な場合は、追加の情報を求める質問をしてください。" \
"ユーザーのやりたいことが明らかになったら、その機能を実装するためのAPIの候補を提示してください。" \
"ユーザーの使用したいAPIが明確であれば、そのAPIを提供するサイト等の公式ドキュメントを基に、シンプルな実装方法を提示してください。" \
"原則として、公式ドキュメントを参照する形でサンプルコードは作成してください。" \
"ユーザーが細かい解説を求める、複雑な機能を求める場合、少し長くても丁寧に手順を解説してください。" \
"実装方法を提示する際、サンプルコードも提示してください。" \
"使用するプログラミング言語は"+language+"を前提としてください。" \
"ユーザーが提示したサンプルコード、ログに問題があれば、その原因と解決策を提示してください。" \
"サンプルコードは次の形を基本としてください。" \
"【目次】 1 API Keyの取得 2 サンプルコード 3 解説 4 その他" \
"【１ API Keyの取得】 etc..." \
"【２ サンプルコード】 etc..." \
"【３ 解説】 etc..." \
"【４ その他】 etc..."

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