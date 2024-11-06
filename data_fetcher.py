import ccxt
import pandas as pd

class DataFetcher:
    def __init__(self):
        self.exchanges = {
            "Binance": ccxt.binance({'rateLimit': True}),
            "Bybit": ccxt.bybit({'rateLimit': True}),
        }

    def get_symbols(self, exchange_name):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            try:
                markets = exchange.load_markets()  #2 Загружаем все доступные рынки с биржи
                return list(markets.keys())
            except Exception as e:
                print(f"Ошибка при загрузке рынков с биржи {exchange_name}: {e}")
                return []
        return []

    def fetch_data(self, exchange_name, symbol, timeframe='1d'):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=3000)  #3 Получаем данные OHLCV с увеличенным лимитом
                data = pd.DataFrame(
                    ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
                )
                data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')  #4 Преобразование временной метки в читаемый формат даты
                data.set_index('timestamp', inplace=True)  #5 Устанавливаем временную метку в качестве индекса
                return data
            except Exception as e:
                print(f"Ошибка при получении данных с биржи {exchange_name}: {e}")
        return None
