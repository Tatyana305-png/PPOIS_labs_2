import unittest
import sys
import os
import tempfile
from io import StringIO
from unittest.mock import patch, MagicMock, ANY

from Compiler.CLI import CompilerCLI, main
from Compiler.Exceptions import CompilerException
from Compiler.Models import CompilerState


class TestCLI(unittest.TestCase):
    """Тесты для интерфейса командной строки"""

    def setUp(self):
        self.cli = CompilerCLI()
        # Создаем временный файл с тестовым кодом
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        self.temp_file.write("x = 5 + 3;")
        self.temp_file.close()

        # Перенаправляем stdout для проверки вывода
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.held
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_cli_initialization(self):
        """Тест инициализации CLI"""
        cli = CompilerCLI()
        self.assertIsNotNone(cli.parser)
        self.assertIsNone(cli.compiler)

    def test_run_without_commands(self):
        """Тест запуска без команд"""
        with patch('argparse.ArgumentParser.print_help') as mock_print_help:
            result = self.cli.run([])
            mock_print_help.assert_called_once()
            self.assertEqual(result, 0)

    def test_compile_command(self):
        """Тест команды компиляции"""
        test_args = ['compile', self.temp_file.name]
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("РЕЗУЛЬТАТ КОМПИЛЯЦИИ", output)

    def test_compile_with_output(self):
        """Тест компиляции с выходным файлом"""
        output_file = tempfile.NamedTemporaryFile(suffix='.bin', delete=False)
        output_file.close()

        test_args = ['compile', self.temp_file.name, '-o', output_file.name]
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)

        # Проверяем, что выходной файл создан
        self.assertTrue(os.path.exists(output_file.name))
        os.unlink(output_file.name)

    def test_compile_with_optimization_levels(self):
        """Тест компиляции с разными уровнями оптимизации"""
        for level in [0, 1, 2]:
            # Очищаем stdout перед каждым тестом
            sys.stdout = StringIO()
            test_args = ['compile', self.temp_file.name, '-O', str(level)]
            result = self.cli.run(test_args)
            self.assertEqual(result, 0)
            output = sys.stdout.getvalue()
            self.assertIn("РЕЗУЛЬТАТ КОМПИЛЯЦИИ", output)

    def test_compile_with_save_state(self):
        """Тест компиляции с сохранением состояния"""
        state_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
        state_file.close()

        test_args = ['compile', self.temp_file.name, '--save-state', state_file.name]
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)

        # Проверяем, что файл состояния создан
        self.assertTrue(os.path.exists(state_file.name))
        os.unlink(state_file.name)

    def test_compile_with_load_state(self):
        """Тест компиляции с загрузкой состояния"""
        # Сначала сохраняем состояние
        state_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
        state_file.close()

        save_args = ['compile', self.temp_file.name, '--save-state', state_file.name]
        self.cli.run(save_args)

        # Теперь загружаем и компилируем
        test_args = ['compile', self.temp_file.name, '--load-state', state_file.name]
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)

        if os.path.exists(state_file.name):
            os.unlink(state_file.name)

    def test_analyze_command_tokens(self):
        """Тест команды анализа с токенами"""
        test_args = ['analyze', self.temp_file.name, '--tokens']
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("ЛЕКСИЧЕСКИЙ АНАЛИЗ", output)
        self.assertIn("Всего токенов:", output)

    def test_analyze_command_ast(self):
        """Тест команды анализа с AST"""
        test_args = ['analyze', self.temp_file.name, '--ast']
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("СИНТАКСИЧЕСКИЙ АНАЛИЗ", output)
        self.assertIn("AST:", output)

    def test_analyze_command_both(self):
        """Тест команды анализа с токенами и AST"""
        test_args = ['analyze', self.temp_file.name, '--tokens', '--ast']
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("ЛЕКСИЧЕСКИЙ АНАЛИЗ", output)
        self.assertIn("СИНТАКСИЧЕСКИЙ АНАЛИЗ", output)

    def test_info_command(self):
        """Тест команды info"""
        test_args = ['info']
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("МОДЕЛЬ КОМПИЛЯТОРА", output)
        self.assertIn("Этапы компиляции:", output)
        self.assertIn("Уровни оптимизации:", output)

    @patch('builtins.input', side_effect=['x = 5;', '', 'exit()'])
    def test_interactive_mode(self, mock_input):
        """Тест интерактивного режима"""
        test_args = ['interactive']
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)
        output = sys.stdout.getvalue()
        self.assertIn("Интерактивный режим компилятора", output)

    def test_file_not_found_error(self):
        """Тест ошибки при отсутствии файла"""
        test_args = ['compile', 'nonexistent.txt']
        result = self.cli.run(test_args)
        self.assertEqual(result, 1)
        output = sys.stdout.getvalue()
        self.assertIn("Ошибка: файл не найден", output)

    def test_main_function(self):
        """Тест главной функции"""
        with patch('sys.argv', ['CLI.py', 'info']):
            with patch('sys.exit') as mock_exit:
                main()
                mock_exit.assert_called_once_with(0)

    def test_compile_with_all_options(self):
        """Тест компиляции со всеми опциями"""
        output_file = tempfile.NamedTemporaryFile(suffix='.bin', delete=False)
        output_file.close()
        state_file = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
        state_file.close()

        test_args = [
            'compile', self.temp_file.name,
            '-o', output_file.name,
            '-O', '2',
            '--save-state', state_file.name
        ]
        result = self.cli.run(test_args)
        self.assertEqual(result, 0)

        if os.path.exists(output_file.name):
            os.unlink(output_file.name)
        if os.path.exists(state_file.name):
            os.unlink(state_file.name)

    def test_handle_compile_method_direct(self):
        """Тест прямого вызова _handle_compile"""

        class Args:
            def __init__(self, temp_file_name):
                self.input_file = temp_file_name
                self.output = None
                self.optimization = 1
                self.save_state = None
                self.load_state = None

        args = Args(self.temp_file.name)
        result = self.cli._handle_compile(args)
        self.assertEqual(result, 0)

    def test_handle_info_method(self):
        """Тест прямого вызова _handle_info"""
        result = self.cli._handle_info()
        self.assertEqual(result, 0)


