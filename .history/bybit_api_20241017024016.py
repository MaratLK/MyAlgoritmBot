import csv
import time
import requests

API_KEY = '43SGGtUXH5HMWI5HV2'
API_SECRET = 'w98kSFBGxKE5aF8hkC3wNEqhafOsCboRt5cb'

# Функция для получения всех торговых пар с Bybit
def get_all_bybit_symbols():
    url = 'https://api.bybit.com/v2/public/symbols'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        symbols = [item['name'] for item in data['result']]
        return symbols
    else:
        print(f'Ошибка: {response.status_code}')
        return []

# Функция для получения цены для конкретной пары (символа)
def get_symbol_price(symbol):
    url = f'https://api.bybit.com/v2/public/tickers?symbol={symbol}'
    headers = {
        'X-BYBIT-API-KEY': API_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        remaining_requests = response.headers.get('X-RateLimit-Remaining')
        if remaining_requests and int(remaining_requests) < 10:
            print(f'Осталось мало запросов ({remaining_requests}). Ждем 60 секунд.')
            time.sleep(60)  # Ждем 60 секунд перед следующими запросами
        if data['result']:
            return {'price': data['result'][0]['last_price']}
    else:
        print(f'Ошибка при получении данных для {symbol}: {response.status_code}')
        return None

# Функция для сохранения символов и их цен в CSV
def save_symbols_to_csv(symbols):
    with open('bybit_symbols.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['symbol', 'price'])  # Заголовки

        for symbol in symbols:
            price_data = get_symbol_price(symbol)
            if price_data:
                writer.writerow([symbol, price_data['price']])
            else:
                writer.writerow([symbol, 'N/A'])
            time.sleep(5)  # Пауза в полсекунды между запросами
