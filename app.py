from bs4 import BeautifulSoup
import requests, time, uvicorn
from fastapi import FastAPI, BackgroundTasks

headers = {
    'api-key': 'uhmmmmmmmm',
}
RATES2NGN = {
    "a":"a"
}
CURRENCIES = {
    "USD-NGN": {
        "abbr": "USD",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/USD-NGN",
    },
    "CAD-NGN": {
        "abbr": "CAD",
        "name": "Canadian Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CAD-NGN",
    },
    "GBP-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/GBP-NGN",
    },
    "EUR-NGN": {
        "abbr": "EUR",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/EUR-NGN",
    },
    "AUD-NGN": {
        "abbr": "USD",
        "name": "Austrailian Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/AUD-NGN",
    },
    "CHF-NGN": {
        "abbr": "USD",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CHF-NGN",
    },
    "NZD-NGN": {
        "abbr": "USD",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/NZD-NGN",
    },
    "CNH-NGN": {
        "abbr": "USD",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CNH-NGN",
    },
    "SEK-NGN": {
        "abbr": "USD",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/SEK-NGN",
    },
    "JPY-NGN": {
        "abbr": "USD",
        "name": "United State Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/JPY-NGN",
    },
}
CRYPTOCURRENCIES = {
    "USD-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/USD-NGN",
    },
    "CAD-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CAD-NGN",
    },
    "GBP-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/GBP-NGN",
    },
    "EUR-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/EUR-NGN",
    },
    "AUD-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/AUD-NGN",
    },
    "CHF-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CHF-NGN",
    },
    "NZD-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/NZD-NGN",
    },
    "CNH-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CNH-NGN",
    },
    "SEK-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/SEK-NGN",
    },
    "JPY-NGN": {
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/JPY-NGN",
    },
}

def get_google_finance_stock_data(ticker):
    while True:
        url = f"https://www.google.com/finance/quote/{ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find("div", class_="YMlKec fxKbKc").text
        previous_close = soup.find("div", class_="gyFHrc").find("div", class_="P6K39c").text
        CURRENCIES[ticker]["price"] = price
        CURRENCIES[ticker]["previous_close"] = previous_close
        time.sleep(5)

def update_rates2ngn():
    while True:
        RATES2NGN["CURRENCIES"] = CURRENCIES
        RATES2NGN["CRYPTOCURRENCIES"] = CRYPTOCURRENCIES
        resp = requests.post('http://127.0.0.1:8000/update/rate', headers=headers, json=RATES2NGN)
        print(resp.json())
        time.sleep(5)

@app.get("/")
def set_rates2ngn(background_tasks: BackgroundTasks):
    for ticker in CURRENCIES.keys():
        background_tasks.add_task(get_google_finance_stock_data(ticker))
    return RATES2NGN

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

