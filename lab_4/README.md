# Лабораторная работа №4: Веб-интерфейс для компилятора

## Описание

Веб-приложение, предоставляющее графический интерфейс для компилятора из лабораторной работы №1. Приложение позволяет выполнять все этапы компиляции через веб-интерфейс и визуализировать результаты.

## Функциональность

- **Ввод исходного кода** через текстовое поле
- **Выбор этапа компиляции**:
  - Лексический анализ (токены)
  - Синтаксический анализ (AST)
  - Оптимизация
  - Генерация кода
  - Полная компиляция
- **Выбор уровня оптимизации** (0, 1, 2)
- **Визуализация результатов**:
  - Список токенов с таблицей
  - Древовидное представление AST
  - Оптимизированное AST
  - Машинный код
- **Интерактивный режим** для поэтапной компиляции
- **Пример кода** для быстрого тестирования

## Общий код для ЛР №1 и ЛР №4

Вся логика компиляции вынесена в отдельный пакет `compiler/`, который используется как в CLI, так и в веб-приложении:

```python
# ОБЩИЙ КОД - используется и в CLI, и в Web
from compiler.SourceCode import SourceCode
from compiler.Compiler import Compiler
from compiler.Models import ProgrammingLanguage, CompilerState, ASTNode
from compiler.Exceptions import CompilerException
```

## Технологии

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Архитектура**: Клиент-серверное приложение

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/compiler-web.git
cd compiler-web
```

### 2. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск приложения

```bash
python app.py
```

Приложение будет доступно по [адресу](http://localhost:5000)
