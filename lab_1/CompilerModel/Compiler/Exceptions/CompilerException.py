from Compiler.Models import CompilerState


class CompilerException(Exception):
    """Базовое исключение компилятора"""

    def __init__(self, message: str, stage: CompilerState, line: int = 0, column: int = 0):
        self.message = message
        self.stage = stage
        self.line = line
        self.column = column
        super().__init__(self.__str__())

    def __str__(self) -> str:
        base = f"[{self.stage.value}] {self.message}"
        if self.line > 0:
            base += f" в строке {self.line}"
            if self.column > 0:
                base += f", позиция {self.column}"
        return base