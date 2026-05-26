import requests
import time

BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/Home/GetHistogramData"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.bi.go.id/hargapangan"
}

def get_histogram_data(tanggal: str, commodity: int = 1):
    params = {
        "tanggal": tanggal,
        "commodity": commodity,
        "priceType": 1,
        "isPasokan": 1,
        "jenis": 1,
        "periode": 1,
        "provId": 0,
        "_": int(time.time() * 1000)  # 🔥 IMPORTANT FIX
    }

    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()