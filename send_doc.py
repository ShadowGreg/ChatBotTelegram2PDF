from start_bot import bot


# отправка файла
def send_document(file_name: str, chat_id: str):
    doc = open(file_name, 'rb')
    bot.send_document(chat_id, doc)
    doc.close()
