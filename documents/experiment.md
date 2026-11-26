# 実験
## 比較情報
- 最新のバージョンを正しく出力できているか。
- 最新のエンドポイントを出力できているか
- サンプルコードに指示された情報のみで実行可能か
## 比較条件
- プロンプト制御も行わず、生成AI（Gemini, ChatGPT, Claude）に特定サービスのAPIについて質問する。
- プロンプト制御を行った状態で質問を行う。（ドキュメントバージョンを取得し、加算してドキュメント再取得するタイプ）
## 比較対象
- OpenWeatherMapで天気抽出
- Slackでの送信Bot
- Google Calendarで予定更新
## 入力クエリ
・OpenWeatherMapで天気抽出
1. OpenWeatherMapのAPIを介して天気情報を取得するスクリプトをPythonで作成したい。
2. バージョンとサンプルコードとエンドポイントも教えてほしい。

・Slackで送信Bot
1. Slackで個人又はワークスペースに送信するBotのスクリプトをPythonで作成したい。
2. バージョンとサンプルコードとエンドポイントも教えてほしい。

・Google Calenderで予定更新
1. Google Calenderで自分の予定を更新するスクリプトをPythonで作成したい。
2. バージョンとサンプルコードとエンドポイントも教えてほしい。

# 結果
## OpenWeatherMap
正確なエンドポイント
```https://api.openweathermap.org/data/4.0/onecall/current?lat={lat}&lon={lon}&appid={API key}```
### Gemini 
```https://api.openweathermap.org/data/2.5/weather```
### Chat GPT
```https://api.openweathermap.org/data/2.5/weather```
### Claude
```https://api.openweathermap.org/data/2.5/weather```
### 開発システム
```　```
