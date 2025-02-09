import requests

headers = {
    "api-key": "uhmmmmmmmm"
}

resp = requests.get('http://127.0.0.1:8000/rates', headers=headers)
print(resp.text)