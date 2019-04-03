from flask import Flask, render_template, request
from pymongo import MongoClient, TEXT

app = Flask(__name__)
client = MongoClient()

db = client["race_results"]
collection = db["race_results"]

collection.create_index(
    [("firstname", TEXT), ("lastname", TEXT), ("team", TEXT), ("name", TEXT)]
)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        search = request.form["search"].replace('"', "")
        search_query = ('"' + '""'.join(search.split()) + '"').replace('""', '" "')
        years = collection.aggregate(
            [
                {"$match": {"$text": {"$search": search_query}}},
                {"$sort": {"event_date": -1}},
                {"$group": {"_id": "$event_year", "raceresults": {"$push": "$$ROOT"}}},
                {"$sort": {"_id": -1}},
            ]
        )

        return render_template("index.html", years=years, search=search)
    return render_template("index.html")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True, host="0.0.0.0")