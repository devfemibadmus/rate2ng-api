import os, sys, uvicorn, time, websockets
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Header, HTTPException, WebSocket, Request

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)

rates = {
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
currencies = {
    "USD-NGN": {
      "abbr": "USD",
      "name": "United States Dollar",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/USD-NGN",
      "about": "The United States dollar is the official currency of the United States and several other countries. The Coinage Act of 1792 introduced the U.S. dollar at par with the Spanish silver dollar, divided it into 100 cents, and authorized the minting of coins denominated in dollars and cents. U.S. banknotes are issued in the form of Federal Reserve Notes, popularly called greenbacks due to their predominantly green color.\nThe U.S. dollar was originally defined under a bimetallic standard of 371.25 grains fine silver or, from 1834, 23.22 grains fine gold, or $20.67 per troy ounce. The Gold Standard Act of 1900 linked the dollar solely to gold. From 1934, its equivalence to gold was revised to $35 per troy ounce. In 1971 all links to gold were repealed. The U.S. dollar became an important international reserve currency after the First World War, and displaced the pound sterling as the world's primary reserve currency by the Bretton Woods Agreement towards the end of the Second World War. The dollar is the most widely used currency in international transactions, and a free-floating currency. Wikipedia"
    },
    "CAD-NGN": {
      "abbr": "CAD",
      "name": "Canadian Dollar",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/CAD-NGN",
      "about": "The Canadian dollar is the currency of Canada. It is abbreviated with the dollar sign $. There is no standard disambiguating form, but the abbreviations Can$, CA$ and C$ are frequently used for distinction from other dollar-denominated currencies. It is divided into 100 cents.\nOwing to the image of a common loon on its reverse, the dollar coin, and sometimes the unit of currency itself, may be referred to as the loonie by English-speaking Canadians and foreign exchange traders and analysts.\nAccounting for approximately two per cent of all global reserves, as of January 2024 the Canadian dollar is the fifth-most held reserve currency in the world, behind the US dollar, euro, yen, and sterling. The Canadian dollar is popular with central banks because of Canada's relative economic soundness, the Canadian government's strong sovereign position, and the stability of the country's legal and political systems. Wikipedia"
    },
    "GBP-NGN": {
      "abbr": "GBP",
      "name": "British Pound Sterling",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/GBP-NGN",
      "about": "Sterling is the currency of the United Kingdom and nine of its associated territories. The pound is the main unit of sterling, and the word pound is also used to refer to the British currency generally, often qualified in international contexts as the British pound or the pound sterling.\nSterling is the world's oldest currency in continuous use since its inception. In 2022, it was the fourth-most-traded currency in the foreign exchange market, after the United States dollar, the euro, and the Japanese yen. Together with those three currencies and the renminbi, it forms the basket of currencies that calculate the value of IMF special drawing rights. As of late 2022, sterling is also the fourth most-held reserve currency in global reserves.\nThe Bank of England is the central bank for sterling, issuing its own banknotes and regulating issuance of banknotes by private banks in Scotland and Northern Ireland. Sterling banknotes issued by other jurisdictions are not regulated by the Bank of England; their governments guarantee convertibility at par. Historically, sterling was also used to varying degrees by the colonies and territories of the British Empire. Wikipedia"
    },
    "EUR-NGN": {
      "abbr": "EUR",
      "name": "Euro",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/EUR-NGN",
      "about": "The euro is the official currency of 20 of the 27 member states of the European Union. This group of states is officially known as the euro area or, more commonly, the eurozone. The euro is divided into 100 euro cents.\nThe currency is also used officially by the institutions of the European Union, by four European microstates that are not EU members, the British Overseas Territory of Akrotiri and Dhekelia, as well as unilaterally by Montenegro and Kosovo. Outside Europe, a number of special territories of EU members also use the euro as their currency.\nThe euro is used by 350 million people in Europe and additionally, over 200 million people worldwide use currencies pegged to the euro. It is the second-largest reserve currency as well as the second-most traded currency in the world after the United States dollar. As of December 2019, with more than €1.3 trillion in circulation, the euro has one of the highest combined values of banknotes and coins in circulation in the world.\nThe name euro was officially adopted on 16 December 1995 in Madrid. Wikipedia"
    },
    "AUD-NGN": {
      "abbr": "AUD",
      "name": "Australian Dollar",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/AUD-NGN",
      "about": "The naira is the currency of Nigeria. One naira is divided into 100 kobo.\nThe Central Bank of Nigeria is the sole issuer of legal tender money throughout the Federal Republic of Nigeria. It controls the volume of money supplied in the economy in order to ensure monetary and price stability. The Currency Operations Department of the CBN is in charge of currency management, through the designs, procurement, distribution and supply, processing, reissue and disposal or disintegration of bank notes and coins.\nA major cash crunch occurred in February 2023 when the Nigerian government used a currency note changeover—delivering too few of the new notes into circulation—to attempt to force citizens to use a newly-created government-sponsored central bank digital currency. This led to extensive street protests. Wikipedia"
    },
    "CHF-NGN": {
      "abbr": "CHF",
      "name": "Swiss Franc",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/CHF-NGN",
      "about": "The naira is the currency of Nigeria. One naira is divided into 100 kobo.\nThe Central Bank of Nigeria is the sole issuer of legal tender money throughout the Federal Republic of Nigeria. It controls the volume of money supplied in the economy in order to ensure monetary and price stability. The Currency Operations Department of the CBN is in charge of currency management, through the designs, procurement, distribution and supply, processing, reissue and disposal or disintegration of bank notes and coins.\nA major cash crunch occurred in February 2023 when the Nigerian government used a currency note changeover—delivering too few of the new notes into circulation—to attempt to force citizens to use a newly-created government-sponsored central bank digital currency. This led to extensive street protests. Wikipedia"
    },
    "NZD-NGN": {
      "abbr": "NZD",
      "name": "New Zealand Dollar",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/NZD-NGN",
      "about": "The New Zealand dollar is the official currency and legal tender of New Zealand, the Cook Islands, Niue, the Ross Dependency, Tokelau, and a British territory, the Pitcairn Islands. Within New Zealand, it is almost always abbreviated with the dollar sign. The abbreviations \"$NZ\" or \"NZ$\" are used when necessary to distinguish it from other dollar-denominated currencies.\nThe New Zealand dollar was introduced in 1967. It is subdivided into 100 cents. Altogether it has five coins and five banknotes with the smallest being the 10-cent coin; smaller denominations have been discontinued due to inflation and production costs.\nIn the context of currency trading, the New Zealand dollar is sometimes informally called the \"Kiwi\" or \"Kiwi dollar\", since the flightless bird, the kiwi, is depicted on its one-dollar coin. It is the tenth most traded currency in the world, representing 2.1% of global foreign exchange market daily turnover in 2019. Wikipedia"
    },
    "CNH-NGN": {
      "abbr": "CNH",
      "name": "Chinese Yuan (Offshore)",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/CNH-NGN",
      "about": "The naira is the currency of Nigeria. One naira is divided into 100 kobo.\nThe Central Bank of Nigeria is the sole issuer of legal tender money throughout the Federal Republic of Nigeria. It controls the volume of money supplied in the economy in order to ensure monetary and price stability. The Currency Operations Department of the CBN is in charge of currency management, through the designs, procurement, distribution and supply, processing, reissue and disposal or disintegration of bank notes and coins.\nA major cash crunch occurred in February 2023 when the Nigerian government used a currency note changeover—delivering too few of the new notes into circulation—to attempt to force citizens to use a newly-created government-sponsored central bank digital currency. This led to extensive street protests. Wikipedia"
    },
    "SEK-NGN": {
      "abbr": "SEK",
      "name": "Swedish Krona",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/SEK-NGN",
      "about": "The krona is the currency of the Kingdom of Sweden. It is one of the currencies of the European Union. Both the ISO code \"SEK\" and currency sign \"kr\" are in common use for the krona; the former precedes or follows the value, the latter usually follows it but, especially in the past, it sometimes preceded the value. In English, the currency is sometimes referred to as the Swedish crown, as krona means \"crown\" in Swedish. The Swedish krona was the ninth-most traded currency in the world by value in April 2016.\nOne krona is subdivided into 100 öre. Coins as small as 1 öre were formerly in use, but the last coin smaller than 1 krona was discontinued in 2010. Goods can still be priced in öre, but all sums are rounded to the nearest krona when paying with cash. The word öre is ultimately derived from the Latin word for gold. Wikipedia"
    },
    "JPY-NGN": {
      "abbr": "JPY",
      "name": "Japanese Yen",
      "cover": "https://static.com/placeholder/image",
      "preview": "https://www.google.com/finance/quote/JPY-NGN",
      "about": "The yen is the official currency of Japan. It is the third-most traded currency in the foreign exchange market, after the United States dollar and the euro. It is also widely used as a third reserve currency after the US dollar and the euro.\nThe New Currency Act of 1871 introduced Japan's modern currency system, with the yen defined as 1.5 g of gold, or 24.26 g of silver, and divided decimally into 100 sen or 1,000 rin. The yen replaced the previous Tokugawa coinage as well as the various hansatsu paper currencies issued by feudal han. The Bank of Japan was founded in 1882 and given a monopoly on controlling the money supply.\nFollowing World War II, the yen lost much of its pre-war value. To stabilize the Japanese economy, the exchange rate of the yen was fixed at ¥360 per US$ as part of the Bretton Woods system. When that system was abandoned in 1971, the yen became undervalued and was allowed to float. The yen had appreciated to a peak of ¥271 per US$ in 1973, then underwent periods of depreciation and appreciation due to the 1973 oil crisis, arriving at a value of ¥227 per US$ by 1980. Wikipedia"
    }
}
app_credentials = [
    "uhmmmmmmmm",
    "uhmmmmmmmmm",
]
secrete_credential = "uhmmmmmmmmmmmmmmmmmmmm"


@app.websocket("/update/rates/")
async def websocket_set_rates(websocket: WebSocket):
    await websocket.accept()
    headers = websocket.headers
    api_key = headers.get("api_key")
    if api_key != secrete_credential:
        await websocket.close(code=1008)
        return
    while True:
        data = await websocket.receive_json()
        for key, value in data.items():
            rates[key] = value

@app.get("/rates")
@limiter.limit("1/minute")
def get_rates(api_key: str, request: Request):
    if api_key not in app_credentials:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return rates

@app.get("/")
@limiter.limit("1/minute")
async def get_currencies(request: Request):
    return currencies

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
