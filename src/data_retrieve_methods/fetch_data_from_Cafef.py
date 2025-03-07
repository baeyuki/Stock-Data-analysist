import requests
import datetime

def fetch_stock_data(stock_name):

    # Fetching data from Cafef with para stock_name from 28-07-2000

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
    
    return stock_data

# Example
if __name__ == "__main__":
    stock_name = "VCB"
    try:
        data = fetch_stock_data(stock_name)
        print(data)
    except Exception as e:
        print(f"Error: {e}")
