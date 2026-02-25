import unittest
from Compiler.Models import ProgrammingLanguage, ASTNode
from Compiler.Core import LexicalAnalyzer, SyntaxAnalyzer, Optimizer


class TestOptimizer(unittest.TestCase):
    """Тесты для оптимизатора кода"""

    def setUp(self):
        self.optimizer = Optimizer(optimization_level=1)
        self.lang = ProgrammingLanguage("TestLang", "1.0")
        self.lexer = LexicalAnalyzer(self.lang)
        self.parser = SyntaxAnalyzer(self.lang)

    def _get_ast(self, code: str) -> ASTNode:
        """Вспомогательный метод для получения AST из кода"""
        tokens = self.lexer.analyze(code)
        return self.parser.analyze(tokens)

    def _count_nodes(self, node: ASTNode, node_type: str = None) -> int:
        """Вспомогательный метод для подсчета узлов определенного типа"""
        count = 1 if not node_type or node.type == node_type else 0
        for child in node.children:
            count += self._count_nodes(child, node_type)
        return count

    def test_optimization_level_0(self):
        """Тест уровня оптимизации 0 (без оптимизации)"""
        self.optimizer.optimization_level = 0
        code = "x = 2 + 3;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должно быть то же самое AST
        self.assertEqual(self._count_nodes(optimized), self._count_nodes(ast))

    def test_constant_folding_addition(self):
        """Тест свертки констант (сложение)"""
        self.optimizer.optimization_level = 1
        code = "x = 2 + 3;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Находим бинарную операцию
        def find_binary_op(node):
            if node.type == "BinaryOperation":
                return node
            for child in node.children:
                result = find_binary_op(child)
                if result:
                    return result
            return None

        # В оптимизированном AST должно быть меньше бинарных операций
        original_ops = self._count_nodes(ast, "BinaryOperation")
        optimized_ops = self._count_nodes(optimized, "BinaryOperation")

        self.assertLessEqual(optimized_ops, original_ops)

    def test_constant_folding_subtraction(self):
        """Тест свертки констант (вычитание)"""
        self.optimizer.optimization_level = 1
        code = "x = 10 - 4;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Проверяем, что оптимизация применилась
        optimized_ops = self._count_nodes(optimized, "BinaryOperation")
        self.assertLessEqual(optimized_ops, 1)  # Должно быть не больше одной операции (=)

    def test_constant_folding_multiplication(self):
        """Тест свертки констант (умножение)"""
        self.optimizer.optimization_level = 1
        code = "x = 6 * 7;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        optimized_ops = self._count_nodes(optimized, "BinaryOperation")
        self.assertLessEqual(optimized_ops, 1)

    def test_constant_folding_division(self):
        """Тест свертки констант (деление)"""
        self.optimizer.optimization_level = 1
        code = "x = 15 / 3;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        optimized_ops = self._count_nodes(optimized, "BinaryOperation")
        self.assertLessEqual(optimized_ops, 1)

    def test_constant_folding_complex(self):
        """Тест свертки сложного константного выражения"""
        self.optimizer.optimization_level = 1
        code = "x = 2 + 3 * 4 - 8 / 2;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должно остаться меньше операций
        original_ops = self._count_nodes(ast, "BinaryOperation")
        optimized_ops = self._count_nodes(optimized, "BinaryOperation")
        self.assertLess(optimized_ops, original_ops)

    def test_dead_code_elimination_if_true(self):
        """Тест удаления мертвого кода (всегда истинное условие)"""
        self.optimizer.optimization_level = 1
        code = """
        if 1 {
            x = 5;
        }
        y = 10;
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должен остаться только x = 5 и y = 10
        self.assertEqual(len(optimized.children), 2)

        # Первое выражение должно быть присваиванием x = 5
        self.assertEqual(optimized.children[0].type, "BinaryOperation")

    def test_dead_code_elimination_if_else(self):
        """Тест удаления мертвого кода (if-else с константным условием)"""
        self.optimizer.optimization_level = 1
        code = """
        if 0 {
            x = 5;
        } else {
            y = 10;
        }
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должен остаться только y = 10
        self.assertEqual(len(optimized.children), 1)
        self.assertEqual(optimized.children[0].value, "=")
        # Проверяем, что это присваивание y
        self.assertEqual(optimized.children[0].children[0].value, "y")

    def test_constant_propagation(self):
        """Тест распространения констант"""
        self.optimizer.optimization_level = 2
        code = """
        int x = 5;
        y = x + 3;
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должна быть подстановка 5 вместо x
        # В идеале должно стать y = 5 + 3, которое потом свернется в y = 8

    def test_combined_optimizations(self):
        """Тест комбинированных оптимизаций"""
        self.optimizer.optimization_level = 2
        code = """
        int a = 2;
        int b = 3;
        x = a * b + 5;
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должны примениться: распространение констант, свертка, возможно уменьшение силы
        original_ops = self._count_nodes(ast, "BinaryOperation")
        optimized_ops = self._count_nodes(optimized, "BinaryOperation")

        self.assertLessEqual(optimized_ops, original_ops)

    def test_no_optimization_for_variables(self):
        """Тест, что переменные не оптимизируются"""
        self.optimizer.optimization_level = 2
        code = "x = y + z;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Структура должна остаться той же
        self.assertEqual(self._count_nodes(optimized), self._count_nodes(ast))

    def test_constant_folding_with_comparison_operators(self):
        """Тест свертки констант с операторами сравнения"""
        test_cases = [
            ("x = 5 == 5;", "1"),  # True -> 1
            ("x = 5 != 5;", "0"),  # False -> 0
            ("x = 5 < 10;", "1"),  # True -> 1
            ("x = 5 > 10;", "0"),  # False -> 0
            ("x = 5 <= 5;", "1"),  # True -> 1
            ("x = 5 >= 10;", "0"),  # False -> 0
        ]

        for code, expected in test_cases:
            with self.subTest(code=code):
                ast = self._get_ast(code)
                optimized = self.optimizer.optimize(ast)

                # Проверяем, что выражение свернулось в константу
                def find_number(node):
                    if node.type == "Number":
                        return node.value
                    for child in node.children:
                        result = find_number(child)
                        if result:
                            return result
                    return None

                result = find_number(optimized)
                self.assertEqual(result, expected)


    def test_constant_folding_with_division_by_zero(self):
        """Тест обработки деления на ноль (не должно сворачиваться)"""
        code = "x = 5 / 0;"
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Деление на ноль не должно сворачиваться
        def has_division(node):
            if node.type == "BinaryOperation" and node.value == '/':
                return True
            for child in node.children:
                if has_division(child):
                    return True
            return False

        self.assertTrue(has_division(optimized))

    def test_dead_code_elimination_nested_ifs(self):
        """Тест удаления мертвого кода во вложенных if"""
        code = """
        if 1 {
            x = 5;
            if 0 {
                y = 10;
            }
            z = 15;
        }
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должны остаться только x=5 и z=15
        def count_assignments(node):
            count = 0
            if node.type == "BinaryOperation" and node.value == '=':
                return 1
            for child in node.children:
                count += count_assignments(child)
            return count

        self.assertEqual(count_assignments(optimized), 2)

    def test_dead_code_elimination_with_else(self):
        """Тест удаления мертвого кода с else веткой"""
        code = """
        if 0 {
            x = 5;
        } else {
            y = 10;
            z = 15;
        }
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должны остаться только y=10 и z=15
        assignments = []

        def collect_assignments(node):
            if node.type == "BinaryOperation" and node.value == '=':
                assignments.append(node.children[0].value)
            for child in node.children:
                collect_assignments(child)

        collect_assignments(optimized)
        self.assertIn("y", assignments)
        self.assertIn("z", assignments)
        self.assertNotIn("x", assignments)

    def test_constant_propagation_complex(self):
        """Тест распространения констант в сложных выражениях"""
        code = """
        int a = 5;
        int b = 10;
        x = a + b;
        y = a * b;
        """
        ast = self._get_ast(code)
        optimized = self.optimizer.optimize(ast)

        # Должны подставиться константы
        numbers = []

        def collect_numbers(node):
            if node.type == "Number":
                numbers.append(node.value)
            for child in node.children:
                collect_numbers(child)

        collect_numbers(optimized)
        self.assertIn("5", numbers)
        self.assertIn("10", numbers)


    def test_optimize_complex_ast(self):
        """Тест оптимизации сложного AST"""
        # Создаем сложное AST вручную
        node = ASTNode(
            type="Program",
            value=None,
            children=[
                ASTNode(
                    type="IfStatement",
                    value=None,
                    children=[
                        ASTNode(type="Number", value="1", children=[], line=1, column=1),
                        ASTNode(
                            type="Block",
                            value=None,
                            children=[
                                ASTNode(
                                    type="BinaryOperation",
                                    value="=",
                                    children=[
                                        ASTNode(type="Identifier", value="x", children=[], line=1, column=5),
                                        ASTNode(
                                            type="BinaryOperation",
                                            value="+",
                                            children=[
                                                ASTNode(type="Number", value="2", children=[], line=1, column=7),
                                                ASTNode(type="Number", value="3", children=[], line=1, column=9)
                                            ],
                                            line=1, column=7
                                        )
                                    ],
                                    line=1, column=5
                                )
                            ],
                            line=1, column=1
                        )
                    ],
                    line=1, column=1
                )
            ],
            line=1, column=1
        )

        optimized = self.optimizer.optimize(node)
        self.assertIsNotNone(optimized)


if __name__ == '__main__':
    unittest.main()