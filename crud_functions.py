import sqlite3


def initiate_db():
    try:
        connection = sqlite3.connect('not_telegram_2.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INT NOT NULL
        );
        ''')
        tabs_names = ('Помагин', 'Неболин', 'Работин', 'Соннеслабин')
        for i in range(1, 5):
            cursor.execute('''
            INSERT INTO Products(id, title, description, price) VALUES(?, ?, ?, ?)
            ''', (i, tabs_names[i-1], f"Описание {i}", i * 100))
        connection.commit()
        connection.close()
    except sqlite3.Error as err:
        print('Ошибка при работе с SQLite', err)
    finally:
        if connection:
            connection.close()


def get_all_products():
    try:
        connection = sqlite3.connect('not_telegram_2.db')
        cursor = connection.cursor()

        result = cursor.execute('SELECT * FROM Products').fetchall()
        connection.commit()
        connection.close()

        return result
    except sqlite3.Error as err:
        print('Ошибка при работе с SQLite', err)
    finally:
        if connection:
            connection.close()
