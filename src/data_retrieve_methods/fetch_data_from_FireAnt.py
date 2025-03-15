import requests
import json
import os
import pandas as pd
from datetime import datetime

API_BEARER_TOKEN = "your_token_here"  # Thay bằng token của bạn
BASE_URL = "https://restv2.fireant.vn/symbols"

def get_stock_data(ticker, start_date, end_date):
    """
    Truy xuất dữ liệu chứng khoán từ FireAnt API.
    
    :param ticker: Mã chứng khoán (VD: "VNINDEX")
    :param start_date: Ngày bắt đầu (YYYY-MM-DD)
    :param end_date: Ngày kết thúc (YYYY-MM-DD)
    :return: Danh sách chứa dữ liệu chứng khoán dạng dict
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
        print(f"Lỗi khi truy xuất dữ liệu: {e}")
        return []

def save_to_csv(stock_data, ticker):
    """
    Lưu dữ liệu vào file CSV trong thư mục data/raw.
    
    :param stock_data: Dữ liệu chứng khoán dạng list
    :param ticker: Mã chứng khoán
    """
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/{ticker}.csv"
    df = pd.DataFrame(stock_data)
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"Data saved to {file_path}")

