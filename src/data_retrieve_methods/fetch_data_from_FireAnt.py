import requests
import os
import pandas as pd
from datetime import datetime

API_BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoyMDQxMTcyNDIwLCJuYmYiOjE3NDExNzI0MjAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsInJvbGVzIiwiZW1haWwiLCJhY2NvdW50cy1yZWFkIiwiYWNjb3VudHMtd3JpdGUiLCJvcmRlcnMtcmVhZCIsIm9yZGVycy13cml0ZSIsImNvbXBhbmllcy1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImZpbmFuY2UtcmVhZCIsInBvc3RzLXdyaXRlIiwicG9zdHMtcmVhZCIsInN5bWJvbHMtcmVhZCIsInVzZXItZGF0YS1yZWFkIiwidXNlci1kYXRhLXdyaXRlIiwidXNlcnMtcmVhZCIsInNlYXJjaCIsImFjYWRlbXktcmVhZCIsImFjYWRlbXktd3JpdGUiLCJibG9nLXJlYWQiLCJpbnZlc3RvcGVkaWEtcmVhZCJdLCJzdWIiOiI3ODY5YzE1ZS1kOTNlLTQ5ZGQtOWE5NC1iOTFmMDMyNjVhZmIiLCJhdXRoX3RpbWUiOjE3NDExNzI0MjAsImlkcCI6Ikdvb2dsZSIsIm5hbWUiOiJiZXN0eGFteGloaWV1QGdtYWlsLmNvbSIsInNlY3VyaXR5X3N0YW1wIjoiOGNlYmQwNDMtZTIyZi00N2Q0LThiMjAtN2RlZGNkMDJlY2M0IiwianRpIjoiOGY5MWMyMWQ0YWY4OGM3NGIzNGMxODVkZjQ2OTdiNjAiLCJhbXIiOlsiZXh0ZXJuYWwiXX0.vR1jAm3n1jaYcEiYgxKBgpVdM-IiclcuYMHNYO5eaS9jXOKPr-qtVnszQ-IjU6CUy65hz2aRXNHlOaRnD8z5kHJQuqgTS_2AxZwUD2hsnyqqtBtwluFt7BlZWEZH2FDgbRrg4h7qvmFI9iojFph8vWZr8NgGZed30T6lFGkAIzfEJeMraYIJabHK8Kmw-KX8C-kyYNHHDR0_CUrZ5BXoptlMJjv8XPLN3ROa8TFWIlU1e50S0V0fMxoc01jezLyWZXk0rn-x4fvnnCROMEeKY_TQr3cyfnyBiXLG7U_Qa9PnhqxoIrIU2L6fxcuaXvA-Cd5fWu24XO3H0dZqU6FK0A"
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

        save_to_csv(stock_list, ticker)
        return stock_list

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi truy xuất dữ liệu: {e}")
        return []
    
def save_to_csv(stock_data, stock_name):
    """Save stock data to CSV in the data/raw directory."""
    current_dir = os.getcwd()  # Get the current working directory (where the notebook is running)
    project_root = os.path.dirname(current_dir)  # Go up one level to the project root

    # Define the path to data/raw relative to the project root
    raw_data_path = os.path.join(project_root, "data", "raw")
    os.makedirs(raw_data_path, exist_ok=True)  # Ensure the directory exists
    
    # Define the file path for the CSV
    file_path = os.path.join(raw_data_path, f"{stock_name}_stock_data.csv")
    df = pd.DataFrame(stock_data) 
    df.to_csv(file_path, index=False, encoding='utf-8')

    print(f"Data for {stock_name} saved to {file_path}")



