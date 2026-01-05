import os
import requests

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
SYMBOL = "1357.T"   # 日経225ダブルインバースETF

if not API_KEY:
    print("❌ 環境変数 ALPHAVANTAGE_API_KEY が設定されていません")
    exit(1)

url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": SYMBOL,
    "apikey": API_KEY
}

response = requests.get(url, params=params)
print("HTTP status:", response.status_code)

data = response.json()

# エラー対策
if "Time Series (Daily)" not in data:
    print("❌ 株価データが取得できません")
    print("Raw response:", data)
    exit(1)

time_series = data["Time Series (Daily)"]

# 最新日付を取得
latest_date = sorted(time_series.keys(), reverse=True)[0]

latest = time_series[latest_date]
open_price = latest["1. open"]
high_price = latest["2. high"]
low_price = latest["3. low"]
close_price = latest["4. close"]
volume = latest["5. volume"]

print("\n=== 株価取得結果 ===")
print(f"銘柄: {SYMBOL}")
print(f"日付: {latest_date}")
print(f"始値: {open_price}")
print(f"高値: {high_price}")
print(f"安値: {low_price}")
print(f"終値: {close_price}")
print(f"出来高: {volume}")
