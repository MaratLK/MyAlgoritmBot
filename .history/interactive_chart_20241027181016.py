#interactive_chart.py

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from data_fetcher import DataFetcher


class InteractiveChart(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Interactive Trading Chart")
        layout = QVBoxLayout()

        # Проверяем наличие необходимых данных перед созданием графика
        required_columns = {'open', 'high', 'low', 'close'}
        if data is not None and not data.empty and required_columns.issubset(data.columns):
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close']
            )])
            fig.update_layout(
                title="Candlestick Chart",
                xaxis_title="Date",
                yaxis_title="Price",
                template="plotly_white",  # Добавляем тему для графика
                xaxis=dict(showgrid=True),  # Включаем отображение сетки по оси X
                yaxis=dict(showgrid=True)   # Включаем отображение сетки по оси Y
            )

            # Конвертируем график в HTML и отображаем его в QWebEngineView
            try:
                self.browser = QWebEngineView()
                self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
                layout.addWidget(self.browser)
            except ImportError:
                QMessageBox.critical(self, "Ошибка", "QWebEngineView не установлен или не поддерживается в вашей среде.")
        else:
            QMessageBox.warning(self, "Предупреждение", "Недостаточно данных для построения графика.")

        self.setLayout(layout)


# Основное приложение
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()

    # Взаимодействие с пользователем для выбора биржи, валютной пары и таймфрейма
    data_fetcher = DataFetcher()  # Предполагается, что этот модуль реализован для получения данных с биржи

    # Пример выбора - эти параметры могут быть заменены выбором из интерфейса
    exchange_name = "Binance"
    symbols = data_fetcher.get_symbols(exchange_name)
    symbol = "BTC/USDT" if "BTC/USDT" in symbols else symbols[0]  # По умолчанию выбираем 'BTC/USDT' или первую доступную пару
    timeframe = "1d"  # Таймфрейм по умолчанию - этот параметр тоже может быть изменен пользователем

    # Получение данных с выбранной биржи для выбранной валютной пары и таймфрейма
    data = data_fetcher.fetch_data(exchange_name, symbol, timeframe)

    chart = InteractiveChart(data)
    window.setCentralWidget(chart)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())