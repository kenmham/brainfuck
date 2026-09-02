from bf.frontend import Frontend
from bf import compile_ft

ft = Frontend()

ft.print("hello world")

print(compile_ft(ft, annotate=True))
