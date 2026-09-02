from .lower import lower_program, annotated_lower_program
from .writer import write, write_annotated
from .frontend import Frontend

def compile(program, ctx, annotate=False) -> str: # High-level Program -> lowered primitives -> BF string
    if annotate:
        return write_annotated(annotated_lower_program(program, ctx))
    else:
        return write(lower_program(program, ctx))

def compile_ft(frontend: Frontend, annotate=False) -> str:
    return compile(frontend.program, frontend.context, annotate)
