import unittest
from Compiler.Models import ProgrammingLanguage


class TestProgrammingLanguage(unittest.TestCase):
    """Тесты для класса ProgrammingLanguage"""

    def setUp(self):
        self.lang = ProgrammingLanguage("TestLang", "1.0")

    def test_initialization(self):
        """Тест инициализации языка программирования"""
        self.assertEqual(self.lang.name, "TestLang")
        self.assertEqual(self.lang.version, "1.0")
        self.assertIn("if", self.lang.keywords)
        self.assertIn("+", self.lang.operators)
        self.assertIn(";", self.lang.separators)

    def test_get_name(self):
        """Тест получения имени языка"""
        self.assertEqual(self.lang.get_name(), "TestLang")

    def test_is_keyword(self):
        """Тест проверки ключевых слов"""
        self.assertTrue(self.lang.is_keyword("if"))
        self.assertTrue(self.lang.is_keyword("while"))
        self.assertTrue(self.lang.is_keyword("return"))
        self.assertTrue(self.lang.is_keyword("int"))
        self.assertTrue(self.lang.is_keyword("float"))
        self.assertFalse(self.lang.is_keyword("variable"))
        self.assertFalse(self.lang.is_keyword("123"))
        self.assertFalse(self.lang.is_keyword("+"))

    def test_is_operator(self):
        """Тест проверки операторов"""
        self.assertTrue(self.lang.is_operator("+"))
        self.assertTrue(self.lang.is_operator("-"))
        self.assertTrue(self.lang.is_operator("*"))
        self.assertTrue(self.lang.is_operator("/"))
        self.assertTrue(self.lang.is_operator("="))
        self.assertTrue(self.lang.is_operator("=="))
        self.assertTrue(self.lang.is_operator("!="))
        self.assertTrue(self.lang.is_operator("<"))
        self.assertTrue(self.lang.is_operator(">"))
        self.assertFalse(self.lang.is_operator("a"))
        self.assertFalse(self.lang.is_operator("if"))
        self.assertFalse(self.lang.is_operator(";"))

    def test_is_separator(self):
        """Тест проверки разделителей"""
        self.assertTrue(self.lang.is_separator(";"))
        self.assertTrue(self.lang.is_separator(","))
        self.assertTrue(self.lang.is_separator("("))
        self.assertTrue(self.lang.is_separator(")"))
        self.assertTrue(self.lang.is_separator("{"))
        self.assertTrue(self.lang.is_separator("}"))
        self.assertFalse(self.lang.is_separator("x"))
        self.assertFalse(self.lang.is_separator("+"))
        self.assertFalse(self.lang.is_separator("if"))

    def test_string_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.lang), "TestLang 1.0")


if __name__ == '__main__':
    unittest.main()