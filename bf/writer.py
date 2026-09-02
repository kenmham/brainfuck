from .config import ANNOTATION_WIDTH
from . import ir

def write(program: ir.PrimitiveProgram) -> str:
    out = ""
    for op in program:
        match op:
            case ir.Add(n):   out += ("+" if n >= 0 else "-") * abs(n)
            case ir.Move(n):  out += (">" if n >= 0 else "<") * abs(n)
            case ir.Read():   out += ","
            case ir.Write():  out += "."
            case ir.Loop(body): out += "[" + write(body) + "]"
    return out

def write_annotated(annotated: ir.AnnotatedProgram) -> str:
    lines = []
    for node, block in annotated:
        bf = write(block)
        chunks = [bf[i:i+ANNOTATION_WIDTH] for i in range(0, len(bf), ANNOTATION_WIDTH)] or [""]
        for j, chunk in enumerate(chunks):
            note = repr(node) if j == 0 else ""
            lines.append(f"{chunk:<{ANNOTATION_WIDTH}}  {note}".rstrip())
    return "\n".join(lines)
