class String(str):
    def __init__(self, value):
        super().__init__()

    def __add__(self, other):
        return String(str(self) + str(other))

    def __sub__(self, other):
        return String(str(self).replace(str(other), '', 1))
# проверка
a=String('New') + String(890)
print(a)
b=String('New bala7nce') - 7
print(b)

с=String('pineapple apple pine') - 'apple'
print(с)

