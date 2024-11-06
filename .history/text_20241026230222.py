import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QCheckBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ccxt
import pandas as pd
import plotly.graph_objects as go

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
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
            data = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('timestamp', inplace=True)
            return data
        return None

# --- Расчет индикатора Арун ---
def calculate_aroon(data, period=14):
    # Находим индекс максимума и минимума за заданный период
    high_period = data['high'].rolling(window=period, min_periods=1).apply(lambda x: x.argmax(), raw=True)
    low_period = data['low'].rolling(window=period, min_periods=1).apply(lambda x: x.argmin(), raw=True)
    
    # Переводим индексы в числовой формат
    days_since_high = period - (period - high_period).astype(int)
    days_since_low = period - (period - low_period).astype(int)
    
    # Рассчитываем Aroon Up и Aroon Down
    aroon_up = ((period - days_since_high) / period) * 100
    aroon_down = ((period - days_since_low) / period) * 100
    
    return aroon_up, aroon_down


# --- Основное окно ---
class TradingViewLikeInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface - TradingView Style")
        self.setGeometry(300, 300, 1200, 800)
        self.data_fetcher = DataFetcher()
        self.aroon_enabled = False  # Флаг для включения/выключения индикатора Арун

        # --- Виджеты интерфейса ---
        self.initUI()

    def initUI(self):
        # Панель управления
        control_layout = QHBoxLayout()

        # Биржа
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(self.data_fetcher.exchanges.keys())
        self.exchange_combo.currentIndexChanged.connect(self.update_pairs)
        control_layout.addWidget(QLabel("Биржа:"))
        control_layout.addWidget(self.exchange_combo)

        # Валютная пара
        self.pair_combo = QComboBox()
        control_layout.addWidget(QLabel("Валютная пара:"))
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

        # Чекбокс для включения индикатора Арун
        self.aroon_checkbox = QCheckBox("Показать индикатор Арун")
        self.aroon_checkbox.stateChanged.connect(self.toggle_aroon)
        control_layout.addWidget(self.aroon_checkbox)

        # Интерфейс графика
        self.chart_view = QWebEngineView()

        # Основной макет
        layout = QVBoxLayout()
        layout.addLayout(control_layout)
        layout.addWidget(self.chart_view)

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

    def toggle_aroon(self, state):
        self.aroon_enabled = state == Qt.Checked

    def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()
        symbol = self.pair_combo.currentText()
        timeframe = self.timeframe_combo.currentText()
        chart_type = self.chart_type_combo.currentText()

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)
        if data is not None:
            fig = go.Figure()

            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close']
                ))
            elif chart_type == "Line":
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['close'],
                    mode='lines',
                    name=symbol
                ))

            # Добавляем индикатор Арун, если включен
            if self.aroon_enabled:
                aroon_up, aroon_down = calculate_aroon(data)
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=aroon_up,
                    mode='lines',
                    name='Aroon Up',
                    line=dict(color='green', dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=aroon_down,
                    mode='lines',
                    name='Aroon Down',
                    line=dict(color='red', dash='dash')
                ))

            # Настройки графика
            fig.update_layout(
                title=f"{symbol} {timeframe} {chart_type}",
                xaxis_title="Дата",
                yaxis_title="Цена",
                template="plotly_dark",
                xaxis_rangeslider_visible=False,  # Отключить стандартный слайдер
                hovermode='x unified'  # Перекрестие
            )

            # Отображаем график в QWebEngineView
            self.chart_view.setHtml(fig.to_html(include_plotlyjs='cdn'))

# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()
main_window.show()
sys.exit(app.exec_())
