import sqlite3

DB_NAME = "pihps.db"

def init_user_table():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id TEXT PRIMARY KEY,
            province TEXT,
            threshold REAL DEFAULT 5
        )
    """)

    conn.commit()
    conn.close()

def init_sent_alerts_table():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sent_alerts (
            chat_id TEXT,
            alert_date TEXT,
            commodity TEXT,
            PRIMARY KEY (chat_id, alert_date, commodity)
        )
    """)

    conn.commit()
    conn.close()

def save_user_preferences(chat_id, province, threshold=5):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO users (
        chat_id,
        province,
        threshold
    )
    VALUES (?, ?, ?)
    """, (chat_id, province, threshold))

    conn.commit()
    conn.close()


def get_user_preferences(chat_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT province, threshold
    FROM user_preferences
    WHERE chat_id = ?
    """, (chat_id,))

    row = cursor.fetchone()

    conn.close()

    return row

def get_all_users():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT chat_id
        FROM users
    """)

    rows = cur.fetchall()

    conn.close()

    return [row[0] for row in rows]

def alert_already_sent(chat_id, alert_date, commodity):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM sent_alerts
        WHERE chat_id = ?
        AND alert_date = ?
        AND commodity = ?
    """, (chat_id, alert_date, commodity))

    result = cur.fetchone()

    conn.close()

    return result is not None

def save_sent_alert(chat_id, alert_date, commodity):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO sent_alerts
        (chat_id, alert_date, commodity)
        VALUES (?, ?, ?)
    """, (chat_id, alert_date, commodity))

    conn.commit()
    conn.close()

init_user_table()
init_sent_alerts_table()