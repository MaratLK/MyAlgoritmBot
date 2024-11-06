import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ccxt
import pandas as pd
import plotly.graph_objects as go
import pyqtgraph as pg
import numpy as np

# --- Модуль для получения данных ---
class DataFetcher:
    def __init__(self):
        self.exchanges = {
            "Binance": ccxt.binance(),
            "Bybit": ccxt.bybit()
        }

    def get_symbols(self, exchange_name):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            markets = exchange.load_markets()
            return list(markets.keys())
        return []

    def fetch_data(self, exchange_name, symbol, timeframe='1d'):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=3000)
            data = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('timestamp', inplace=True)
            return data
        return None

# --- Основное окно ---
# --- Основное окно ---
class TradingViewLikeInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface - TradingView Style")
        self.setGeometry(300, 300, 1200, 800)
        self.data_fetcher = DataFetcher()
        
        # --- Виджеты интерфейса ---
        self.initUI()
    
    def initUI(self):
        # Панель управления
        control_layout = QHBoxLayout()
        
        # Биржа
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(self.data_fetcher.exchanges.keys())
        self.exchange_combo.currentIndexChanged.connect(self.update_pairs)
        control_layout.addWidget(QLabel("Выберите биржу:"))
        control_layout.addWidget(self.exchange_combo)
        
        # Валютная пара
        self.pair_combo = QComboBox()
        control_layout.addWidget(QLabel("Выберите валютную пару:"))
        control_layout.addWidget(self.pair_combo)
        
        # Таймфрейм
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])
        control_layout.addWidget(QLabel("Таймфрейм:"))
        control_layout.addWidget(self.timeframe_combo)
        
        # Кнопка "Построить график"
        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_chart)
        control_layout.addWidget(self.plot_button)

        # Интерфейс графика (PyQtGraph)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # Белый фон
        self.plot_widget.addLegend()  # Добавляем легенду
        
        # Основной макет
        layout = QVBoxLayout()
        layout.addLayout(control_layout)
        layout.addWidget(self.plot_widget)

        # Центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Загрузка пар для начальной биржи
        self.update_pairs()

    def update_pairs(self):
        exchange_name = self.exchange_combo.currentText()
        pairs = self.data_fetcher.get_symbols(exchange_name)
        self.pair_combo.clear()
        self.pair_combo.addItems(pairs)

    def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()
        symbol = self.pair_combo.currentText()
        timeframe = self.timeframe_combo.currentText()

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)
        if data is not None:
            self.plot_widget.clear()  # Очищаем график перед отрисовкой

            # Построение графика цен закрытия
            self.plot_widget.plot(
                x=data.index.astype(np.int64) // 10**9,  # преобразуем даты в Unix формат
                y=data['close'],
                pen=pg.mkPen(color='b', width=2),
                name='Close Price'
            )

            # Построение объема
            volume_bar = pg.BarGraphItem(
                x=data.index.astype(np.int64) // 10**9,
                height=data['volume'],
                width=0.8,
                brush='c',
                name='Volume'
            )
            self.plot_widget.addItem(volume_bar)

            # Построение скользящих средних
            data['SMA20'] = data['close'].rolling(window=20).mean()
            self.plot_widget.plot(
                x=data.index.astype(np.int64) // 10**9,
                y=data['SMA20'],
                pen=pg.mkPen(color='g', width=1.5),
                name='SMA 20'
            )

            data['SMA50'] = data['close'].rolling(window=50).mean()
            self.plot_widget.plot(
                x=data.index.astype(np.int64) // 10**9,
                y=data['SMA50'],
                pen=pg.mkPen(color='r', width=1.5),
                name='SMA 50'
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TradingViewLikeInterface()
    main_window.show()
    sys.exit(app.exec_())
# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()
main_window.show()
sys.exit(app.exec_())
