import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import sports
import users
import re

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_sports = sports.get_allsports()
    if session.get("user_id"):
        user_sports = sports.get_sports(session["user_id"])
        return render_template("index.html", user_sports = user_sports, sports = all_sports)
    return render_template("index.html", sports = all_sports)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_sports = users.get_sports(user_id)
    return render_template("show_user.html", user=user, user_sports = user_sports)

@app.route("/find_sport")
def find_sport():
    query = request.args.get("query")
    if query:
        results = sports.find_sports(query)
    else:
        query = ""
        results = []
    return render_template("find_sport.html", query=query, results=results)

@app.route("/sport/<int:sport_id>")
def show_sport(sport_id):
    sport = sports.get_sport(sport_id)
    if not sport:
        abort(404)
    classes = sports.get_classes(sport_id)
    return render_template("show_sport.html", sport=sport, classes=classes)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/new_sport")
def new_sport():
    require_login()
    classes = sports.get_all_classes()
    return render_template("new_sport.html", classes=classes)

@app.route("/create_sport", methods=["POST"])
def create_sport():
    require_login()
    sport = request.form["sport"]
    duration = request.form["duration"]
    distance = request.form["distance"]
    description = request.form["description"]
    if len(sport) > 50 or len(description) > 1000:
        abort(403)
    if not re.search("^[1-9][0-9]{0,2}$", duration):
        abort(403)
    if not re.search("^[1-9][0-9]{0,2}$", distance):
        abort(403)
    if not sport or not duration or not distance or not description:
        abort(403)
    user_id = session["user_id"]

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))

    sports.add_sport(sport, duration, distance, description, user_id, classes)

    return redirect("/")

@app.route("/edit_sport/<int:sport_id>")
def edit_sport(sport_id):
    require_login()
    sport = sports.get_sport(sport_id)
    if not sport:
        abort(404)
    if sport["user_id"] != session["user_id"]:
        abort(403)

    all_classes = sports.get_all_classes()
    classes = {}
    for this_class in all_classes:
        classes[this_class] = ""
    for entry in sports.get_classes(sport_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_sport.html", sport=sport, classes=classes, all_classes=all_classes)

@app.route("/update_sport", methods=["POST"])
def update_sport():
    require_login()
    sport_id = request.form["sport_id"]
    user_sport = sports.get_sport(sport_id)
    if not user_sport:
        abort(404)

    if user_sport["user_id"] != session["user_id"]:
        abort(403)

    sport = request.form["sport"]
    duration = request.form["duration"]
    distance = request.form["distance"]
    description = request.form["description"]

    if len(sport) > 50 or len(description) > 1000:
        abort(403)
    if not re.search("^[1-9][0-9]{0,2}$", duration):
        abort(403)
    if not re.search("^[1-9][0-9]{0,2}$", distance):
        abort(403)
    if not sport or not duration or not distance or not description:
        abort(403)

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))

    sports.update_sport(sport_id, sport, duration, distance, description, classes)

    return redirect("/sport/" + str(sport_id))

@app.route("/remove_sport/<int:sport_id>", methods=["GET", "POST"])
def remove_sport(sport_id):
    require_login()
    sport = sports.get_sport(sport_id)
    if not sport:
        abort(404)

    if sport["user_id"] != session["user_id"]:
        abort(403)
        
    if request.method == "GET":
        return render_template("remove_sport.html", sport=sport)
    if request.method == "POST":
        if "remove" in request.form:
            sports.remove_sport(sport_id)
            return redirect("/")
    else:
        return redirect("/sport/" + str(sport_id))

