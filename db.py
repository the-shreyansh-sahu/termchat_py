import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="termchat-termchat.d.aivencloud.com",
        user="shreyanshsahu",
        password="AVNS_QfV4jS-v9NElK1mqXc-",
        database="chatapp",
        port=26232
    )

def register_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return True
    except mysql.connector.Error:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None

def save_message(sender, receiver, message):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO messages (sender, receiver, message) VALUES (%s, %s, %s)", (sender, receiver, message))
        conn.commit()
        return True
    except mysql.connector.Error:
        return False
    finally:
        conn.close()

def get_messages(user1, user2, last_id=0):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM messages WHERE ((sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s)) AND id > %s ORDER BY id",
        (user1, user2, user2, user1, last_id)
    )
    msgs = cur.fetchall()
    conn.close()
    return msgs
