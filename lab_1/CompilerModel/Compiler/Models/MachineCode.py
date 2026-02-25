from typing import List
from .Instruction import Instruction


class MachineCode:
    """Машинный код"""

    def __init__(self):
        self.instructions: List[Instruction] = []
        self.data_section: List[bytes] = []
        self.entry_point: int = 0

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions.append(instruction)

    def __str__(self) -> str:
        result = ["Машинный код:"]
        for i, instr in enumerate(self.instructions):
            ops = ', '.join(instr.operands)
            result.append(f"  {i:04x}: {instr.opcode} {ops}")
        return '\n'.join(result)