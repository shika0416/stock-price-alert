import requests
import os
import smtplib
from email.mime.text import MIMEText

ALPHA_KEY = os.environ["ALPHAVANTAGE_API_KEY"]

FROM = os.environ["MAIL_FROM"]
TO = os.environ["MAIL_TO"]
MAIL_PASS = os.environ["MAIL_PASS"]

SYMBOL = "1357.T"

def get_stock_price():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": SYMBOL,
        "apikey": ALPHA_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["Global Quote"]["05. price"]

def send_mail(message):
    msg = MIMEText(message)
    msg["Subject"] = "株価通知"
    msg["From"] = FROM
    msg["To"] = TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(FROM, MAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    price = get_stock_price()
    send_mail(f"1357株価: {price} 円")
