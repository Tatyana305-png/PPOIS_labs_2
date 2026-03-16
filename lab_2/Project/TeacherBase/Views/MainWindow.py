from PyQt5.QtWidgets import (QMainWindow, QAction, QToolBar, QStatusBar,
                             QVBoxLayout, QWidget, QTabWidget,
                             QTreeWidget, QTreeWidgetItem)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from TeacherBase.Views.PaginatedTable import PaginatedTable
from TeacherBase.Utils.Constants import TABLE_HEADERS
from typing import List
from TeacherBase.Models.Teacher import Teacher


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        self._create_actions()
        self._create_menus()
        self._create_toolbar()
        self._create_status_bar()  # Это создает статус бар

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Система учета преподавателей - Вариант 12")
        self.setGeometry(100, 100, 1200, 600)

        # Центральный виджет с вкладками
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Создаем вкладки
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Вкладка с табличным представлением
        self.table_view = QWidget()
        self.tab_widget.addTab(self.table_view, "Табличное представление")

        table_layout = QVBoxLayout(self.table_view)
        self.paginated_table = PaginatedTable()
        table_layout.addWidget(self.paginated_table)

        # Вкладка с древовидным представлением
        self.tree_view = QWidget()
        self.tab_widget.addTab(self.tree_view, "Древовидное представление")

        tree_layout = QVBoxLayout(self.tree_view)
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Преподаватели")
        tree_layout.addWidget(self.tree_widget)

    def _create_actions(self):
        """Создание действий"""
        # Действие для добавления
        self.add_action = QAction("&Добавить", self)
        self.add_action.setShortcut(QKeySequence.New)
        self.add_action.setStatusTip("Добавить нового преподавателя")

        # Действие для поиска
        self.search_action = QAction("&Поиск", self)
        self.search_action.setShortcut(QKeySequence.Find)
        self.search_action.setStatusTip("Поиск преподавателей")

        # Действие для удаления
        self.delete_action = QAction("&Удалить", self)
        self.delete_action.setShortcut(QKeySequence.Delete)
        self.delete_action.setStatusTip("Удалить преподавателей")

        # Действие для сохранения
        self.save_action = QAction("&Сохранить в XML", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setStatusTip("Сохранить данные в XML файл")

        # Действие для загрузки
        self.load_action = QAction("&Загрузить из XML", self)
        self.load_action.setShortcut(QKeySequence.Open)
        self.load_action.setStatusTip("Загрузить данные из XML файла")

        # Действие для выхода
        self.exit_action = QAction("&Выход", self)
        self.exit_action.setShortcut(QKeySequence.Quit)
        self.exit_action.setStatusTip("Выйти из приложения")

        # Действие для переключения представления
        self.tree_view_action = QAction("Древовидное представление", self)
        self.tree_view_action.setCheckable(True)
        self.tree_view_action.setStatusTip("Переключиться на древовидное представление")

    def _create_menus(self):
        """Создание меню"""
        menubar = self.menuBar()

        # Меню Файл
        file_menu = menubar.addMenu("&Файл")
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.load_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Меню Правка
        edit_menu = menubar.addMenu("&Правка")
        edit_menu.addAction(self.add_action)
        edit_menu.addAction(self.search_action)
        edit_menu.addAction(self.delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.tree_view_action)

        # Меню Вид
        view_menu = menubar.addMenu("&Вид")
        view_menu.addAction(self.tree_view_action)

    def _create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = QToolBar("Основная панель")
        self.addToolBar(toolbar)

        toolbar.addAction(self.add_action)
        toolbar.addAction(self.search_action)
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.load_action)
        toolbar.addSeparator()
        toolbar.addAction(self.exit_action)

    def _create_status_bar(self):
        """Создание строки состояния"""
        # Используем встроенный метод statusBar() для получения объекта статус-бара
        status_bar = self.statusBar()
        status_bar.showMessage("Готово")

    def update_teacher_table(self, teachers: List[Teacher]):
        """Обновление таблицы с преподавателями"""

        def extractor(teacher: Teacher):
            return [
                str(teacher.id) if teacher.id else "",
                teacher.faculty,
                teacher.department,
                teacher.full_name,
                teacher.academic_title,
                teacher.academic_degree,
                f"{teacher.work_experience} лет"
            ]

        self.paginated_table.set_data(teachers, TABLE_HEADERS, extractor)
        self._update_tree_view(teachers)

        # Обновляем статус бар - используем встроенный метод statusBar()
        self.statusBar().showMessage(f"Всего записей: {len(teachers)}")

    def _update_tree_view(self, teachers: List[Teacher]):
        """Обновление древовидного представления"""
        self.tree_widget.clear()

        if not teachers:
            return

        # Группировка по факультетам
        faculties = {}
        for teacher in teachers:
            if teacher.faculty not in faculties:
                faculties[teacher.faculty] = []
            faculties[teacher.faculty].append(teacher)

        # Создание дерева
        for faculty, faculty_teachers in faculties.items():
            faculty_item = QTreeWidgetItem(self.tree_widget)
            faculty_item.setText(0, faculty)
            faculty_item.setExpanded(False)

            for teacher in faculty_teachers:
                teacher_item = QTreeWidgetItem(faculty_item)
                teacher_item.setText(0, f"{teacher.full_name} - {teacher.department}")

                # Добавляем поля как листья
                fields = [
                    f"Кафедра: {teacher.department}",
                    f"Ученое звание: {teacher.academic_title}",
                    f"Ученая степень: {teacher.academic_degree}",
                    f"Стаж работы: {teacher.work_experience} лет"
                ]

                for field in fields:
                    field_item = QTreeWidgetItem(teacher_item)
                    field_item.setText(0, field)