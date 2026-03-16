import xml.dom.minidom as minidom
from xml.dom.minidom import Document
from typing import List
from TeacherBase.Models.Teacher import Teacher


class XMLWriter:
    """Класс для записи XML с использованием DOM парсера"""

    @staticmethod
    def write_to_file(teachers: List[Teacher], filepath: str):
        """Запись данных в XML файл"""
        doc = Document()

        # Корневой элемент
        root = doc.createElement('teachers')
        doc.appendChild(root)

        for teacher in teachers:
            teacher_elem = doc.createElement('teacher')

            # Добавляем атрибут id
            teacher_elem.setAttribute('id', str(teacher.id))

            # Создаем элементы для каждого поля
            fields = [
                ('faculty', teacher.faculty),
                ('department', teacher.department),
                ('full_name', teacher.full_name),
                ('academic_title', teacher.academic_title),
                ('academic_degree', teacher.academic_degree),
                ('work_experience', str(teacher.work_experience))
            ]

            for field_name, field_value in fields:
                field_elem = doc.createElement(field_name)
                field_text = doc.createTextNode(field_value)
                field_elem.appendChild(field_text)
                teacher_elem.appendChild(field_elem)

            root.appendChild(teacher_elem)

        # Запись в файл с красивым форматированием
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc.toprettyxml(indent='  ', encoding='utf-8').decode('utf-8'))