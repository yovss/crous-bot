import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers (
    chat_id INTEGER PRIMARY KEY
)
""")
conn.commit()


def add_subscriber(chat_id):
    cursor.execute(
        "INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)",
        (chat_id,)
    )
    conn.commit()


def remove_subscriber(chat_id):
    cursor.execute(
        "DELETE FROM subscribers WHERE chat_id = ?",
        (chat_id,)
    )
    conn.commit()


def get_subscribers():
    cursor.execute("SELECT chat_id FROM subscribers")
    return [row[0] for row in cursor.fetchall()]