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

# --- Модуль для получения данных --- #1
class DataFetcher:
    def __init__(self):
        self.exchanges = {
            "Binance": ccxt.binance(),
            "Bybit": ccxt.bybit()
        }

    def get_symbols(self, exchange_name):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            markets = exchange.load_markets()  #2 Загружаем все доступные рынки с биржи
            return list(markets.keys())
        return []

    def fetch_data(self, exchange_name, symbol, timeframe='1d'):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)  #3 Получаем данные OHLCV (Open, High, Low, Close, Volume)
            data = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')  #4 Преобразование временной метки в читаемый формат даты
            data.set_index('timestamp', inplace=True)  #5 Устанавливаем временную метку в качестве индекса
            return data
        return None

# --- Расчет индикатора Арун --- #6
# Функция для расчета Aroon Up и Aroon Down на основе цены
# Индикатор Арун показывает силу и направление тренда

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
        self.initUI()  #16 Инициализация пользовательского интерфейса

    def initUI(self):
        # Панель управления
        control_layout = QHBoxLayout()  #17 Создание горизонтального макета для панели управления

        # Биржа
        self.exchange_combo = QComboBox()  #18 Комбобокс для выбора биржи
        self.exchange_combo.addItems(self.data_fetcher.exchanges.keys())  #19 Добавление списка доступных бирж
        self.exchange_combo.currentIndexChanged.connect(self.update_pairs)  #20 Сигнал для обновления списка валютных пар при смене биржи
        control_layout.addWidget(QLabel("Биржа:"))  #21 Добавление метки "Биржа"
        control_layout.addWidget(self.exchange_combo)

        # Валютная пара
        self.pair_combo = QComboBox()  #22 Комбобокс для выбора валютной пары
        control_layout.addWidget(QLabel("Валютная пара:"))  #23 Добавление метки "Валютная пара"
        control_layout.addWidget(self.pair_combo)

        # Таймфрейм
        self.timeframe_combo = QComboBox()  #24 Комбобокс для выбора таймфрейма
        self.timeframe_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])  #25 Добавление списка таймфреймов
        control_layout.addWidget(QLabel("Таймфрейм:"))  #26 Добавление метки "Таймфрейм"
        control_layout.addWidget(self.timeframe_combo)

        # Тип графика
        self.chart_type_combo = QComboBox()  #27 Комбобокс для выбора типа графика
        self.chart_type_combo.addItems(["Candlestick", "Line"])  #28 Добавление списка типов графиков
        control_layout.addWidget(QLabel("Тип графика:"))  #29 Добавление метки "Тип графика"
        control_layout.addWidget(self.chart_type_combo)

        # Кнопка "Построить график"
        self.plot_button = QPushButton("Построить график")  #30 Кнопка для построения графика
        self.plot_button.clicked.connect(self.plot_chart)  #31 Привязка события нажатия к функции построения графика
        control_layout.addWidget(self.plot_button)

        # Чекбокс для включения индикатора Арун
        self.aroon_checkbox = QCheckBox("Показать индикатор Арун")  #32 Чекбокс для включения индикатора Арун
        self.aroon_checkbox.stateChanged.connect(self.toggle_aroon)  #33 Привязка события изменения состояния к функции включения индикатора
        control_layout.addWidget(self.aroon_checkbox)

        # Интерфейс графика
        self.chart_view = QWebEngineView()  #34 Виджет для отображения графика на основе HTML

        # Основной макет
        layout = QVBoxLayout()  #35 Создание вертикального основного макета
        layout.addLayout(control_layout)  #36 Добавление панели управления в основной макет
        layout.addWidget(self.chart_view)  #37 Добавление виджета графика в основной макет

        # Центральный виджет
        central_widget = QWidget()  #38 Создание центрального виджета
        central_widget.setLayout(layout)  #39 Установка основного макета на центральный виджет
        self.setCentralWidget(central_widget)  #40 Установка центрального виджета в качестве центрального элемента окна

        # Загрузка пар для начальной биржи
        self.update_pairs()  #41 Инициализация списка валютных пар для выбранной биржи

    def update_pairs(self):
        exchange_name = self.exchange_combo.currentText()  #42 Получение имени текущей биржи
        pairs = self.data_fetcher.get_symbols(exchange_name)  #43 Получение списка валютных пар для выбранной биржи
        self.pair_combo.clear()  #44 Очистка списка валютных пар
        self.pair_combo.addItems(pairs)  #45 Добавление валютных пар в комбобокс

    def toggle_aroon(self, state):
        self.aroon_enabled = state == Qt.Checked  #46 Переключение флага включения индикатора Арун в зависимости от состояния чекбокса

    def plot_chart(self):
        exchange_name = self.exchange_combo.currentText()  #47 Получение имени выбранной биржи
        symbol = self.pair_combo.currentText()  #48 Получение выбранной валютной пары
        timeframe = self.timeframe_combo.currentText()  #49 Получение выбранного таймфрейма
        chart_type = self.chart_type_combo.currentText()  #50 Получение типа графика

        # Получение данных и построение графика
        data = self.data_fetcher.fetch_data(exchange_name, symbol, timeframe)  #51 Получение данных для построения графика
        if data is not None:
            fig = go.Figure()  #52 Создание новой фигуры для графика

            if chart_type == "Candlestick":  #53 Если выбран тип "свечной график"
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close']
                ))  #54 Добавление данных свечей в график
            elif chart_type == "Line":  #55 Если выбран линейный график
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['close'],
                    mode='lines',
                    name=symbol
                ))  #56 Добавление данных линии в график

            # Добавляем индикатор Арун, если включен
            if self.aroon_enabled:  #57 Проверка флага включения индикатора Арун
                aroon_up, aroon_down = calculate_aroon(data)  #58 Расчет значений Aroon Up и Aroon Down
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=aroon_up,
                    mode='lines',
                    name='Aroon Up',
                    line=dict(color='green', dash='dash')
                ))  #59 Добавление линии Aroon Up
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=aroon_down,
                    mode='lines',
                    name='Aroon Down',
                    line=dict(color='red', dash='dash')
                ))  #60 Добавление линии Aroon Down

            # Настройки графика
            fig.update_layout(
                title=f"{symbol} {timeframe} {chart_type}",  #61 Название графика
                xaxis_title="Дата",  #62 Название оси X
                yaxis_title="Цена",  #63 Название оси Y
                template="plotly_dark",  #64 Тема оформления графика
                xaxis_rangeslider_visible=False,  #65 Отключение стандартного слайдера диапазона на оси X
                hovermode='x unified'  #66 Единое перекрестие для всех точек по оси X
            )

            # Отображаем график в QWebEngineView
            self.chart_view.setHtml(fig.to_html(include_plotlyjs='cdn'))  #67 Конвертация графика в HTML и отображение в интерфейсе

# --- Запуск приложения --- #68
app = QApplication(sys.argv)
main_window = TradingViewLikeInterface()  #69 Создание экземпляра основного окна приложения
main_window.show()  #70 Отображение главного окна
sys.exit(app.exec_())  #71 Запуск основного цикла обработки событий приложения
