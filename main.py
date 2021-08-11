import os
import requests
import pprint

ALPHA_VANTAGE_WEB = "https://www.alphavantage.co/query"
ALPHA_API = os.environ.get("ALPHA_API")

NEWSAPI_WEB = "https://newsapi.org/v2/everything"
NEWS_API = os.environ.get("NEWS_API")

alpha_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "ETH",
    "market": "USD",
    "interval": "5min",
    "apikey": ALPHA_API,
}

response = requests.get(ALPHA_VANTAGE_WEB, params=alpha_params)
response.raise_for_status()

pp = pprint.PrettyPrinter(indent=4)
crypto_data = response.json()
pp.pprint(crypto_data)
