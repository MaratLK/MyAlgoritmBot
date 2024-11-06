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

    def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()
        symbol = self.pair_combo.currentText()
        timeframe = self.timeframe_combo.currentText()
        chart_type = self.chart_type_combo.currentText()

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)
        if data is not None:
            fig = go.Figure()
            
            # Построение основного графика (свечи или линии)
            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name='Candlestick'
                ))
            elif chart_type == "Line":
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['close'],    
                    mode='lines',
                    name=symbol
                ))

            # Добавление объема на график по умолчанию
            colors = ['rgba(0, 204, 0, 0.4)' if close >= open_ else 'rgba(255, 0, 0, 0.4)'
                  for open_, close in zip(data['open'], data['close'])]
            fig.add_trace(go.Bar(
            x=data.index,
            y=data['volume'],
            name='Volume',
            marker=dict(color=colors),
            yaxis='y2'
        ))

            # Добавление SMA по умолчанию
            data['SMA20'] = data['close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA20'],
                mode='lines',
                name='Short SMA',
                line=dict(color='blue', width=1),
                yaxis='y'  # Накладываем SMA на основной график
            ))

            data['SMA50'] = data['close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA50'],
                mode='lines',
                name='Long SMA',
                line=dict(color='orange', width=1),
                yaxis='y'  # Накладываем SMA на основной график
            ))

            # Добавление индикатора Aroon, если включен
            if hasattr(self, 'aroon_checkbox') and self.aroon_checkbox.isChecked():
                data['Aroon Up'], data['Aroon Down'] = self.calculate_aroon(data)
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['Aroon Up'], mode='lines', name='Aroon Up', line=dict(color='green'),
                    yaxis='y'  # Также накладываем Aroon на основной график
                ))
                fig.add_trace(go.Scatter(
                    x=data.index, y=data['Aroon Down'], mode='lines', name='Aroon Down', line=dict(color='red'),
                    yaxis='y'  # Также накладываем Aroon на основной график
                ))

            # Настройки отображения объемов и индикаторов на основном графике
            fig.update_layout(
                title=f"{symbol} {timeframe} {chart_type}",
                xaxis_title="Дата",
                yaxis_title="Цена",
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                hovermode='x unified',
                yaxis=dict(
                    title='Price and Indicators',
                    side='left',
                    showgrid=True
                ),
                yaxis2=dict(
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    title='Volume'
                )
            )

            self.chart_view.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def calculate_aroon(self, data, period=14):
        high_period = data['high'].rolling(window=period, min_periods=1).apply(lambda x: x.argmax(), raw=True)
        low_period = data['low'].rolling(window=period, min_periods=1).apply(lambda x: x.argmin(), raw=True)

        days_since_high = period - (period - high_period).astype(int)
        days_since_low = period - (period - low_period).astype(int)

        aroon_up = ((period - days_since_high) / period) * 100
        aroon_down = ((period - days_since_low) / period) * 100

        return aroon_up, aroon_down

# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()
main_window.show()
sys.exit(app.exec_())
