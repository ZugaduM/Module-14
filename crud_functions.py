import sqlite3


def initiate_db():
    tabs_names = ('Помагин', 'Неболин', 'Работин', 'Соннеслабин')
    try:
        connection = sqlite3.connect('not_telegram_2.db')
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INT PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INT NOT NULL,
        balance INT NOT NULL
        );
        ''')
        connection.commit()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INT NOT NULL
        );
        ''')
        connection.commit()

        for i in range(1, 5):
            cursor.execute('''
            INSERT OR IGNORE INTO Products(id, title, description, price) VALUES(?, ?, ?, ?)
            ''', (i, tabs_names[i-1], f"Описание {i}", i * 100))
        connection.commit()

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


def add_user(username, email, age):
    try:
        connection = sqlite3.connect('not_telegram_2.db')
        cursor = connection.cursor()

        last_id = cursor.execute('SELECT MAX(id) from Users').fetchone()
        connection.commit()
        if last_id[0] is None:
            last_id = [1,]

        check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
        connection.commit()

        if check_user is None:
            cursor.execute('''
            INSERT INTO Users(id, username, email, age, balance) VALUES(?, ? ,? ,? ,?)
            ''',(last_id[0]+1, username, email, age, 1000))
            connection.commit()

    except sqlite3.Error as err:
        print('Ошибка при работе с SQLite', err)

    finally:
        if connection:
            connection.close()


def is_exist(username):
    try:
        connection = sqlite3.connect('not_telegram_2.db')
        cursor = connection.cursor()

        result = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        connection.commit()
        if result.fetchone() is None:
            return False
        else:
            return True

    except sqlite3.Error as err:
        print('Ошибка при работе с SQLite', err)

    finally:
        if connection:
            connection.close()