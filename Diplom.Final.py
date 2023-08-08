import csv
import datetime
import re

class Person:
    def __init__(self, first_name, last_name=None, middle_name=None, birth_date=None, death_date=None, sex=None):
        self.first_name = first_name.title()
        self.last_name = last_name.title() if last_name else None
        self.middle_name = middle_name.title() if middle_name else None
        self.birth_date = birth_date
        self.death_date = death_date
        self.sex = sex

    @property
    def age(self):
        if self.birth_date:
            end_date = self.death_date or datetime.datetime.now()
            return end_date.year - self.birth_date.year - ((end_date.month, end_date.day) < (self.birth_date.month, self.birth_date.day))
        return None

class DB:
    def __init__(self):
        self.data = {}

    def input_data(self):
        while True:
            first_name = input("Введите имя: ")
            if first_name.isalpha():
                break
            print('Вы ввели неправильный формат имени')

        while True:
            last_name = input("Введите фамилию (опционально,нажмите Enter, чтобы пропустить): ")
            if not last_name or last_name.isalpha():
                break
            print('Вы ввели неправильный формат фамилии')

        while True:
            middle_name = input("Введите отчество (опционально, нажмите Enter, чтобы пропустить): ")
            if not middle_name or middle_name.isalpha():
                break
            print('Вы ввели неправильный формат отчества')

        while True:
            gender = input("Введите пол (m/f/o): ")
            if gender.lower() in ['m', 'f', 'o']:
                break
            print("Неправильный ввод пола. Пожалуйста, выберите 'm', 'f' или 'o'")

        while True:
            birth_date = input("Введите дату рождения (в формате дд.мм.гггг, дд/мм/гггг или дд,мм,гггг): ")
            if not birth_date:
                print("Дата рождения не может быть пустой.")
            else:
                birth_date_obj = self.str_to_date(birth_date)
                if birth_date_obj:
                    if birth_date_obj.year < 1899:
                        print('Дата рождения не может быть раньше 1899 года.')
                    elif birth_date_obj > datetime.datetime.now():
                        print('Дата рождения не может быть в будущем.')
                    else:
                        break
                else:
                    print("Дата рождения не валидна. Дата должна быть в формате дд.мм.гггг, дд/мм/гггг или дд,мм,гггг.")

        while True:
            death_date = input("Введите дату смерти (опционально, нажмите Enter, чтобы пропустить): ")
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
                print("Дата смерти не валидна. Дата должна быть в формате дд.мм.гггг, дд/мм/гггг или дд,мм,гггг.")

        person_id = len(self.data) + 1
        self.data[person_id] = Person(first_name, last_name, middle_name, birth_date_obj, death_date_obj, gender)

    @staticmethod
    def str_to_date(date_str):
        if date_str:
            for fmt in ('%d.%m.%Y', '%d/%m/%Y', '%d,%m,%Y'):
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
                gender_str = 'мужчина' if r.sex == 'm' else 'женщина' if r.sex == 'f' else 'не бинарная личность'
                birth_or_date = 'дата рождения' if r.sex == 'o' else 'родился' if r.sex == 'm' else 'родилась'
                death_or_date = 'дата смерти' if r.sex == 'o' else 'умер' if r.sex == 'm' else 'умерла'
                age_label = 'возраст' if r.death_date is None else 'возраст на момент смерти'
                print(f"{r.first_name} {r.last_name or ''} {r.middle_name or ''}, {age_label}: {r.age}, {gender_str}. {birth_or_date}: {birth_date_str}, {death_or_date}: {death_date_str}")

    def save_to_file(self):
        file_name = 'database.csv'
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'first_name', 'last_name', 'middle_name', 'birth_date', 'death_date', 'sex']
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

            writer.writeheader()
            for id, person in self.data.items():
                writer.writerow({
                    'id': id,
                    'first_name': person.first_name,
                    'last_name': person.last_name,
                    'middle_name': person.middle_name,
                    'birth_date': person.birth_date.strftime('%d.%m.%Y') if person.birth_date else '',
                    'death_date': person.death_date.strftime('%d.%m.%Y') if person.death_date else '',
                    'sex': person.sex
                })
        print(f"Данные сохранены в {file_name}")

    def load_from_file(self):
        file_name = 'database.csv'
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.data = {}
            for row in reader:
                self.data[int(row['id'])] = Person(row['first_name'], row['last_name'], row['middle_name'],
                                                   self.str_to_date(row['birth_date']) if row['birth_date'] else None,
                                                   self.str_to_date(row['death_date']) if row['death_date'] else None,
                                                   row['sex'])
        print(f"Данные загружены из {file_name}")

    @staticmethod
    def csv_encoder(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%d.%m.%Y')
        return str(obj)

def main():
    db = DB()

    while True:
        print("\nВыберите операцию:")
        print("1. Добавить новые данные")
        print("2. Поиск по данным")
        print("3. Загрузить данные из файла")
        print("4. Сохранить данные в файл")
        print("5. Выйти")
        choice = input("> ")

        if choice == "1":
            db.input_data()
        elif choice == "2":
            db.find()
        elif choice == "3":
            db.load_from_file()
        elif choice == "4":
            db.save_to_file()
        elif choice == "5":
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")

if __name__ == "__main__":
    main()
