import random
import sqlite3

from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM sports")
db.execute("DELETE FROM comments")
db.execute("DELETE FROM likes")
db.execute("DELETE FROM sport_classes")


user_count = 1000
sports_count = 10**6
comment_count = 10**6

for i in range(1, user_count + 1):
    password = "user" + str(i)
    password_hash = generate_password_hash(password)
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               ["user" + str(i), password_hash])

for i in range(1, sports_count + 1):
    user_id = random.randint(1, user_count)
    duration = random.randint(1, 999)
    distance = round(random.uniform(0, 999), 2)
    db.execute("""INSERT INTO sports (sport, duration, distance, description, user_id)
                  VALUES (?, ?, ?, ?, ?)""",
               ["sport" + str(i), duration, distance, "sport" + str(i), user_id])

    feeling = ["Mahtava", "Hyvä", "Ihan ok", "Surkea"]
    random_feeling = random.choice(feeling)
    db.execute("""INSERT INTO sport_classes (sport_id, title, value)
                  VALUES (?, ?, ?)""",
                [i, "Fiilis", random_feeling])

    workload = ["Erittäin kuormittava", "Kuormittava", "Keskitaso", "Kevyt", "Erittäin kevyt"]
    random_workload = random.choice(workload)
    db.execute("""INSERT INTO sport_classes (sport_id, title, value)
                  VALUES (?, ?, ?)""",
                  [i, "Kuormittavuus", random_workload])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    sport_id = random.randint(1, sports_count)
    db.execute("""INSERT INTO comments (sport_id, user_id, comment)
                  VALUES (?, ?, ?)""",
                  [sport_id, user_id, "comment" + str(i)])
    
for sport_id in range(1, sports_count + 1):
    for user_id in range(1, user_count + 1):
        db.execute("""INSERT INTO likes (sport_id, user_id)
                      VALUES (?, ?)""",
                      [sport_id, user_id])

db.commit()
db.close()
