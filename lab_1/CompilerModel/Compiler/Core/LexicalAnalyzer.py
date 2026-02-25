from typing import List
from Compiler.Interfaces import IAnalyzer
from Compiler.Models import ProgrammingLanguage, Token, TokenType
from Compiler.Exceptions import LexicalError


class LexicalAnalyzer(IAnalyzer):
    """Лексический анализатор"""

    def __init__(self, language: ProgrammingLanguage):
        self._language = language

    def analyze(self, code: str) -> List[Token]:
        """
        Выполняет лексический анализ исходного кода
        Возвращает список токенов
        """
        tokens: List[Token] = []
        lines = code.split('\n')

        for line_num, line in enumerate(lines, 1):
            col = 1
            i = 0
            while i < len(line):
                # Пропускаем пробелы
                if line[i].isspace():
                    i += 1
                    col += 1
                    continue

                # Проверяем комментарии
                if i + 1 < len(line) and line[i:i + 2] == '//':
                    token = Token(TokenType.COMMENT, line[i:], line_num, col)
                    tokens.append(token)
                    break

                # Проверяем числа
                if line[i].isdigit() or (line[i] == '.' and i + 1 < len(line) and line[i + 1].isdigit()):
                    j = i
                    has_dot = False
                    while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                        if line[j] == '.':
                            if has_dot:
                                break
                            has_dot = True
                        j += 1
                    token = Token(TokenType.NUMBER, line[i:j], line_num, col)
                    tokens.append(token)
                    i = j
                    col += len(token.value)
                    continue

                # Проверяем строки
                if line[i] == '"':
                    j = i + 1
                    while j < len(line) and line[j] != '"':
                        j += 1
                    if j < len(line):
                        token = Token(TokenType.STRING, line[i:j + 1], line_num, col)
                        tokens.append(token)
                        i = j + 1
                        col += len(token.value)
                        continue
                    else:
                        token = Token(TokenType.UNKNOWN, line[i:], line_num, col)
                        tokens.append(token)
                        break

                # Проверяем двухсимвольные операторы
                if i + 1 < len(line) and line[i:i + 2] in ['==', '!=', '<=', '>=', '&&', '||']:
                    token = Token(TokenType.OPERATOR, line[i:i + 2], line_num, col)
                    tokens.append(token)
                    i += 2
                    col += 2
                    continue

                # Проверяем односимвольные операторы
                if line[i] in '+-*/=<>!&|':
                    token = Token(TokenType.OPERATOR, line[i], line_num, col)
                    tokens.append(token)
                    i += 1
                    col += 1
                    continue

                # Проверяем разделители - ВАЖНО: делаем это ДО проверки идентификаторов
                if line[i] in ';,(){}[]':
                    token = Token(TokenType.SEPARATOR, line[i], line_num, col)
                    tokens.append(token)
                    i += 1
                    col += 1
                    continue

                # Обрабатываем идентификаторы и ключевые слова
                if line[i].isalpha() or line[i] == '_':
                    j = i
                    while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                        j += 1
                    word = line[i:j]

                    # Проверяем, не является ли слово ключевым
                    if self._language.is_keyword(word):
                        token = Token(TokenType.KEYWORD, word, line_num, col)
                    else:
                        token = Token(TokenType.IDENTIFIER, word, line_num, col)

                    tokens.append(token)
                    i = j
                    col += len(word)
                    continue

                # Неизвестный символ
                token = Token(TokenType.UNKNOWN, line[i], line_num, col)
                tokens.append(token)
                i += 1
                col += 1

        return tokens