import unittest
from Compiler.Models import ProgrammingLanguage, TokenType
from Compiler.Core import LexicalAnalyzer


class TestLexicalAnalyzer(unittest.TestCase):
    """Тесты для лексического анализатора"""

    def setUp(self):
        self.lang = ProgrammingLanguage("TestLang", "1.0")
        self.analyzer = LexicalAnalyzer(self.lang)

    def test_empty_code(self):
        """Тест анализа пустого кода"""
        tokens = self.analyzer.analyze("")
        self.assertEqual(len(tokens), 0)

    def test_whitespace_only(self):
        """Тест кода только с пробелами"""
        tokens = self.analyzer.analyze("   \n  \t  ")
        self.assertEqual(len(tokens), 0)

    def test_numbers(self):
        """Тест анализа чисел"""
        tokens = self.analyzer.analyze("123 45.67 0 3.14")
        self.assertEqual(len(tokens), 4)

        # Проверяем первое число
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, "123")
        self.assertEqual(tokens[0].line, 1)

        # Проверяем число с плавающей точкой
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, "45.67")

        # Проверяем ноль
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, "0")

        # Проверяем еще одно число с точкой
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].value, "3.14")

    def test_keywords_and_identifiers(self):
        """Тест анализа ключевых слов и идентификаторов"""
        tokens = self.analyzer.analyze("if x while y int variable")
        self.assertEqual(len(tokens), 6)

        # Проверяем ключевые слова
        self.assertEqual(tokens[0].type, TokenType.KEYWORD)
        self.assertEqual(tokens[0].value, "if")

        self.assertEqual(tokens[2].type, TokenType.KEYWORD)
        self.assertEqual(tokens[2].value, "while")

        self.assertEqual(tokens[4].type, TokenType.KEYWORD)
        self.assertEqual(tokens[4].value, "int")

        # Проверяем идентификаторы
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "x")

        self.assertEqual(tokens[3].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[3].value, "y")

        self.assertEqual(tokens[5].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[5].value, "variable")

    def test_operators(self):
        """Тест анализа операторов"""
        tokens = self.analyzer.analyze("a + b - c * d / e = f == g != h < i > j")
        self.assertEqual(len(tokens), 19)  # 10 идентификаторов + 9 операторов

        # Проверяем позиции операторов
        operator_positions = [1, 3, 5, 7, 9, 11, 13, 15, 17]
        operator_values = ['+', '-', '*', '/', '=', '==', '!=', '<', '>']

        for pos, expected_value in zip(operator_positions, operator_values):
            self.assertEqual(tokens[pos].type, TokenType.OPERATOR)
            self.assertEqual(tokens[pos].value, expected_value)

    def test_comments(self):
        """Тест анализа комментариев"""
        tokens = self.analyzer.analyze("x = 5 // это комментарий\n y = 10")

        # Должны быть: x, =, 5, комментарий, y, =, 10
        self.assertEqual(len(tokens), 7)

        # Проверяем комментарий
        self.assertEqual(tokens[3].type, TokenType.COMMENT)
        self.assertTrue(tokens[3].value.startswith("//"))
        self.assertEqual(tokens[3].value, "// это комментарий")
        self.assertEqual(tokens[3].line, 1)

    def test_strings(self):
        """Тест анализа строк"""
        tokens = self.analyzer.analyze('x = "hello world" y = "test"')

        # Должны быть: x, =, строка, y, =, строка
        self.assertEqual(len(tokens), 6)

        # Проверяем первую строку
        self.assertEqual(tokens[2].type, TokenType.STRING)
        self.assertEqual(tokens[2].value, '"hello world"')

        # Проверяем вторую строку
        self.assertEqual(tokens[5].type, TokenType.STRING)
        self.assertEqual(tokens[5].value, '"test"')

    def test_multiline_code(self):
        """Тест анализа многострочного кода"""
        code = """
        int x = 5;
        if x > 0 {
            y = x + 1;
        }
        """
        tokens = self.analyzer.analyze(code)

        # Проверяем, что строки определены правильно
        for token in tokens:
            self.assertGreater(token.line, 0)
            self.assertGreater(token.column, 0)

    def test_unknown_characters(self):
        """Тест обработки неизвестных символов"""
        tokens = self.analyzer.analyze("x @ $ %")

        # Должны быть: x, @, $, %
        self.assertEqual(len(tokens), 4)

        # Проверяем неизвестные символы
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].type, TokenType.UNKNOWN)
        self.assertEqual(tokens[1].value, "@")
        self.assertEqual(tokens[2].type, TokenType.UNKNOWN)
        self.assertEqual(tokens[2].value, "$")
        self.assertEqual(tokens[3].type, TokenType.UNKNOWN)
        self.assertEqual(tokens[3].value, "%")

    def test_line_and_column_numbers(self):
        """Тест правильности номеров строк и колонок"""
        code = "x = 5\ny = 10"
        tokens = self.analyzer.analyze(code)

        # Проверяем позиции
        self.assertEqual(tokens[0].line, 1)  # x
        self.assertEqual(tokens[0].column, 1)

        self.assertEqual(tokens[1].line, 1)  # =
        self.assertEqual(tokens[1].column, 3)

        self.assertEqual(tokens[2].line, 1)  # 5
        self.assertEqual(tokens[2].column, 5)

        self.assertEqual(tokens[3].line, 2)  # y
        self.assertEqual(tokens[3].column, 1)

        self.assertEqual(tokens[4].line, 2)  # =
        self.assertEqual(tokens[4].column, 3)

        self.assertEqual(tokens[5].line, 2)  # 10
        self.assertEqual(tokens[5].column, 5)


if __name__ == '__main__':
    unittest.main()