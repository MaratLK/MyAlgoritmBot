import csv
import time
from bybit_api import get_symbol_price
import requests

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
            time.sleep(0.5)  # Пауза в полсекунды между запросами