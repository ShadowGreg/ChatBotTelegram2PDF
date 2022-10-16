import sqlite3
from start_bot import bot

conn = sqlite3.connect('db/data_base.db', check_same_thread=False)  # Connect DB.
cursor = conn.cursor()  # Create cursor for work with tables.


# Work with DB.
def db_table_val(user_id: int, username: str, registration_date: str, last_used: str):
    cursor.execute('INSERT INTO users (user_id, username, registration_date, last_used) VALUES (?, ?, ?, ?)',
                   (user_id, username, registration_date, last_used))
    conn.commit()


def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Привет! Ваше имя добавленно в базу данных!')
    us_id = message.from_user.id
    username = message.from_user.username
    registration_date = message.text
    last_used = message.text
    db_table_val(user_id=us_id, username=username, registration_date=registration_date, last_used=last_used)
