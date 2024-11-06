# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel
from exchange_module import get_exchange_pairs, EXCHANGE_OPTIONS

class TradingBotInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trading Bot Interface")
        self.setGeometry(200, 200, 700, 500)

        # Выпадающий список выбора биржи
        self.exchange_label = QLabel("Выберите биржу:")
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems(EXCHANGE_OPTIONS.keys())

        # Кнопка загрузки пар
        self.load_button = QPushButton("Загрузить валютные пары")
        self.load_button.clicked.connect(self.load_pairs)

        # Поле поиска и кнопка поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск валютной пары")
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search_pairs)

        # Таблица для отображения пар
        self.pair_table = QTableWidget()
        self.pair_table.setColumnCount(1)
        self.pair_table.setHorizontalHeaderLabels(["Валютная пара"])

        # Слой для размещения всех виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.exchange_label)
        layout.addWidget(self.exchange_combo)
        layout.addWidget(self.load_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.pair_table)

        # Установка слоя в центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_pairs(self):
        """
        Загрузка валютных пар с выбранной биржи и отображение в таблице.
        """
        exchange_name = self.exchange_combo.currentText()
        pairs = get_exchange_pairs(exchange_name)

        # Очистка таблицы и добавление новых данных
        self.pair_table.setRowCount(0)
        for row, pair in enumerate(pairs):
            self.pair_table.insertRow(row)
            self.pair_table.setItem(row, 0, QTableWidgetItem(pair))

    def search_pairs(self):
        """
        Фильтрует пары на основе введенного текста поиска.
        """
        search_text = self.search_input.text().strip().lower()  # Поиск без учета регистра
        for row in range(self.pair_table.rowCount()):
            item = self.pair_table.item(row, 0)
            self.pair_table.setRowHidden(row, search_text not in item.text().lower())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles.qss").read())  # Загрузка стилей

    window = TradingBotInterface()
    window.show()
    sys.exit(app.exec_())
