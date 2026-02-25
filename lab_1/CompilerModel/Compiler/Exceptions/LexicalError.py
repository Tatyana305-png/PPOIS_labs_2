from Compiler.Models import CompilerState
from .CompilerException import CompilerException


class LexicalError(CompilerException):
    """Ошибка лексического анализа"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        super().__init__(message, CompilerState.LEXICAL_ANALYSIS, line, column)