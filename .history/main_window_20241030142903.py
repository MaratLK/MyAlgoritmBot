import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ccxt
import pandas as pd
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
        
        # Тип графика
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Candlestick", "Line"])
        control_layout.addWidget(QLabel("Тип графика:"))
        control_layout.addWidget(self.chart_type_combo)
        
        # Кнопка "Построить график"
        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_chart)
        control_layout.addWidget(self.plot_button)

        # Интерфейс графика (PyQtGraph)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # Белый фон
        self.plot_widget.addLegend()  # Добавляем легенду

        # Настройка оси для объемов
        self.volume_axis = pg.ViewBox()
        self.plot_widget.showAxis('right')
        self.plot_widget.getAxis('right').linkToView(self.volume_axis)
        self.plot_widget.scene().addItem(self.volume_axis)
        self.plot_widget.getViewBox().sigResized.connect(self.update_views)
        
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
        chart_type = self.chart_type_combo.currentText()

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)
        if data is not None:
            self.plot_widget.clear()  # Очищаем график перед отрисовкой

            if chart_type == "Line":
                # Построение графика цен закрытия
                self.plot_widget.plot(
                    x=data.index.view(int) // 10**9,
                    y=data['close'],
                    pen=pg.mkPen(color='b', width=2),
                    name='Close Price'
                )
            elif chart_type == "Candlestick":
                # Построение свечного графика
                candlesticks = []
                for i in range(len(data)):
                    timestamp = data.index[i]
                    open_price = data['open'][i]
                    high_price = data['high'][i]
                    low_price = data['low'][i]
                    close_price = data['close'][i]

                    if close_price >= open_price:
                        color = (0, 255, 0)  # Зеленый цвет для свечей на повышение
                    else:
                        color = (255, 0, 0)  # Красный цвет для свечей на понижение

                    # Тело свечи
                    body = pg.BarGraphItem(
                        x=[timestamp], height=[close_price - open_price], width=0.8,
                        brush=color, pen=color, y0=open_price
                    )
                    self.plot_widget.addItem(body)

                    # Тени свечи (высокая и низкая цена)
                    line = pg.PlotDataItem(
                        x=[timestamp, timestamp], y=[low_price, high_price],
                        pen=pg.mkPen(color=color, width=1)
                    )
                    self.plot_widget.addItem(line)

            # Построение объема
            volume_bar = pg.BarGraphItem(
                x=data.index.view(int) // 10**9,
                height=data['volume'],
                width=0.8,
                brush=pg.mkBrush(150, 0, 0, 150),  # Красный цвет с прозрачностью
                name='Volume'
            )
            self.volume_axis.addItem(volume_bar)

            # Построение скользящих средних
            data['SMA20'] = data['close'].rolling(window=20).mean()
            self.plot_widget.plot(
                x=data.index.view(int) // 10**9,
                y=data['SMA20'],
                pen=pg.mkPen(color='g', width=1.5),
                name='SMA 20'
            )

            data['SMA50'] = data['close'].rolling(window=50).mean()
            self.plot_widget.plot(
                x=data.index.view(int) // 10**9,
                y=data['SMA50'],
                pen=pg.mkPen(color='r', width=1.5),
                name='SMA 50'
            )

    def update_views(self):
        self.volume_axis.setGeometry(self.plot_widget.getViewBox().sceneBoundingRect())
        self.volume_axis.linkedViewChanged(self.plot_widget.getViewBox(), self.volume_axis.XAxis)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = TradingViewLikeInterface()
    main_window.show()
    sys.exit(app.exec_())
