import sqlite3

DB_NAME = "pihps.db"


def get_all_provinces():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT province
        FROM prices
        ORDER BY province
    """)

    rows = cur.fetchall()

    conn.close()

    return [row[0] for row in rows]