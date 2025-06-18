
from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("corpus.json", "r", encoding="utf-8") as f:
    CORPUS = json.load(f)

def smart_reply(user_input):
    matches = []
    for entry in CORPUS:
        for kw in entry["keywords"]:
            if kw in user_input:
                matches.append((entry["scene"], entry["reply"]))
                break
    if matches:
        scene, reply = matches[0]
        return scene, reply
    return "無對應情境", "目前無法判斷最適當的回應，請確認說法是否清楚。"

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = ""
    response = ""
    scene = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        scene, response = smart_reply(user_input)
    return render_template("index.html", user_input=user_input, response=response, scene=scene)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
