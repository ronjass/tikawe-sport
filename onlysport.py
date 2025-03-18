import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import sports

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_sports = sports.get_allsports()
    if session.get("user_id"):
        user_sports = sports.get_sports(session["user_id"])
        return render_template("index.html", user_sports = user_sports, sports = all_sports)
    return render_template("index.html", sports = all_sports)

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
    return render_template("show_sport.html", sport=sport)

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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
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
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/new_sport")
def new_sport():
    return render_template("new_sport.html")

@app.route("/create_sport", methods=["POST"])
def create_sport():
    sport = request.form["sport"]
    duration = request.form["duration"]
    distance = request.form["distance"]
    description = request.form["description"]
    user_id = session["user_id"]

    sports.add_sport(sport, duration, distance, description, user_id)

    return redirect("/")

@app.route("/edit_sport/<int:sport_id>")
def edit_sport(sport_id):
    sport = sports.get_sport(sport_id)
    return render_template("edit_sport.html", sport=sport)

@app.route("/update_sport", methods=["POST"])
def update_sport():
    sport_id = request.form["sport_id"]
    sport = request.form["sport"]
    duration = request.form["duration"]
    distance = request.form["distance"]
    description = request.form["description"]

    sports.update_sport(sport_id, sport, duration, distance, description)

    return redirect("/sport/" + str(sport_id))

@app.route("/remove_sport/<int:sport_id>", methods=["GET", "POST"])
def remove_sport(sport_id):
    if request.method == "GET":
        sport = sports.get_sport(sport_id)
        return render_template("remove_sport.html", sport=sport)
    if request.method == "POST":
        if "remove" in request.form:
            sports.remove_sport(sport_id)
            return redirect("/")
    else:
        return redirect("/sport/" + str(sport_id))

