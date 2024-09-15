import psycopg2
from faker import Faker
import random

fake = Faker()

def seed_data():
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost"
    )
    cur = conn.cursor()

    # Додавання статусів
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))

    # Додавання користувачів
    for _ in range(10):
        fullname = fake.name()
        email = fake.unique.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))

    # Додавання завдань
    for _ in range(20):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status_id = random.randint(1, 3)  # Припускаємо, що є три статуси
        user_id = random.randint(1, 10)  # Припускаємо, що є десять користувачів
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
                    (title, description, status_id, user_id))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_data()
