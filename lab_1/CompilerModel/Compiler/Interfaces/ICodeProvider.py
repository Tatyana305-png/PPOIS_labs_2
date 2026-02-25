from abc import ABC, abstractmethod


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