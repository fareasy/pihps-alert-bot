import sqlite3

DB_NAME = "pihps.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        commodity TEXT,
        province TEXT,
        price REAL
    )
    """)

    conn.commit()
    conn.close()

def save_prices(date, commodity, data):
    conn = get_conn()
    cursor = conn.cursor()

    for row in data:
        cursor.execute("""
        INSERT OR IGNORE INTO prices (date, commodity, province, price)
        VALUES (?, ?, ?, ?)
        """, (
            date,
            commodity,
            row["Provinsi"],
            row["Nilai"]
        ))

        if cursor.rowcount > 0:
            print("Inserted:", date, commodity,  row["Provinsi"])
        else:
            print("Skipped duplicate:", date, commodity,  row["Provinsi"])

    conn.commit()
    conn.close()