"""
Frontend: manages tooling for creating IR, and manages bindings for named variables.
"""

from functools import wraps

from .context import Context
from . import ir

def char_to_int(char: str): return ord(char)

UseAfterFreeError: Exception = Exception("Binding has been freed and cannot be used.")

def requires_alive(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.deleted:
            raise UseAfterFreeError
        return method(self, *args, **kwargs)   # forward the rest
    return wrapper

class Binding: # named cell
    def __init__(self, parent: "Frontend", id: int) -> None:
        self.id: int = id
        self.parent: "Frontend" = parent

        self.deleted = False

    @requires_alive
    def set(self, value: int):
        self.parent.append(
            ir.Set(self.id, value)
        )

    def set_char(self, value: str): self.set(char_to_int(value))

    @requires_alive
    def add(self, value: int | Binding): # add literal
        if isinstance(value, int):
            self.parent.append(
                ir.AddTo(self.id, value)
            )
        else:
            self.parent.append(
                ir.AddVar(self.id, value.id)
            )

    @requires_alive
    def multiply(self, value: int | Binding):  # self = self * value
        if isinstance(value, int):
            self.parent.append(
                ir.Multiply(self.id, self.id, value)
            )
        else:
            self.parent.append(
                ir.Multiply(self.id, self.id, value.id)
            )

    @requires_alive
    def free(self):
        self.parent.context.dealloc(self.id)
        self.deleted = True

class Frontend:
    def __init__(self) -> None:
        self.context: Context = Context()
        self.program: ir.MutableProgram = [] # -> ir.PrimitiveProgram

        self._sinks = [self.program] # level

    def new(self, n=1):
        return (Binding(self, self.context.alloc()) for _ in range(n))

    def append(self, node: ir.Node):
        self.program.append(node)

    def print(self, value: Binding | int | str):
        if isinstance(value, Binding): # check it exists, not deleted, etc
            self.program.append(
                ir.Print(value.id)
            )
        elif isinstance(value, int):
            self.program.append(
                ir.PrintValue(value)
            )
        else:
            for c in value: # errs?
                self.program.append(
                    ir.PrintValue(char_to_int(c))
                    )
