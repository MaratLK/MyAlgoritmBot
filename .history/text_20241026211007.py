import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import pandas as pd

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
        
        fig.update_layout(
            title="Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price"
        )
        
        # Конвертируем график в HTML и отображаем его в QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        
        layout.addWidget(self.browser)
        self.setLayout(layout)

def main():
    # Создаем пример данных OHLCV для отображения на графике
    data = pd.DataFrame({
        'open': [100, 101, 102, 103, 104],
        'high': [105, 106, 107, 108, 109],
        'low': [99, 100, 101, 102, 103],
        'close': [102, 103, 104, 105, 106]
    })
    data.index = pd.date_range(start='2023-01-01', periods=5, freq='D')  # Индекс с датами

    # Запускаем приложение
    app = QApplication(sys.argv)
    window = QMainWindow()
    chart = InteractiveChart(data)
    window.setCentralWidget(chart)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
