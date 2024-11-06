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
