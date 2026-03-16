from typing import List, Dict, Any
from TeacherBase.Models.Teacher import Teacher
from TeacherBase.Models.Database import Database

class DataController:
    """Контроллер для работы с данными (Open/Closed Principle)"""

    def __init__(self, database: Database):
        self.database = database

    def get_all_teachers(self) -> List[Teacher]:
        """Получение всех преподавателей"""
        return self.database.get_all_teachers()

    def add_teacher(self, teacher_data: Dict[str, Any]) -> int:
        """Добавление нового преподавателя"""
        teacher = Teacher.from_dict(teacher_data)
        return self.database.add_teacher(teacher)

    def search_teachers(self, search_criteria: Dict[str, Any]) -> List[Teacher]:
        """Поиск преподавателей по критериям"""
        return self.database.search_teachers(search_criteria)

    def delete_teachers(self, delete_criteria: Dict[str, Any]) -> int:
        """Удаление преподавателей по критериям"""
        return self.database.delete_teachers(delete_criteria)

    def clear_all(self):
        """Очистка всех данных"""
        self.database.clear_all()

    def get_unique_faculties(self) -> List[str]:
        """Получение уникальных факультетов"""
        return self.database.get_unique_values('faculty')

    def get_unique_departments(self) -> List[str]:
        """Получение уникальных кафедр"""
        return self.database.get_unique_values('department')

    def get_unique_titles(self) -> List[str]:
        """Получение уникальных ученых званий"""
        return self.database.get_unique_values('academic_title')

    def get_unique_degrees(self) -> List[str]:
        """Получение уникальных ученых степеней"""
        return self.database.get_unique_values('academic_degree')