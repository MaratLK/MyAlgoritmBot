# main_window.py

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QCheckBox, QToolBar, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
from data_fetcher import DataFetcher
from indicators import calculate_aroon
from user_interface import initialize_ui, initialize_toolbar
from interactive_chart import InteractiveChart

# --- Основное окно ---
class TradingViewLikeInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface - TradingView Style")
        self.setGeometry(300, 300, 1200, 800)
        self.data_fetcher = DataFetcher()  # Инициализация модуля получения данных
        self.aroon_enabled = False  # Флаг для включения/выключения индикатора Арун

        # --- Виджеты интерфейса ---
        initialize_ui(self)  # Вызов функции инициализации пользовательского интерфейса
        initialize_toolbar(self)  # Вызов функции инициализации панели инструментов

        # --- Переменные для хранения графика ---
        self.chart_view = None  # Добавляем атрибут для хранения ссылки на текущий график

    def update_pairs(self):
        exchange_name = self.exchange_combo.currentText()  # Получение имени текущей биржи
        pairs = self.data_fetcher.get_symbols(exchange_name)  # Получение списка валютных пар для выбранной биржи
        self.pair_combo.clear()  # Очистка списка валютных пар
        self.pair_combo.addItems(pairs)  # Добавление валютных пар в комбобокс

    def toggle_aroon(self, state):
        self.aroon_enabled = state == Qt.Checked  # Переключение флага включения индикатора Арун в зависимости от состояния чекбокса

    def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()  # Получение имени выбранной биржи
        symbol = self.pair_combo.currentText()  # Получение выбранной валютной пары
        timeframe = self.timeframe_combo.currentText()  # Получение выбранного таймфрейма
        chart_type = self.chart_type_combo.currentText()  # Получение типа графика

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)  # Получение данных для построения графика
        
        if data is None or data.empty:
            print("Нет данных для отображения")
            return

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

        self.chart_view = interactive_chart  # Сохраняем ссылку на текущий график
        self.setCentralWidget(self.chart_view)  # Отображение интерактивного графика в главном окне

    def save_chart(self):
        # Проверяем, что график существует
        if self.chart_view and isinstance(self.chart_view, InteractiveChart):
            # Конвертируем содержимое QWebEngineView в изображение и сохраняем
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить график", "", "PNG Files (*.png);;All Files (*)")
            if file_path:
                # Логика для сохранения графика
                page = self.chart_view.browser.page()
                page.grab().save(file_path)
                QMessageBox.information(self, "Успешно", f"График сохранен в файл: {file_path}")
        else:
            QMessageBox.warning(self, "Ошибка", "График не найден для сохранения.")

    def toggle_zoom(self, checked):
        # Функция для включения/выключения зума графика
        if checked:
            print("Зум включен")  # Заглушка для включения зума
        else:
            print("Зум выключен")  # Заглушка для выключения зума

    def toggle_pan(self, checked):
        # Функция для включения/выключения режима перемещения
        if checked:
            print("Перемещение включено")  # Заглушка для включения перемещения
        else:
            print("Перемещение выключено")  # Заглушка для выключения перемещения

# --- Запуск приложения ---
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()  # Создание экземпляра основного окна приложения
main_window.show()  # Отображение главного окна
sys.exit(app.exec_())  # Запуск основного цикла обработки событий приложения
