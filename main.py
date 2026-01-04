import requests
import os
import sys
import json

SYMBOL = "1357.T"  # 日経ダブルインバース

# =========================
# 環境変数チェック
# =========================
ALPHA_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

if not ALPHA_KEY:
    print("❌ 環境変数 ALPHAVANTAGE_API_KEY が設定されていません")
    sys.exit(1)

print("✅ APIキー存在確認 OK")

# =========================
# 株価取得
# =========================
def get_stock_price():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": SYMBOL,
        "apikey": ALPHA_KEY
    }

    try:
        r = requests.get(url, params=params, timeout=10)
    except Exception as e:
        raise RuntimeError(f"HTTPリクエスト失敗: {e}")

    print("HTTP status:", r.status_code)
    print("Raw response:", r.text[:500])

    if r.status_code != 200:
        raise RuntimeError("APIが正常応答しませんでした")

    try:
        data = r.json()
    except json.JSONDecodeError:
        raise RuntimeError("JSONとして解析できません（API制限・キー不正の可能性）")

    if "Global Quote" not in data or not data["Global Quote"]:
        raise RuntimeError("株価データが空です（API制限の可能性）")

    price_str = data["Global Quote"].get("05. price")
    if not price_str:
        raise RuntimeError("価格フィールドが存在しません")

    return float(price_str)

# =========================
# メイン処理
# =========================
if __name__ == "__main__":
    try:
        price = get_stock_price()
        print(f"📈 {SYMBOL} 現在値: {price} 円")
        print("✅ 正常終了")

    except Exception as e:
        print("❌ エラー発生")
        print(str(e))
        sys.exit(1)


print("Current price:", price)
