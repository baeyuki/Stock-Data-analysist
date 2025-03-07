import requests
import json
from datetime import datetime

API_BEARER_TOKEN = "your_bearer_token_here"  # Thay bằng token thật

BASE_URL = "https://restv2.fireant.vn/symbols"

def get_stock_data(ticker, start_date, end_date):
    """
    Truy xuất dữ liệu chứng khoán từ FireAnt API.
    """
    url = f"{BASE_URL}/{ticker}/historical-quotes?startDate={start_date}&endDate={end_date}&offset=0&limit=1000"
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        stock_list = []
        for item in data:
            stock_list.append({
                "ticker": ticker,
                "date": datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y%m%d"),
                "open": item.get("priceOpen", 0),
                "high": item.get("priceHigh", 0),
                "low": item.get("priceLow", 0),
                "close": item.get("priceClose", 0),
                "volume": item.get("totalVolume", 0)
            })
        return stock_list

    except requests.exceptions.RequestException as e:
        print(f" Lỗi khi truy xuất dữ liệu: {e}")
        return []
