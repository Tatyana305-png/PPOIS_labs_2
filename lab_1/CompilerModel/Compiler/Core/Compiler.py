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

    def compile_to_stage(self, target_stage: CompilerState) -> bool:
        """
        Компилирует до указанного этапа
        Возвращает True если успешно, False если была ошибка
        """
        try:
            # Определяем, с какого этапа начинать
            start_stage = self.state
            start_index = CompilerState.get_stage_index(start_stage)
            target_index = CompilerState.get_stage_index(target_stage)

            if target_index < 0:
                print(f"Неверный целевой этап: {target_stage}")
                return False

            print(f"Компиляция до этапа: {target_stage.value}")
            print(f"Текущий этап: {start_stage.value}")

            # Лексический анализ
            if target_index >= CompilerState.get_stage_index(CompilerState.LEXICAL_ANALYSIS) and self._tokens is None:
                self._update_state(CompilerState.LEXICAL_ANALYSIS)
                self._tokens = self.lexical_analyzer.analyze(self.source_code.get_code())
                print(f"Лексический анализ завершен. Найдено токенов: {len(self._tokens)}")

                # Если достигли целевого этапа, сохраняем и выходим
                if target_stage == CompilerState.LEXICAL_ANALYSIS:
                    self._update_state(CompilerState.LEXICAL_ANALYSIS)
                    return True

            # Синтаксический анализ
            if target_index >= CompilerState.get_stage_index(CompilerState.SYNTAX_ANALYSIS) and self._ast is None:
                self._update_state(CompilerState.SYNTAX_ANALYSIS)
                self._ast = self.syntax_analyzer.analyze(self._tokens)
                print("Синтаксический анализ завершен")

                if target_stage == CompilerState.SYNTAX_ANALYSIS:
                    self._update_state(CompilerState.SYNTAX_ANALYSIS)
                    return True

            # Оптимизация
            if target_index >= CompilerState.get_stage_index(
                    CompilerState.OPTIMIZATION) and self._optimized_ast is None:
                self._update_state(CompilerState.OPTIMIZATION)
                self._optimized_ast = self.optimizer.optimize(self._ast)
                print("Оптимизация завершена")

                if target_stage == CompilerState.OPTIMIZATION:
                    self._update_state(CompilerState.OPTIMIZATION)
                    return True

            # Генерация кода
            if target_index >= CompilerState.get_stage_index(
                    CompilerState.CODE_GENERATION) and self._machine_code is None:
                self._update_state(CompilerState.CODE_GENERATION)
                self._machine_code = self.code_generator.generate(self._optimized_ast or self._ast)
                print("Генерация кода завершена")

                if target_stage == CompilerState.CODE_GENERATION:
                    self._update_state(CompilerState.CODE_GENERATION)
                    return True

            # Завершено
            if target_index >= CompilerState.get_stage_index(CompilerState.COMPLETED):
                self._update_state(CompilerState.COMPLETED)
                return True

            return True

        except CompilerException as e:
            self._update_state(CompilerState.ERROR)
            print(f"Ошибка компиляции: {e}")
            return False
        except Exception as e:
            self._update_state(CompilerState.ERROR)
            print(f"Неизвестная ошибка: {e}")
            return False

    def compile(self) -> Optional[MachineCode]:
        """Выполняет полный цикл компиляции"""
        if self.compile_to_stage(CompilerState.COMPLETED):
            return self._machine_code
        return None

    def compile_to_stage_with_optimization(self, target_stage: CompilerState, level: int) -> bool:
        """Компиляция до указанного этапа с уровнем оптимизации"""
        self.optimizer.optimization_level = level
        return self.compile_to_stage(target_stage)

    def save_stage_state(self, filepath: str, stage: Optional[CompilerState] = None) -> None:
        """
        Сохраняет состояние компилятора на определенном этапе
        Если stage не указан, сохраняет текущее состояние
        """
        state = {
            'state': stage or self.state,
            'source_code': self.source_code.get_code(),
            'language': {
                'name': self.source_code.get_language().name,
                'version': self.source_code.get_language().version
            },
            'tokens': self._tokens,
            'ast': self._ast,
            'optimized_ast': self._optimized_ast,
            'machine_code': self._machine_code,
            'optimization_level': self.optimizer.optimization_level
        }

        with open(filepath, 'wb') as f:
            pickle.dump(state, f)

        stage_name = stage.value if stage else self.state.value
        print(f"Состояние ({stage_name}) сохранено в {filepath}")

    def load_stage_state(self, filepath: str) -> bool:
        """
        Загружает состояние компилятора из файла
        Возвращает True если успешно
        """
        try:
            with open(filepath, 'rb') as f:
                state = pickle.load(f)

            self.state = state['state']
            language = ProgrammingLanguage(
                state['language']['name'],
                state['language']['version']
            )
            self.source_code = SourceCode(state['source_code'], language)
            self._tokens = state.get('tokens')
            self._ast = state.get('ast')
            self._optimized_ast = state.get('optimized_ast')
            self._machine_code = state.get('machine_code')
            self.optimizer.optimization_level = state.get('optimization_level', 1)

            # Пересоздаем анализаторы с загруженным языком
            self.lexical_analyzer = LexicalAnalyzer(language)
            self.syntax_analyzer = SyntaxAnalyzer(language)

            print(f"Состояние ({self.state.value}) загружено из {filepath}")
            return True

        except Exception as e:
            print(f"Ошибка загрузки состояния: {e}")
            return False
