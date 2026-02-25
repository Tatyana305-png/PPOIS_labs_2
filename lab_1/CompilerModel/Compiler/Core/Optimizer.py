from typing import Dict, Optional
from Compiler.Interfaces import IOptimizer
from Compiler.Models import ASTNode


class Optimizer(IOptimizer):
    """Оптимизатор кода"""

    def __init__(self, optimization_level: int = 1):
        self.optimization_level = optimization_level

    def optimize(self, ast: ASTNode) -> ASTNode:
        """
        Выполняет оптимизацию AST
        """
        if self.optimization_level <= 0:
            return ast

        # Копируем AST для оптимизации
        optimized = self._copy_ast(ast)

        # Применяем оптимизации в зависимости от уровня
        if self.optimization_level >= 1:
            optimized = self._constant_folding(optimized)
            optimized = self._dead_code_elimination(optimized)

        if self.optimization_level >= 2:
            optimized = self._constant_propagation(optimized)
            # Снова применяем constant_folding после propagation
            optimized = self._constant_folding(optimized)
            optimized = self._strength_reduction(optimized)

        return optimized

    def _copy_ast(self, node: ASTNode) -> ASTNode:
        """Создает копию узла AST"""
        return ASTNode(
            type=node.type,
            value=node.value,
            children=[self._copy_ast(child) for child in node.children],
            line=node.line,
            column=node.column
        )

    def _constant_folding(self, node: ASTNode) -> ASTNode:
        """
        Сворачивает константные выражения
        """
        if node.type == "BinaryOperation":
            node.children = [self._constant_folding(child) for child in node.children]

            if (len(node.children) == 2 and
                    node.children[0].type == "Number" and
                    node.children[1].type == "Number"):

                try:
                    left = float(node.children[0].value)
                    right = float(node.children[1].value)

                    if node.value == '+':
                        result = left + right
                    elif node.value == '-':
                        result = left - right
                    elif node.value == '*':
                        result = left * right
                    elif node.value == '/':
                        if right != 0:
                            result = left / right
                        else:
                            return node
                    elif node.value in ['==', '!=', '<', '>', '<=', '>=']:
                        if node.value == '==':
                            result = 1 if left == right else 0
                        elif node.value == '!=':
                            result = 1 if left != right else 0
                        elif node.value == '<':
                            result = 1 if left < right else 0
                        elif node.value == '>':
                            result = 1 if left > right else 0
                        elif node.value == '<=':
                            result = 1 if left <= right else 0
                        elif node.value == '>=':
                            result = 1 if left >= right else 0
                        else:
                            return node
                    else:
                        return node

                    return ASTNode(
                        type="Number",
                        value=str(int(result)) if result.is_integer() else str(result),
                        children=[],
                        line=node.line,
                        column=node.column
                    )
                except (ValueError, ZeroDivisionError):
                    pass
        else:
            node.children = [self._constant_folding(child) for child in node.children]

        return node

    def _dead_code_elimination(self, node: ASTNode) -> ASTNode:
        """
        Удаляет мертвый код
        """
        if node.type == "IfStatement":
            condition = node.children[0]
            then_branch = node.children[1]
            else_branch = node.children[2] if len(node.children) > 2 else None

            # Если условие - константа
            if condition.type == "Number":
                try:
                    if float(condition.value) != 0:
                        # Всегда истинно - оставляем только then
                        result = self._dead_code_elimination(then_branch)
                        # Если результат - блок с одним оператором, можем его упростить
                        if result.type == "Block" and len(result.children) == 1:
                            return result.children[0]
                        return result
                    else:
                        # Всегда ложно - оставляем else если есть
                        if else_branch:
                            result = self._dead_code_elimination(else_branch)
                            if result.type == "Block" and len(result.children) == 1:
                                return result.children[0]
                            return result
                        else:
                            return ASTNode(
                                type="EmptyStatement",
                                value=None,
                                children=[],
                                line=node.line,
                                column=node.column
                            )
                except ValueError:
                    pass

        elif node.type == "Block":
            # Обрабатываем каждый оператор в блоке
            new_children = []
            for child in node.children:
                optimized_child = self._dead_code_elimination(child)
                if optimized_child.type != "EmptyStatement":
                    new_children.append(optimized_child)

            if len(new_children) == 1:
                # Если в блоке остался один оператор, возвращаем его напрямую
                return new_children[0]
            elif len(new_children) == 0:
                return ASTNode(
                    type="EmptyStatement",
                    value=None,
                    children=[],
                    line=node.line,
                    column=node.column
                )
            else:
                node.children = new_children
                return node

        # Рекурсивно обрабатываем детей
        node.children = [self._dead_code_elimination(child) for child in node.children
                         if child.type != "EmptyStatement"]

        return node

    def _constant_propagation(self, node: ASTNode) -> ASTNode:
        """
        Распространяет константы
        """
        constants: Dict[str, str] = {}

        def propagate(current_node: ASTNode, consts: Dict[str, str]) -> ASTNode:
            if current_node.type == "Declaration":
                if current_node.children:
                    init = propagate(current_node.children[0], consts)
                    if init.type == "Number":
                        consts[current_node.value] = init.value
                    current_node.children = [init]

            elif current_node.type == "Identifier":
                if current_node.value in consts:
                    return ASTNode(
                        type="Number",
                        value=consts[current_node.value],
                        children=[],
                        line=current_node.line,
                        column=current_node.column
                    )

            current_node.children = [propagate(child, consts.copy())
                                     for child in current_node.children]

            return current_node

        return propagate(node, constants)

    def _strength_reduction(self, node: ASTNode) -> ASTNode:
        """
        Уменьшение силы операций
        """
        if node.type == "BinaryOperation":
            node.children = [self._strength_reduction(child) for child in node.children]

            if node.value == '*':
                # Проверяем умножение на 2
                if (node.children[0].type == "Number" and node.children[0].value == "2" and
                        node.children[1].type != "Number"):
                    # a * 2 -> a + a
                    return ASTNode(
                        type="BinaryOperation",
                        value='+',
                        children=[node.children[1], self._copy_ast(node.children[1])],
                        line=node.line,
                        column=node.column
                    )
                elif (node.children[1].type == "Number" and node.children[1].value == "2" and
                      node.children[0].type != "Number"):
                    # 2 * a -> a + a
                    return ASTNode(
                        type="BinaryOperation",
                        value='+',
                        children=[node.children[0], self._copy_ast(node.children[0])],
                        line=node.line,
                        column=node.column
                    )

        return node