from abc import ABC, abstractmethod
from typing import Any


class IOptimizer(ABC):
    """Интерфейс для оптимизатора"""

    @abstractmethod
    def optimize(self, code: Any) -> Any:
        """Выполнить оптимизацию"""
        pass