class String(str):
    def __init__(self, value):
        super().__init__()

    def __add__(self, other):
        return String(str(self) + str(other))

    def __sub__(self, other):
        return String(str(self).replace(str(other), '', 1))


