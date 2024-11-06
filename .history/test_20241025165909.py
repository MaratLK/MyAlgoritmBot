import ccxt

# Инициализация бирж
bybit = ccxt.bybit()
binance = ccxt.binance()

# Получение всех пар для Bybit
def get_bybit_symbols():
    markets = bybit.load_markets()
    return list(markets.keys())  # Список всех доступных торговых пар

# Получение цены пары для Bybit
def get_bybit_price(symbol):
    ticker = bybit.fetch_ticker(symbol)
    return ticker['last']  # Последняя цена

# Получение всех пар для Binance
def get_binance_symbols():
    markets = binance.load_markets()
    return list(markets.keys())

# Получение цены пары для Binance
def get_binance_price(symbol):
    ticker = binance.fetch_ticker(symbol)
    return ticker['last']

# Пример использования
print("Bybit Pairs:", get_bybit_symbols()[:5])  # Первые 5 пар для Bybit
print("Binance Pairs:", get_binance_symbols()[:5])  # Первые 5 пар для Binance
print("Bybit BTC/USDT Price:", get_bybit_price('BTC/USDT'))
print("Binance BTC/USDT Price:", get_binance_price('BTC/USDT'))
