from start_bot import bot
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))
from db import data_base


# отправка файла
def send_document(file_name: str, chat_id: str, message):
    doc = open(file_name, 'rb')
    bot.send_document(chat_id, doc)
    data_base.connect_db(message)
    doc.close()
