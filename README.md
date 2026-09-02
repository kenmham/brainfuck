# Brainfuck

A handwritten tooling library for writing Brainfuck using high-level Python objects.

The different files in bf/ are modular, and can be reused to connect to any frontend, for example direct Python transpiling or a custom programming language.

## Example

(programs/math.py)

```py
from bf.frontend import Frontend
from bf import compile_ft

ft = Frontend()

a, b = ft.new(2)

a.set(6)
b.set(3)

a.multiply(b)

ft.print(a)

print(compile_ft(ft, annotate=True))
```

Run it from root with:

```bash
python3 -m programs.math
```