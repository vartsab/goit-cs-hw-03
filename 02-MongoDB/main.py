from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Конфігурація підключення
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cats_database"

def connect_to_mongodb(uri, db_name):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        return db
    except PyMongoError as e:
        print(f"Помилка підключення до MongoDB: {e}")
        return None

def print_all_cats(db):
    try:
        collection = db['cats']
        count = collection.count_documents({})
        if count == 0:
            print("Немає записів у базі даних.")
            return
        cats = collection.find()
        for cat in cats:
            print(f"Ім'я: {cat['name']}")
            print(f"Вік: {cat['age']}")
            print(f"Характеристики: {', '.join(cat['features'])}")
            print("----------------------------")
    except PyMongoError as e:
        print(f"Помилка при виведенні всіх котів: {e}")

def print_cat_by_name(db, name):
    try:
        collection = db['cats']
        cat = collection.find_one({"name": name})
        if cat:
            print(f"Ім'я: {cat['name']}")
            print(f"Вік: {cat['age']}")
            print(f"Характеристики: {', '.join(cat['features'])}")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при виведенні кота за ім'ям: {e}")

def update_cat_age(db, name, new_age):
    try:
        collection = db['cats']
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print("Вік кота оновлено.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_feature_to_cat(db, name, new_feature):
    try:
        collection = db['cats']
        result = collection.update_one({"name": name}, {"$addToSet": {"features": new_feature}})
        if result.matched_count > 0:
            print("Характеристику додано.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики коту: {e}")

def delete_cat(db, name):
    try:
        collection = db['cats']
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print("Кота видалено.")
        else:
            print("Кота з таким ім'ям не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats(db):
    try:
        collection = db['cats']
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except PyMongoError as e:
        print(f"Помилка при видаленні всіх котів: {e}")

def main():
    db = connect_to_mongodb(MONGO_URI, DB_NAME)
    if db is None:
        return

    # Додаємо приклади котів
    db['cats'].insert_many([
        {
         'name': 'Lama',
         'age': 2,
	 'features': ['ходить в лоток', 'не дає себе гладити', 'сірий'],
         },
         {
          'name': 'Liza',
          'age': 4,
          'features': ['ходить в лоток', 'дає себе гладити', 'білий'],
          },
          {
           'name': 'Boris',
           'age': 12,
           'features': ['ходить в лоток', 'не дає себе гладити', 'сірий'],
           },
           {
            'name': 'Murzik',
            'age': 1,
            'features': ['ходить в лоток', 'дає себе гладити', 'чорний'],
            },
        ])

    while True:
        print("\n1. Додати кота")
        print("2. Вивести всіх котів")
        print("3. Вивести кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота")
        print("7. Видалити всіх котів")
        print("8. Вийти")

        choice = input("Оберіть опцію (1-8): ")

        if choice == '1':
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики кота через кому: ").split(",")
            features = [feature.strip() for feature in features]
            try:
                db['cats'].insert_one({"name": name, "age": age, "features": features})
                print("Кота додано.")
            except PyMongoError as e:
                print(f"Помилка при додаванні кота: {e}")
        elif choice == '2':
            print_all_cats(db)
        elif choice == '3':
            name = input("Введіть ім'я кота: ")
            print_cat_by_name(db, name)
        elif choice == '4':
            name = input("Введіть ім'я кота: ")
            new_age = int(input("Введіть новий вік кота: "))
            update_cat_age(db, name, new_age)
        elif choice == '5':
            name = input("Введіть ім'я кота: ")
            new_feature = input("Введіть нову характеристику кота: ")
            add_feature_to_cat(db, name, new_feature)
        elif choice == '6':
            name = input("Введіть ім'я кота: ")
            delete_cat(db, name)
        elif choice == '7':
            delete_all_cats(db)
        elif choice == '8':
            print("Вихід з програми.")
            break
        else:
            print("Неправильний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()

