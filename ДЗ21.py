import json

dict_1 = {
    123456: ('Алексей', 42),
    234567: ('Дарья', 28),
    345678: ('Сергей', 20),
    456789: ('Эдуард', 31),
    567890: ('Андрей', 36),
    678901: ('Даниил', 31)
}

dict_1 = {str(key): value for key, value in dict_1.items()}

with open('dictionary.json', 'w') as file:
    json.dump(dict_1, file)
