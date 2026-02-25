from enum import Enum


class CompilerState(Enum):
    """Состояния компилятора"""
    INITIALIZED = "Инициализирован"
    LEXICAL_ANALYSIS = "Лексический анализ"
    SYNTAX_ANALYSIS = "Синтаксический анализ"
    OPTIMIZATION = "Оптимизация"
    CODE_GENERATION = "Генерация кода"
    COMPLETED = "Завершено"
    ERROR = "Ошибка"