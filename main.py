import requests
import os
import json

# ===== 環境変数 =====
ALPHA_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
LINE_TOKEN = os.environ.get("LINE_CHANNEL_TOKEN")
USER_ID = os.environ.get("LINE_USER_ID")

SYMBOL = "7203.T"  # トヨタ

# ===== 株価取得 =====
def get_stock_price():
    if not ALPHA_KEY:
        raise RuntimeError("ALPHAVANTAGE_API_KEY が設定されていません")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": SYMBOL,
        "apikey": ALPHA_KEY
    }

    r = requests.get(url, params=params, timeout=10)

    # ---- デバッグ用（Actionsログで必ず確認できる）----
    print("Alpha Vantage status:", r.status_code)
    print("Alpha Vantage response:", r.text[:500])
    # -----------------------------------------------

    r.raise_for_status()

    data = r.json()

    if "Global Quote" not in data or not data["Global Quote"]:
        raise RuntimeError("株価データが取得できません（API制限・キー不正の可能性）")

    return float(data["Global Quote"]["05. price"])


# ===== LINE送信 =====
def send_line_message(message):
    if not LINE_TOKEN or not USER_ID:
        raise RuntimeError("LINEの環境変数が設定されていません")

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    r = requests.post(url, headers=headers, data=json.dumps(body))
    print("LINE status:", r.status_code)
    print("LINE response:", r.text)
    r.raise_for_status()


# ===== メイン処理 =====
if __name__ == "__main__":
    try:
        price = get_stock_price()
        message = f"📈 トヨタ株価\n{price} 円"
        send_line_message(message)
        print("✅ 正常終了：LINEに通知しました")

    except Exception as e:
        # 失敗時も原因が分かるようにログに出す
        print("❌ エラー発生")
        print(str(e))
        raise
