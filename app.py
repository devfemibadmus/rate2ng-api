from bs4 import BeautifulSoup
import requests, time, uvicorn
from fastapi import FastAPI, BackgroundTasks
from concurrent.futures import ThreadPoolExecutor
import threading

app = FastAPI()
stop_flag = threading.Event()
executor = ThreadPoolExecutor(max_workers=10)

host = 'http://127.0.0.1:8000'
headers = {
    'api-key': 'uhmmmmmmmm',
}
KEYS = {
    "keys": [
        "CURRENCIES",
        "CRYPTOCURRENCIES"
    ]
}
RATES2NGN = {}
CURRENCIES = {
    "USD-NGN": {
        "abbr": "USD",
        "name": "United States Dollar",
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
        "abbr": "GBP",
        "name": "British Pound Sterling",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/GBP-NGN",
    },
    "EUR-NGN": {
        "abbr": "EUR",
        "name": "Euro",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/EUR-NGN",
    },
    "AUD-NGN": {
        "abbr": "AUD",
        "name": "Australian Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/AUD-NGN",
    },
    "CHF-NGN": {
        "abbr": "CHF",
        "name": "Swiss Franc",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CHF-NGN",
    },
    "NZD-NGN": {
        "abbr": "NZD",
        "name": "New Zealand Dollar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/NZD-NGN",
    },
    "CNH-NGN": {
        "abbr": "CNH",
        "name": "Chinese Yuan (Offshore)",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/CNH-NGN",
    },
    "SEK-NGN": {
        "abbr": "SEK",
        "name": "Swedish Krona",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/SEK-NGN",
    },
    "JPY-NGN": {
        "abbr": "JPY",
        "name": "Japanese Yen",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://www.google.com/finance/quote/JPY-NGN",
    },
}
CRYPTOCURRENCIES = {
    "BTC-USD": {
        "abbr": "BTC",
        "name": "Bitcoin",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/BTC-USD/",
    },
    "ETH-USD": {
        "abbr": "ETH",
        "name": "Ethereum",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/ETH-USD/",
    },
    "USDT-USD": {
        "abbr": "USDT",
        "name": "Tether",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/USDT-USD/",
    },
    "BNB-USD": {
        "abbr": "BNB",
        "name": "Binance Coin",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/BNB-USD/",
    },
    "XRP-USD": {
        "abbr": "XRP",
        "name": "XRP",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/XRP-USD/",
    },
    "USDC-USD": {
        "abbr": "USDC",
        "name": "USD Coin",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/USDC-USD/",
    },
    "ADA-USD": {
        "abbr": "ADA",
        "name": "Cardano",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/ADA-USD/",
    },
    "DOGE-USD": {
        "abbr": "DOGE",
        "name": "Dogecoin",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/DOGE-USD/",
    },
    "SOL-USD": {
        "abbr": "SOL",
        "name": "Solana",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/SOL-USD/",
    },
    "TRX-USD": {
        "abbr": "TRX",
        "name": "TRON",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/TRX-USD/",
    },
    "DOT-USD": {
        "abbr": "DOT",
        "name": "Polkadot",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/DOT-USD/",
    },
    "MATIC-USD": {
        "abbr": "MATIC",
        "name": "Polygon",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/MATIC-USD/",
    },
    "LTC-USD": {
        "abbr": "LTC",
        "name": "Litecoin",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/LTC-USD/",
    },
    "SHIB-USD": {
        "abbr": "SHIB",
        "name": "Shiba Inu",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/SHIB-USD/",
    },
    "AVAX-USD": {
        "abbr": "AVAX",
        "name": "Avalanche",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/AVAX-USD/",
    },
    "WBTC-USD": {
        "abbr": "WBTC",
        "name": "Wrapped Bitcoin",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/WBTC-USD/",
    },
    "LINK-USD": {
        "abbr": "LINK",
        "name": "Chainlink",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/LINK-USD/",
    },
    "ATOM-USD": {
        "abbr": "ATOM",
        "name": "Cosmos",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/ATOM-USD/",
    },
    "XLM-USD": {
        "abbr": "XLM",
        "name": "Stellar",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/XLM-USD/",
    },
    "UNI-USD": {
        "abbr": "UNI",
        "name": "Uniswap",
        "cover": "https://static.com/placeholder/image",
        "preview": "https://finance.yahoo.com/quote/UNI-USD/",
    },
}

IS_PROCESSING = False

def get_google_finance_stock_data(ticker):
    print("HI")
    while not stop_flag.is_set():
        url = f"https://www.google.com/finance/quote/{ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find("div", class_="YMlKec fxKbKc").text
        about = soup.find("span", role="region").text
        previous_close = soup.find("div", class_="gyFHrc").find("div", class_="P6K39c").text
        CURRENCIES[ticker]["price"] = price
        CURRENCIES[ticker]["about"] = about
        CURRENCIES[ticker]["previous_close"] = previous_close
        time.sleep(5)

def update_rates2ngn():
    print("HIqqq")
    while not stop_flag.is_set():
        RATES2NGN["CURRENCIES"] = CURRENCIES
        RATES2NGN["CRYPTOCURRENCIES"] = CRYPTOCURRENCIES
        resp = requests.post(f'{host}/update/rate', headers=headers, json=RATES2NGN)
        print(resp.json())
        time.sleep(5)

@app.get("/keys")
def update_keys():
    resp = requests.post(f'{host}/update/keys', headers=headers, json=KEYS)
    return resp.json()

@app.get("/stop")
def stop_app():
    global IS_PROCESSING
    stop_flag.set()
    IS_PROCESSING = False
    executor.shutdown(wait=False)
    return {"message": "Background tasks stopped"}

@app.get("/")
def set_rates2ngn(background_tasks: BackgroundTasks):
    global IS_PROCESSING, executor, stop_flag
    stop_flag.clear()
    executor = ThreadPoolExecutor(max_workers=10) 
    if not IS_PROCESSING:
        for ticker in CURRENCIES.keys():
            executor.submit(get_google_finance_stock_data, ticker)
        background_tasks.add_task(update_rates2ngn)
        IS_PROCESSING = True
    return RATES2NGN

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

