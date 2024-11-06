import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QCheckBox, QToolBar, QAction
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from data_fetcher import DataFetcher


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
        self.initToolbar()  #17 Инициализация панели инструментов

    def initUI(self):
        # Панель управления
        control_layout = QHBoxLayout()  #18 Создание горизонтального макета для панели управления

        # Биржа
        self.exchange_combo = QComboBox()  #19 Комбобокс для выбора биржи
        self.exchange_combo.addItems(self.data_fetcher.exchanges.keys())  #20 Добавление списка доступных бирж
        self.exchange_combo.currentIndexChanged.connect(self.update_pairs)  #21 Сигнал для обновления списка валютных пар при смене биржи
        control_layout.addWidget(QLabel("Биржа:"))  #22 Добавление метки "Биржа"
        control_layout.addWidget(self.exchange_combo)

        # Валютная пара
        self.pair_combo = QComboBox()  #23 Комбобокс для выбора валютной пары
        control_layout.addWidget(QLabel("Валютная пара:"))  #24 Добавление метки "Валютная пара"
        control_layout.addWidget(self.pair_combo)

        # Таймфрейм
        self.timeframe_combo = QComboBox()  #25 Комбобокс для выбора таймфрейма
        self.timeframe_combo.addItems(["1m", "5m", "15m", "1h", "4h", "1d"])  #26 Добавление списка таймфреймов
        control_layout.addWidget(QLabel("Таймфрейм:"))  #27 Добавление метки "Таймфрейм"
        control_layout.addWidget(self.timeframe_combo)

        # Тип графика
        self.chart_type_combo = QComboBox()  #28 Комбобокс для выбора типа графика
        self.chart_type_combo.addItems(["Candlestick", "Line"])  #29 Добавление списка типов графиков
        control_layout.addWidget(QLabel("Тип графика:"))  #30 Добавление метки "Тип графика"
        control_layout.addWidget(self.chart_type_combo)

        # Кнопка "Построить график"
        self.plot_button = QPushButton("Построить график")  #31 Кнопка для построения графика
        self.plot_button.clicked.connect(self.plot_chart)  #32 Привязка события нажатия к функции построения графика
        control_layout.addWidget(self.plot_button)

        # Чекбокс для включения индикатора Арун
        self.aroon_checkbox = QCheckBox("Показать индикатор Арун")  #33 Чекбокс для включения индикатора Арун
        self.aroon_checkbox.stateChanged.connect(self.toggle_aroon)  #34 Привязка события изменения состояния к функции включения индикатора
        control_layout.addWidget(self.aroon_checkbox)

        # Интерфейс графика
        self.chart_view = QWebEngineView()  #35 Виджет для отображения графика на основе HTML

        # Основной макет
        layout = QVBoxLayout()  #36 Создание вертикального основного макета
        layout.addLayout(control_layout)  #37 Добавление панели управления в основной макет
        layout.addWidget(self.chart_view)  #38 Добавление виджета графика в основной макет

        # Центральный виджет
        central_widget = QWidget()  #39 Создание центрального виджета
        central_widget.setLayout(layout)  #40 Установка основного макета на центральный виджет
        self.setCentralWidget(central_widget)  #41 Установка центрального виджета в качестве центрального элемента окна

        # Загрузка пар для начальной биржи
        self.update_pairs()  #42 Инициализация списка валютных пар для выбранной биржи

    def update_pairs(self):
        exchange_name = self.exchange_combo.currentText()  #56 Получение имени текущей биржи
        pairs = self.data_fetcher.get_symbols(exchange_name)  #57 Получение списка валютных пар для выбранной биржи
        self.pair_combo.clear()  #58 Очистка списка валютных пар
        self.pair_combo.addItems(pairs)  #59 Добавление валютных пар в комбобокс

    def toggle_aroon(self, state):
        self.aroon_enabled = state == Qt.Checked  #60 Переключение флага включения индикатора Арун в зависимости от состояния чекбокса

    
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
