import requests_cache
import requests
import smtplib
import os

requests_cache.install_cache("stock_cache")

AV_API_KEY = os.getenv("AV_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# STEP 1: cene akcija
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": AV_API_KEY,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()

data_list = [value for (key, value) in stock_data["Time Series (Daily)"].items()]

yesterday_closing_price = float(data_list[0]["4. close"])
day_before_yesterday_closing_price = float(data_list[1]["4. close"])

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
percentage_difference = difference / yesterday_closing_price * 100


# STEP 2: vesti, samo ako je promena velika
if percentage_difference > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "searchIn": "title",
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()

    articles = news_data["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}.\nBrief: {article['description']}"
                          for article in three_articles]

    # STEP 3: jedan mejl sa sve tri vesti
    body = "\n\n".join(formatted_articles)
    subject = f"{STOCK_NAME}: {round(percentage_difference, 2)}%"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: {subject}\n\n{body}".encode("utf-8"),
        )