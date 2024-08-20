import sqlite3


connection = sqlite3.connect('not_telegram_2.db')
cursor = connection.cursor()

# cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
data_count = cursor.fetchone()[0]
print(data_count)

cursor.execute('SELECT SUM(balance) FROM Users')
balance_sum = cursor.fetchone()[0]
print(balance_sum)

cursor.execute('SELECT AVG(balance) FROM Users')
avg_balance = cursor.fetchone()[0]
print(avg_balance)

connection.commit()
connection.close()
