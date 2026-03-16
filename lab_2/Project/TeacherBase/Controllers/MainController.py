from PyQt5.QtWidgets import QFileDialog, QMessageBox
from TeacherBase.Models.Database import Database
from TeacherBase.Controllers.DataController import DataController
from TeacherBase.Views.MainWindow import MainWindow
from TeacherBase.Views.AddDialog import AddDialog
from TeacherBase.Views.SearchDialog import SearchDialog
from TeacherBase.Views.DeleteDialog import DeleteDialog
from TeacherBase.Parsers.XMLWriter import XMLWriter
from TeacherBase.Parsers.XMLReader import XMLReader


class MainController:
    """Главный контроллер приложения (MVC)"""

    def __init__(self):
        self.database = Database()
        self.data_controller = DataController(self.database)
        self.view = MainWindow(self)
        self._setup_connections()
        self.refresh_view()

    def _setup_connections(self):
        """Настройка связей между представлением и контроллером"""
        self.view.add_action.triggered.connect(self.show_add_dialog)
        self.view.search_action.triggered.connect(self.show_search_dialog)
        self.view.delete_action.triggered.connect(self.show_delete_dialog)
        self.view.save_action.triggered.connect(self.save_to_xml)
        self.view.load_action.triggered.connect(self.load_from_xml)
        self.view.exit_action.triggered.connect(self.view.close)
        self.view.tree_view_action.triggered.connect(self.toggle_tree_view)

    def run(self):
        """Запуск приложения"""
        self.view.show()

    def refresh_view(self):
        """Обновление представления"""
        teachers = self.data_controller.get_all_teachers()
        self.view.update_teacher_table(teachers)

    def show_add_dialog(self):
        """Показать диалог добавления"""
        dialog = AddDialog(self.view)
        if dialog.exec_():
            teacher_data = dialog.get_teacher_data()
            self.data_controller.add_teacher(teacher_data)
            self.refresh_view()
            QMessageBox.information(self.view, "Успех", "Преподаватель успешно добавлен")

    def show_search_dialog(self):
        """Показать диалог поиска"""
        dialog = SearchDialog(self.view, self.data_controller)
        dialog.exec_()

    def show_delete_dialog(self):
        """Показать диалог удаления"""
        dialog = DeleteDialog(self.view, self.data_controller)
        if dialog.exec_():
            self.refresh_view()

    def save_to_xml(self):
        """Сохранение данных в XML файл"""
        filepath, _ = QFileDialog.getSaveFileName(
            self.view, "Сохранить в XML", "", "XML Files (*.xml)"
        )

        if filepath:
            try:
                teachers = self.data_controller.get_all_teachers()
                XMLWriter.write_to_file(teachers, filepath)
                QMessageBox.information(
                    self.view, "Успех",
                    f"Данные успешно сохранены в {filepath}\n"
                    f"Сохранено записей: {len(teachers)}"
                )
            except Exception as e:
                QMessageBox.critical(self.view, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def load_from_xml(self):
        """Загрузка данных из XML файла"""
        filepath, _ = QFileDialog.getOpenFileName(
            self.view, "Загрузить из XML", "", "XML Files (*.xml)"
        )

        if filepath:
            try:
                self.data_controller.clear_all()

                teachers = XMLReader.read_from_file(filepath)

                for teacher in teachers:
                    self.data_controller.add_teacher(teacher.to_dict())

                self.refresh_view()
                QMessageBox.information(
                    self.view, "Успех",
                    f"Данные успешно загружены из {filepath}\n"
                    f"Загружено записей: {len(teachers)}"
                )
            except Exception as e:
                QMessageBox.critical(self.view, "Ошибка", f"Ошибка при загрузке: {str(e)}")

    def toggle_tree_view(self):
        """Переключение между табличным и древовидным представлением"""
        current_state = self.view.tree_view_action.isChecked()
        self.view.tree_view_action.setChecked(current_state)
        QMessageBox.information(
            self.view, "Информация",
            "Древовидное представление будет реализовано в следующей версии"
        )