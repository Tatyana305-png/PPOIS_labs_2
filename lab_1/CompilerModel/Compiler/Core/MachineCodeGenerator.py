from typing import Dict
from Compiler.Interfaces import ICodeGenerator
from Compiler.Models import ASTNode, MachineCode, Instruction


class MachineCodeGenerator(ICodeGenerator):
    """Генератор машинного кода"""

    def __init__(self, target_architecture: str = "x86"):
        self.target_architecture = target_architecture
        self._current_address = 0
        self._labels: Dict[str, int] = {}

    def generate(self, ast: ASTNode) -> MachineCode:
        """
        Генерирует машинный код из AST
        """
        machine_code = MachineCode()
        self._current_address = 0
        self._labels.clear()

        # Генерируем код
        self._generate_node(ast, machine_code)

        return machine_code

    def _generate_node(self, node: ASTNode, code: MachineCode) -> str:
        """
        Генерирует код для узла AST
        Возвращает имя регистра или метку с результатом
        """
        if node.type == "Program":
            for child in node.children:
                self._generate_node(child, code)

        elif node.type == "Declaration":
            # Выделяем память для переменной
            if node.value:
                # В реальном компиляторе здесь было бы выделение памяти
                # Для простоты просто запоминаем переменную
                pass

            if node.children:
                # Генерируем код для инициализатора
                result = self._generate_node(node.children[0], code)
                # Сохраняем результат в переменную
                code.add_instruction(Instruction("MOV", [f"[{node.value}]", result]))

        elif node.type == "BinaryOperation":
            # Генерируем код для левого операнда
            left = self._generate_node(node.children[0], code)
            # Генерируем код для правого операнда
            right = self._generate_node(node.children[1], code)

            # Выполняем операцию
            if node.value == '+':
                code.add_instruction(Instruction("ADD", [left, right]))
                return left
            elif node.value == '-':
                code.add_instruction(Instruction("SUB", [left, right]))
                return left
            elif node.value == '*':
                code.add_instruction(Instruction("MUL", [left, right]))
                return left
            elif node.value == '/':
                code.add_instruction(Instruction("DIV", [left, right]))
                return left
            elif node.value == '==':
                code.add_instruction(Instruction("CMP", [left, right]))
                # Генерируем метку для результата
                result_label = f"cmp_result_{len(self._labels)}"
                self._labels[result_label] = self._current_address
                code.add_instruction(Instruction("SETE", [result_label]))
                return result_label

        elif node.type == "Number":
            # Загружаем число в регистр
            reg = f"R{len(code.instructions) % 8}"
            code.add_instruction(Instruction("MOV", [reg, node.value]))
            return reg

        elif node.type == "Identifier":
            # Загружаем переменную в регистр
            reg = f"R{len(code.instructions) % 8}"
            code.add_instruction(Instruction("MOV", [reg, f"[{node.value}]"]))
            return reg

        elif node.type == "IfStatement":
            condition = node.children[0]
            then_branch = node.children[1]
            else_branch = node.children[2] if len(node.children) > 2 else None

            # Генерируем условие
            cond_result = self._generate_node(condition, code)

            # Создаем метки
            else_label = f"else_{len(self._labels)}"
            end_label = f"endif_{len(self._labels)}"

            # Условный переход
            code.add_instruction(Instruction("CMP", [cond_result, "0"]))
            code.add_instruction(Instruction("JE", [else_label]))

            # Then ветка
            self._generate_node(then_branch, code)
            code.add_instruction(Instruction("JMP", [end_label]))

            # Else ветка
            self._labels[else_label] = self._current_address
            if else_branch:
                self._generate_node(else_branch, code)

            # Конец if
            self._labels[end_label] = self._current_address

        elif node.type == "WhileStatement":
            condition = node.children[0]
            body = node.children[1]

            # Создаем метки
            start_label = f"while_start_{len(self._labels)}"
            end_label = f"while_end_{len(self._labels)}"

            self._labels[start_label] = self._current_address

            # Проверяем условие
            cond_result = self._generate_node(condition, code)
            code.add_instruction(Instruction("CMP", [cond_result, "0"]))
            code.add_instruction(Instruction("JE", [end_label]))

            # Тело цикла
            self._generate_node(body, code)
            code.add_instruction(Instruction("JMP", [start_label]))

            self._labels[end_label] = self._current_address

        elif node.type == "ReturnStatement":
            if node.children:
                result = self._generate_node(node.children[0], code)
                code.add_instruction(Instruction("MOV", ["RETURN_VALUE", result]))
            code.add_instruction(Instruction("RET", []))

        return "R0"  # По умолчанию возвращаем R0