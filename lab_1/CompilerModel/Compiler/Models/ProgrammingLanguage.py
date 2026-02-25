from typing import List


class ProgrammingLanguage:
    """Модель языка программирования"""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.keywords: List[str] = ['if', 'else', 'while', 'return', 'int', 'float']
        self.operators: List[str] = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!']
        self.separators: List[str] = [';', ',', '(', ')', '{', '}']

    def get_name(self) -> str:
        return self.name

    def is_keyword(self, word: str) -> bool:
        return word in self.keywords

    def is_operator(self, char: str) -> bool:
        return char in self.operators

    def is_separator(self, char: str) -> bool:
        return char in self.separators

    def __str__(self) -> str:
        return f"{self.name} {self.version}"