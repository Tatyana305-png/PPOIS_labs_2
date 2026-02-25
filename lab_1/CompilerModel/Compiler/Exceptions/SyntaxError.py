from Compiler.Models import CompilerState
from .CompilerException import CompilerException


class SyntaxError(CompilerException):
    """Ошибка синтаксического анализа"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        super().__init__(message, CompilerState.SYNTAX_ANALYSIS, line, column)