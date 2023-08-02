class NegativePowerError(Exception):
    """Exception raised when power is negative."""
    pass

class Calculator:

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def subtract(x, y):
        return x - y

    @staticmethod
    def multiply(x, y):
        return x * y

    @staticmethod
    def divide(x, y):
        try:
            return x / y
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")
    @staticmethod
    def power(x, y):
        try:
            if y < 0:
                raise NegativePowerError("Error: Negative powers are not allowed.")
            else:
                return x ** y
        except NegativePowerError as npe:
            print(npe)

    @staticmethod
    def sqrt(x):
        try:
            if x < 0:
                raise ValueError("Error: Negative value. Square root from negative numbers is not allowed.")
            else:
                return x ** 0.5
        except ValueError as ve:
            print(ve)
...
#проверка

calc = Calculator()

print(calc.add(5, 3))
print(calc.subtract(5, 3))
print(calc.multiply(5, 3))
print(calc.divide(5, 2))
print(calc.divide(5, 0))
print(calc.power(5, 3))
print(calc.power(5, -3))
print(calc.sqrt(9))
print(calc.sqrt(-9))
