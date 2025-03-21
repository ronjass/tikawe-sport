import db

def add_sport(sport, duration, distance, description, user_id):
    sql = """INSERT INTO sports (sport, duration, distance, description, user_id) 
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [sport, duration, distance, description, user_id])

def get_sports(user_id):
    sql = "SELECT id, sport FROM sports WHERE sports.user_id = ? ORDER BY id DESC"

    return db.query(sql, [user_id])

def get_allsports():
    sql = "SELECT id, sport FROM sports ORDER BY id DESC"

    return db.query(sql)

def get_sport(sport_id):
    sql = """SELECT sports.id,
                    sports.sport,
                    sports.duration,
                    sports.distance,
                    sports.description,
                    users.id user_id,
                    users.username
            FROM sports, users
            WHERE sports.user_id = users.id AND sports.id = ?"""
    
    result = db.query(sql, [sport_id])
    return result[0] if result else None

def update_sport(sport_id, sport, duration, distance, description):
    sql = """UPDATE sports SET sport = ?,
                                duration = ?,
                                distance = ?,
                                description = ?
                            WHERE id = ?"""
    db.execute(sql, [sport, duration, distance, description, sport_id])

def remove_sport(sport_id):
    sql = "DELETE FROM sports WHERE id = ?"
    db.execute(sql, [sport_id])

def find_sports(query):
    sql = """SELECT id, sport
             FROM sports
             WHERE sport LIKE ? OR DESCRIPTION LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])