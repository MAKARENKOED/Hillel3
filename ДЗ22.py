import json
import csv
import random

with open('dictionary.json', 'r') as file:
    data = json.load(file)

operators = ['095', '066', '098', '096', '050', '097']

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Имя', 'Возраст', 'Телефон'])

    for key, value in data.items():
        operator = random.choice(operators)
        phone = ''.join(random.choice('0123456789') for _ in range(7))
        phone = operator + phone
        if random.random() < 0.25:
            phone = ""
        writer.writerow([key, value[0], value[1], phone])

