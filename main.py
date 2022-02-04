from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("settings.json", "r") as f:
    settings = json.load(f)
    # print(settings["online"])

with open("candidates.json", "r") as f:
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
            page_candidate = f"""
            <h1>{candidate["name"]}</h1>
            <p>{candidate["position"]}</p>
            <img src="{candidate["picture"]}" width=200/>
            <p>{candidate["skills"]}</p>
"""
            return page_candidate


@app.route("/list")
def list():
    list_candidate = "<h1>Все кандидаты</h1>"
    for candidate in candidates:
        list_candidate += f"""
        <p><a href="/candidate/{candidate["id"]}">{candidate["name"]}</a></p>
"""
    return list_candidate


@app.route("/search")
def search():
    counter = 0
    name_candidate = ""
    query = request.values.get("name")
    for candidate in candidates:
        if settings["case-sensitive"] is False:
            query = query.lower()
            candidate["name"] = candidate["name"].lower()
        if query in candidate["name"]:
            counter += 1
            name_candidate += f"""<p><a href="/candidate/{candidate["id"]}">{candidate["name"].title()}</a></p>"""
    search_name_candidate = f"""
    <h1>найдено кандидатов {counter}</h2>
    {name_candidate}"""
    return search_name_candidate


@app.route("/skill/<sk>")
def skill(sk):
    counter1 = 0
    skill_candidate = ""
    sk = sk.lower()
    quantity = settings["limit"]
    for candidate in candidates:
        if sk in candidate["skills"].lower():
            counter1 += 1
            skill_candidate += f"""<p><a href="/candidate/{candidate["id"]}">{candidate["name"]}</a></p>"""
            if quantity == counter1:
                break
    return f"""
            <h1>Найдено со скиллом {sk}: {counter1}</h2>
            {skill_candidate}
"""


app.run()
