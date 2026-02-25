import pickle
from typing import Optional, List
from .SourceCode import SourceCode
from Compiler.Models import (
    CompilerState, ProgrammingLanguage,
    Token, ASTNode, MachineCode
)
from Compiler.Exceptions import CompilerException
from Compiler.Core import (
    LexicalAnalyzer, SyntaxAnalyzer,
    Optimizer, MachineCodeGenerator
)


class Compiler:
    """Основной класс компилятора"""

    def __init__(self, source_code: SourceCode):
        self.source_code = source_code
        self.lexical_analyzer = LexicalAnalyzer(source_code.get_language())
        self.syntax_analyzer = SyntaxAnalyzer(source_code.get_language())
        self.optimizer = Optimizer(optimization_level=1)
        self.code_generator = MachineCodeGenerator()

        self.state = CompilerState.INITIALIZED
        self._tokens: Optional[List[Token]] = None
        self._ast: Optional[ASTNode] = None
        self._optimized_ast: Optional[ASTNode] = None
        self._machine_code: Optional[MachineCode] = None

    def _update_state(self, new_state: CompilerState) -> None:
        """Обновляет состояние компилятора"""
        self.state = new_state
        print(f"Состояние изменено: {new_state.value}")

    def compile(self) -> MachineCode:
        """
        Выполняет полный цикл компиляции
        """
        try:
            # Лексический анализ
            self._update_state(CompilerState.LEXICAL_ANALYSIS)
            self._tokens = self.lexical_analyzer.analyze(self.source_code.get_code())
            print(f"Лексический анализ завершен. Найдено токенов: {len(self._tokens)}")

            # Синтаксический анализ
            self._update_state(CompilerState.SYNTAX_ANALYSIS)
            self._ast = self.syntax_analyzer.analyze(self._tokens)
            print("Синтаксический анализ завершен")

            # Оптимизация
            self._update_state(CompilerState.OPTIMIZATION)
            self._optimized_ast = self.optimizer.optimize(self._ast)
            print("Оптимизация завершена")

            # Генерация кода
            self._update_state(CompilerState.CODE_GENERATION)
            self._machine_code = self.code_generator.generate(self._optimized_ast)
            print("Генерация кода завершена")

            self._update_state(CompilerState.COMPLETED)
            return self._machine_code

        except CompilerException as e:
            self._update_state(CompilerState.ERROR)
            print(f"Ошибка компиляции: {e}")
            raise
        except Exception as e:
            self._update_state(CompilerState.ERROR)
            print(f"Неизвестная ошибка: {e}")
            raise CompilerException(str(e), self.state)

    def compile_with_optimization(self, level: int) -> MachineCode:
        """
        Компиляция с указанным уровнем оптимизации
        """
        self.optimizer.optimization_level = level
        return self.compile()

    def save_state(self, filepath: str) -> None:
        """
        Сохраняет состояние компилятора в файл
        """
        state = {
            'state': self.state,
            'source_code': self.source_code.get_code(),
            'language': {
                'name': self.source_code.get_language().name,
                'version': self.source_code.get_language().version
            },
            'tokens': self._tokens,
            'optimization_level': self.optimizer.optimization_level
        }

        with open(filepath, 'wb') as f:
            pickle.dump(state, f)

        print(f"Состояние сохранено в {filepath}")

    def load_state(self, filepath: str) -> None:
        """
        Загружает состояние компилятора из файла
        """
        with open(filepath, 'rb') as f:
            state = pickle.load(f)

        self.state = state['state']
        language = ProgrammingLanguage(
            state['language']['name'],
            state['language']['version']
        )
        self.source_code = SourceCode(state['source_code'], language)
        self._tokens = state.get('tokens')
        self.optimizer.optimization_level = state.get('optimization_level', 1)

        # Пересоздаем анализаторы с загруженным языком
        self.lexical_analyzer = LexicalAnalyzer(language)
        self.syntax_analyzer = SyntaxAnalyzer(language)

        print(f"Состояние загружено из {filepath}")