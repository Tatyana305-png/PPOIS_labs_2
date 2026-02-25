from abc import ABC, abstractmethod
from typing import Any


class IAnalyzer(ABC):
    """Интерфейс для анализаторов"""

    @abstractmethod
    def analyze(self, code: Any) -> Any:
        """Выполнить анализ"""
        pass