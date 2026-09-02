from typing import Sequence

from . import ir
from .context import Context

SelfCopyException: BaseException = Exception("Cannot Project source onto source.")

def goto(ctx: Context, target: int) -> Sequence[ir.Primitive]:
    delta = ctx.delta_to(target)
    ctx.cursor = target
    
    return [ir.Move(delta)] if delta else []

def maybe_clear(ctx, cell): # clear temp after use if Context is in safe mode
    if not ctx.safe:
        return []
    return [*goto(ctx, cell), ir.Loop([ir.Add(-1)])]

def lower(node: ir.Node, ctx: Context) -> Sequence[ir.Primitive]:
    match node:
        case ir.Clear(target): # goto target, loop[add -1]
            return [*goto(ctx, target), ir.Loop([ir.Add(-1)])]

        case ir.Project(source, targets): # Loop(-1 at source, move to target1, +1, target2 +2, ..., goto source)
            if source in targets: raise SelfCopyException

            return [
                *goto(ctx, source),                                  # position at source
                ir.Loop([
                    ir.Add(-1),                                   # decrement counter
                    *[op for t in targets for op in lower(ir.AddTo(t, 1), ctx)],   # fan-out
                    *goto(ctx, source),                              # back to source before ]
                ]),
            ]
        
        case ir.Copy(source, dest): # non-destructive copy ; fetch temp, project source to tmp, dest ; project tmp to source
            if source == dest: raise SelfCopyException

            with ctx.temp() as tmp:
                return [
                    *lower(ir.Project(source, [dest, tmp]), ctx),
                    *lower(ir.Project(tmp, [source]), ctx),
                    *maybe_clear(ctx, tmp)
                ]

        case ir.Set(target, value):
            return [
                *lower(ir.Clear(target), ctx),
                *lower(ir.AddTo(target, value), ctx)
            ]

        case ir.AddTo(target, value):
            return [*goto(ctx, target), *lower(ir.Add(value), ctx)]

        case ir.Print(target):
            return [*goto(ctx, target), ir.Write()]

        case ir.PrintValue(value):     # borrow t, t = v, write t
            with ctx.temp() as tmp:
                return [
                    *lower(ir.Set(tmp, value), ctx),
                    *lower(ir.Print(tmp), ctx),
                    *maybe_clear(ctx, tmp),
                ]

        case ir.AddVar(target, source): # non-destructive target = target + source ; source unchanged.
            return [
                *lower(ir.Copy(source, target), ctx),
            ]

        case ir.Repeat(counter, body): # # while counter > 0: body(), counter-=1 -> Loop ; counter will be 0
            return [
                *goto(ctx, counter),
                ir.Loop(
                    [ir.Add(-1), *lower_program(body, ctx), *goto(ctx, counter)]
                )
            ]

        case ir.Multiply(target, count, addend): # non-destructive ; *target = addend * count ; source unchanged 
            with ctx.temp() as counter:
                return [
                    *lower(ir.Copy(count, counter), ctx),                    # counter = count
                    *lower(ir.Clear(target), ctx),
                    *lower(ir.Repeat(counter, [ir.AddVar(target, addend)]), ctx),  # target += addend, count times
                    *maybe_clear(ctx, counter),
                ]

        case ir.IfEquals: #  a - b until either a or b is 0, then check if the other one is zero, if not skip, else enter body
            return []

        case _ if isinstance(node, ir.Primitive):
            return [node]

    raise NotImplementedError("Unknown Lowerable node.")


def lower_program(program: ir.Program, ctx: Context) -> ir.PrimitiveProgram:
    return [op for n in program for op in lower(n, ctx)]

def annotated_lower_program(program, ctx) -> ir.AnnotatedProgram:
    return [(n, list(lower(n, ctx))) for n in program]