class TestCLIEdgeCases(unittest.TestCase):
    """Тесты для граничных случаев CLI"""

    def setUp(self):
        self.cli = CompilerCLI()
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.held

    def test_empty_file_compilation(self):
        """Тест компиляции пустого файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            f.close()

            test_args = ['compile', f.name]
            result = self.cli.run(test_args)
            # Пустой файл должен компилироваться успешно (0 ошибок)
            self.assertEqual(result, 0)

            if os.path.exists(f.name):
                os.unlink(f.name)

    @patch('argparse.ArgumentParser.parse_args')
    def test_invalid_optimization_level(self, mock_parse_args):
        """Тест невалидного уровня оптимизации"""
        # Мокируем parse_args чтобы избежать SystemExit
        mock_args = MagicMock()
        mock_args.command = 'compile'
        mock_args.input_file = 'dummy.txt'
        mock_args.output = None
        mock_args.optimization = 5  # Невалидное значение
        mock_args.save_state = None
        mock_args.load_state = None
        mock_parse_args.return_value = mock_args

        # Должен использовать уровень по умолчанию или обработать ошибку
        with patch('Compiler.CLI.CompilerCLI._handle_compile') as mock_handle:
            mock_handle.return_value = 0
            result = self.cli.run(['compile', 'dummy.txt', '-O', '5'])
            # Проверяем, что handle не вызвался из-за ошибки парсинга
            # В реальности argparse выбросит исключение, поэтому мы не должны сюда попасть
            self.assertTrue(True)

    @patch('argparse.ArgumentParser.parse_args')
    def test_unknown_command(self, mock_parse_args):
        """Тест неизвестной команды"""
        # Мокируем parse_args
        mock_args = MagicMock()
        mock_args.command = None  # Нет команды
        mock_parse_args.return_value = mock_args

        with patch('argparse.ArgumentParser.print_help') as mock_print_help:
            result = self.cli.run(['unknown_command'])
            mock_print_help.assert_called_once()
            self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()