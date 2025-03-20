import requests
import datetime

def get_VN30_company_names():
    # Get the list of companies in VN30
    TimeStamp = int(datetime.datetime.now().timestamp())

    url = f"https://www.hsx.vn/Modules/Listed/Web/StockIndex/1964531007?_search=false&nd={TimeStamp}&rows=2147483647&page=1&sidx=id&sord=desc"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    data = response.json()
    
    company_names = []
    for entry in data["rows"]:
        company_names.append(entry["cell"][2].replace(" ", ""))

    return sorted(set(company_names))
