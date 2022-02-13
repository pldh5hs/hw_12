from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("settings.json", "r", encoding='utf-8') as f:
    settings = json.load(f)
    # print(settings["online"])

with open("candidates.json", "r", encoding='utf-8') as f:
    candidates = json.load(f)
    # print(candidates)


@app.route("/")
def mainpage():
    if settings["online"] is True:
        return "Приложение работает"
    else:
        return "Приложение не работает"


@app.route("/candidate/<int:x>")
def candidate(x):
    for candidate in candidates:
        if candidate["id"] == x:
            return render_template('candidate.html', candidate=candidate)


@app.route("/list")
def list():
    return render_template('list.html', candidates=candidates)


@app.route("/search")
def search():
    counter = 0
    name_candidate = []
    query = request.values.get("name")
    for candidate in candidates:
        if settings["case-sensitive"] is False:
            query = query.lower()
            candidate["name"] = candidate["name"].lower()
        if query in candidate["name"]:
            counter += 1
            name_candidate.append(candidate)
        candidate["name"] = candidate["name"].title()
    return render_template('search.html', candidates=name_candidate, counter=counter)


@app.route("/skill/<sk>")
def skill(sk):
    counter1 = 0
    skill_candidate = []
    sk = sk.lower()
    quantity = settings["limit"]
    for candidate in candidates:
        if sk in candidate["skills"].lower():
            counter1 += 1
            skill_candidate.append(candidate)
            if quantity == counter1:
                break
    return render_template('search.html', candidates=skill_candidate, counter=counter1, sk=sk)


app.run()
