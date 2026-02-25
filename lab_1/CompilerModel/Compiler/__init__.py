"""Модель компилятора - пакет для трансляции исходного кода в машинный код"""

from Compiler.Core import (
    SourceCode, Compiler, LexicalAnalyzer,
    SyntaxAnalyzer, Optimizer, MachineCodeGenerator
)
from Compiler.Models import (
    CompilerState, ProgrammingLanguage, Token,
    TokenType, ASTNode, Instruction, MachineCode
)
from Compiler.Exceptions import (
    CompilerException, LexicalError, SyntaxError
)

__all__ = [
    # Core
    'SourceCode',
    'Compiler',
    'LexicalAnalyzer',
    'SyntaxAnalyzer',
    'Optimizer',
    'MachineCodeGenerator',

    # Models
    'CompilerState',
    'ProgrammingLanguage',
    'Token',
    'TokenType',
    'ASTNode',
    'Instruction',
    'MachineCode',

    # Exceptions
    'CompilerException',
    'LexicalError',
    'SyntaxError'
]

__version__ = '1.0.0'