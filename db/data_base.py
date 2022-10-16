import sqlite3
from ChatBotTelegram2PDF.start_bot import bot
from datetime import datetime
from os import path
import os
import sys
sys.path.insert(0, os.path.abspath(".."))


# Work with DB.
def db_add_val(user_id: int, username: str, registration_date: str, last_used: str):
    cursor.execute('INSERT INTO users (user_id, username, registration_date, last_used) VALUES (?, ?, ?, ?)',
                   (user_id, username, registration_date, last_used))
    db.commit()


def upd_last_used(username: str, last_used: str):
    cursor.execute(
        'UPDATE users SET (username, last_used) VALUES (?, ?) WHERE user_id = ?',
        (username, last_used))
    db.commit()


def get_script_dir():
    abs_path = path.abspath(__file__)  # полный путь к файлу скрипта
    return path.dirname(abs_path)


DB_NAME = 'data_base.db'
DB_FILE = get_script_dir() + path.sep + DB_NAME

try:
    db = sqlite3.connect(DB_FILE, check_same_thread=False)  # Connect DB.
    cursor = db.cursor()  # Create cursor for work with tables.
except sqlite3.Error as e:
    print("Ошибка при работе с SQLite", e)


# finally: # закрыть соединение, когда все закончено.
#   if db:
#      cursor.close()
#     print("Соединение с SQLite закрыто")


def update_db(message):
    bot.send_message(message.from_user.id, 'Привет! Ваше имя добавленно в базу данных!')

    user_id = message.from_user.id
    username = message.from_user.username
    registration_date = str(datetime.today().strftime('%Y%m%d%H%M%S'))
    last_used = str(datetime.today().strftime('%Y%m%d%H%M%S'))

    check_for_user_id = cursor.execute('SELECT * FROM data_base.db WHERE user_id=?', (user_id,))
    if check_for_user_id.fetchone() is None:  # Делаем когда нету человека в бд
        db_add_val(user_id=user_id, username=username, registration_date=registration_date, last_used=last_used)

# else:  # Делаем когда есть человек в бд
#    upd_last_used(username=username, last_used=last_used)
