#interactive_chart.py

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

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

    # Подставьте ваши данные OHLCV в формате DataFrame
    # Пример данных
    ohlcv_data = {
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'open': pd.Series(range(100)),
        'high': pd.Series(range(1, 101)),
        'low': pd.Series(range(0, 100)),
        'close': pd.Series(range(50, 150)),
        'volume': pd.Series(range(200, 300))
    }
    data = pd.DataFrame(ohlcv_data)
    data.set_index('timestamp', inplace=True)

    chart = InteractiveChart(data)
    window.setCentralWidget(chart)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
