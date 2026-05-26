from price_db import save_prices
from pihps_api import get_histogram_data
from datetime import datetime

def normalize_date(date_string):

    formats = [
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y",
        "%d/%m/%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")
        except:
            continue

    raise ValueError(f"Unknown date format: {date_string}")

COMMODITIES = {
    1: "beras",
    2: "daging ayam",
    3: "daging sapi",
    4: "telur ayam",
    5: "bawang merah",
    6: "bawang putih",
    7: "cabai merah",
    8: "cabai rawit",
    9: "minyak goreng",
    10: "gula pasir"
}

def fetch_and_store_all(tanggal):
    for commodity_id, commodity_name in COMMODITIES.items():

        print(f"Fetching {commodity_name}...")

        data = get_histogram_data(tanggal, commodity_id)

        if not data:
            print(f"No data for {commodity_name}")
            continue

        save_prices(
            date = normalize_date(tanggal),
            commodity=commodity_name,
            data=data
        )

        print(f"Saved {commodity_name} → {len(data)} rows")