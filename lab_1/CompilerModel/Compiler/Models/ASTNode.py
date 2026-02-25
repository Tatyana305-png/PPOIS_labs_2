from dataclasses import dataclass
from typing import List, Any


@dataclass
class ASTNode:
    """Узел абстрактного синтаксического дерева"""
    type: str
    value: Any
    children: List['ASTNode']
    line: int
    column: int