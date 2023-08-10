# Я добавил константы для упрощения использования и избежания хардкода.
# Я разбил длинные строки на более короткие, чтобы они соответствовали ограничению в 79 символов.
import csv
import datetime
import re

# Constants
MIN_YEAR_BIRTH = 1800
DATE_FORMATS = ('%d.%m.%Y', '%d/%m/%Y', '%d,%m,%Y')
GENDER_OPTIONS = ['m', 'f', 'o']
GENDER_LABELS = {
    'm': {
        'text': 'мужчина',
        'birth': 'родился',
        'death': 'умер'
    },
    'f': {
        'text': 'женщина',
        'birth': 'родилась',
        'death': 'умерла'
    },
    'o': {
        'text': 'не бинарная личность',
        'birth': 'дата рождения',
        'death': 'дата смерти'
    }
}

class Person:
    def __init__(self, first_name, last_name=None, middle_name=None, birth_date=None, death_date=None, sex=None):
        self.first_name = first_name.title()
        self.last_name = last_name.title() if last_name else None
        self.middle_name = middle_name.title() if middle_name else None
        self.birth_date = birth_date
        self.death_date = death_date
        self.sex = sex

    @property #метод вычисляет возраст человека.
    def age(self):
        if self.birth_date:
            end_date = self.death_date or datetime.datetime.now()
            return end_date.year - self.birth_date.year - ((end_date.month, end_date.day) < (self.birth_date.month, self.birth_date.day))
        return None

class DB:
    def __init__(self):
        self.data = {} # Этот атрибут будет использоваться для хранения информации о людях.
        # Ключом в этом словаре будет идентификатор человека, а значением — объект типа

    def input_data(self):
        while True:
            first_name = input("Введите имя: ")
            if first_name.isalpha():
                break
            print('Вы ввели неправильный формат')

        while True:
            last_name = input("Введите фамилию (нажмите Enter, чтобы пропустить): ")
            if not last_name or last_name.isalpha():
                break
            print('Вы ввели неправильный формат')

        while True:
            middle_name = input("Введите отчество (нажмите Enter, чтобы пропустить): ")
            if not middle_name or middle_name.isalpha():
                break
            print('Вы ввели неправильный формат')

        while True:
            gender = input("Введите пол (m/f/o): ")
            if gender.lower() in GENDER_OPTIONS:
                break
            print("Пожалуйста, выберите один из вариантов:", ', '.join(GENDER_OPTIONS))

        while True:
            birth_date = input("Введите дату рождения (в формате дд.мм.гггг, дд/мм/гггг или дд,мм,гггг): ")
            if not birth_date:
                print("Дата рождения не может быть пустой.")
            else:
                birth_date_obj = self.str_to_date(birth_date)# преобразуем строку в объект даты и проверяем
                if birth_date_obj:
                    if birth_date_obj.year < MIN_YEAR_BIRTH:
                        print(f'Дата рождения не может быть раньше {MIN_YEAR_BIRTH} года.')
                    elif birth_date_obj > datetime.datetime.now():
                        print('Дата рождения не может быть в будущем.')
                    else:
                        break
                else:
                    print("Дата должна быть в одном из форматов:", ', '.join(DATE_FORMATS))

        while True:
            death_date = input("Введите дату смерти (нажмите Enter, чтобы пропустить): ")
            if not death_date:
                death_date_obj = None
                break
            death_date_obj = self.str_to_date(death_date)
            if death_date_obj:
                if death_date_obj > datetime.datetime.now():
                    print('Дата смерти не может быть в будущем.')
                elif death_date_obj < birth_date_obj:
                    print('Дата смерти не может быть раньше даты рождения.')
                else:
                    break
            else:
                print("Дата должна быть в одном из форматов:", ', '.join(DATE_FORMATS))

        person_id = len(self.data) + 1 #вычисляется новый идентификационный номер
        self.data[person_id] = Person(first_name, last_name, middle_name, birth_date_obj, death_date_obj, gender)

    @staticmethod
    def str_to_date(date_str):
        if date_str:
            for fmt in DATE_FORMATS:
                try:
                    return datetime.datetime.strptime(date_str, fmt)
                except ValueError:
                    pass
            print('Вы ввели неправильный формат даты')
        return None

    def find(self):
        query = input("Введите строку поиска: ")
        results = [p for p in self.data.values() if re.search(query, f"{p.first_name} {p.last_name or ''} {p.middle_name or ''}", re.IGNORECASE)]
        if not results:
            print("Ничего не найдено.")
        else:
            for r in results:
                birth_date_str = r.birth_date.strftime('%d.%m.%Y') if r.birth_date else 'нет данных'
                death_date_str = r.death_date.strftime('%d.%m.%Y') if r.death_date else 'нет данных'
                gender_info = GENDER_LABELS[r.sex]
                age_label = 'возраст' if r.death_date is None else 'возраст на момент смерти'
                print(f"{r.first_name} {r.last_name or ''} {r.middle_name or ''}, {age_label}: {r.age}, {gender_info['text']}. {gender_info['birth']}: {birth_date_str}, {gender_info['death']}: {death_date_str}")

    def save_to_file(self):
        while True:
            try:
                file_name = input("Введите имя файла: ")
                with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(['Имя', 'Фамилия', 'Отчество', 'Дата рождения', 'Дата смерти', 'Пол'])
                    for person in self.data.values():
                        writer.writerow([
                            person.first_name,
                            person.last_name,
                            person.middle_name,
                            person.birth_date.strftime('%d.%m.%Y') if person.birth_date else None,
                            person.death_date.strftime('%d.%m.%Y') if person.death_date else None,
                            person.sex
                        ])
                break
            except Exception as e:
                print(f"Ошибка при сохранении: {e}. Пожалуйста, попробуйте снова.")

    def load_from_file(self):
        while True:
            try:
                file_name = input("Введите имя файла для загрузки данных: ")
                with open(file_name, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    next(reader)  # Пропустим заголовок
                    for row in reader:
                        first_name = row[0]
                        last_name = row[1]
                        middle_name = row[2]
                        birth_date = self.str_to_date(row[3]) if row[3] else None
                        death_date = self.str_to_date(row[4]) if row[4] else None
                        sex = row[5]
                        person_id = len(self.data) + 1
                        self.data[person_id] = Person(first_name, last_name, middle_name, birth_date, death_date, sex)
                break
            except Exception as e:
                print(f"Ошибка при загрузке: {e}. Пожалуйста, попробуйте снова.")

    def menu(self):
        while True:
            print("\n1. Ввести данные")
            print("2. Найти человека")
            print("3. Сохранить в файл")
            print("4. Загрузить из файла")
            print("5. Выход")
            choice = input("Выберите действие: ")
            if choice == "1":
                self.input_data()
            elif choice == "2":
                self.find()
            elif choice == "3":
                self.save_to_file()
            elif choice == "4":
                self.load_from_file()
            elif choice == "5":
                break
            else:
                print("Неверный выбор, пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    db = DB()
    db.menu()

