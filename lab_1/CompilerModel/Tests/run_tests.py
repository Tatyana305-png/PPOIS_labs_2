#!/usr/bin/env python3
"""Скрипт для запуска всех тестов"""

import unittest
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем все тестовые классы
from Tests.TestProgrammingLanguage import TestProgrammingLanguage
from Tests.TestLexicalAnalyzer import TestLexicalAnalyzer
from Tests.TestSyntaxAnalyzer import TestSyntaxAnalyzer
from Tests.TestOptimizer import TestOptimizer
from Tests.TestMachineCodeGenerator import TestMachineCodeGenerator
from Tests.TestCompiler import TestCompiler


def create_test_suite():
    """Создает тестовый набор из всех тестов"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тесты
    suite.addTests(loader.loadTestsFromTestCase(TestProgrammingLanguage))
    suite.addTests(loader.loadTestsFromTestCase(TestLexicalAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSyntaxAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestOptimizer))
    suite.addTests(loader.loadTestsFromTestCase(TestMachineCodeGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestCompiler))

    return suite


def run_tests(verbose: bool = False):
    """Запускает все тесты"""
    suite = create_test_suite()

    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()


def main():
    """Точка входа"""
    import argparse

    parser = argparse.ArgumentParser(description='Запуск тестов модели компилятора')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Подробный вывод')
    parser.add_argument('--test', type=str,
                        help='Запустить конкретный тест (например, TestCompiler.test_compile)')

    args = parser.parse_args()

    if args.test:
        # Запускаем конкретный тест
        suite = unittest.TestSuite()
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(args.test))

        runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
        result = runner.run(suite)
        success = result.wasSuccessful()
    else:
        # Запускаем все тесты
        success = run_tests(args.verbose)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()