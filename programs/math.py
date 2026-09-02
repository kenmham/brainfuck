from bf.frontend import Frontend
from bf import compile_ft

ft = Frontend()

a, b = ft.new(2)

a.set(6)
b.set(3)

a.multiply(b)

ft.print(a)

print(compile_ft(ft, annotate=True))
