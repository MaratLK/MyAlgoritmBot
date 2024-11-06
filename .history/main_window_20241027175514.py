import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QCheckBox, QToolBar, QAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
from data_fetcher import DataFetcher
from indicators import calculate_aroon
from chart_plotter import plot_chart  # Импорт функции построения графиков из chart_plotter.py
from user_interface import initialize_ui, initialize_toolbar  # Импорт функций инициализации интерфейса из user_interface.py
from interactive_chart import InteractiveChart  # Импортируем класс для работы с интерактивным графиком

# --- Основное окно --- #13
# Главное окно приложения
class TradingViewLikeInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface - TradingView Style")
        self.setGeometry(300, 300, 1200, 800)
        self.data_fetcher = DataFetcher()  #14 Инициализация модуля получения данных
        self.aroon_enabled = False  #15 Флаг для включения/выключения индикатора Арун

        # --- Виджеты интерфейса ---
        initialize_ui(self)  # Вызов функции инициализации пользовательского интерфейса
        initialize_toolbar(self)  # Вызов функции инициализации панели инструментов

    def update_pairs(self):
        exchange_name = self.exchange_combo.currentText()  #56 Получение имени текущей биржи
        pairs = self.data_fetcher.get_symbols(exchange_name)  #57 Получение списка валютных пар для выбранной биржи
        self.pair_combo.clear()  #58 Очистка списка валютных пар
        self.pair_combo.addItems(pairs)  #59 Добавление валютных пар в комбобокс

    def toggle_aroon(self, state):
        self.aroon_enabled = state == Qt.Checked  #60 Переключение флага включения индикатора Арун в зависимости от состояния чекбокса

    def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()  #61 Получение имени выбранной биржи
        symbol = self.pair_combo.currentText()  #62 Получение выбранной валютной пары
        timeframe = self.timeframe_combo.currentText()  #63 Получение выбранного таймфрейма
        chart_type = self.chart_type_combo.currentText()  #64 Получение типа графика

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)  #65 Получение данных для построения графика
        if data is not None:
            # Создание интерактивного графика и добавление его в центральный виджет
            interactive_chart = InteractiveChart(data)  # Используем класс для создания графика

            # Добавляем индикатор Aroon, если он включен
            if self.aroon_enabled:
                aroon_up, aroon_down = calculate_aroon(data)  # Вызываем функцию для расчета Aroon
                fig = go.Figure()  # Создаем новую фигуру графика
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name=symbol
                ))
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
                interactive_chart.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

            self.setCentralWidget(interactive_chart)  # Отображение интерактивного графика в главном окне

    def save_chart(self):
        # Функция для сохранения текущего графика
        print("Сохранение графика")  #83 Заглушка для функции сохранения графика

    def toggle_zoom(self, checked):
        # Функция для включения/выключения зума графика
        if checked:
            print("Зум включен")  #84 Заглушка для включения зума
        else:
            print("Зум выключен")  #85 Заглушка для выключения зума

    def toggle_pan(self, checked):
        # Функция для включения/выключения режима перемещения
        if checked:
            print("Перемещение включено")  #86 Заглушка для включения перемещения
        else:
            print("Перемещение выключено")  #87 Заглушка для выключения перемещения

# --- Запуск приложения --- #88
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()  #89 Создание экземпляра основного окна приложения
main_window.show()  #90 Отображение главного окна
sys.exit(app.exec_())  #91 Запуск основного цикла обработки событий приложения
