import sqlite3


connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
Id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', 10*i,'1000'))

for i in range(1, 11):
    if i %2 != 0:
        cursor.execute('UPDATE Users SET balance = ? WHERE id = ?',
                       ('500', i))

for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE id = ?',
                   (i,))

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', ('60',))
users_data = cursor.fetchall()
for user, mail, age, bal in users_data:
    print(f'Имя: {user} | Почта: {mail} | Возраст: {age} | Баланс: {bal}')

connection.commit()
connection.close()
