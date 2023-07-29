import time
from ДЗ17 import Auto

class Truck(Auto):
    def __init__(self, brand, age, mark, max_load, color=None, weight=None):
        super().__init__(brand, age, mark, color, weight)
        self.max_load = max_load

    def move(self):
        print('attention')
        super().move()

    def load(self):
        time.sleep(1)
        print('load')
        time.sleep(1)

class Car(Auto):
    def __init__(self, brand, age, mark, max_speed, color=None, weight=None):
        super().__init__(brand, age, mark, color, weight)
        self.max_speed = max_speed

    def move(self):
        super().move()
        print('max speed is', self.max_speed)


truck1 = Truck('Volvo', 3, 'FH16', 40, 'White', 8000)
truck2 = Truck('Mercedes', 2, 'Benz', 50, 'Red', 9000)

car1 = Car('Audi', 4, 'R8', 330, 'Grey', 1600)
car2 = Car('Ford', 1, 'Focus', 200, 'Red', 1500)

# Тестирование объектов truck
for truck in [truck1, truck2]:
    truck.move()
    truck.stop()
    truck.birthday()
    truck.load()
    print(truck.age)

# Тестирование объектов car
for car in [car1, car2]:
    car.move()
    car.stop()
    car.birthday()
    print(car.age)
