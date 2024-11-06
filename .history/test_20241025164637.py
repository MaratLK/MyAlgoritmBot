import requests

# Binance: Получение всех пар
def get_binance_symbols():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        symbols = [item['symbol'] for item in data['symbols']]
        return symbols
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return []

# Binance: Получение текущей цены пары
def get_binance_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['price']
    else:
        print(f"Ошибка при получении цены для {symbol}: {response.status_code}")
        return None

# Пример использования
symbols_binance = get_binance_symbols()
for symbol in symbols_binance[:5]:  # Ограничимся первыми 5 парами для теста
    price = get_binance_price(symbol)
    print(f"{symbol}: {price}")
