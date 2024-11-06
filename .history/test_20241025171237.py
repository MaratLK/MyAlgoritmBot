import ccxt
import csv

# Инициализация бирж
bybit = ccxt.bybit()
binance = ccxt.binance()

# Функция для получения пар и цен с Bybit
def get_bybit_data():
    markets = bybit.load_markets()
    data = []
    for symbol in markets:
        ticker = bybit.fetch_ticker(symbol)
        price = ticker['last']
        data.append([symbol, price])
    return data

# Функция для получения пар и цен с Binance
def get_binance_data():
    markets = binance.load_markets()
    data = []
    for symbol in markets:
        ticker = binance.fetch_ticker(symbol)
        price = ticker['last']
        data.append([symbol, price])
    return data

# Сохранение данных в CSV
def save_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Symbol', 'Price'])
        writer.writerows(data)

# Получаем данные и сохраняем их
bybit_data = get_bybit_data()
binance_data = get_binance_data()

save_to_csv(bybit_data, 'bybit_data.csv')
save_to_csv(binance_data, 'binance_data.csv')

print("Данные сохранены в файлы bybit_data.csv и binance_data.csv")
