#!/usr/bin/env python3
"""Скрипт для запуска тестов с измерением покрытия"""

import pytest
import sys
import os


def main():
    """Запускает тесты с измерением покрытия"""

    # Аргументы для pytest с coverage
    args = [
        "--cov=compiler",  # Измерять покрытие для пакета compiler
        "--cov-report=term",  # Отчет в терминале
        "--cov-report=html",  # HTML отчет
        "--cov-report=xml",  # XML отчет (для CI/CD)
        "--cov-branch",  # Измерять покрытие ветвлений
        "--verbose",  # Подробный вывод
        "tests/"  # Директория с тестами
    ]

    # Запускаем pytest
    result = pytest.main(args)

    print("\n" + "=" * 60)
    print("ОТЧЕТЫ О ПОКРЫТИИ СОЗДАНЫ:")
    print("  - Терминальный отчет: выше")
    print("  - HTML отчет: htmlcov/index.html")
    print("  - XML отчет: coverage.xml")
    print("=" * 60)

    return result


if __name__ == "__main__":
    sys.exit(main())