import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ccxt
import plotly.graph_objects as go
import pandas as pd
from interactive_chart import InteractiveChart  # Импортируем новый модуль

# --- Модуль для получения данных ---
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
        self.setGeometry(300, 300, 1200, 800)

        # Инстанс для получения данных
        self.data_fetcher = DataFetcher()

        # Виджеты для выбора биржи и пары
        self.exchange_combo = QComboBox(self)
        self.exchange_combo.addItems(self.data_fetcher.exchanges.keys())
        self.exchange_combo.currentIndexChanged.connect(self.update_pairs)

        self.pair_combo = QComboBox(self)

        # Кнопка для построения графика
        self.plot_button = QPushButton("Построить график", self)
        self.plot_button.clicked.connect(self.plot_chart)

        # Макет для виджетов выбора
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Биржа:"))
        top_layout.addWidget(self.exchange_combo)
        top_layout.addWidget(QLabel("Валютная пара:"))
        top_layout.addWidget(self.pair_combo)
        top_layout.addWidget(self.plot_button)

        # Виджет для отображения интерактивного графика
        self.chart_view = QWebEngineView()

        # Основной макет
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.chart_view)

        # Центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Инициализировать список валютных пар
        self.update_pairs()

    def update_pairs(self):
        exchange_name = self.exchange_combo.currentText()
        pairs = self.data_fetcher.get_symbols(exchange_name)
        self.pair_combo.clear()
        self.pair_combo.addItems(pairs)

    def plot_chart(self):
        if data is None or data.empty:
            print("Data is missing or empty.")
            return
        exchange_name = self.exchange_combo.currentText()
        symbol = self.pair_combo.currentText()

        # Получаем данные для выбранной пары
        data = self.data_fetcher.fetch_data(exchange_name, symbol)
        if data is not None:
            # Создаем интерактивный график
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close']
            )])
            fig.update_layout(title=f"{symbol} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")

            # Отображаем график в QWebEngineView
            self.chart_view.setHtml(fig.to_html(include_plotlyjs='cdn'))

# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
