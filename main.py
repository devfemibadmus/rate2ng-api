import os, sys, uvicorn, time
from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_CREDENTIALS=True,
    allow_methods=["GET", "POST"],
)
PROCESSING = False
RATES2NGN = {}
CREDENTIALS = [
    "uhmmmmmmmm",
    "uhmmmmmmmmm",
]

def get_api_key(api_key: str = Header(...)):
    if api_key not in CREDENTIALS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


@app.post("/update/keys")
def update_kyes(valid_keys: dict):
    for key in list(RATES2NGN.keys()):
        if key not in valid_keys['keys']:
            del RATES2NGN[key]

@app.post("/update/rate")
def set_rates2ngn(data: dict, api_key: str = Depends(get_api_key)):
    if api_key in CREDENTIALS:
        for key, value in data.items():
            RATES2NGN[key] = value
    return RATES2NGN

@app.get("/{key}")
async def get_value(key: str):
    return RATES2NGN.get(key)

@app.get("/")
async def get_rates2ngn(key: str):
    return RATES2NGN

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
