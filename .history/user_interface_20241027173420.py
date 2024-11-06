from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QCheckBox, QToolBar, QAction
)

def initToolbar(self):
        # Создание панели инструментов
        toolbar = QToolBar("Панель инструментов")  #43 Создание панели инструментов
        self.addToolBar(Qt.TopToolBarArea, toolbar)  #44 Добавление панели инструментов в верхнюю часть окна

        # Кнопка "Сохранить график"
        save_action = QAction("Сохранить график", self)  #45 Создание действия для сохранения графика
        save_action.triggered.connect(self.save_chart)  #46 Привязка действия к функции сохранения графика
        toolbar.addAction(save_action)  #47 Добавление действия в панель инструментов

        # Кнопка "Зум"
        zoom_action = QAction("Зум", self)  #48 Создание действия для зума графика
        zoom_action.setCheckable(True)  #49 Делаем действие переключаемым (включение/выключение зума)
        zoom_action.triggered.connect(self.toggle_zoom)  #50 Привязка действия к функции включения/выключения зума
        toolbar.addAction(zoom_action)  #51 Добавление действия в панель инструментов

        # Кнопка "Перемещение"
        pan_action = QAction("Перемещение", self)  #52 Создание действия для режима перемещения
        pan_action.setCheckable(True)  #53 Делаем действие переключаемым
        pan_action.triggered.connect(self.toggle_pan)  #54 Привязка действия к функции включения/выключения режима перемещения
        pan_action.setChecked(True)  # Устанавливаем панорамирование по умолчанию
        toolbar.addAction(pan_action)  #55 Добавление действия в панель инструментов