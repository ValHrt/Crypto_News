import os
import requests

COINMARKET_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
COINMARKET_API = os.environ.get("COINMARKET_API")

NEWSAPI_WEB = "https://newsapi.org/v2/everything"
NEWS_API = os.environ.get("NEWS_API")

parameters = {
    "slug": "bitcoin,ethereum,ripple",
    "convert": "EUR",
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINMARKET_API,
}

response = requests.get(COINMARKET_URL, params=parameters, headers=headers)
response.raise_for_status()

crypto_data = response.json()['data']

final_data = {}

for key in crypto_data.keys():
    value = crypto_data[key]["quote"]["EUR"]
    coin = crypto_data[key]["name"]
    final_data[coin] = value

print(final_data)
