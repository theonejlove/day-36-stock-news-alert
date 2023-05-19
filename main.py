import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_ID_STOCK = os.environ["API_ID_STOCK"]
API_ID_NEWS = os.environ["API_ID NEWS"]

daily_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": API_ID_STOCK,
}

news_params = {
    "q": COMPANY_NAME,
    "apiKey": API_ID_NEWS
}
account_sid = os.environ["account_sid"]
auth_token = os.environ["auth_token"]

response = requests.get(STOCK_ENDPOINT, params=daily_params)
data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
dby_closing_price = day_before_yesterday_data["4. close"]

closing_price_difference = float(yesterday_closing_price) - float(dby_closing_price)
up_down = None
if closing_price_difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

diff_percent = round(closing_price_difference / float(yesterday_closing_price) * 100)
print(diff_percent)

if abs(diff_percent) > 0.1:
    response_news = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response_news.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body= article,
            from= "YOUR TWILIO VIRTUAL NUMBER",
            to= "YOUR TWILIO VERIFIED REAL NUMBER"
            )