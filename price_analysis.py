import sqlite3

DB_NAME = "pihps.db"


def get_latest_two_dates():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT date
        FROM prices
        ORDER BY date DESC
        LIMIT 2
    """)

    rows = cur.fetchall()

    conn.close()

    return [row[0] for row in rows]


def get_price_changes(province):

    dates = get_latest_two_dates()

    if len(dates) < 2:
        return []

    latest_date = dates[0]
    previous_date = dates[1]

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p1.commodity,
            p1.price,
            p2.price
        FROM prices p1
        JOIN prices p2
            ON p1.commodity = p2.commodity
            AND p1.province = p2.province
        WHERE p1.date = ?
            AND p2.date = ?
            AND p1.province = ?
    """, (latest_date, previous_date, province))

    rows = cur.fetchall()

    conn.close()

    results = []

    for commodity, latest_price, previous_price in rows:

        if previous_price == 0:
            continue

        percent_change = (
            (latest_price - previous_price)
            / previous_price
        ) * 100

        results.append({
            "commodity": commodity,
            "latest_price": latest_price,
            "previous_price": previous_price,
            "percent_change": round(percent_change,1),
            "latest_date": latest_date
        })

    return results

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