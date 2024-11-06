# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QStackedWidget
from exchange_module import get_exchange_pairs, EXCHANGE_OPTIONS
from backtesting_module import BacktestingPage

class TradingBotInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface")
        self.setGeometry(200, 200, 700, 500)

        # Создаем главный виджет
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Страница главного экрана
        self.main_page = QWidget()
        self.central_widget.addWidget(self.main_page)

        # Страница для бэктестинга
        self.backtesting_page = BacktestingPage()
        self.central_widget.addWidget(self.backtesting_page)

        # Элементы интерфейса главной страницы
        self.exchange_label = QLabel("Выберите биржу:")
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(EXCHANGE_OPTIONS.keys())
        self.load_button = QPushButton("Загрузить валютные пары")
        self.load_button.clicked.connect(self.load_pairs)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск валютной пары")
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search_pairs)
        self.pair_table = QTableWidget()
        self.pair_table.setColumnCount(1)
        self.pair_table.setHorizontalHeaderLabels(["Валютная пара"])

        # Кнопка для перехода на страницу бэктестинга
        self.backtesting_button = QPushButton("Перейти к бэктестингу")
        self.backtesting_button.clicked.connect(self.show_backtesting_page)

        # Устанавливаем элементы на главной странице
        layout = QVBoxLayout()
        layout.addWidget(self.exchange_label)
        layout.addWidget(self.exchange_combo)
        layout.addWidget(self.load_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.pair_table)
        layout.addWidget(self.backtesting_button)
        self.main_page.setLayout(layout)

    def load_pairs(self):
        """
        Загрузка валютных пар с выбранной биржи и отображение в таблице.
        """
        exchange_name = self.exchange_combo.currentText()
        pairs = get_exchange_pairs(exchange_name)
        self.pair_table.setRowCount(0)
        for row, pair in enumerate(pairs):
            self.pair_table.insertRow(row)
            self.pair_table.setItem(row, 0, QTableWidgetItem(pair))

    def search_pairs(self):
        """
        Фильтрует пары на основе введенного текста поиска.
        """
        search_text = self.search_input.text().strip().lower()
        for row in range(self.pair_table.rowCount()):
            item = self.pair_table.item(row, 0)
            self.pair_table.setRowHidden(row, search_text not in item.text().lower())

    def show_backtesting_page(self):
        """
        Переход на страницу бэктестинга.
        """
        self.central_widget.setCurrentWidget(self.backtesting_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingBotInterface()
    window.show()
    sys.exit(app.exec_())
