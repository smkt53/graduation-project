import json

# json読み込み
json_open = open("session.json", "r")
json_load = json.load(json_open)
print(json_load["interaction1"]["id"])

json_open.close()
