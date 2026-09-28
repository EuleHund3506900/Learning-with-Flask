import sqlite3

import bcrypt

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
    user = result[0]

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
        return result[0]

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
