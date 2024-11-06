import requests

response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
print(response.json())
