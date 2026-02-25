import unittest
from Compiler.Models import ProgrammingLanguage, MachineCode, Instruction
from Compiler.Core import LexicalAnalyzer, SyntaxAnalyzer, MachineCodeGenerator


class TestMachineCodeGenerator(unittest.TestCase):
    """Тесты для генератора машинного кода"""

    def setUp(self):
        self.generator = MachineCodeGenerator("x86")
        self.lang = ProgrammingLanguage("TestLang", "1.0")
        self.lexer = LexicalAnalyzer(self.lang)
        self.parser = SyntaxAnalyzer(self.lang)

    def _get_ast(self, code: str):
        """Вспомогательный метод для получения AST из кода"""
        tokens = self.lexer.analyze(code)
        return self.parser.analyze(tokens)

    def test_generate_empty_program(self):
        """Тест генерации для пустой программы"""
        ast = self._get_ast("")
        machine_code = self.generator.generate(ast)

        self.assertIsInstance(machine_code, MachineCode)
        self.assertEqual(len(machine_code.instructions), 0)

    def test_generate_simple_assignment(self):
        """Тест генерации для простого присваивания"""
        code = "x = 5;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        self.assertGreater(len(machine_code.instructions), 0)

        # Должна быть инструкция MOV
        mov_found = any(instr.opcode == "MOV" for instr in machine_code.instructions)
        self.assertTrue(mov_found)

    def test_generate_addition(self):
        """Тест генерации для операции сложения"""
        code = "x = 5 + 3;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Должна быть инструкция ADD
        add_found = any(instr.opcode == "ADD" for instr in machine_code.instructions)
        self.assertTrue(add_found)

    def test_generate_subtraction(self):
        """Тест генерации для операции вычитания"""
        code = "x = 10 - 4;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        sub_found = any(instr.opcode == "SUB" for instr in machine_code.instructions)
        self.assertTrue(sub_found)

    def test_generate_multiplication(self):
        """Тест генерации для операции умножения"""
        code = "x = 6 * 7;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        mul_found = any(instr.opcode == "MUL" for instr in machine_code.instructions)
        self.assertTrue(mul_found)

    def test_generate_division(self):
        """Тест генерации для операции деления"""
        code = "x = 15 / 3;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        div_found = any(instr.opcode == "DIV" for instr in machine_code.instructions)
        self.assertTrue(div_found)

    def test_generate_complex_expression(self):
        """Тест генерации для сложного выражения"""
        code = "x = (a + b) * c - d / e;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Должны быть разные типы инструкций
        opcodes = [instr.opcode for instr in machine_code.instructions]
        self.assertTrue("MOV" in opcodes)
        self.assertTrue(any(op in opcodes for op in ["ADD", "SUB", "MUL", "DIV"]))

    def test_generate_if_statement(self):
        """Тест генерации для условного оператора"""
        code = "if x > 5 y = 10;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Должны быть инструкции сравнения и переходов
        opcodes = [instr.opcode for instr in machine_code.instructions]
        self.assertTrue("CMP" in opcodes)
        self.assertTrue("JE" in opcodes or "JMP" in opcodes)

    def test_generate_if_else_statement(self):
        """Тест генерации для условного оператора с else"""
        code = "if x > 5 y = 10; else y = 0;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        opcodes = [instr.opcode for instr in machine_code.instructions]
        self.assertTrue("CMP" in opcodes)
        self.assertTrue("JE" in opcodes)
        self.assertTrue("JMP" in opcodes)

    def test_generate_while_statement(self):
        """Тест генерации для цикла while"""
        code = "while i < 10 i = i + 1;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        opcodes = [instr.opcode for instr in machine_code.instructions]
        self.assertTrue("CMP" in opcodes)
        self.assertTrue("JE" in opcodes)
        self.assertTrue("JMP" in opcodes)

    def test_generate_return_statement(self):
        """Тест генерации для оператора return"""
        code = "return x + 5;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Должна быть инструкция RET
        ret_found = any(instr.opcode == "RET" for instr in machine_code.instructions)
        self.assertTrue(ret_found)

        # Должен быть MOV для возвращаемого значения
        mov_found = any(instr.opcode == "MOV" and "RETURN_VALUE" in instr.operands
                        for instr in machine_code.instructions)
        self.assertTrue(mov_found)

    def test_generate_declaration(self):
        """Тест генерации для объявления переменной"""
        code = "int x = 5;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Должна быть инструкция MOV для инициализации
        mov_found = any(instr.opcode == "MOV" and "[x]" in instr.operands
                        for instr in machine_code.instructions)
        self.assertTrue(mov_found)

    def test_instruction_properties(self):
        """Тест свойств инструкций"""
        code = "x = 5;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        for instr in machine_code.instructions:
            self.assertTrue(hasattr(instr, 'opcode'))
            self.assertTrue(hasattr(instr, 'operands'))
            self.assertTrue(hasattr(instr, 'address'))
            self.assertIsInstance(instr.opcode, str)
            self.assertIsInstance(instr.operands, list)

    def test_machine_code_string_representation(self):
        """Тест строкового представления машинного кода"""
        code = "x = 5;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        str_repr = str(machine_code)
        self.assertTrue(str_repr.startswith("Машинный код:"))
        self.assertIn("MOV", str_repr)

    def test_register_allocation(self):
        """Тест выделения регистров"""
        code = "x = a + b + c;"
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Проверяем, что используются разные регистры
        registers = set()
        for instr in machine_code.instructions:
            for op in instr.operands:
                if op.startswith('R') and len(op) > 1 and op[1:].isdigit():
                    registers.add(op)

        self.assertGreater(len(registers), 0)

    def test_label_generation(self):
        """Тест генерации меток"""
        code = """
        if x > 5 {
            y = 10;
        }
        while i < 10 {
            i = i + 1;
        }
        """
        ast = self._get_ast(code)
        machine_code = self.generator.generate(ast)

        # Проверяем, что метки сохраняются
        self.assertTrue(hasattr(self.generator, '_labels'))
        self.assertGreater(len(self.generator._labels), 0)


if __name__ == '__main__':
    unittest.main()