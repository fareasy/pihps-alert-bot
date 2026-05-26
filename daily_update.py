from fetch_pihps import fetch_and_store_all
from price_db import save_prices


def update_latest_prices():

    print("Fetching latest PIHPS data...")

    prices = fetch_and_store_all()

    print(f"Fetched {len(prices)} rows")

    save_prices(prices)

    print("Prices saved.")