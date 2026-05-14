from enum import Enum
from typing import List, Optional, Any
from dataclasses import dataclass, field


class CompilerState(Enum):
    """Состояния компилятора"""
    INITIALIZED = "Инициализирован"
    LEXICAL_ANALYSIS = "Лексический анализ"
    SYNTAX_ANALYSIS = "Синтаксический анализ"
    OPTIMIZATION = "Оптимизация"
    CODE_GENERATION = "Генерация кода"
    COMPLETED = "Завершён"
    ERROR = "Ошибка"


class ProgrammingLanguage:
    """Модель языка программирования"""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self._keywords = {
            'if', 'else', 'while', 'return', 'int', 'float'
        }

    def is_keyword(self, word: str) -> bool:
        """Проверяет, является ли слово ключевым"""
        return word in self._keywords

    def add_keyword(self, keyword: str) -> None:
        """Добавляет ключевое слово"""
        self._keywords.add(keyword)


class TokenType(Enum):
    """Типы токенов"""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    SEPARATOR = "SEPARATOR"
    COMMENT = "COMMENT"
    UNKNOWN = "UNKNOWN"


@dataclass
class Token:
    """Токен - минимальная единица лексического анализа"""
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"


@dataclass
class ASTNode:
    """Узел абстрактного синтаксического дерева"""
    type: str
    value: Optional[Any]
    children: List['ASTNode']
    line: int = 0
    column: int = 0

    def __repr__(self) -> str:
        return f"ASTNode({self.type}, {self.value}, children={len(self.children)})"


@dataclass
class Instruction:
    """Машинная инструкция"""
    opcode: str
    operands: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.opcode} {', '.join(self.operands)}".strip()


@dataclass
class MachineCode:
    """Машинный код программы"""
    instructions: List[Instruction] = field(default_factory=list)

    def add_instruction(self, instruction: Instruction) -> None:
        """Добавляет инструкцию"""
        self.instructions.append(instruction)

    def __repr__(self) -> str:
        return '\n'.join(str(instr) for instr in self.instructions)