from werkzeug.security import generate_password_hash, check_password_hash
import db

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users 
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_sports(user_id):
    sql = """SELECT id, sport, duration, distance, sent_at
             FROM sports
             WHERE user_id = ?
             ORDER BY id DESC"""
    return db.query(sql, [user_id])

def count_query_users(query):
    sql = "SELECT COUNT(*) FROM users WHERE username LIKE ?"
    like = "%" + query + "%"
    return db.query(sql, [like])[0][0]

def find_users(query, page, page_size):
    offset = (page - 1) * page_size
    sql = """SELECT id, username
             FROM users
             WHERE username LIKE ?
             ORDER BY username
             LIMIT ? OFFSET ?"""
    like = "%" + query + "%"
    return db.query(sql, [like, page_size, offset])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]

    if check_password_hash(password_hash, password):
        return user_id
    return None

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None

def remove_image(user_id):
    sql = "UPDATE users SET image = NULL WHERE id = ?"
    db.execute(sql, [user_id])

def remove_user(user_id):
    sql = "DELETE FROM comments WHERE user_id = ?"
    db.execute(sql, [user_id])
    sql = "DELETE FROM likes WHERE user_id = ?"
    db.execute(sql, [user_id])
    sql = "DELETE FROM users WHERE id = ?"
    db.execute(sql, [user_id])
