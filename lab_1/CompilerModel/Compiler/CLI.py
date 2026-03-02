import argparse
import sys
from typing import List, Optional

from Compiler.Core import SourceCode, Compiler
from Compiler.Models import ProgrammingLanguage, CompilerState, ASTNode
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
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        subparsers = self.parser.add_subparsers(dest='command', help='Команды')

        # Команда компиляции с выбором этапа
        compile_parser = subparsers.add_parser('compile', help='Компиляция до указанного этапа')
        compile_parser.add_argument('input_file', help='Входной файл с исходным кодом')
        compile_parser.add_argument('-s', '--stage', choices=['lexical', 'syntax', 'optimize', 'code', 'full'],
                                    default='full', help='Этап компиляции')
        compile_parser.add_argument('-o', '--output', help='Выходной файл')
        compile_parser.add_argument('-O', '--optimization', type=int, choices=[0, 1, 2],
                                    default=1, help='Уровень оптимизации (0-2)')
        compile_parser.add_argument('--save-state', help='Сохранить состояние в файл')
        compile_parser.add_argument('--load-state', help='Загрузить состояние из файла')

        # Команда меню
        subparsers.add_parser('menu', help='Интерактивное меню')

        # Остальные команды
        subparsers.add_parser('info', help='Информация о компиляторе')

    def _stage_to_state(self, stage: str) -> CompilerState:
        """Преобразует строку этапа в CompilerState"""
        mapping = {
            'lexical': CompilerState.LEXICAL_ANALYSIS,
            'syntax': CompilerState.SYNTAX_ANALYSIS,
            'optimize': CompilerState.OPTIMIZATION,
            'code': CompilerState.CODE_GENERATION,
            'full': CompilerState.COMPLETED
        }
        return mapping.get(stage, CompilerState.COMPLETED)

    def run(self, args: Optional[List[str]] = None) -> int:
        """Запускает CLI"""
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self._show_main_menu()
            return 0

        try:
            if parsed_args.command == 'compile':
                return self._handle_compile(parsed_args)
            elif parsed_args.command == 'menu':
                return self._interactive_menu()
            elif parsed_args.command == 'info':
                return self._handle_info()
            else:
                self._show_main_menu()
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

    def _show_main_menu(self):
        """Показывает главное меню"""
        print("=" * 60)
        print(" МОДЕЛЬ КОМПИЛЯТОРА - ГЛАВНОЕ МЕНЮ")
        print("=" * 60)
        print("1.  Компиляция файла")
        print("2.  Интерактивное меню")
        print("3.  Информация о компиляторе")
        print("4.  Выход")
        print("=" * 60)

        choice = input("Выберите опцию (1-4): ").strip()

        if choice == '1':
            self._compile_file_menu()
        elif choice == '2':
            self._interactive_menu()
        elif choice == '3':
            self._handle_info()
            input("\nНажмите Enter для продолжения...")
            self._show_main_menu()
        else:
            print(" До свидания!")

    def _compile_file_menu(self):
        """Меню компиляции файла"""
        print("\n" + "=" * 60)
        print(" КОМПИЛЯЦИЯ ФАЙЛА")
        print("=" * 60)

        input_file = input("Введите путь к файлу с исходным кодом: ").strip()

        print("\n Выберите этап компиляции:")
        print("1.  Лексический анализ (токены)")
        print("2.  Синтаксический анализ (AST)")
        print("3.  Оптимизация")
        print("4.  Генерация кода")
        print("5.  Полная компиляция")

        stage_choice = input("Выберите этап (1-5): ").strip()

        stage_mapping = {
            '1': 'lexical',
            '2': 'syntax',
            '3': 'optimize',
            '4': 'code',
            '5': 'full'
        }
        stage = stage_mapping.get(stage_choice, 'full')

        opt_level = input("Уровень оптимизации (0-2) [1]: ").strip() or '1'

        save_state = input("Сохранить состояние в файл? (y/n): ").strip().lower()
        state_file = None
        if save_state == 'y':
            state_file = input("Имя файла для сохранения [state.pkl]: ").strip() or 'state.pkl'

        load_state = input("Загрузить состояние из файла? (y/n): ").strip().lower()
        load_file = None
        if load_state == 'y':
            load_file = input("Имя файла для загрузки: ").strip()

        # Создаем аргументы
        class Args:
            pass

        cmd_args = Args()
        cmd_args.input_file = input_file
        cmd_args.stage = stage
        cmd_args.optimization = int(opt_level)
        cmd_args.save_state = state_file
        cmd_args.load_state = load_file
        cmd_args.output = None

        self._handle_compile(cmd_args)

        input("\nНажмите Enter для продолжения...")
        self._show_main_menu()

    def _interactive_menu(self):
        """Интерактивное меню для поэтапной компиляции"""
        print("\n" + "=" * 60)
        print(" МЕНЮ")
        print("=" * 60)

        # Загружаем состояние если есть
        load_choice = input("Загрузить предыдущее состояние? (y/n): ").strip().lower()
        if load_choice == 'y':
            state_file = input("Имя файла состояния [state.pkl]: ").strip() or 'state.pkl'

            lang = ProgrammingLanguage("SimpleLang", "1.0")
            source = SourceCode("", lang)
            self.compiler = Compiler(source)

            if not self.compiler.load_stage_state(state_file):
                print(" Не удалось загрузить состояние. Начинаем с начала.")
                self.compiler = None

        if not self.compiler:
            # Создаем новый компилятор
            print("\n Введите исходный код (многострочный, пустая строка для завершения):")
            lines = []
            while True:
                line = input(">>> ")
                if line == "":
                    break
                lines.append(line)

            if not lines:
                print(" Код не введен. Использую пример.")
                lines = ["x = 5 + 3;", "y = 10;", "result = x * y;"]

            full_code = "\n".join(lines)
            lang = ProgrammingLanguage("SimpleLang", "1.0")
            source = SourceCode(full_code, lang)
            self.compiler = Compiler(source)

        while True:
            print("\n" + "=" * 60)
            print(f" ТЕКУЩИЙ ЭТАП: {self.compiler.state.value}")
            print("=" * 60)
            print("1.  Выполнить лексический анализ")
            print("2.  Выполнить синтаксический анализ")
            print("3.  Выполнить оптимизацию")
            print("4.  Выполнить генерацию кода")
            print("5.  Выполнить до указанного этапа")
            print("6.  Показать текущие результаты")
            print("7.  Сохранить текущее состояние")
            print("8.  Загрузить состояние из файла")
            print("9.  Сбросить компилятор")
            print("10.  Вернуться в главное меню")
            print("11.  Выход")

            choice = input("Выберите опцию: ").strip()

            if choice == '1':
                print("\n Выполняется лексический анализ...")
                self.compiler.compile_to_stage(CompilerState.LEXICAL_ANALYSIS)
                self._show_lexical_results()

            elif choice == '2':
                print("\n Выполняется синтаксический анализ...")
                self.compiler.compile_to_stage(CompilerState.SYNTAX_ANALYSIS)
                self._show_syntax_results()

            elif choice == '3':
                print("\n Выполняется оптимизация...")
                self.compiler.compile_to_stage(CompilerState.OPTIMIZATION)
                self._show_optimization_results()

            elif choice == '4':
                print("\n Выполняется генерация кода...")
                self.compiler.compile_to_stage(CompilerState.CODE_GENERATION)
                self._show_code_generation_results()

            elif choice == '5':
                self._compile_to_selected_stage()

            elif choice == '6':
                self._show_all_results()

            elif choice == '7':
                state_file = input("Имя файла для сохранения [state.pkl]: ").strip() or 'state.pkl'
                self.compiler.save_stage_state(state_file)

            elif choice == '8':
                state_file = input("Имя файла для загрузки: ").strip()
                if state_file:
                    lang = ProgrammingLanguage("SimpleLang", "1.0")
                    source = SourceCode("", lang)
                    new_compiler = Compiler(source)
                    if new_compiler.load_stage_state(state_file):
                        self.compiler = new_compiler
                        print(" Состояние загружено успешно!")
                    else:
                        print(" Ошибка загрузки состояния")

            elif choice == '9':
                print("\n Сброс компилятора...")
                lang = ProgrammingLanguage("SimpleLang", "1.0")
                source = SourceCode(self.compiler.source_code.get_code(), lang)
                self.compiler = Compiler(source)
                print(" Компилятор сброшен к начальному состоянию")

            elif choice == '10':
                self._show_main_menu()
                return

            elif choice == '11':
                print(" До свидания!")
                sys.exit(0)

    def _show_lexical_results(self):
        """Показывает результаты лексического анализа"""
        if not self.compiler._tokens:
            print(" Нет токенов для отображения")
            return

        print("\n" + "=" * 60)
        print(" РЕЗУЛЬТАТЫ ЛЕКСИЧЕСКОГО АНАЛИЗА")
        print("=" * 60)
        print(f" Всего токенов: {len(self.compiler._tokens)}")
        print("\n Список токенов:")
        print("-" * 50)
        print(f"{'№':<4} {'Линия':<6} {'Колонка':<8} {'Тип':<20} {'Значение'}")
        print("-" * 50)

        for i, token in enumerate(self.compiler._tokens):
            if i < 20:  # Показываем первые 20
                print(f"{i + 1:<4} {token.line:<6} {token.column:<8} {token.type.value:<20} '{token.value}'")
            else:
                print(f"... и еще {len(self.compiler._tokens) - 20} токенов")
                break

    def _show_syntax_results(self):
        """Показывает результаты синтаксического анализа"""
        if not self.compiler._ast:
            print(" Нет AST для отображения")
            return

        print("\n" + "=" * 60)
        print(" РЕЗУЛЬТАТЫ СИНТАКСИЧЕСКОГО АНАЛИЗА")
        print("=" * 60)
        print(" Абстрактное синтаксическое дерево (AST):")
        self._print_ast_detailed(self.compiler._ast)

    def _show_optimization_results(self):
        """Показывает результаты оптимизации"""
        print("\n" + "=" * 60)
        print("⚡ РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ")
        print("=" * 60)

        if not self.compiler._optimized_ast:
            print(" Нет оптимизированного AST")
            return

        print(f" Уровень оптимизации: {self.compiler.optimizer.optimization_level}")

        # Показываем изменения
        changes = self._analyze_optimization_changes()
        if changes:
            print("\n Выполненные оптимизации:")
            for change in changes:
                print(f"   • {change}")
        else:
            print("\nℹ Оптимизации не применились или не изменили AST")

        print("\n Оптимизированное AST:")
        self._print_ast_detailed(self.compiler._optimized_ast)

    def _show_code_generation_results(self):
        """Показывает результаты генерации кода"""
        if not self.compiler._machine_code:
            print(" Нет машинного кода для отображения")
            return

        print("\n" + "=" * 60)
        print(" РЕЗУЛЬТАТЫ ГЕНЕРАЦИИ КОДА")
        print("=" * 60)
        print(f" Всего инструкций: {len(self.compiler._machine_code.instructions)}")
        print("\n Машинный код:")
        print("-" * 50)
        print(f"{'Адрес':<8} {'Инструкция':<10} {'Операнды'}")
        print("-" * 50)

        for i, instr in enumerate(self.compiler._machine_code.instructions[:20]):
            addr = f"{i * 2:04x}"  # Примерный адрес
            ops = ', '.join(instr.operands)
            print(f"{addr:<8} {instr.opcode:<10} {ops}")

        if len(self.compiler._machine_code.instructions) > 20:
            print(f"... и еще {len(self.compiler._machine_code.instructions) - 20} инструкций")

    def _show_all_results(self):
        """Показывает все результаты компиляции"""
        print("\n" + "=" * 60)
        print(" ПОЛНЫЕ РЕЗУЛЬТАТЫ КОМПИЛЯЦИИ")
        print("=" * 60)
        print(f" Текущий этап: {self.compiler.state.value}")

        # Токены
        if self.compiler._tokens:
            print(f"\n ЛЕКСИЧЕСКИЙ АНАЛИЗ: {len(self.compiler._tokens)} токенов")
            token_types = {}
            for token in self.compiler._tokens:
                token_types[token.type.value] = token_types.get(token.type.value, 0) + 1
            print("   Статистика токенов:")
            for t_type, count in token_types.items():
                print(f"   • {t_type}: {count}")

        # AST
        if self.compiler._ast:
            node_count = self._count_ast_nodes(self.compiler._ast)
            print(f"\n СИНТАКСИЧЕСКИЙ АНАЛИЗ: {node_count} узлов в AST")

        # Оптимизированный AST
        if self.compiler._optimized_ast:
            opt_node_count = self._count_ast_nodes(self.compiler._optimized_ast)
            print(f"\n⚡ ОПТИМИЗАЦИЯ: {opt_node_count} узлов в оптимизированном AST")
            if self.compiler._ast:
                diff = opt_node_count - self._count_ast_nodes(self.compiler._ast)
                if diff < 0:
                    print(f"   Удалено {abs(diff)} узлов")
                elif diff > 0:
                    print(f"   Добавлено {diff} узлов")

        # Машинный код
        if self.compiler._machine_code:
            print(f"\n ГЕНЕРАЦИЯ КОДА: {len(self.compiler._machine_code.instructions)} инструкций")

        # Предложение показать детали
        print("\n Выберите, что показать детально:")
        print("1. Токены")
        print("2. AST")
        print("3. Оптимизированный AST")
        print("4. Машинный код")
        print("5. Вернуться")

        detail_choice = input("Выберите опцию (1-5): ").strip()

        if detail_choice == '1':
            self._show_lexical_results()
        elif detail_choice == '2':
            self._show_syntax_results()
        elif detail_choice == '3':
            self._show_optimization_results()
        elif detail_choice == '4':
            self._show_code_generation_results()

    def _compile_to_selected_stage(self):
        """Компиляция до выбранного этапа"""
        print("\n Выберите целевой этап:")
        print("1.  Лексический анализ")
        print("2.  Синтаксический анализ")
        print("3.  Оптимизация")
        print("4.  Генерация кода")
        print("5.  Полная компиляция")

        stage_choice = input("Выберите этап (1-5): ").strip()

        stage_mapping = {
            '1': CompilerState.LEXICAL_ANALYSIS,
            '2': CompilerState.SYNTAX_ANALYSIS,
            '3': CompilerState.OPTIMIZATION,
            '4': CompilerState.CODE_GENERATION,
            '5': CompilerState.COMPLETED
        }

        target_stage = stage_mapping.get(stage_choice)
        if target_stage:
            print(f"\n Компиляция до этапа: {target_stage.value}")
            success = self.compiler.compile_to_stage(target_stage)
            if success:
                print(" Компиляция завершена успешно!")
                self._show_stage_results(target_stage)
            else:
                print(" Ошибка компиляции")

    def _show_stage_results(self, stage: CompilerState):
        """Показывает результаты конкретного этапа"""
        if stage == CompilerState.LEXICAL_ANALYSIS:
            self._show_lexical_results()
        elif stage == CompilerState.SYNTAX_ANALYSIS:
            self._show_syntax_results()
        elif stage == CompilerState.OPTIMIZATION:
            self._show_optimization_results()
        elif stage in [CompilerState.CODE_GENERATION, CompilerState.COMPLETED]:
            self._show_code_generation_results()

    def _print_ast_detailed(self, node: ASTNode, level: int = 0, prefix: str = " "):
        """Детальный вывод AST с визуализацией"""
        indent = "   " * level
        tree_char = "└─" if level > 0 else ""

        value_str = f": {node.value}" if node.value is not None else ""
        type_str = f"{node.type}{value_str}"

        # Добавляем информацию о позиции
        pos_str = f" [{node.line}:{node.column}]"

        print(f"{indent}{tree_char}{prefix}{type_str}{pos_str}")

        for i, child in enumerate(node.children):
            is_last = (i == len(node.children) - 1)
            child_prefix = "└─ " if is_last else "├─ "
            self._print_ast_detailed(child, level + 1, child_prefix)

    def _count_ast_nodes(self, node: ASTNode) -> int:
        """Подсчитывает количество узлов в AST"""
        count = 1
        for child in node.children:
            count += self._count_ast_nodes(child)
        return count

    def _analyze_optimization_changes(self) -> List[str]:
        """Анализирует изменения после оптимизации"""
        changes = []

        if not self.compiler._ast or not self.compiler._optimized_ast:
            return changes

        # Проверяем свертку констант
        if self._has_constant_folding(self.compiler._ast, self.compiler._optimized_ast):
            changes.append("Свертка констант (например, 2+3 → 5)")

        # Проверяем удаление мертвого кода
        if self._has_dead_code_elimination(self.compiler._ast, self.compiler._optimized_ast):
            changes.append("Удаление мертвого кода")

        # Проверяем распространение констант
        if self._has_constant_propagation(self.compiler._ast, self.compiler._optimized_ast):
            changes.append("Распространение констант")

        # Проверяем уменьшение силы
        if self._has_strength_reduction(self.compiler._ast, self.compiler._optimized_ast):
            changes.append("Уменьшение силы операций (например, y*2 → y+y)")

        return changes

    def _has_constant_folding(self, original: ASTNode, optimized: ASTNode) -> bool:
        """Проверяет наличие свертки констант"""

        # Простая проверка - ищем числа, которые могли появиться
        def count_numbers(node):
            count = 0
            if node.type == "Number":
                count += 1
            for child in node.children:
                count += count_numbers(child)
            return count

        orig_numbers = count_numbers(original)
        opt_numbers = count_numbers(optimized)

        # Если чисел стало больше, возможно, была свертка
        return opt_numbers > orig_numbers

    def _has_dead_code_elimination(self, original: ASTNode, optimized: ASTNode) -> bool:
        """Проверяет наличие удаления мертвого кода"""
        # Проверяем уменьшение количества узлов
        orig_nodes = self._count_ast_nodes(original)
        opt_nodes = self._count_ast_nodes(optimized)

        return opt_nodes < orig_nodes

    def _has_constant_propagation(self, original: ASTNode, optimized: ASTNode) -> bool:
        """Проверяет наличие распространения констант"""

        # Ищем идентификаторы, которые могли быть заменены на числа
        def find_identifiers(node):
            ids = []
            if node.type == "Identifier":
                ids.append(node.value)
            for child in node.children:
                ids.extend(find_identifiers(child))
            return ids

        orig_ids = set(find_identifiers(original))
        opt_ids = set(find_identifiers(optimized))

        # Если идентификаторов стало меньше, возможно, была замена
        return len(opt_ids) < len(orig_ids)

    def _has_strength_reduction(self, original: ASTNode, optimized: ASTNode) -> bool:
        """Проверяет наличие уменьшения силы операций"""

        # Ищем умножение, которое могло замениться на сложение
        def has_multiplication(node):
            if node.type == "BinaryOperation" and node.value == '*':
                return True
            for child in node.children:
                if has_multiplication(child):
                    return True
            return False

        orig_has_mul = has_multiplication(original)
        opt_has_mul = has_multiplication(optimized)

        return orig_has_mul and not opt_has_mul

    def _handle_compile(self, args) -> int:
        """Обрабатывает команду компиляции"""
        # Загружаем состояние если указано
        if args.load_state:
            lang = ProgrammingLanguage("SimpleLang", "1.0")
            source = SourceCode("", lang)
            self.compiler = Compiler(source)
            if not self.compiler.load_stage_state(args.load_state):
                print(" Не удалось загрузить состояние. Начинаем с начала.")
                self.compiler = None

        # Если состояние не загружено или его нет, читаем файл
        if not self.compiler:
            try:
                with open(args.input_file, 'r', encoding='utf-8') as f:
                    code = f.read()
            except FileNotFoundError:
                print(f" Ошибка: файл {args.input_file} не найден")
                return 1

            language = ProgrammingLanguage("SimpleLang", "1.0")
            source_code = SourceCode(code, language)
            self.compiler = Compiler(source_code)

        # Устанавливаем уровень оптимизации
        self.compiler.optimizer.optimization_level = args.optimization

        # Определяем целевой этап
        target_stage = self._stage_to_state(args.stage)

        # Компилируем до указанного этапа
        print(f"\n Компиляция до этапа: {target_stage.value}")
        success = self.compiler.compile_to_stage(target_stage)

        if success:
            print(f"\n{'=' * 60}")
            print(f" КОМПИЛЯЦИЯ ДО ЭТАПА: {target_stage.value} УСПЕШНО ЗАВЕРШЕНА")
            print('=' * 60)

            # Показываем результаты
            self._show_stage_results(target_stage)

        # Сохраняем состояние если указано
        if args.save_state:
            self.compiler.save_stage_state(args.save_state, target_stage)

        # Сохраняем машинный код если указано
        if args.output and self.compiler._machine_code:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(str(self.compiler._machine_code))
            print(f"\n Машинный код сохранен в {args.output}")

        return 0 if success else 1

    def _handle_info(self) -> int:
        """Выводит информацию о компиляторе"""
        print("=" * 60)
        print(" МОДЕЛЬ КОМПИЛЯТОРА v2.0")
        print("=" * 60)
        print("\n ОПИСАНИЕ:")
        print("  Программная система для трансляции исходного кода")
        print("  в машинный код с поддержкой поэтапной компиляции")

        print("\n ЭТАПЫ КОМПИЛЯЦИИ:")
        print("  1.  Лексический анализ - разбор на токены")
        print("     Вход: исходный код → Выход: список токенов")
        print("     Пример: 'x = 5' → [IDENTIFIER(x), OPERATOR(=), NUMBER(5)]")

        print("\n  2.  Синтаксический анализ - построение AST")
        print("     Вход: токены → Выход: абстрактное синтаксическое дерево")
        print("     Пример: [x,=,5] → BinaryOperation(=) с детьми Identifier(x) и Number(5)")

        print("\n  3.  Оптимизация - улучшение кода")
        print("     Вход: AST → Выход: оптимизированное AST")
        print("     Пример: 2+3*4 → 14 (свертка констант)")

        print("\n  4.  Генерация кода - создание машинного кода")
        print("     Вход: AST → Выход: машинные инструкции")
        print("     Пример: x=5 → MOV R0, 5; MOV [x], R0")

        print("\n УРОВНИ ОПТИМИЗАЦИИ:")
        print("  0: Без оптимизации")
        print("  1: Базовая оптимизация (свертка констант, удаление мертвого кода)")
        print("  2: Полная оптимизация (все оптимизации)")

        print("\n ПОЭТАПНАЯ КОМПИЛЯЦИЯ:")
        print("  • Можно остановиться на любом этапе")
        print("  • Сохранить промежуточное состояние в файл")
        print("  • Загрузить состояние и продолжить с того же места")
        print("  • Просмотреть результаты каждого этапа")

        print("\n ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:")
        print("  python -m Compiler.CLI compile test.txt --stage lexical")
        print("  python -m Compiler.CLI compile test.txt --stage optimize -O2")
        print("  python -m Compiler.CLI menu")
        print("=" * 60)
        return 0


def main():
    """Точка входа в программу"""
    cli = CompilerCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
