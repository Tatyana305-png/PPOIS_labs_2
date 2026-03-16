from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QSpinBox, QPushButton,
                             QDialogButtonBox, QMessageBox, QGroupBox, QLabel,
                             QTabWidget, QWidget)
from typing import Dict, Any


class DeleteDialog(QDialog):
    """Диалог удаления преподавателей"""

    def __init__(self, parent, data_controller):
        super().__init__(parent)
        self.data_controller = data_controller
        self.setWindowTitle("Удаление преподавателей")
        self.setModal(True)
        self.setMinimumWidth(500)
        self._setup_ui()
        self._load_unique_values()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        layout = QVBoxLayout(self)

        info_label = QLabel("Укажите условия для удаления записей:")
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)

        tab_widget = QTabWidget()

        tab1 = QWidget()
        tab1_layout = QFormLayout(tab1)

        self.full_name_edit = QLineEdit()
        self.full_name_edit.setPlaceholderText("Введите фамилию...")
        tab1_layout.addRow("Фамилия преподавателя:", self.full_name_edit)

        self.department_combo = QComboBox()
        self.department_combo.addItem("Любая")
        tab1_layout.addRow("Кафедра:", self.department_combo)

        tab_widget.addTab(tab1, "По фамилии и кафедре")

        tab2 = QWidget()
        tab2_layout = QFormLayout(tab2)

        self.title_combo = QComboBox()
        self.title_combo.addItem("Любое")
        tab2_layout.addRow("Ученое звание:", self.title_combo)

        self.faculty_combo = QComboBox()
        self.faculty_combo.addItem("Любой")
        tab2_layout.addRow("Факультет:", self.faculty_combo)

        tab_widget.addTab(tab2, "По званию и факультету")

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

        self.delete_btn = QPushButton("Удалить записи")
        self.delete_btn.clicked.connect(self.perform_delete)
        self.delete_btn.setStyleSheet(
            "background-color: #ff6b6b; color: white; font-weight: bold;"
        )
        layout.addWidget(self.delete_btn)

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_unique_values(self):
        """Загрузка уникальных значений для комбобоксов"""
        departments = self.data_controller.get_unique_departments()
        self.department_combo.addItems(departments)

        titles = self.data_controller.get_unique_titles()
        self.title_combo.addItems(titles)

        faculties = self.data_controller.get_unique_faculties()
        self.faculty_combo.addItems(faculties)

    def perform_delete(self):
        """Выполнение удаления"""
        criteria = self._get_delete_criteria()

        if not criteria:
            QMessageBox.warning(self, "Предупреждение",
                                "Укажите хотя бы одно условие для удаления")
            return

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            "Вы действительно хотите удалить записи по указанным условиям?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            deleted_count = self.data_controller.delete_teachers(criteria)

            if deleted_count > 0:
                QMessageBox.information(
                    self, "Успех",
                    f"Было удалено {deleted_count} записей"
                )
                self.accept()
            else:
                QMessageBox.information(
                    self, "Результат",
                    "Записей, соответствующих условиям, не найдено"
                )

    def _get_delete_criteria(self) -> Dict[str, Any]:
        """Получение критериев удаления"""
        criteria = {}

        if self.full_name_edit.text().strip():
            criteria['full_name'] = self.full_name_edit.text().strip()

        if self.department_combo.currentText() != "Любая":
            criteria['department'] = self.department_combo.currentText()

        if self.title_combo.currentText() != "Любое":
            criteria['academic_title'] = self.title_combo.currentText()

        if self.faculty_combo.currentText() != "Любой":
            criteria['faculty'] = self.faculty_combo.currentText()

        if self.experience_min.value() > 0:
            criteria['work_experience_min'] = self.experience_min.value()

        if self.experience_max.value() > 0:
            criteria['work_experience_max'] = self.experience_max.value()

        return criteria