import requests
import datetime
import os
import pandas as pd

def fetch_stock_data(stock_name):
    # Fetching data from Cafef with parameter stock_name from 28-07-2000
    url = f"https://msh-devappdata.cafef.vn/rest-api/api/v1/TradingViewsData?symbol={stock_name}&type=D1"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    data = response.json()
    
    if not data.get("succeeded") or not data["data"]["value"].get("status"):
        raise Exception("API response indicates failure.")
    
    stock_data = []
    for entry in data["data"]["value"]["dataInfor"]:
        stock_data.append({
            "ticket": entry["symbol"],
            "date": datetime.datetime.fromtimestamp(entry["time"]).strftime('%Y-%m-%d %H:%M:%S'),
            "open": entry["open"],
            "high": entry["high"],
            "low": entry["low"],
            "close": entry["close"],
            "volume": entry["volume"]
        })

    save_to_csv(stock_data, stock_name)    
    return stock_data

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


