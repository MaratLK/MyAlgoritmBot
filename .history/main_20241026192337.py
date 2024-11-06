import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QFrame
)
from PyQt5.QtCore import Qt
import mplfinance as mpf
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- Основное окно (главная страница) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface")
        self.setGeometry(200, 200, 800, 600)

        # Кнопка для перехода в раздел бэктестинга
        self.backtest_button = QPushButton("Backtesting", self)
        self.backtest_button.clicked.connect(self.open_backtesting)
        
        # Макет главного окна
        layout = QVBoxLayout()
        layout.addWidget(self.backtest_button)

        # Создаем центральный виджет и устанавливаем его как основной
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_backtesting(self):
        # Открываем окно бэктестинга
        self.backtest_window = BacktestingWindow()
        self.backtest_window.show()

# --- Окно для раздела бэктестинга ---
class BacktestingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backtesting")
        self.setGeometry(300, 300, 1000, 700)

        # Поле для поиска
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Введите валютную пару...")

        # Выпадающий список для выбора типа графика
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems(["Candlestick", "Line", "Heikin Ashi", "Renko", "Range"])

        # Кнопка для построения графика
        self.plot_button = QPushButton("Построить график", self)
        self.plot_button.clicked.connect(self.plot_chart)

        # Создаем холст для графика
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        
        # Макет для бэктестинга
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Тип графика:"))
        top_layout.addWidget(self.chart_type_combo)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.plot_button)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def plot_chart(self):
        # Здесь будет логика для построения графика
        chart_type = self.chart_type_combo.currentText()
        search_text = self.search_bar.text().upper()  # Текст из поля поиска
        
        # Тестовые данные для отображения
        # Генерируем данные с помощью Pandas
        dates = pd.date_range("2023-01-01", periods=100)
        data = pd.DataFrame({
            "Date": dates,
            "Open": pd.Series(range(100)) + 10,
            "High": pd.Series(range(100)) + 15,
            "Low": pd.Series(range(100)),
            "Close": pd.Series(range(100)) + 5,
            "Volume": pd.Series(range(100)) * 100
        }).set_index("Date")
        
        self.canvas.figure.clear()  # Очищаем холст
        
        # Построение графика в зависимости от выбранного типа
        if chart_type == "Candlestick":
            mpf.plot(data, type='candle', ax=self.canvas.figure.add_subplot(111), volume=True)
        elif chart_type == "Line":
            mpf.plot(data, type='line', ax=self.canvas.figure.add_subplot(111))
        elif chart_type == "Heikin Ashi":
            mpf.plot(data, type='heikin', ax=self.canvas.figure.add_subplot(111))
        elif chart_type == "Renko":
            mpf.plot(data, type='renko', ax=self.canvas.figure.add_subplot(111))
        elif chart_type == "Range":
            mpf.plot(data, type='range', ax=self.canvas.figure.add_subplot(111))
        
        self.canvas.draw()  # Отображаем обновленный график

# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
