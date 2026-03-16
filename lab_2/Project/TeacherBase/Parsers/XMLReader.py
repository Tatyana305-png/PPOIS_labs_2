import xml.sax
from typing import List, Callable
from TeacherBase.Models.Teacher import Teacher


class TeacherHandler(xml.sax.ContentHandler):
    """SAX обработчик для чтения XML"""

    def __init__(self):
        self.teachers = []
        self.current_teacher = {}
        self.current_tag = ""
        self.current_id = None
        self.in_teacher = False

    def startElement(self, tag, attributes):
        self.current_tag = tag
        if tag == "teacher":
            self.in_teacher = True
            self.current_teacher = {}
            self.current_id = attributes.get('id', None)

    def endElement(self, tag):
        if tag == "teacher":
            if self.current_teacher:
                teacher = Teacher(
                    id=self.current_id,
                    faculty=self.current_teacher.get('faculty', ''),
                    department=self.current_teacher.get('department', ''),
                    full_name=self.current_teacher.get('full_name', ''),
                    academic_title=self.current_teacher.get('academic_title', ''),
                    academic_degree=self.current_teacher.get('academic_degree', ''),
                    work_experience=int(self.current_teacher.get('work_experience', 0))
                )
                self.teachers.append(teacher)
            self.in_teacher = False
        self.current_tag = ""

    def characters(self, content):
        if self.in_teacher and self.current_tag and content.strip():
            if self.current_tag in self.current_teacher:
                self.current_teacher[self.current_tag] += content.strip()
            else:
                self.current_teacher[self.current_tag] = content.strip()


class XMLReader:
    """Класс для чтения XML с использованием SAX парсера"""

    @staticmethod
    def read_from_file(filepath: str, progress_callback: Callable[[int], None] = None) -> List[Teacher]:
        """Чтение данных из XML файла"""
        handler = TeacherHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)

        # Простой подсчет строк для прогресса (опционально)
        if progress_callback:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total_lines = len(lines)
                for i, line in enumerate(lines):
                    if i % 100 == 0:
                        progress_callback(int(i / total_lines * 100))

        parser.parse(filepath)
        return handler.teachers