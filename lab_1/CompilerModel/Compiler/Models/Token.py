from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    """Типы токенов для лексического анализа"""
    KEYWORD = "Ключевое слово"
    IDENTIFIER = "Идентификатор"
    NUMBER = "Число"
    OPERATOR = "Оператор"
    SEPARATOR = "Разделитель"
    STRING = "Строка"
    COMMENT = "Комментарий"
    UNKNOWN = "Неизвестный"


@dataclass
class Token:
    """Токен - результат лексического анализа"""
    type: TokenType
    value: str
    line: int
    column: int