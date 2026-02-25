import unittest
from Compiler.Core import SourceCode
from Compiler.Models import ProgrammingLanguage


class TestSourceCodeExtra(unittest.TestCase):
    """Дополнительные тесты для SourceCode"""

    def setUp(self):
        self.lang = ProgrammingLanguage("TestLang", "1.0")
        self.code = "line1\nline2\nline3"
        self.source = SourceCode(self.code, self.lang)

    def test_get_line_existing(self):
        """Тест получения существующей строки"""
        self.assertEqual(self.source.get_line(0), "line1")
        self.assertEqual(self.source.get_line(1), "line2")
        self.assertEqual(self.source.get_line(2), "line3")

    def test_get_line_out_of_range(self):
        """Тест получения несуществующей строки"""
        self.assertEqual(self.source.get_line(-1), "")
        self.assertEqual(self.source.get_line(3), "")
        self.assertEqual(self.source.get_line(100), "")

    def test_set_code_updates_lines(self):
        """Тест обновления кода"""
        new_code = "new line 1\nnew line 2"
        self.source.set_code(new_code)

        self.assertEqual(self.source.get_line(0), "new line 1")
        self.assertEqual(self.source.get_line(1), "new line 2")
        self.assertEqual(self.source.get_code(), new_code)

    def test_get_language(self):
        """Тест получения языка"""
        self.assertEqual(self.source.get_language(), self.lang)

    def test_empty_lines(self):
        """Тест с пустыми строками"""
        source = SourceCode("", self.lang)
        self.assertEqual(source.get_line(0), "")
        self.assertEqual(source.get_line(1), "")


if __name__ == '__main__':
    unittest.main()