import requests

SYMBOL = "1357.T"

url = f"https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}"
params = {
    "interval": "1d",
    "range": "5d"
}

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; stock-bot/1.0)"
}

res = requests.get(url, params=params, headers=headers)

# デバッグ用（失敗時に原因が分かる）
print("HTTP status:", res.status_code)
print("Raw text (first 200 chars):", res.text[:200])

data = res.json()

try:
    result = data["chart"]["result"][0]
    indicators = result["indicators"]["quote"][0]

    close_price = indicators["close"][-1]

    print("=== 株価取得結果 ===")
    print(f"銘柄: {SYMBOL}")
    print(f"終値: {close_price}")

except Exception:
    print("❌ 株価データが取得できません")
    print("Raw response:", data)
    raise


import smtplib
from email.mime.text import MIMEText
import os

SMTP_SERVER = os.getenv("MAIL_HOST")
SMTP_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS")
MAIL_TO = os.getenv("MAIL_TO")

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = MAIL_USER
msg["To"] = MAIL_TO

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(MAIL_USER, MAIL_PASS)
    server.send_message(msg)

print("📧 メール送信完了")
