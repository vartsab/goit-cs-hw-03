import psycopg2

def create_tables():
    # Налаштування з'єднання з PostgreSQL
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="localhost"
    )
    cur = conn.cursor()

    # SQL запити для створення таблиць
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """

    create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
    """

    # Виконання SQL запитів
    cur.execute(create_users_table)
    cur.execute(create_status_table)
    cur.execute(create_tasks_table)

    # Закриття з'єднання
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
