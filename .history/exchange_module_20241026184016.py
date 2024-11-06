# exchange_module.py
import ccxt

# Получаем список всех поддерживаемых бирж
EXCHANGE_OPTIONS = {
    'Binance': 'binance',
    'Bybit': 'bybit',
    'OKX': 'okx'
}

def get_exchange_pairs(exchange_name):
    """
    Получает список пар с указанной биржи.
    """
    exchange_id = EXCHANGE_OPTIONS.get(exchange_name)
    if exchange_id is None:
        return []

    exchange = getattr(ccxt, exchange_id)()
    try:
        markets = exchange.load_markets()
        return list(markets.keys())  # Возвращаем пары в виде списка
    except Exception as e:
        print(f"Ошибка при загрузке пар с биржи {exchange_name}: {e}")
        return []
