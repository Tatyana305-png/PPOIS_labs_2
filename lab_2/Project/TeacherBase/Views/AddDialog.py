from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QSpinBox, QDialogButtonBox,
                             QMessageBox)
from PyQt5.QtCore import Qt
from TeacherBase.Utils.Constants import FACULTIES, DEPARTMENTS, ACADEMIC_TITLES, ACADEMIC_DEGREES


class AddDialog(QDialog):
    """Диалог добавления нового преподавателя"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление преподавателя")
        self.setModal(True)
        self.setMinimumWidth(500)
        self._setup_ui()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        layout = QVBoxLayout(self)

        # Форма для ввода данных
        form_layout = QFormLayout()

        # Факультет
        self.faculty_combo = QComboBox()
        self.faculty_combo.addItems(FACULTIES)
        self.faculty_combo.setEditable(True)
        form_layout.addRow("Факультет:", self.faculty_combo)

        # Кафедра
        self.department_combo = QComboBox()
        self.department_combo.addItems(DEPARTMENTS)
        self.department_combo.setEditable(True)
        form_layout.addRow("Кафедра:", self.department_combo)

        # ФИО
        self.full_name_edit = QLineEdit()
        self.full_name_edit.setPlaceholderText("Иванов Иван Иванович")
        form_layout.addRow("ФИО:", self.full_name_edit)

        # Ученое звание
        self.title_combo = QComboBox()
        self.title_combo.addItems(ACADEMIC_TITLES)
        self.title_combo.setEditable(True)
        form_layout.addRow("Ученое звание:", self.title_combo)

        # Ученая степень
        self.degree_combo = QComboBox()
        self.degree_combo.addItems(ACADEMIC_DEGREES)
        form_layout.addRow("Ученая степень:", self.degree_combo)

        # Стаж работы
        self.experience_spin = QSpinBox()
        self.experience_spin.setRange(0, 70)
        self.experience_spin.setSuffix(" лет")
        form_layout.addRow("Стаж работы:", self.experience_spin)

        layout.addLayout(form_layout)

        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def validate_and_accept(self):
        """Валидация данных перед принятием"""
        if not self.full_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Поле ФИО обязательно для заполнения")
            return

        if self.experience_spin.value() == 0:
            reply = QMessageBox.question(
                self, "Подтверждение",
                "Стаж работы равен 0. Продолжить?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        self.accept()

    def get_teacher_data(self):
        """Получение данных преподавателя"""
        return {
            'faculty': self.faculty_combo.currentText().strip(),
            'department': self.department_combo.currentText().strip(),
            'full_name': self.full_name_edit.text().strip(),
            'academic_title': self.title_combo.currentText().strip(),
            'academic_degree': self.degree_combo.currentText().strip(),
            'work_experience': self.experience_spin.value()
        }