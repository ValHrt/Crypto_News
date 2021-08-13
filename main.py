import os
import requests
import datetime as dt
import time
from telethon.sync import TelegramClient

COINMARKET_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
COINMARKET_API = os.environ.get("COINMARKET_API")

NEWSAPI_WEB = "https://newsapi.org/v2/everything"
NEWS_API = os.environ.get("NEWS_API")

CRYPTO_NAME = ["bitcoin", "ethereum", "ripple"]

CHAT_ID = int(os.environ.get("CHAT_ID"))
APP_TELEGRAM_API_ID = int(os.environ.get("APP_TELEGRAM_API_ID"))
APP_TELEGRAM_API_HASH = os.environ.get("APP_TELEGRAM_API_HASH")

today = (dt.datetime.today() - dt.timedelta(days=1)).strftime("%Y-%m-%d")

parameters = {
    "slug": ",".join(CRYPTO_NAME),
    "convert": "EUR",
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINMARKET_API,
}

# News data API configuration:

news_data = {}

for index, name in enumerate(CRYPTO_NAME):
    newsapi_params = {
        "qInTitle": CRYPTO_NAME[index],
        "from": today,
        "sortBy": "popularity",
        "pageSize": 1,
        "apiKey": NEWS_API,
    }

    response = requests.get(NEWSAPI_WEB, params=newsapi_params)
    response.raise_for_status()

    news_data[name] = response.json()["articles"][0]
    time.sleep(1)

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(news_data)

news_text = []

for key in news_data.keys():
    news_text.append(f'Titre : {news_data[key]["title"]}\nDescription : {news_data[key]["description"]}'
                     f'\nLien article : {news_data[key]["url"]}\nSource: '
                     f'{news_data[key]["source"]["name"]}\n\n')

# news_text = "".join(news_text)
# print(news_text)

# CoinMarketCap API configuration :

response = requests.get(COINMARKET_URL, params=parameters, headers=headers)
response.raise_for_status()

crypto_data = response.json()['data']

final_data = {}

for key in crypto_data.keys():
    value = crypto_data[key]["quote"]["EUR"]
    coin = crypto_data[key]["name"]
    final_data[coin] = value

data_text = []
emojis = ["🔺", "🔻"]


def get_emoji(key: str, target: str):
    if final_data[key][target] > 0:
        emoji = emojis[0]
    else:
        emoji = emojis[1]
    return emoji


# print(final_data)

for key in final_data.keys():
    data_text.append(f"<b>{key}</b> :\nPrix actuel : {round(final_data[key]['price'], ndigits=2)} €\nVariation sur 24h : "
                     f"{get_emoji(key, 'percent_change_24h')}{round(final_data[key]['percent_change_24h'], ndigits=2)}%"
                     f"\nVariation sur une semaine : {get_emoji(key, 'percent_change_7d')}"
                     f"{round(final_data[key]['percent_change_7d'], ndigits=2)}%\n")

data_text = sorted(data_text, key=str.lower)

# Telegram Bot configuration :

client = TelegramClient("Valby_Bot", APP_TELEGRAM_API_ID, APP_TELEGRAM_API_HASH)

for (data, news) in zip(data_text, news_text):
    tmp = f"{data}{news}"
    "".join(tmp)

    async def main():
        await client.send_message(CHAT_ID, tmp, parse_mode="HTML")

    with client:
        client.loop.run_until_complete(main())
    time.sleep(1)
