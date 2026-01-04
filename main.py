import requests

def get_stock_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=1357.T"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # HTTPエラー検出

    data = response.json()
    result = data["quoteResponse"]["result"]

    if not result:
        raise ValueError("株価データが取得できませんでした")

    return result[0]["regularMarketPrice"]

if __name__ == "__main__":
    price = get_stock_price()
    print(f"日経ダブルインバ現在値: {price}円")
