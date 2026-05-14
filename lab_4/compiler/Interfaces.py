from abc import ABC, abstractmethod
from typing import Any, List


class ICodeProvider(ABC):
    """Интерфейс для работы с кодом"""

    @abstractmethod
    def get_code(self) -> str:
        """Получить исходный код"""
        pass

    @abstractmethod
    def set_code(self, code: str) -> None:
        """Установить исходный код"""
        pass


class IAnalyzer(ABC):
    """Интерфейс для анализаторов"""

    @abstractmethod
    def analyze(self, code: Any) -> Any:
        """Выполнить анализ"""
        pass


class IOptimizer(ABC):
    """Интерфейс для оптимизатора"""

    @abstractmethod
    def optimize(self, code: Any) -> Any:
        """Выполнить оптимизацию"""
        pass


class ICodeGenerator(ABC):
    """Интерфейс для генератора кода"""

    @abstractmethod
    def generate(self, ast: Any) -> Any:
        """Сгенерировать машинный код"""
        pass