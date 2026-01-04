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
    f"&interval=5min"
    f"&apikey={API_KEY}"
)

res = requests.get(url)
print("HTTP status:", res.status_code)

data = res.json()

# API制限チェック
if "Note" in data:
    print("❌ API制限に達しました")
    print(data["Note"])
    sys.exit(1)

series = data.get("Time Series (5min)")

if not series:
    print("❌ 株価データが取得できません")
    print("Raw response:", data)
    sys.exit(1)

latest_time = sorted(series.keys())[0]
price = series[latest_time]["4. close"]

print(f"✅ {SYMBOL} 最新株価:", price)
