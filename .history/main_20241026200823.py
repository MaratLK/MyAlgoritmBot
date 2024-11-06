import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
import mplfinance as mpf
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import ccxt

# --- Модуль с запросами данных ---
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

    def fetch_data(self, exchange_name, symbol):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d', limit=100)
            data = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            # Преобразуем 'timestamp' в datetime и устанавливаем как индекс
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('timestamp', inplace=True)
            return data
        return None

# --- Основное окно ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface")
        self.setGeometry(200, 200, 1200, 800)

        # Инициализация окна для бэктестинга
        self.backtesting_window = BacktestingWindow()
        self.setCentralWidget(self.backtesting_window)

# --- Окно для бэктестинга ---
class BacktestingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backtesting")

        # Инстанс для получения данных
        self.data_fetcher = DataFetcher()

        # Выпадающий список для выбора биржи
        self.exchange_combo = QComboBox(self)
        self.exchange_combo.addItems(self.data_fetcher.exchanges.keys())
        self.exchange_combo.currentIndexChanged.connect(self.update_pairs)

        # Поле для выбора валютной пары
        self.pair_combo = QComboBox(self)

        # Выпадающий список для выбора типа графика
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems([
            "Candlestick", "Hollow Candles", "Volume Candles", "Line", "Heikin Ashi", "Renko"
        ])

        # Кнопка для построения графика
        self.plot_button = QPushButton("Построить график", self)
        self.plot_button.clicked.connect(self.plot_chart)

        # Создаем холст для графика
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))

        # Макет для бэктестинга
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Биржа:"))
        top_layout.addWidget(self.exchange_combo)
        top_layout.addWidget(QLabel("Валютная пара:"))
        top_layout.addWidget(self.pair_combo)
        top_layout.addWidget(QLabel("Тип графика:"))
        top_layout.addWidget(self.chart_type_combo)
        top_layout.addWidget(self.plot_button)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Инициализируем пары валют для выбранной биржи
        self.update_pairs()

    def update_pairs(self):
        # Обновляем список пар валют для выбранной биржи
        exchange_name = self.exchange_combo.currentText()
        pairs = self.data_fetcher.get_symbols(exchange_name)
        self.pair_combo.clear()
        self.pair_combo.addItems(pairs)

    def plot_chart(self):
        # Получаем выбранные значения
        exchange_name = self.exchange_combo.currentText()
        symbol = self.pair_combo.currentText()
        chart_type = self.chart_type_combo.currentText()

    # Получаем данные OHLCV
        data = self.data_fetcher.fetch_data(exchange_name, symbol)
        if data is not None:
        # Очищаем холст
            self.canvas.figure.clear()

        # Если выбран Volume Candles, создаём вторую ось для объёма
            if chart_type == "Volume Candles":
                ax1 = self.canvas.figure.add_subplot(211)  # График цен
                ax2 = self.canvas.figure.add_subplot(212, sharex=ax1)  # График объёма
                mpf.plot(data, type='candle', ax=ax1, volume=ax2)
            else:
                ax = self.canvas.figure.add_subplot(111)
            # Построение графика на основе типа
                if chart_type == "Candlestick":
                    mpf.plot(data, type='candle', ax=ax)
                elif chart_type == "Hollow Candles":
                    mpf.plot(data, type='candle', style='yahoo', ax=ax)
                elif chart_type == "Line":
                    mpf.plot(data, type='line', ax=ax)
                elif chart_type == "Heikin Ashi":
                    mpf.plot(data, type='heikin', ax=ax)
                elif chart_type == "Renko":
                    mpf.plot(data, type='renko', ax=ax)

        # Обновляем холст для отображения графика
            self.canvas.draw()
        else:
            print("Не удалось загрузить данные для:", symbol)


# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
