from typing import Dict
from .Interfaces import ICodeGenerator
from .Models import ASTNode, MachineCode, Instruction


class MachineCodeGenerator(ICodeGenerator):
    """Генератор машинного кода"""

    def __init__(self, target_architecture: str = "x86"):
        self.target_architecture = target_architecture
        self._current_address = 0
        self._labels: Dict[str, int] = {}
        self._register_counter = 0

    def _get_next_register(self) -> str:
        """Возвращает следующий доступный регистр"""
        reg = f"R{self._register_counter % 8}"
        self._register_counter += 1
        return reg

    def generate(self, ast: ASTNode) -> MachineCode:
        """
        Генерирует машинный код из AST
        """
        machine_code = MachineCode()
        self._current_address = 0
        self._labels.clear()
        self._register_counter = 0

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
            return ""

        elif node.type == "Declaration":
            # Объявление переменной
            if node.children:
                # Генерируем код для инициализатора
                result = self._generate_node(node.children[0], code)
                # Сохраняем результат в переменную
                code.add_instruction(Instruction("MOV", [f"[{node.value}]", result]))
            return ""

        elif node.type == "BinaryOperation":
            # Генерируем код для левого операнда
            left = self._generate_node(node.children[0], code)
            # Генерируем код для правого операнда
            right = self._generate_node(node.children[1], code)

            # Выполняем операцию в зависимости от типа
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
            elif node.value == '=':
                # Присваивание
                code.add_instruction(Instruction("MOV", [left, right]))
                return left
            elif node.value in ['==', '!=', '<', '>', '<=', '>=']:
                # Операции сравнения
                result_reg = self._get_next_register()
                code.add_instruction(Instruction("CMP", [left, right]))

                if node.value == '==':
                    code.add_instruction(Instruction("SETE", [result_reg]))
                elif node.value == '!=':
                    code.add_instruction(Instruction("SETNE", [result_reg]))
                elif node.value == '<':
                    code.add_instruction(Instruction("SETL", [result_reg]))
                elif node.value == '>':
                    code.add_instruction(Instruction("SETG", [result_reg]))
                elif node.value == '<=':
                    code.add_instruction(Instruction("SETLE", [result_reg]))
                elif node.value == '>=':
                    code.add_instruction(Instruction("SETGE", [result_reg]))

                return result_reg
            else:
                # Неизвестная операция
                return left

        elif node.type == "Number":
            # Загружаем число в регистр
            reg = self._get_next_register()
            # Убеждаемся, что значение - строка, но для инструкции MOV оно подходит
            value = node.value
            code.add_instruction(Instruction("MOV", [reg, str(value)]))
            return reg

        elif node.type == "Identifier":
            # Загружаем переменную в регистр
            reg = self._get_next_register()
            code.add_instruction(Instruction("MOV", [reg, f"[{node.value}]"]))
            return reg

        elif node.type == "String":
            # Загружаем строку
            reg = self._get_next_register()
            code.add_instruction(Instruction("MOV", [reg, node.value]))
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

            # Условный переход (если результат 0 - переход на else)
            code.add_instruction(Instruction("CMP", [cond_result, "0"]))
            code.add_instruction(Instruction("JE", [else_label]))

            # Then ветка
            self._generate_node(then_branch, code)
            code.add_instruction(Instruction("JMP", [end_label]))

            # Else ветка
            code.add_instruction(Instruction("LABEL", [else_label]))
            if else_branch:
                self._generate_node(else_branch, code)

            # Конец if
            code.add_instruction(Instruction("LABEL", [end_label]))
            return ""

        elif node.type == "WhileStatement":
            condition = node.children[0]
            body = node.children[1]

            # Создаем метки
            start_label = f"while_start_{len(self._labels)}"
            end_label = f"while_end_{len(self._labels)}"

            # Начало цикла
            code.add_instruction(Instruction("LABEL", [start_label]))

            # Проверяем условие
            cond_result = self._generate_node(condition, code)
            code.add_instruction(Instruction("CMP", [cond_result, "0"]))
            code.add_instruction(Instruction("JE", [end_label]))

            # Тело цикла
            self._generate_node(body, code)
            code.add_instruction(Instruction("JMP", [start_label]))

            # Конец цикла
            code.add_instruction(Instruction("LABEL", [end_label]))
            return ""

        elif node.type == "ReturnStatement":
            if node.children:
                result = self._generate_node(node.children[0], code)
                code.add_instruction(Instruction("MOV", ["RETURN_VALUE", result]))
            code.add_instruction(Instruction("RET", []))
            return ""

        elif node.type == "Block":
            for child in node.children:
                self._generate_node(child, code)
            return ""

        elif node.type == "EmptyStatement":
            return ""

        elif node.type == "UnaryOperation":
            operand = self._generate_node(node.children[0], code)
            if node.value == '-':
                # Унарный минус
                result_reg = self._get_next_register()
                code.add_instruction(Instruction("MOV", [result_reg, "0"]))
                code.add_instruction(Instruction("SUB", [result_reg, operand]))
                return result_reg
            elif node.value == '!':
                # Логическое НЕ
                result_reg = self._get_next_register()
                code.add_instruction(Instruction("CMP", [operand, "0"]))
                code.add_instruction(Instruction("SETE", [result_reg]))
                return result_reg
            return operand

        else:
            # Для неизвестных типов узлов просто обрабатываем детей
            for child in node.children:
                self._generate_node(child, code)
            return "R0"