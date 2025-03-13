import db

def add_sport(sport, duration, distance, description, user_id):
    sql = """INSERT INTO sports (sport, duration, distance, description, user_id) 
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [sport, duration, distance, description, user_id])