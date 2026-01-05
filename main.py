import os
import requests
import sys

API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
SYMBOL = "AAPL"

if not API_KEY:
    print("❌ APIキーが設定されていません")
    sys.exit(1)

url = (
    "https://www.alphavantage.co/query"
    f"?function=TIME_SERIES_DAILY"
    f"&symbol={SYMBOL}"
    f"&apikey={API_KEY}"
)

res = requests.get(url)
print("HTTP status:", res.status_code)

data = res.json()

# API制限・エラー表示
if "Information" in data or "Note" in data:
    print("❌ APIエラー")
    print(data)
    sys.exit(1)

# ★ 正しい取り出し方
series = data["Time Series (Daily)"]

# 最新日付を取得
latest_date = max(series.keys())
latest = series[latest_date]
price = latest["4. close"]

print(f"✅ {SYMBOL} {latest_date} 終値:", price)

print("=== 株価取得結果 ===")
print(f"銘柄: AAPL")
print(f"日付: {latest_date}")
print(f"終値: {close_price}")
