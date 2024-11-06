# main_window.py

import sys
import ccxt
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QCheckBox, QToolBar, QAction, QFileDialog, QMessageBox, QWidget, QVBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go

# --- Основное окно --- #13
# Главное окно приложения
class TradingViewLikeInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface - TradingView Style")
        self.setGeometry(300, 300, 1200, 800)
        self.data_fetcher = DataFetcher()  #14 Инициализация модуля получения данных
        self.aroon_enabled = False  #15 Флаг для включения/выключения индикатора Арун

        # --- Центральный виджет ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # --- Виджеты интерфейса ---
        self.initialize_ui()  # Вызов функции инициализации пользовательского интерфейса
        self.initialize_toolbar()  # Вызов функции инициализации панели инструментов

        # --- Переменные для хранения графика ---
        self.chart_view = None  # Добавляем атрибут для хранения ссылки на текущий график

    def initialize_ui(self):
        # Создание основного интерфейса
        self.exchange_combo = QComboBox()
        self.pair_combo = QComboBox()
        self.chart_type_combo = QComboBox()
        self.timeframe_combo = QComboBox()
        self.aroon_checkbox = QCheckBox("Показать индикатор Арун")

        self.layout.addWidget(QLabel("Выберите биржу:"))
        self.layout.addWidget(self.exchange_combo)
        self.layout.addWidget(QLabel("Выберите валютную пару:"))
        self.layout.addWidget(self.pair_combo)
        self.layout.addWidget(QLabel("Тип графика:"))
        self.layout.addWidget(self.chart_type_combo)
        self.layout.addWidget(QLabel("Таймфрейм:"))
        self.layout.addWidget(self.timeframe_combo)
        self.layout.addWidget(self.aroon_checkbox)

        # Привязываем событие к чекбоксу
        self.aroon_checkbox.stateChanged.connect(self.toggle_aroon)

    def initialize_toolbar(self):
        # Создание панели инструментов
        toolbar = QToolBar("Панель инструментов")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Кнопка "Сохранить график"
        save_action = QAction("Сохранить график", self)
        save_action.triggered.connect(self.save_chart)
        toolbar.addAction(save_action)

        # Кнопка "Зум"
        zoom_action = QAction("Зум", self)
        zoom_action.setCheckable(True)
        zoom_action.triggered.connect(self.toggle_zoom)
        toolbar.addAction(zoom_action)

        # Кнопка "Перемещение"
        pan_action = QAction("Перемещение", self)
        pan_action.setCheckable(True)
        pan_action.triggered.connect(self.toggle_pan)
        pan_action.setChecked(True)
        toolbar.addAction(pan_action)

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
        self.layout.addWidget(self.chart_view)  # Отображение интерактивного графика в центральном виджете

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
            print("Зум включен")  #84 Заглушка для включения зума
        else:
            print("Зум выключен")  #85 Заглушка для выключения зума

    def toggle_pan(self, checked):
        # Функция для включения/выключения режима перемещения
        if checked:
            print("Перемещение включено")  #86 Заглушка для включения перемещения
        else:
            print("Перемещение выключено")  #87 Заглушка для выключения перемещения

# --- Модули для получения данных ---
class DataFetcher:
    def __init__(self):
        self.exchanges = {
            "Binance": ccxt.binance({'rateLimit': True}),
            "Bybit": ccxt.bybit({'rateLimit': True}),
        }

    def get_symbols(self, exchange_name):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            try:
                markets = exchange.load_markets()  #2 Загружаем все доступные рынки с биржи
                return list(markets.keys())
            except Exception as e:
                print(f"Ошибка при загрузке рынков с биржи {exchange_name}: {e}")
                return []
        return []

    def fetch_data(self, exchange_name, symbol, timeframe='1d'):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=3000)  #3 Получаем данные OHLCV с увеличенным лимитом
                data = pd.DataFrame(
                    ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
                )
                data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')  #4 Преобразование временной метки в читаемый формат даты
                data.set_index('timestamp', inplace=True)  #5 Устанавливаем временную метку в качестве индекса
                return data
            except Exception as e:
                print(f"Ошибка при получении данных с биржи {exchange_name}: {e}")
        return None

# --- Расчет индикатора Aroon ---
def calculate_aroon(data, period=14):
    # Находим индекс максимума и минимума за заданный период
    high_period = data['high'].rolling(window=period, min_periods=1).apply(lambda x: x.argmax(), raw=True)  #7
    low_period = data['low'].rolling(window=period, min_periods=1).apply(lambda x: x.argmin(), raw=True)  #8
    
    # Переводим индексы в числовой формат
    days_since_high = period - (period - high_period).astype(int)  #9
    days_since_low = period - (period - low_period).astype(int)  #10
    
    # Рассчитываем Aroon Up и Aroon Down
    aroon_up = ((period - days_since_high) / period) * 100  #11 Расчет силы восходящего тренда
    aroon_down = ((period - days_since_low) / period) * 100  #12 Расчет силы нисходящего тренда
    
    return aroon_up, aroon_down

# --- Класс для интерактивного графика ---
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

# --- Запуск приложения --- #88
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()  #89 Создание экземпляра основного окна приложения
main_window.show()  #90 Отображение главного окна
sys.exit(app.exec_())  #91 Запуск основного цикла обработки событий приложения
