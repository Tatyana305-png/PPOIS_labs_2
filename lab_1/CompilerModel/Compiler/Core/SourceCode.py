from Compiler.Interfaces import ICodeProvider
from Compiler.Models import ProgrammingLanguage


class SourceCode(ICodeProvider):
    """Исходный код программы"""

    def __init__(self, content: str, language: ProgrammingLanguage):
        self._content = content
        self._language = language
        self._lines = content.split('\n')

    def get_code(self) -> str:
        return self._content

    def set_code(self, code: str) -> None:
        self._content = code
        self._lines = code.split('\n')

    def get_language(self) -> ProgrammingLanguage:
        return self._language

    def get_line(self, line_number: int) -> str:
        if 0 <= line_number < len(self._lines):
            return self._lines[line_number]
        return ""