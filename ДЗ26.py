def progression(start, step):
    current = start
    while True:
        yield current
        current *= step
#проверяем
prog_1 = progression(-2, -5)
for _ in range(6):
    print(next(prog_1))
print("-"*50)
prog_2=progression(10, 3)
for _ in range(6):
    print(next(prog_2))
