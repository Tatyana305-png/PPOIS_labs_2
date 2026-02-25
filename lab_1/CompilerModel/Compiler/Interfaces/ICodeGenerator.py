from abc import ABC, abstractmethod
from typing import Any


class ICodeGenerator(ABC):
    """Интерфейс для генератора кода"""

    @abstractmethod
    def generate(self, ast: Any) -> Any:
        """Сгенерировать машинный код"""
        pass