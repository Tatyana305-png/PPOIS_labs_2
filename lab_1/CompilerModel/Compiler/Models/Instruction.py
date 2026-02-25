from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Instruction:
    """Инструкция машинного кода"""
    opcode: str
    operands: List[str]
    address: Optional[int] = None