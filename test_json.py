import json

# json読み込み
json_open = open("session.json", "r")
json_load = json.load(json_open)
print(json_load["interaction1"]["id"])

json_open.close()
try:
    f = open("prompt.txt", "r", encoding="utf-8")
    text = f.read()
    print(text)
    f.close()
except:
    print("File not found.")