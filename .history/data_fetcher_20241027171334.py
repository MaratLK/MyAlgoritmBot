import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QCheckBox, QToolBar, QAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ccxt
import pandas as pd
import plotly.graph_objects as go

class DataFetcher:
    def __init__(self):
        self.exchanges = {
            "Binance": ccxt.binance(),
            "Bybit": ccxt.bybit()
        }

    def get_symbols(self, exchange_name):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            markets = exchange.load_markets()  #2 Загружаем все доступные рынки с биржи
            return list(markets.keys())
        return []

    def fetch_data(self, exchange_name, symbol, timeframe='1d'):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=3000)  #3 Получаем данные OHLCV (Open, High, Low, Close, Volume) с увеличенным лимитом
            data = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')  #4 Преобразование временной метки в читаемый формат даты
            data.set_index('timestamp', inplace=True)  #5 Устанавливаем временную метку в качестве индекса
            return data
        return None