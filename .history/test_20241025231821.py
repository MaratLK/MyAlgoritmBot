import ccxt

# Инициализация бирж
bybit = ccxt.bybit()
binance = ccxt.binance()

# Функция для получения списка пар с Bybit
def get_bybit_symbols():
    markets = bybit.load_markets()
    return list(markets.keys())

# Функция для получения цен с Bybit
def get_bybit_prices(symbols):
    prices = {}
    for symbol in symbols:
        ticker = bybit.fetch_ticker(symbol)
        prices[symbol] = ticker['last']
    return prices

# Функция для получения списка пар с Binance
def get_binance_symbols():
    markets = binance.load_markets()
    return list(markets.keys())

# Функция для получения цен с Binance
def get_binance_prices(symbols):
    prices = {}
    for symbol in symbols:
        ticker = binance.fetch_ticker(symbol)
        prices[symbol] = ticker['last']
    return prices

# Тестирование функций
bybit_symbols = get_bybit_symbols()[:5]  # Получаем первые 5 пар
binance_symbols = get_binance_symbols()[:5]

print("Bybit Symbols:", bybit_symbols)
print("Binance Symbols:", binance_symbols)

bybit_prices = get_bybit_prices(bybit_symbols)
binance_prices = get_binance_prices(binance_symbols)

print("Bybit Prices:", bybit_prices)
print("Binance Prices:", binance_prices)
