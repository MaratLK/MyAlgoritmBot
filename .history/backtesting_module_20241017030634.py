import csv
import time
import requests

API_KEY = '43SGGtUXH5HMWI5HV2'
API_SECRET = 'w98kSFBGxKE5aF8hkC3wNEqhafOsCboRt5cb'


# Функция для получения цены для конкретной пары (символа)
def get_symbol_price(symbol):
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {
        'category': 'spot',  # Указываем категорию
        'symbol': symbol
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'result' in data and len(data['result']) > 0:  # Проверяем, есть ли результат
            if 'lastPrice' in data['result'][0]:  # Проверяем наличие ключа 'lastPrice'
                return {'price': data['result'][0]['lastPrice']}
            else:
                print(f"Ключ 'lastPrice' отсутствует в данных для {symbol}")
                return None
        else:
            print(f'Нет данных для {symbol}')
            return None
    elif response.status_code == 429:
        print(f'Превышен лимит запросов для {symbol}. Ждем 10 секунд...')
        time.sleep(10)
        return get_symbol_price(symbol)
    else:
        print(f'Ошибка при получении данных для {symbol}: {response.status_code}')
        return None


# Список популярных торговых пар
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'SOLUSDT', 'ADAUSDT', 'DOGEUSDT', 'MATICUSDT', 'DOTUSDT', 'LTCUSDT']

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
            time.sleep(10)  # Пауза в 1 секунду между запросами

# Вызов функции для сохранения символов и их цен
save_symbols_to_csv(symbols)