import sqlite3
import secrets
from math import ceil

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe

import config
import sports
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    all_sports = sports.get_all_sports(5, 0)
    if session.get("user_id"):
        user_sports = sports.get_user_sports_limit(session["user_id"], 5, 0)
        user = users.get_user(session["user_id"])
        return render_template("index.html", user_sports=user_sports, sports=all_sports, user=user)
    return render_template("index.html", sports=all_sports)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_sports = users.get_sports(user_id)
    return render_template("show_user.html", user=user, user_sports=user_sports)

@app.route("/find_user/<int:page>")
def find_user(page=1):
    query = request.args.get("query", "")
    page_size = 10

    if query:
        total_results = users.count_query_users(query)
        total_pages = ceil(total_results / page_size)
        total_pages = max(total_pages, 1)
        users_list = users.find_users(query, page, page_size)
    else:
        total_results = users.count_query_users(query)
        total_pages = 0
        users_list = []

    return render_template("find_user.html", results=users_list, query=query,
                           total_results=total_results, page=page, total_pages=total_pages)

@app.route("/find_sport/<int:page>")
def find_sport(page=1):
    query = request.args.get("query", "")
    page_size = 10

    if query:
        total_results = sports.count_query_sports(query)
        total_pages = ceil(total_results / page_size)
        total_pages = max(total_pages, 1)
        sports_list = sports.find_sports(query, page, page_size)
    else:
        total_results = sports.count_query_sports(query)
        total_pages = 0
        sports_list = []

    return render_template("find_sport.html", results=sports_list, query=query,
                           total_results=total_results, page=page, total_pages=total_pages)

@app.route("/show_user_sports/<int:user_id>/<int:page>")
def show_user_sports(user_id, page=1):
    page_size = 10
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_sports_count = sports.get_user_sports_count(user_id)
    total_pages = ceil(user_sports_count / page_size)
    total_pages = max(total_pages, 1)

    if page < 1:
        return redirect("/show_user_sports/1")
    if page > total_pages:
        return redirect("/show_user_sports/" + str(total_pages))

    offset = (page - 1) * page_size
    current_page_sports = sports.get_user_sports_limit(user_id, page_size, offset)

    return render_template("show_user_sports.html", user=user, user_sports=current_page_sports,
                           page=page, total_pages=total_pages)

@app.route("/show_all_sports/<int:page>")
def show_all_sports(page=1):
    page_size = 10
    total_sports_count = sports.get_total_sports_count()

    total_pages = ceil(total_sports_count / page_size)
    total_pages = max(total_pages, 1)

    if page < 1:
        return redirect("/show_all_sports/1")
    if page > total_pages:
        return redirect("/show_all_sports/" + str(total_pages))

    offset = (page - 1) * page_size
    current_page_sports = sports.get_all_sports(page_size, offset)

    return render_template("show_all_sports.html", sports=current_page_sports,
                           page=page, total_pages=total_pages)

@app.route("/sport/<int:sport_id>")
def show_sport(sport_id):
    sport = sports.get_sport(sport_id)
    if not sport:
        abort(404)
    classes = sports.get_classes(sport_id)
    comments = sports.get_comments(sport_id)
    likes_count = sports.get_likes_count(sport_id)
    return render_template("show_sport.html", sport=sport, classes=classes,
                           comments=comments, likes_count=likes_count)

@app.route("/register")
def register():
    return render_template("register.html", filled={})

@app.route("/create_user", methods=["POST"])
def create_user():
    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: salasanat eivät ole samat", "error")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1)
            flash("Tunnus luotu. Kirjaudu sisään käyttäjällesi.", "info")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("VIRHE: tunnus on jo varattu", "error")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={}, next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)

        flash("VIRHE: väärä tunnus tai salasana", "error")
        filled = {"username": username}
        return render_template("login.html", filled=filled, next_page=next_page)

@app.route("/add_image/<int:user_id>", methods=["GET", "POST"])
def add_image(user_id):
    require_login()

    user = users.get_user(user_id)
    if not user:
        abort(404)
    if user["id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("add_image.html", user=user)

    if request.method == "POST":
        check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: väärä tiedostomuoto", "error")
            return redirect("/add_image/" + str(user_id))

        image = file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: liian suuri kuva", "error")
            return redirect("/add_image/" + str(user_id))

        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/remove_image", methods=["POST"])
def remove_image():
    require_login()
    check_csrf()

    user_id = request.form["user_id"]
    user = users.get_user(user_id)
    if not user:
        abort(404)
    if user["id"] != session["user_id"]:
        abort(403)

    users.remove_image(user_id)

    return redirect("/add_image/" + str(user_id))

@app.route("/logout")
def logout():
    require_login()
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/remove_user/<int:user_id>", methods=["GET", "POST"])
def remove_user(user_id):
    require_login()
    user = users.get_user(user_id)
    if not user:
        abort(404)
    if user["id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_user.html", user=user)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            user_sports = sports.get_user_sports(user_id)
            if user_sports:
                for sport in user_sports:
                    sports.remove_sport(sport["id"])
            users.remove_user(user_id)
            del session["user_id"]
            del session["username"]
            flash("Käyttäjän poistaminen onnistui.", "info")
            return redirect("/")
        return redirect("/user/" + str(user_id))

@app.route("/new_sport")
def new_sport():
    require_login()
    classes = sports.get_all_classes()
    return render_template("new_sport.html", classes=classes)

@app.route("/create_sport", methods=["POST"])
def create_sport():
    require_login()
    check_csrf()
    sport = request.form["sport"]
    duration = request.form["duration"]
    distance = request.form["distance"]
    description = request.form["description"]
    if len(sport) > 50 or len(description) > 1000:
        abort(403)
    if not 1 <= int(duration) <= 999:
        abort(403)
    if not 0 <= float(distance) <= 999:
        abort(403)
    if not sport or not duration or not distance or not description:
        abort(403)
    user_id = session["user_id"]

    all_classes = sports.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            title, value = entry.split(":")
            if title not in all_classes:
                abort(403)
            if value not in all_classes[title]:
                abort(403)
            classes.append((title, value))

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
    check_csrf()
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
    if not 1 <= int(duration) <= 999:
        abort(403)
    if not 0 <= float(distance) <= 999:
        abort(403)
    if not sport or not duration or not distance or not description:
        abort(403)

    all_classes = sports.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            title, value = entry.split(":")
            if title not in all_classes:
                abort(403)
            if value not in all_classes[title]:
                abort(403)
            classes.append((title, value))

    sports.update_sport(sport_id, sport, duration, distance, description, classes)

    return redirect("/sport/" + str(sport_id))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()
    comment = request.form["comment"]
    if len(comment) > 1000 or not comment:
        abort(403)
    sport_id = request.form["sport_id"]
    sport = sports.get_sport(sport_id)
    if not sport:
        abort(403)
    user_id = session["user_id"]

    sports.add_comment(sport_id, user_id, comment)

    return redirect("/sport/" + str(sport_id))

@app.route("/like", methods=["POST"])
def like_sport():
    require_login()
    check_csrf()

    if "user_id" in session:
        sport_id = request.form["sport_id"]
        user_id = session["user_id"]
        sport = sports.get_sport(sport_id)
        if not sport:
            abort(404)
        sports.add_like(sport_id, user_id)
        return redirect("/sport/" + str(sport_id))

    return redirect("/login")

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
        check_csrf()
        if "remove" in request.form:
            sports.remove_sport(sport_id)
            flash("Urheilusuorituksen poistaminen onnistui.", "info")
            return redirect("/")
        return redirect("/sport/" + str(sport_id))
