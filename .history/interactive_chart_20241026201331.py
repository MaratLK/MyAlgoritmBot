from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import sys

class InteractiveChart(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Interactive Trading Chart")
        layout = QVBoxLayout()
        
        # Создаем интерактивный график с Plotly
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close']
        )])
        
        fig.update_layout(title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price")
        
        # Конвертируем график в HTML и отображаем его в QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        
        layout.addWidget(self.browser)
        self.setLayout(layout)

# Основное приложение
app = QApplication(sys.argv)
window = QMainWindow()
data = ...  # Подставьте ваши данные OHLCV
chart = InteractiveChart(data)
window.setCentralWidget(chart)
window.resize(800, 600)
window.show()
sys.exit(app.exec_())
