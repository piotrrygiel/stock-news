import requests
import os
import smtplib
# import datetime
from dotenv import load_dotenv

load_dotenv("E:/EnvironmentVariables/.env.txt")

api_key_stock = os.environ["API_KEY_ALPHAVANTAGE"]
api_key_news = os.environ["API_KEY_NEWSAPI"]
MY_EMAIL = "rygielpiotr18@gmail.com"
MY_PASSWORD = os.environ["EMAIL_PASS"]
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


def get_news():
    # today = datetime.date.today()
    # yesterday = today - datetime.timedelta(days=1)
    yesterday = data_stock["Global Quote"]["07. latest trading day"]
    # url_news = f"https://newsapi.org/v2/top-headlines?q=tesla&apiKey={api_key_news}"
    url_news = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={yesterday}" \
               f"&sortBy=popularity&apiKey={api_key_news}"
    r_news = requests.get(url=url_news)
    data_news = r_news.json()
    return data_news["articles"][:3]


def send_notification():
    with smtplib.SMTP(host="smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:TSLA: {round(price_dif)}%\n\nHeadline:"
                                f"{data_news_top3[0]['title'].encode('utf-8')}\n"
                                f"Brief:{data_news_top3[0]['description'].encode('utf-8')}\n\n"
                                f"Headline:{data_news_top3[1]['title'].encode('utf-8')}\n"
                                f"Brief:{data_news_top3[1]['description'].encode('utf-8')}\n\n"
                                f"Headline:{data_news_top3[2]['title'].encode('utf-8')}\n"
                                f"Brief:{data_news_top3[2]['description'].encode('utf-8')}\n")


url_stock = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={STOCK}&apikey={api_key_stock}"
r_stock = requests.get(url=url_stock)
data_stock = r_stock.json()

price_dif = float(data_stock["Global Quote"]["10. change percent"][:-1])

if price_dif >= 5 or price_dif <= -5:
    data_news_top3 = get_news()
    send_notification()
