import requests

# Bybit: Получение всех пар
def get_bybit_symbols():
    url = 'https://api.bybit.com/v2/public/symbols'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        symbols = [item['name'] for item in data['result']]
        return symbols
    else:
        print(f"Ошибка при получении данных: {response.status_code}")
        return []

# Bybit: Получение текущей цены пары
def get_bybit_price(symbol):
    url = f'https://api.bybit.com/v2/public/tickers?symbol={symbol}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['result']:
            return data['result'][0]['last_price']
    else:
        print(f"Ошибка при получении цены для {symbol}: {response.status_code}")
        return None

# Пример использования
symbols_bybit = get_bybit_symbols()
for symbol in symbols_bybit[:5]:  # Ограничимся первыми 5 парами для теста
    price = get_bybit_price(symbol)
    print(f"{symbol}: {price}")
