import unittest
from Compiler.Models import ProgrammingLanguage, TokenType, ASTNode
from Compiler.Core import LexicalAnalyzer, SyntaxAnalyzer
from Compiler.Exceptions import SyntaxError


class TestSyntaxAnalyzer(unittest.TestCase):
    """Тесты для синтаксического анализатора"""

    def setUp(self):
        self.lang = ProgrammingLanguage("TestLang", "1.0")
        self.lexer = LexicalAnalyzer(self.lang)
        self.parser = SyntaxAnalyzer(self.lang)

    def test_empty_program(self):
        """Тест анализа пустой программы"""
        tokens = self.lexer.analyze("")
        ast = self.parser.analyze(tokens)

        self.assertEqual(ast.type, "Program")
        self.assertEqual(len(ast.children), 0)

    def test_simple_expression(self):
        """Тест анализа простого выражения"""
        code = "x = 5 + 3;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        self.assertEqual(ast.type, "Program")
        self.assertEqual(len(ast.children), 1)

        # Проверяем структуру выражения
        expr = ast.children[0]
        self.assertEqual(expr.type, "BinaryOperation")
        self.assertEqual(expr.value, "=")
        self.assertEqual(len(expr.children), 2)

    def test_multiple_statements(self):
        """Тест анализа нескольких выражений"""
        code = """
        x = 5;
        y = 10;
        z = x + y;
        """
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        self.assertEqual(len(ast.children), 3)

    def test_if_statement(self):
        """Тест анализа условного оператора if"""
        code = "if x > 5 y = 10;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        self.assertEqual(ast.type, "Program")
        self.assertEqual(len(ast.children), 1)

        if_stmt = ast.children[0]
        self.assertEqual(if_stmt.type, "IfStatement")
        self.assertEqual(len(if_stmt.children), 2)  # condition и then

        # Проверяем условие
        condition = if_stmt.children[0]
        self.assertEqual(condition.type, "BinaryOperation")
        self.assertEqual(condition.value, ">")

    def test_if_else_statement(self):
        """Тест анализа условного оператора if-else"""
        code = "if x > 5 y = 10; else y = 0;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        if_stmt = ast.children[0]
        self.assertEqual(if_stmt.type, "IfStatement")
        self.assertEqual(len(if_stmt.children), 3)  # condition, then, else

        # Проверяем else ветку
        else_branch = if_stmt.children[2]
        self.assertIsNotNone(else_branch)

    def test_if_statement_with_braces(self):
        """Тест анализа if с блоком кода"""
        code = "if x > 5 { y = 10; z = 20; }"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        if_stmt = ast.children[0]
        then_branch = if_stmt.children[1]

        # Проверяем, что then_branch - это составное выражение
        # В нашей реализации блок кода будет представлен несколькими выражениями
        self.assertIsNotNone(then_branch)

    def test_while_statement(self):
        """Тест анализа цикла while"""
        code = "while i < 10 i = i + 1;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        while_stmt = ast.children[0]
        self.assertEqual(while_stmt.type, "WhileStatement")
        self.assertEqual(len(while_stmt.children), 2)  # condition и body

        # Проверяем условие
        condition = while_stmt.children[0]
        self.assertEqual(condition.type, "BinaryOperation")
        self.assertEqual(condition.value, "<")

    def test_return_statement(self):
        """Тест анализа оператора return"""
        code = "return x + 5;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        return_stmt = ast.children[0]
        self.assertEqual(return_stmt.type, "ReturnStatement")
        self.assertEqual(len(return_stmt.children), 1)

        # Проверяем возвращаемое значение
        value = return_stmt.children[0]
        self.assertEqual(value.type, "BinaryOperation")

    def test_return_without_value(self):
        """Тест анализа return без значения"""
        code = "return;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        return_stmt = ast.children[0]
        self.assertEqual(return_stmt.type, "ReturnStatement")
        self.assertEqual(return_stmt.value, None)
        self.assertEqual(len(return_stmt.children), 0)

    def test_declaration(self):
        """Тест анализа объявления переменной"""
        code = "int x = 5;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        decl = ast.children[0]
        self.assertEqual(decl.type, "Declaration")
        self.assertEqual(decl.value, "x")
        self.assertEqual(len(decl.children), 1)

        # Проверяем инициализатор
        init = decl.children[0]
        self.assertEqual(init.type, "Number")
        self.assertEqual(init.value, "5")

    def test_declaration_without_initializer(self):
        """Тест анализа объявления переменной без инициализации"""
        code = "int x;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        decl = ast.children[0]
        self.assertEqual(decl.type, "Declaration")
        self.assertEqual(decl.value, "x")
        self.assertEqual(len(decl.children), 0)

    def test_complex_expression(self):
        """Тест анализа сложного выражения"""
        code = "x = (a + b) * c - d / e;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        # Проверяем, что выражение распарсилось без ошибок
        self.assertEqual(ast.type, "Program")
        self.assertEqual(len(ast.children), 1)

    def test_nested_structures(self):
        """Тест анализа вложенных структур"""
        code = """
        if x > 0 {
            while y < 10 {
                y = y + 1;
                if y == 5 {
                    return y;
                }
            }
        }
        """
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        # Проверяем, что вложенные структуры распарсились
        self.assertEqual(ast.type, "Program")
        self.assertEqual(len(ast.children), 1)

    def test_missing_parenthesis_error(self):
        """Тест ошибки при пропущенной скобке"""
        code = "if (x > 5 y = 10;"  # Пропущена )
        tokens = self.lexer.analyze(code)

        with self.assertRaises(SyntaxError) as context:
            self.parser.analyze(tokens)

        self.assertIn("Ожидалась закрывающая скобка", str(context.exception))

    def test_invalid_expression_error(self):
        """Тест ошибки при некорректном выражении"""
        code = "x = + 5;"  # Некорректное выражение
        tokens = self.lexer.analyze(code)

        with self.assertRaises(SyntaxError):
            self.parser.analyze(tokens)

    def test_ast_node_properties(self):
        """Тест свойств узлов AST"""
        code = "x = 42;"
        tokens = self.lexer.analyze(code)
        ast = self.parser.analyze(tokens)

        # Проверяем, что у узлов есть все необходимые свойства
        def check_node(node: ASTNode):
            self.assertTrue(hasattr(node, 'type'))
            self.assertTrue(hasattr(node, 'value'))
            self.assertTrue(hasattr(node, 'children'))
            self.assertTrue(hasattr(node, 'line'))
            self.assertTrue(hasattr(node, 'column'))

            for child in node.children:
                check_node(child)

        check_node(ast)


if __name__ == '__main__':
    unittest.main()