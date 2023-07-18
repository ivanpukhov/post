import sqlite3

def create_database():
    # Подключение к базе данных (или ее создание, если она не существует)
    conn = sqlite3.connect('packages.db')

    # Создание курсора
    cursor = conn.cursor()

    # Создание таблицы packages с полем tracking_number
    cursor.execute('''
    CREATE TABLE packages (
        tracking_number TEXT PRIMARY KEY
    );
    ''')

    # Добавление значения AP023620989KZ в поле tracking_number
    cursor.execute('''
    INSERT INTO packages (tracking_number) VALUES (?);
    ''', ('AP023620989KZ',))

    # Применение изменений
    conn.commit()

    # Закрытие соединения с базой данных
    conn.close()

if __name__ == "__main__":
    create_database()
