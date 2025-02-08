from bs4 import BeautifulSoup
from fastapi import FastAPI, BackgroundTasks
import requests, time, uvicorn, asyncio, threading, signal, websockets, json

app = FastAPI()
stop_flag = threading.Event()

host = "http://127.0.0.1:8000"
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

async def update_rates_from_google_finance(ticker):
    while not stop_flag.is_set():
        url = f"https://www.google.com/finance/quote/{ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find("div", class_="YMlKec fxKbKc").text
        previous_close = soup.find("div", class_="gyFHrc").find("div", class_="P6K39c").text
        currencies[ticker]["price"] = {"current": price, "last24hrs": previous_close}
        await asyncio.sleep(5)

async def update_rates():
    while not stop_flag.is_set():
        async with websockets.connect(f"{host}/update/currencies", extra_headers={"api_key": api_key}) as websocket:
            await websocket.send(json.dumps(currencies))
        await asyncio.sleep(2)

@app.get("/")
def set_rates(background_tasks: BackgroundTasks):
    if not stop_flag.is_set():
        for ticker in currencies.keys():
            background_tasks.add_task(update_rates_from_google_finance, ticker)
        background_tasks.add_task(update_rates)
    return "started!"

def shutdown_signal_handler(signum, frame):
    stop_flag.set()
    print("Gracefully shutting down...")

signal.signal(signal.SIGINT, shutdown_signal_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

