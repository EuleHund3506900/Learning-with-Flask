import sqlite3

import bcrypt

import logging
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    with open('database/schema.sql', 'r') as f:
        script = f.read()
        cursor.executescript(script)
    conn.commit()
    conn.close()

def create_user(name, password, email):

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user ( name, password, email) VALUES ( ?, ?, ?)", ( name, hashed_password, email))
    except sqlite3.IntegrityError as e:
        print(f"Error creating user: {e}")
        return "error"

    cursor.execute("SELECT id, name, email FROM user WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result is None:
        return "error"
    user = result

    logger.info(f"User {user[0]} created successfully.")

    conn.commit()
    conn.close()
    return user

def verify_user(email, password):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM user WHERE email = ?", (email,))
    result = cursor.fetchone()

    if result is None:
        return False

    stored_password = result[0].encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        cursor.execute("SELECT id, name, email FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result is None:
            return False
        conn.close()
        logger.info(f"User {str(result[0])} verified successfully.")
        return result

    conn.close()
    return (False)

def get_user_by_id(user_id):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM user WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return None

    return {
        "id": result[0],
        "name": result[1],
        "email": result[2],
    }

def get_favorites_by_user(user_id):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_url FROM favorite WHERE user_id = ? ORDER BY id", (user_id,))
    favorites = cursor.fetchall()
    conn.close()

    return [{"id": favorite[0], "item_url": favorite[1]} for favorite in favorites]

def create_favorite(user_id, item_url):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, item_url FROM favorite WHERE user_id = ? AND item_url = ?",
        (user_id, item_url),
    )
    existing_favorite = cursor.fetchone()

    if existing_favorite is not None:
        conn.close()
        return {"id": existing_favorite[0], "item_url": existing_favorite[1]}, False

    cursor.execute(
        "INSERT INTO favorite (user_id, item_url) VALUES (?, ?)",
        (user_id, item_url),
    )
    favorite_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": favorite_id, "item_url": item_url}, True

def delete_favorite(user_id, item_url):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favorite WHERE user_id = ? AND item_url = ?",
        (user_id, item_url),
    )
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_completed_by_user(user_id):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_url FROM completed WHERE user_id = ? ORDER BY id", (user_id,))
    completed = cursor.fetchall()
    conn.close()

    return [{"id": item[0], "item_url": item[1]} for item in completed]

def create_completed(user_id, item_url):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, item_url FROM completed WHERE user_id = ? AND item_url = ?",
        (user_id, item_url),
    )
    existing_item = cursor.fetchone()

    if existing_item is not None:
        conn.close()
        return {"id": existing_item[0], "item_url": existing_item[1]}, False

    cursor.execute(
        "INSERT INTO completed (user_id, item_url) VALUES (?, ?)",
        (user_id, item_url),
    )
    completed_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": completed_id, "item_url": item_url}, True

def delete_completed(user_id, item_url):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM completed WHERE user_id = ? AND item_url = ?",
        (user_id, item_url),
    )
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_user_completed_lessons_count(user_id):
    conn = sqlite3.connect('database/development.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM completed WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return 0

    return result[0]