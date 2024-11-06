# user_interface.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QAction

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
