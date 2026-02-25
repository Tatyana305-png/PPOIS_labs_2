import argparse
import sys
from typing import List, Optional

from Compiler.Core import SourceCode, Compiler
from Compiler.Models import ProgrammingLanguage, ASTNode
from Compiler.Core import LexicalAnalyzer, SyntaxAnalyzer
from Compiler.Exceptions import CompilerException


class CompilerCLI:
    """Интерфейс командной строки для компилятора"""

    def __init__(self):
        self.compiler: Optional[Compiler] = None
        self._setup_parser()

    def _setup_parser(self) -> None:
        """Настраивает парсер аргументов командной строки"""
        self.parser = argparse.ArgumentParser(
            description='Модель компилятора - трансляция исходного кода в машинный код',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Примеры использования:
  %(prog)s compile input.txt -o output.bin
  %(prog)s compile input.txt -O2
  %(prog)s analyze input.txt
  %(prog)s interactive
            """
        )

        subparsers = self.parser.add_subparsers(dest='command', help='Команды')

        # Команда компиляции
        compile_parser = subparsers.add_parser('compile', help='Компиляция файла')
        compile_parser.add_argument('input_file', help='Входной файл с исходным кодом')
        compile_parser.add_argument('-o', '--output', help='Выходной файл для машинного кода')
        compile_parser.add_argument('-O', '--optimization', type=int, choices=[0, 1, 2],
                                    default=1, help='Уровень оптимизации (0-2)')
        compile_parser.add_argument('--save-state', help='Сохранить состояние в файл')
        compile_parser.add_argument('--load-state', help='Загрузить состояние из файла')

        # Команда анализа
        analyze_parser = subparsers.add_parser('analyze', help='Анализ кода без генерации')
        analyze_parser.add_argument('input_file', help='Входной файл с исходным кодом')
        analyze_parser.add_argument('--tokens', action='store_true', help='Показать токены')
        analyze_parser.add_argument('--ast', action='store_true', help='Показать AST')

        # Интерактивный режим
        subparsers.add_parser('interactive', help='Интерактивный режим')

        # Команда информации
        info_parser = subparsers.add_parser('info', help='Информация о компиляторе')

    def run(self, args: Optional[List[str]] = None) -> int:
        """Запускает CLI"""
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return 0

        try:
            if parsed_args.command == 'compile':
                return self._handle_compile(parsed_args)
            elif parsed_args.command == 'analyze':
                return self._handle_analyze(parsed_args)
            elif parsed_args.command == 'interactive':
                return self._handle_interactive()
            elif parsed_args.command == 'info':
                return self._handle_info()
            else:
                self.parser.print_help()
                return 0

        except FileNotFoundError:
            print(f"Ошибка: файл не найден")
            return 1
        except CompilerException as e:
            print(f"Ошибка компиляции: {e}")
            return 1
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return 1

    def _handle_compile(self, args) -> int:
        """Обрабатывает команду компиляции"""
        # Читаем исходный код
        with open(args.input_file, 'r', encoding='utf-8') as f:
            code = f.read()

        # Создаем язык программирования
        language = ProgrammingLanguage("SimpleLang", "1.0")

        # Создаем исходный код
        source_code = SourceCode(code, language)

        # Создаем компилятор
        self.compiler = Compiler(source_code)

        # Загружаем состояние если указано
        if args.load_state:
            self.compiler.load_state(args.load_state)

        # Компилируем
        machine_code = self.compiler.compile_with_optimization(args.optimization)

        # Выводим результат
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ КОМПИЛЯЦИИ")
        print("=" * 50)
        print(machine_code)

        # Сохраняем машинный код
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(str(machine_code))
            print(f"\nМашинный код сохранен в {args.output}")

        # Сохраняем состояние
        if args.save_state:
            self.compiler.save_state(args.save_state)

        return 0

    def _handle_analyze(self, args) -> int:
        """Обрабатывает команду анализа"""
        # Читаем исходный код
        with open(args.input_file, 'r', encoding='utf-8') as f:
            code = f.read()

        # Создаем язык и анализаторы
        language = ProgrammingLanguage("SimpleLang", "1.0")
        source_code = SourceCode(code, language)

        # Лексический анализ
        lexical = LexicalAnalyzer(language)
        tokens = lexical.analyze(code)

        print(f"\nЛЕКСИЧЕСКИЙ АНАЛИЗ")
        print("=" * 50)
        print(f"Всего токенов: {len(tokens)}")

        if args.tokens:
            print("\nТокены:")
            for token in tokens:
                print(f"  {token.line}:{token.column} {token.type.value}: '{token.value}'")

        # Синтаксический анализ
        if args.ast:
            syntax = SyntaxAnalyzer(language)
            ast = syntax.analyze(tokens)

            print(f"\nСИНТАКСИЧЕСКИЙ АНАЛИЗ")
            print("=" * 50)
            print("AST:")
            self._print_ast(ast)

        return 0

    def _print_ast(self, node: ASTNode, level: int = 0) -> None:
        """Рекурсивно выводит AST"""
        indent = "  " * level
        value_str = f": {node.value}" if node.value is not None else ""
        print(f"{indent}{node.type}{value_str} [{node.line}:{node.column}]")

        for child in node.children:
            self._print_ast(child, level + 1)

    def _handle_interactive(self) -> int:
        """Интерактивный режим"""
        print("Интерактивный режим компилятора")
        print("Введите 'exit()' для выхода")
        print("Введите код для компиляции (пустая строка для выполнения):")

        lines = []
        language = ProgrammingLanguage("SimpleLang", "1.0")

        while True:
            line = input(">>> ")
            if line == "exit()":
                break

            if line == "":
                if lines:
                    # Компилируем введенный код
                    code = "\n".join(lines)
                    source = SourceCode(code, language)
                    compiler = Compiler(source)

                    try:
                        print("\nНачало компиляции...")
                        result = compiler.compile()
                        print("\nРезультат:")
                        print(result)
                    except CompilerException as e:
                        print(f"Ошибка: {e}")

                    lines = []
                    print("\nВведите следующий код (или exit() для выхода):")
            else:
                lines.append(line)

        return 0

    def _handle_info(self) -> int:
        """Выводит информацию о компиляторе"""
        print("=" * 60)
        print("МОДЕЛЬ КОМПИЛЯТОРА v1.0")
        print("=" * 60)
        print("\nОписание:")
        print("  Программная система для трансляции исходного кода")
        print("  в машинный код с поддержкой оптимизации")
        print("\nЭтапы компиляции:")
        print("  1. Лексический анализ - разбор на токены")
        print("  2. Синтаксический анализ - построение AST")
        print("  3. Оптимизация - улучшение кода")
        print("  4. Генерация кода - создание машинного кода")
        print("\nУровни оптимизации:")
        print("  0: Без оптимизации")
        print("  1: Базовая оптимизация (свертка констант, удаление мертвого кода)")
        print("  2: Полная оптимизация (распространение констант, уменьшение силы)")
        print("\nПоддерживаемые языки:")
        print("  - SimpleLang 1.0")
        print("=" * 60)
        return 0


def main():
    """Точка входа в программу"""
    cli = CompilerCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()