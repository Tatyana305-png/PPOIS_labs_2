#!/usr/bin/env python3
"""
Веб-интерфейс для компилятора
Лабораторная работа №4
"""

import json
import traceback
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session

from compiler.SourceCode import SourceCode
from compiler.Compiler import Compiler
from compiler.Models import ProgrammingLanguage, CompilerState, ASTNode
from compiler.Exceptions import CompilerException

app = Flask(__name__)
app.secret_key = 'compiler-secret-key-2024'

# Язык по умолчанию
DEFAULT_LANGUAGE = ProgrammingLanguage("SimpleLang", "1.0")

# Пример кода
EXAMPLE_CODE = '''int x = 5 + 3;
int y = 10;
int result = x * y;

if (result > 50) {
    result = result - 10;
} else {
    result = result + 10;
}

while (result > 0) {
    result = result - 1;
}

return result;'''


def create_compiler(code: str) -> Compiler:
    """Создает экземпляр компилятора с заданным кодом"""
    source_code = SourceCode(code, DEFAULT_LANGUAGE)
    return Compiler(source_code)


def ast_to_dict(node: ASTNode) -> dict:
    """Преобразует AST в словарь для JSON"""
    return {
        'type': node.type,
        'value': node.value,
        'line': node.line,
        'column': node.column,
        'children': [ast_to_dict(child) for child in node.children]
    }


def token_to_dict(token) -> dict:
    """Преобразует токен в словарь"""
    return {
        'type': token.type.value,
        'value': token.value,
        'line': token.line,
        'column': token.column
    }


def instruction_to_dict(instr) -> dict:
    """Преобразует инструкцию в словарь"""
    return {
        'opcode': instr.opcode,
        'operands': instr.operands
    }


def count_ast_nodes(node: ASTNode) -> int:
    """Подсчитывает количество узлов в AST"""
    count = 1
    for child in node.children:
        count += count_ast_nodes(child)
    return count


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/compile', methods=['GET', 'POST'])
def compile_page():
    """Страница компиляции"""
    if request.method == 'POST':
        code = request.form.get('code', '')
        stage = request.form.get('stage', 'full')
        optimization_level = int(request.form.get('optimization', '1'))

        # Создаем компилятор
        compiler = create_compiler(code)
        compiler.optimizer.optimization_level = optimization_level

        # Определяем целевой этап
        stage_map = {
            'lexical': CompilerState.LEXICAL_ANALYSIS,
            'syntax': CompilerState.SYNTAX_ANALYSIS,
            'optimize': CompilerState.OPTIMIZATION,
            'code': CompilerState.CODE_GENERATION,
            'full': CompilerState.COMPLETED
        }
        target_stage = stage_map.get(stage, CompilerState.COMPLETED)

        # Выполняем компиляцию
        result = {
            'success': True,
            'stage': stage,
            'optimization_level': optimization_level,
            'errors': [],
            'tokens': None,
            'ast': None,
            'optimized_ast': None,
            'machine_code': None,
            'statistics': {}
        }

        try:
            success = compiler.compile_to_stage(target_stage)
            result['success'] = success

            if not success:
                result['errors'].append("Ошибка компиляции")
                return render_template('compile.html', result=result, example_code=code)

            # Собираем результаты в зависимости от этапа
            if target_stage.value >= CompilerState.LEXICAL_ANALYSIS.value and compiler._tokens:
                result['tokens'] = [token_to_dict(t) for t in compiler._tokens]
                # Статистика токенов
                token_stats = {}
                for token in compiler._tokens:
                    token_stats[token.type.value] = token_stats.get(token.type.value, 0) + 1
                result['statistics']['tokens'] = token_stats

            if target_stage.value >= CompilerState.SYNTAX_ANALYSIS.value and compiler._ast:
                result['ast'] = ast_to_dict(compiler._ast)
                result['statistics']['ast_nodes'] = count_ast_nodes(compiler._ast)

            if target_stage.value >= CompilerState.OPTIMIZATION.value and compiler._optimized_ast:
                result['optimized_ast'] = ast_to_dict(compiler._optimized_ast)
                result['statistics']['optimized_nodes'] = count_ast_nodes(compiler._optimized_ast)

            if target_stage.value >= CompilerState.CODE_GENERATION.value and compiler._machine_code:
                result['machine_code'] = [instruction_to_dict(instr) for instr in compiler._machine_code.instructions]
                result['statistics']['instructions'] = len(compiler._machine_code.instructions)

        except CompilerException as e:
            result['success'] = False
            result['errors'].append(str(e))
            print(f"CompilerException: {e}")
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"Ошибка: {str(e)}")
            print(f"Unexpected error: {e}")
            traceback.print_exc()

        return render_template('compile.html', result=result, example_code=code)

    return render_template('compile.html', example_code=EXAMPLE_CODE)


@app.route('/interactive')
def interactive_page():
    """Интерактивная страница для поэтапной компиляции"""
    return render_template('interactive.html')


@app.route('/api/compile', methods=['POST'])
def api_compile():
    """API для компиляции (для интерактивного режима)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Нет данных'})

        code = data.get('code', '')
        stage = data.get('stage', 'full')
        optimization_level = int(data.get('optimization', '1'))

        compiler = create_compiler(code)
        compiler.optimizer.optimization_level = optimization_level

        stage_map = {
            'lexical': CompilerState.LEXICAL_ANALYSIS,
            'syntax': CompilerState.SYNTAX_ANALYSIS,
            'optimize': CompilerState.OPTIMIZATION,
            'code': CompilerState.CODE_GENERATION,
            'full': CompilerState.COMPLETED
        }
        target_stage = stage_map.get(stage, CompilerState.COMPLETED)

        response = {
            'success': True,
            'stage': stage,
            'tokens': None,
            'ast': None,
            'optimized_ast': None,
            'machine_code': None,
            'error': None
        }

        success = compiler.compile_to_stage(target_stage)
        response['success'] = success

        if success:
            if compiler._tokens:
                response['tokens'] = [token_to_dict(t) for t in compiler._tokens]

            if compiler._ast:
                response['ast'] = ast_to_dict(compiler._ast)

            if compiler._optimized_ast:
                response['optimized_ast'] = ast_to_dict(compiler._optimized_ast)

            if compiler._machine_code:
                response['machine_code'] = [instruction_to_dict(instr) for instr in compiler._machine_code.instructions]
        else:
            response['error'] = "Ошибка компиляции"

    except CompilerException as e:
        response = {'success': False, 'error': str(e)}
        print(f"CompilerException: {e}")
    except Exception as e:
        response = {'success': False, 'error': f"Ошибка: {str(e)}"}
        print(f"Unexpected error: {e}")
        traceback.print_exc()

    return jsonify(response)


@app.route('/about')
def about_page():
    """Информация о компиляторе"""
    return render_template('about.html')


@app.route('/api/example')
def api_example():
    """Возвращает пример кода"""
    return jsonify({'code': EXAMPLE_CODE})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)