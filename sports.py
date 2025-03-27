import db

def add_sport(sport, duration, distance, description, user_id, classes):
    sql = """INSERT INTO sports (sport, duration, distance, description, sent_at, user_id) 
            VALUES (?, ?, ?, ?, strftime('%d-%m-%Y', 'now', 'localtime'), ?)"""
    db.execute(sql, [sport, duration, distance, description, user_id])

    sport_id = db.last_insert_id()

    sql = "INSERT INTO sport_classes (sport_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [sport_id, title, value])

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_classes(sport_id):
    sql = "SELECT title, value FROM sport_classes WHERE sport_id = ?"
    return db.query(sql, [sport_id])

def get_sports(user_id):
    sql = "SELECT id, sport, sent_at FROM sports WHERE sports.user_id = ? ORDER BY id DESC"

    return db.query(sql, [user_id])

def get_allsports():
    sql = "SELECT id, sport, sent_at FROM sports ORDER BY id DESC"

    return db.query(sql)

def get_sport(sport_id):
    sql = """SELECT sports.id,
                    sports.sport,
                    sports.duration,
                    sports.distance,
                    sports.description,
                    sports.sent_at,
                    users.id user_id,
                    users.username
            FROM sports, users
            WHERE sports.user_id = users.id AND sports.id = ?"""
    
    result = db.query(sql, [sport_id])
    return result[0] if result else None

def update_sport(sport_id, sport, duration, distance, description, classes):
    sql = """UPDATE sports SET sport = ?,
                                duration = ?,
                                distance = ?,
                                description = ?
                            WHERE id = ?"""
    db.execute(sql, [sport, duration, distance, description, sport_id])

    sql = "DELETE FROM sport_classes WHERE sport_id = ?"
    db.execute(sql, [sport_id])

    sql = "INSERT INTO sport_classes (sport_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [sport_id, title, value])

def remove_sport(sport_id):
    sql = "DELETE FROM sport_classes WHERE sport_id = ?"
    db.execute(sql, [sport_id])
    sql = "DELETE FROM sports WHERE id = ?"
    db.execute(sql, [sport_id])

def find_sports(query):
    sql = """SELECT id, sport
             FROM sports
             WHERE sport LIKE ? OR DESCRIPTION LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_comment(sport_id, user_id, comment):
    sql = """INSERT INTO comments (sport_id, user_id, comment, sent_at) 
            VALUES (?, ?, ?, strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime'))"""
    db.execute(sql, [sport_id, user_id, comment])

def get_comments(sport_id):
    sql = """SELECT comments.comment, comments.sent_at, users.id user_id, users.username
             FROM comments, users
             WHERE comments.sport_id = ? AND comments.user_id = users.id
             ORDER BY comments.id"""
    return db.query(sql, [sport_id])