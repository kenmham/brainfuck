from .frontend import Frontend
from .lower import annotated_lower_program
from .writer import write_annotated

ft = Frontend()

a = ft.new()
a.set(5)

# -----

pgm = annotated_lower_program(ft.program, ft.context)
bf = write_annotated(pgm)

print(bf)
