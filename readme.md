
# Rate2NG API

The Rate2NG API is a backend service designed to provide real-time currency exchange rates for various currencies against the Nigerian Naira (NGN). It serves as the data source for the [Rate2NG](https://github.com/devfemibadmus/rate2ng) application, enabling users to access up-to-date currency conversion information.

## Overview

The API consists of two main components:

1. **Local Updater (`app.py`)**: This script runs locally and periodically fetches currency exchange rates from Google Finance. It updates the API with the latest rates via a WebSocket connection.

2. **API Server (`main.py`)**: This is the FastAPI-based server that exposes endpoints for retrieving currency data. It also handles WebSocket connections for receiving updates from the local updater.

## Key Features

- **Real-Time Updates**: The local updater (`app.py`) continuously fetches and updates currency rates from Google Finance, ensuring the API always provides the latest data.
- **WebSocket Integration**: The API uses WebSocket to receive real-time updates from the local updater.
- **Rate Limiting**: The API includes rate limiting to prevent abuse and ensure fair usage.
- **Currency Information**: In addition to exchange rates, the API provides detailed information about each currency, including its abbreviation, name, and a brief description.

## How It Works

1. The local updater (`app.py`) fetches currency rates from Google Finance for predefined currency pairs (e.g., USD-NGN, EUR-NGN).
2. The fetched rates are sent to the API server (`main.py`) via a WebSocket connection.
3. The API server stores the updated rates and makes them available through its endpoints.
4. The Rate2NG app or other clients can query the API to retrieve the latest currency rates and information.

## Endpoints

- **GET `/rates`**: Retrieves the latest exchange rates. Requires an API key for authentication.
- **GET `/`**: Returns detailed information about all supported currencies.
- **WebSocket `/update/rates/`**: Used by the local updater to send real-time rate updates to the API server.

## Usage

To use the API, ensure the local updater (`app.py`) is running to keep the rates updated. The API server (`main.py`) can be started using Uvicorn:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

For more details, visit the [Rate2NG GitHub repository](https://github.com/devfemibadmus/rate2ng).