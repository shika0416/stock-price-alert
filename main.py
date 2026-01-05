import requests

SYMBOL = "1357.T"

url = f"https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}"
params = {
    "interval": "1d",
    "range": "5d"
}

res = requests.get(url, params=params)
data = res.json()

try:
    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    indicators = result["indicators"]["quote"][0]

    latest_index = -1
    close_price = indicators["close"][latest_index]

    print("=== 株価取得結果 ===")
    print(f"銘柄: {SYMBOL}")
    print(f"終値: {close_price}")

except Exception as e:
    print("❌ 株価取得に失敗")
    print(data)
    raise e
