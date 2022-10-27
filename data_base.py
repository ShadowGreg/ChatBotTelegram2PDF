import sqlite3
from start_bot import bot
from datetime import datetime
from os import path
import os
import sys

sys.path.insert(0, os.path.abspath(""))  # Absolute path to DB.


# Work with DB.
def db_add_val(db, cursor, user_id: int, username: str, registration_date: str, last_used: str):
    cursor.execute('INSERT INTO users (user_id, username, registration_date, last_used) VALUES (?, ?, ?, ?)',
                   (user_id, username, registration_date, last_used))
    db.commit()


def upd_last_used(db, cursor, username: str, last_used: str, user_id: int):
    cursor.execute(
        'UPDATE users SET username = ?, last_used = ? WHERE user_id = ?',
        (username, last_used, user_id))
    db.commit()


def get_script_dir():
    abs_path = path.abspath(__file__)  # полный путь к файлу скрипта
    return path.dirname(abs_path)


def update_db(db, cursor, message):
    try:
        bot.send_message(message.from_user.id, 'Большой брат следит за тобой!')  # Отладочное сообщение.

        user_id = message.from_user.id
        username = message.from_user.username
        registration_date = str(datetime.today().strftime('%Y%m%d%H%M%S'))
        last_used = str(datetime.today().strftime('%Y%m%d%H%M%S'))

        check_for_user_id = cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        if check_for_user_id.fetchone() is None:  # Делаем когда нету человека в бд
            db_add_val(db, cursor, user_id=user_id, username=username, registration_date=registration_date, last_used=last_used)
        else:  # Делаем когда есть человек в бд
            upd_last_used(db, cursor, username=username, last_used=last_used, user_id=user_id)
    except sqlite3.Error as i:
        print("Ошибка при работе с SQLite", i)


# To be done: hide output from user.

def connect_db(message):
    try:
        db = sqlite3.connect(DB_FILE, check_same_thread=False)  # Connect DB.
        cursor = db.cursor()  # Create cursor for work with tables.
        update_db(db, cursor, message)
    except sqlite3.Error as e:
        print("Ошибка при работе с SQLite", e)
    finally:  # закрыть соединение, когда все закончено.
        if db:
            cursor.close()
        print("Соединение с SQLite закрыто")


DB_NAME = 'data_base.db'
DB_FILE = get_script_dir() + path.sep + DB_NAME
