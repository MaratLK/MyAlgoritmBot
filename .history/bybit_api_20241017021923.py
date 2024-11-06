import time
import requests

def get_symbol_price(symbol):
    url = f'https://api.bybit.com/v2/public/tickers?symbol={symbol}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['result']:
            return {'price': data['result'][0]['last_price']}
    else:
        print(f'Ошибка при получении данных для {symbol}: {response.status_code}')
        return None

# Добавляем задержку перед каждым запросом
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
