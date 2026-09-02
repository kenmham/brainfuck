from dataclasses import dataclass, field
from typing import Sequence

"""
AST

- Non-destructive copy
- Clear memory
- Comparison
"""

# todo: for, while, math

@dataclass
class Add:
    N: int

@dataclass
class AddTo:
    target: int
    N: int

@dataclass
class AddVar: # non-destructive ; target = target + source ; source unchanged.
    target: int
    source: int

@dataclass 
class Multiply: # non-destructive ; target = target * source ; source unchanged 
    target: int
    count: int
    addend: int

@dataclass
class Move: # moves cursor
    N: int

@dataclass
class Read: # ',' input a byte
    ...

@dataclass
class Write: # '.' output a byte
    ...

Operation = Add | Move | Read | Write

@dataclass
class Loop:
    body: list[Node]

@dataclass
class Repeat: # while counter > 0: body(), counter-=1 -> Loop
    counter: int 
    body: list[Node]

@dataclass
class Project:
    source: int
    targets: Sequence[int]

@dataclass
class Copy:
    source: int
    target: int

@dataclass
class Goto:
    destination: int

@dataclass
class Clear: # Loop([Add(-1)])
    target: int

@dataclass
class IfEquals: # a == b ? body() : nill
    x: int
    y: int
    body: Program

@dataclass
class And: # a AND b nonzero ? target = 1 : nothing / 1 iff both nonzero
    # note: target is a flag and must be FREE; force context manager
    ...

@dataclass
class IsZero: # target == 0 ? flag_pos = 1 : flag_pos = 0
    target: int
    flag_pos: int

@dataclass
class Set: # target = value
    target: int
    value: int

@dataclass
class Print: # write from pos
    target: int

@dataclass
class PrintValue:
    N: int

Primitive = Operation | Loop
Lowerable = Copy | Clear | Project | IfEquals | Set | IsZero | And | AddTo | Print | PrintValue | AddVar | Multiply | Repeat
Node = Lowerable | Primitive


Program = Sequence[Node]
MutableProgram = list[Node]
PrimitiveProgram = Sequence[Primitive]

AnnotatedProgram = Sequence[tuple[Node, PrimitiveProgram]] # (origin node, nodes it is lowered into)

