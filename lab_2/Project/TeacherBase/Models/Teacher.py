from dataclasses import dataclass
from typing import Optional


@dataclass
class Teacher:
    """Модель данных преподавателя"""
    faculty: str
    department: str
    full_name: str
    academic_title: str
    academic_degree: str
    work_experience: int
    id: Optional[int] = None

    def __post_init__(self):
        if self.id is not None:
            try:
                self.id = int(self.id)
            except (ValueError, TypeError):
                self.id = None

    def to_dict(self) -> dict:
        """Преобразование в словарь для БД"""
        return {
            'faculty': self.faculty,
            'department': self.department,
            'full_name': self.full_name,
            'academic_title': self.academic_title,
            'academic_degree': self.academic_degree,
            'work_experience': self.work_experience
        }

    @classmethod
    def from_dict(cls, data: dict, id: Optional[int] = None):
        """Создание объекта из словаря"""
        return cls(
            id=id,
            faculty=data.get('faculty', ''),
            department=data.get('department', ''),
            full_name=data.get('full_name', ''),
            academic_title=data.get('academic_title', ''),
            academic_degree=data.get('academic_degree', ''),
            work_experience=int(data.get('work_experience', 0))
        )