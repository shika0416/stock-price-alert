import requests

def get_stock_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=1357.T"
    data = requests.get(url).json()
    price = data["quoteResponse"]["result"][0]["regularMarketPrice"]
    return price

if __name__ == "__main__":
    price = get_stock_price()
    print(f"日経ダブルインバ現在値: {price}円")
