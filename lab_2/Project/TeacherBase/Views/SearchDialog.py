from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QSpinBox, QPushButton,
                             QDialogButtonBox, QTabWidget, QWidget)
from TeacherBase.Views.PaginatedTable import PaginatedTable
from TeacherBase.Utils.Constants import TABLE_HEADERS
from typing import Dict, Any


class SearchDialog(QDialog):
    """Диалог поиска преподавателей"""

    def __init__(self, parent, data_controller):
        super().__init__(parent)
        self.data_controller = data_controller
        self.setWindowTitle("Поиск преподавателей")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        self._setup_ui()
        self._load_unique_values()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        layout = QVBoxLayout(self)

        # Создаем вкладки для разных условий поиска
        tab_widget = QTabWidget()

        # Вкладка 1: Поиск по фамилии и кафедре
        tab1 = QWidget()
        tab1_layout = QFormLayout(tab1)

        self.full_name_edit = QLineEdit()
        self.full_name_edit.setPlaceholderText("Введите фамилию...")
        tab1_layout.addRow("Фамилия преподавателя:", self.full_name_edit)

        self.department_combo = QComboBox()
        self.department_combo.addItem("Все")
        tab1_layout.addRow("Кафедра:", self.department_combo)

        tab_widget.addTab(tab1, "По фамилии и кафедре")

        # Вкладка 2: Поиск по ученому званию и факультету
        tab2 = QWidget()
        tab2_layout = QFormLayout(tab2)

        self.title_combo = QComboBox()
        self.title_combo.addItem("Все")
        tab2_layout.addRow("Ученое звание:", self.title_combo)

        self.faculty_combo = QComboBox()
        self.faculty_combo.addItem("Все")
        tab2_layout.addRow("Факультет:", self.faculty_combo)

        tab_widget.addTab(tab2, "По званию и факультету")

        # Вкладка 3: Поиск по стажу работы
        tab3 = QWidget()
        tab3_layout = QFormLayout(tab3)

        self.experience_min = QSpinBox()
        self.experience_min.setRange(0, 70)
        self.experience_min.setSpecialValueText("Не указано")
        tab3_layout.addRow("Стаж от (лет):", self.experience_min)

        self.experience_max = QSpinBox()
        self.experience_max.setRange(0, 70)
        self.experience_max.setSpecialValueText("Не указано")
        tab3_layout.addRow("Стаж до (лет):", self.experience_max)

        tab_widget.addTab(tab3, "По стажу работы")

        layout.addWidget(tab_widget)

        # Кнопка поиска
        search_btn = QPushButton("Найти")
        search_btn.clicked.connect(self.perform_search)
        layout.addWidget(search_btn)

        # Таблица результатов
        self.results_table = PaginatedTable()
        layout.addWidget(self.results_table)

        # Кнопки
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_unique_values(self):
        """Загрузка уникальных значений для комбобоксов"""
        # Кафедры
        departments = self.data_controller.get_unique_departments()
        self.department_combo.addItems(departments)

        # Ученые звания
        titles = self.data_controller.get_unique_titles()
        self.title_combo.addItems(titles)

        # Факультеты
        faculties = self.data_controller.get_unique_faculties()
        self.faculty_combo.addItems(faculties)

    def perform_search(self):
        """Выполнение поиска"""
        criteria = self._get_search_criteria()
        results = self.data_controller.search_teachers(criteria)

        def extractor(teacher):
            return [
                teacher.id,
                teacher.faculty,
                teacher.department,
                teacher.full_name,
                teacher.academic_title,
                teacher.academic_degree,
                f"{teacher.work_experience} лет"
            ]

        self.results_table.set_data(results, TABLE_HEADERS, extractor)

    def _get_search_criteria(self) -> Dict[str, Any]:
        """Получение критериев поиска"""
        criteria = {}

        # Проверяем все возможные поля
        if self.full_name_edit.text().strip():
            criteria['full_name'] = self.full_name_edit.text().strip()

        if self.department_combo.currentText() != "Все":
            criteria['department'] = self.department_combo.currentText()

        if self.title_combo.currentText() != "Все":
            criteria['academic_title'] = self.title_combo.currentText()

        if self.faculty_combo.currentText() != "Все":
            criteria['faculty'] = self.faculty_combo.currentText()

        if self.experience_min.value() > 0:
            criteria['work_experience_min'] = self.experience_min.value()

        if self.experience_max.value() > 0:
            criteria['work_experience_max'] = self.experience_max.value()

        return criteria