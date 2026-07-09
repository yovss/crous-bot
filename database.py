import sqlite3

DB_NAME = "database.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

# Subscribers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers (
    chat_id INTEGER PRIMARY KEY
)
""")

# Seen rooms table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    room_id TEXT PRIMARY KEY
)
""")

conn.commit()


# --------------------
# Subscribers
# --------------------

def add_subscriber(chat_id):
    cursor.execute(
        "INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)",
        (chat_id,)
    )
    conn.commit()


def remove_subscriber(chat_id):
    cursor.execute(
        "DELETE FROM subscribers WHERE chat_id=?",
        (chat_id,)
    )
    conn.commit()


def get_subscribers():
    cursor.execute("SELECT chat_id FROM subscribers")
    return [row[0] for row in cursor.fetchall()]


# --------------------
# Rooms
# --------------------

def room_exists(room_id):
    cursor.execute(
        "SELECT 1 FROM rooms WHERE room_id=?",
        (room_id,)
    )
    return cursor.fetchone() is not None


def add_room(room_id):
    cursor.execute(
        "INSERT OR IGNORE INTO rooms (room_id) VALUES (?)",
        (room_id,)
    )
    conn.commit()