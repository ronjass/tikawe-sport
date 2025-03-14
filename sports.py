import db

def add_sport(sport, duration, distance, description, user_id):
    sql = """INSERT INTO sports (sport, duration, distance, description, user_id) 
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [sport, duration, distance, description, user_id])

def get_sports(user_id):
    sql = "SELECT id, sport FROM sports WHERE id = ? ORDER BY id DESC"

    return db.query(sql, [user_id])

def get_allsports():
    sql = "SELECT id, sport FROM sports ORDER BY id DESC"

    return db.query(sql)

def get_sport(sport_id):
    sql = """SELECT sports.sport,
                    sports.duration,
                    sports.distance,
                    sports.description,
                    users.username
            FROM sports, users
            WHERE sports.user_id = users.id AND sports.id = ?"""
    
    return db.query(sql, [sport_id])[0]