import sqlite3
import os
from typing import List, Optional, Dict, Any
from TeacherBase.Models.Teacher import Teacher


class Database:
    """Класс для работы с базой данных (Single Responsibility Principle)"""

    def __init__(self, db_path: str = "Data/teachers.db"):
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()

    def _ensure_data_directory(self):
        """Создание папки Data, если она не существует"""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Создана папка: {data_dir}")

    def _init_database(self):
        """Инициализация таблицы в БД"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS teachers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        faculty TEXT NOT NULL,
                        department TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        academic_title TEXT NOT NULL,
                        academic_degree TEXT NOT NULL,
                        work_experience INTEGER NOT NULL
                    )
                ''')
                conn.commit()
                print("База данных инициализирована успешно")
        except Exception as e:
            print(f"Ошибка при инициализации БД: {e}")
            raise

    def _get_connection(self):
        """Получение соединения с БД"""
        try:
            data_dir = os.path.dirname(self.db_path)
            if not os.access(data_dir, os.W_OK):
                print(f"Нет прав на запись в папку: {data_dir}")
                import tempfile
                temp_dir = tempfile.gettempdir()
                self.db_path = os.path.join(temp_dir, "teachers.db")
                print(f"Использую временную папку: {self.db_path}")

            return sqlite3.connect(self.db_path)
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def add_teacher(self, teacher: Teacher) -> int:
        """Добавление преподавателя в БД"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO teachers (faculty, department, full_name, academic_title, academic_degree, work_experience)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                teacher.faculty, teacher.department, teacher.full_name,
                teacher.academic_title, teacher.academic_degree, teacher.work_experience
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_teachers(self) -> List[Teacher]:
        """Получение всех преподавателей"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM teachers')
            rows = cursor.fetchall()

            teachers = []
            for row in rows:
                teacher = Teacher(
                    id=row[0],
                    faculty=row[1],
                    department=row[2],
                    full_name=row[3],
                    academic_title=row[4],
                    academic_degree=row[5],
                    work_experience=row[6]
                )
                teachers.append(teacher)
            return teachers

    def delete_teachers(self, condition: Dict[str, Any]) -> int:
        """Удаление преподавателей по условию"""
        query = "DELETE FROM teachers WHERE 1=1"
        params = []

        if condition.get('full_name'):
            query += " AND full_name LIKE ?"
            params.append(f"%{condition['full_name']}%")

        if condition.get('department'):
            query += " AND department = ?"
            params.append(condition['department'])

        if condition.get('faculty'):
            query += " AND faculty = ?"
            params.append(condition['faculty'])

        if condition.get('academic_title'):
            query += " AND academic_title = ?"
            params.append(condition['academic_title'])

        if condition.get('academic_degree'):
            query += " AND academic_degree = ?"
            params.append(condition['academic_degree'])

        if condition.get('work_experience_min') is not None:
            query += " AND work_experience >= ?"
            params.append(condition['work_experience_min'])

        if condition.get('work_experience_max') is not None:
            query += " AND work_experience <= ?"
            params.append(condition['work_experience_max'])

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count

    def search_teachers(self, condition: Dict[str, Any]) -> List[Teacher]:
        """Поиск преподавателей по условию"""
        query = "SELECT * FROM teachers WHERE 1=1"
        params = []

        if condition.get('full_name'):
            query += " AND full_name LIKE ?"
            params.append(f"%{condition['full_name']}%")

        if condition.get('department'):
            query += " AND department = ?"
            params.append(condition['department'])

        if condition.get('faculty'):
            query += " AND faculty = ?"
            params.append(condition['faculty'])

        if condition.get('academic_title'):
            query += " AND academic_title = ?"
            params.append(condition['academic_title'])

        if condition.get('academic_degree'):
            query += " AND academic_degree = ?"
            params.append(condition['academic_degree'])

        if condition.get('work_experience_min') is not None:
            query += " AND work_experience >= ?"
            params.append(condition['work_experience_min'])

        if condition.get('work_experience_max') is not None:
            query += " AND work_experience <= ?"
            params.append(condition['work_experience_max'])

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            teachers = []
            for row in rows:
                teacher = Teacher(
                    id=row[0],
                    faculty=row[1],
                    department=row[2],
                    full_name=row[3],
                    academic_title=row[4],
                    academic_degree=row[5],
                    work_experience=row[6]
                )
                teachers.append(teacher)
            return teachers

    def clear_all(self):
        """Очистка всех данных"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM teachers')
            conn.commit()

    def get_unique_values(self, column: str) -> List[str]:
        """Получение уникальных значений из колонки"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'SELECT DISTINCT {column} FROM teachers ORDER BY {column}')
            return [row[0] for row in cursor.fetchall() if row[0]]
