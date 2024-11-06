# user_interface.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QLabel, QCheckBox, QToolBar, QAction

def initialize_ui(main_window):
    # Создание основного интерфейса
    main_window.central_widget = QVBoxLayout()
    main_window.exchange_combo = QComboBox()
    main_window.pair_combo = QComboBox()
    main_window.chart_type_combo = QComboBox()
    main_window.timeframe_combo = QComboBox()
    main_window.aroon_checkbox = QCheckBox("Показать индикатор Арун")

    main_window.central_widget.addWidget(QLabel("Выберите биржу:"))
    main_window.central_widget.addWidget(main_window.exchange_combo)
    main_window.central_widget.addWidget(QLabel("Выберите валютную пару:"))
    main_window.central_widget.addWidget(main_window.pair_combo)
    main_window.central_widget.addWidget(QLabel("Тип графика:"))
    main_window.central_widget.addWidget(main_window.chart_type_combo)
    main_window.central_widget.addWidget(QLabel("Таймфрейм:"))
    main_window.central_widget.addWidget(main_window.timeframe_combo)
    main_window.central_widget.addWidget(main_window.aroon_checkbox)

    # Привязываем событие к чекбоксу
    main_window.aroon_checkbox.stateChanged.connect(main_window.toggle_aroon)

def initialize_toolbar(main_window):
    # Создание панели инструментов
    toolbar = QToolBar("Панель инструментов")
    main_window.addToolBar(Qt.TopToolBarArea, toolbar)

    # Кнопка "Сохранить график"
    save_action = QAction("Сохранить график", main_window)
    save_action.triggered.connect(main_window.save_chart)
    toolbar.addAction(save_action)

    # Кнопка "Зум"
    zoom_action = QAction("Зум", main_window)
    zoom_action.setCheckable(True)
    zoom_action.triggered.connect(main_window.toggle_zoom)
    toolbar.addAction(zoom_action)

    # Кнопка "Перемещение"
    pan_action = QAction("Перемещение", main_window)
    pan_action.setCheckable(True)
    pan_action.triggered.connect(main_window.toggle_pan)
    pan_action.setChecked(True)
    toolbar.addAction(pan_action)
