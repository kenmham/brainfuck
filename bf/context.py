from contextlib import contextmanager
from typing import Generator

from .config import DEFAULT_SAFE_DEALLOC

class Context:
    def __init__(self, safe=DEFAULT_SAFE_DEALLOC) -> None:
        self.cursor = 0
        self.used: set[int] = set()
        self.safe = safe

    def delta_to(self, target: int):
        return target - self.cursor

    def unsafe_dealloc(self, cell: int): self.used.discard(cell)

    def safe_dealloc(self, cell: int):
        self.unsafe_dealloc(cell)

    def dealloc(self, cell: int): # decision logic by self.safe config
        if self.safe:
            return self.safe_dealloc(cell)
        else:
            return self.unsafe_dealloc(cell)

    @contextmanager
    def temp(self) -> Generator[int]:
        cell = self.alloc()
        try:
            yield cell
        finally:
            self.dealloc(cell)  # deterministic free on block exit

    def _alloc(self) -> int: # (lowest free cell) can optimize cursor distance using full AST
        cell = 0
        while cell in self.used:      
            cell += 1
        self.used.add(cell)
        return cell

    def alloc(self) -> int:
        return self._alloc()
