from bs4 import BeautifulSoup
import requests, time, threading, signal, json, websockets, asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

stop_flag = threading.Event()
async_stop_flag = asyncio.Event()

host = "127.0.0.1:8000"
api_key = "uhmmmmmmmmmmmmmmmmmmmm"
currencies = {
    "USD-NGN": {},
    "CAD-NGN": {},
    "GBP-NGN": {},
    "EUR-NGN": {},
    "AUD-NGN": {},
    "CHF-NGN": {},
    "NZD-NGN": {},
    "CNH-NGN": {},
    "SEK-NGN": {},
    "JPY-NGN": {},
}

def update_rates_from_google_finance(ticker):
    while not stop_flag.is_set():
        try:
            url = f"https://www.google.com/finance/quote/{ticker}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            price = soup.find("div", class_="YMlKec fxKbKc").text
            previous_close = soup.find("div", class_="gyFHrc").find("div", class_="P6K39c").text
            currencies[ticker]["price"] = {"current": price, "last24hrs": previous_close}
            print(f"Updated {ticker}: {price} (Last 24hrs: {previous_close})")
        except Exception as e:
            print(f"Error updating {ticker}: {e}")
        time.sleep(5)

async def update_rates():
    while not stop_flag.is_set() and not async_stop_flag.is_set():
        try:
            async with websockets.connect(f"ws://{host}/update/rates", extra_headers={"api_key": api_key}) as websocket:
                while not stop_flag.is_set() and not async_stop_flag.is_set():
                    await websocket.send(json.dumps(currencies))
                    print("Sent rates to WebSocket server")
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"WebSocket error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

async def start_tasks():
    for ticker in currencies.keys():
        executor.submit(update_rates_from_google_finance, ticker)
    asyncio.create_task(update_rates())
    print("Application Started!")

    while not stop_flag.is_set() and not async_stop_flag.is_set():
        await asyncio.sleep(1)

    print("Shutting down tasks...")
    executor.shutdown(wait=False)
    async_stop_flag.set()

def shutdown_signal_handler(signum, frame):
    stop_flag.set()
    async_stop_flag.set()
    print("Gracefully shutting down...")

signal.signal(signal.SIGINT, shutdown_signal_handler)

if __name__ == "__main__":
    try:
        asyncio.run(start_tasks())
    except KeyboardInterrupt:
        print("Shutting down...")