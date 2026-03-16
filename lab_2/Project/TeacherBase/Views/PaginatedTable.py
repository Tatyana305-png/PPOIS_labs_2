from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QComboBox,
                             QSpinBox, QHeaderView)
from PyQt5.QtCore import Qt
from typing import List, Any, Callable


class PaginatedTable(QWidget):
    """Компонент для постраничного отображения табличных данных"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.headers = []
        self.current_page = 1
        self.items_per_page = 10
        self.total_pages = 1
        self._setup_ui()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        layout = QVBoxLayout(self)

        # Таблица
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Панель навигации
        nav_layout = QHBoxLayout()

        # Кнопки навигации
        self.first_btn = QPushButton("|<")
        self.prev_btn = QPushButton("<")
        self.next_btn = QPushButton(">")
        self.last_btn = QPushButton(">|")

        nav_layout.addWidget(self.first_btn)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.last_btn)

        # Информация о страницах
        self.page_info = QLabel("Страница: 1 из 1")
        nav_layout.addWidget(self.page_info)

        # Выбор количества записей на странице
        nav_layout.addWidget(QLabel("Записей на странице:"))
        self.items_per_page_combo = QComboBox()
        self.items_per_page_combo.addItems(["5", "10", "20", "50", "100"])
        self.items_per_page_combo.setCurrentText("10")
        nav_layout.addWidget(self.items_per_page_combo)

        # Информация о количестве записей
        self.total_items_label = QLabel("Всего записей: 0")
        nav_layout.addWidget(self.total_items_label)

        nav_layout.addStretch()
        layout.addLayout(nav_layout)

        # Подключение сигналов
        self.first_btn.clicked.connect(self.go_to_first_page)
        self.prev_btn.clicked.connect(self.go_to_prev_page)
        self.next_btn.clicked.connect(self.go_to_next_page)
        self.last_btn.clicked.connect(self.go_to_last_page)
        self.items_per_page_combo.currentTextChanged.connect(self.change_items_per_page)

    def set_data(self, data: List[Any], headers: List[str], data_extractor: Callable[[Any], List[str]]):
        """Установка данных для отображения"""
        self.data = data
        self.headers = headers
        self.data_extractor = data_extractor
        self.total_pages = max(1, (len(data) + self.items_per_page - 1) // self.items_per_page)
        self.current_page = 1
        self.update_table()

    def update_table(self):
        """Обновление таблицы"""
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.data))

        # Настройка таблицы
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setRowCount(end_idx - start_idx)

        # Заполнение данными
        for i, idx in enumerate(range(start_idx, end_idx)):
            item_data = self.data[idx]
            row_values = self.data_extractor(item_data)

            for j, value in enumerate(row_values):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(i, j, item)

        # Автоматическое растягивание колонок
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Обновление информации
        self.page_info.setText(f"Страница: {self.current_page} из {self.total_pages}")
        self.total_items_label.setText(f"Всего записей: {len(self.data)}")

        # Обновление состояния кнопок
        self.first_btn.setEnabled(self.current_page > 1)
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
        self.last_btn.setEnabled(self.current_page < self.total_pages)

    def go_to_first_page(self):
        """Переход на первую страницу"""
        if self.current_page > 1:
            self.current_page = 1
            self.update_table()

    def go_to_prev_page(self):
        """Переход на предыдущую страницу"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()

    def go_to_next_page(self):
        """Переход на следующую страницу"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_table()

    def go_to_last_page(self):
        """Переход на последнюю страницу"""
        if self.current_page < self.total_pages:
            self.current_page = self.total_pages
            self.update_table()

    def change_items_per_page(self, value: str):
        """Изменение количества записей на странице"""
        self.items_per_page = int(value)
        self.total_pages = max(1, (len(self.data) + self.items_per_page - 1) // self.items_per_page)
        self.current_page = min(self.current_page, self.total_pages)
        self.update_table()