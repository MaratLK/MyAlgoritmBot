import requests

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
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['result']:
            return {'price': data['result'][0]['last_price']}
    else:
        print(f'Ошибка при получении данных для {symbol}: {response.status_code}')
        return None
    
    import requests
