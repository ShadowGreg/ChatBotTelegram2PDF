import os
import os.path

from send_doc import send_document
from start_bot import bot
from clear_catalog import clear_catalog
from txt_to_pdf import convert_text_pdf

local_src = ""
SRC = './tmp_files/'


# 2 реакции на команды для бота.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == '/help':
        bot.reply_to(message, "Я умею конвертировать из .txt в .pdf, отправь мне файл c расширением .txt")
    else:
        bot.reply_to(message, "Этот бот конвертирует файлы с расширением .txt в .pdf")


# Чат бот принимает файлы.
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    """
    сохранение любого типа файла на компьютер в указанную директорию
    :type message: object
    """
    try:
        chat_id = message.chat.id
        # получаем имя и расширение файла, так что бы пронести переменные до конца
        real_file_name, real_file_extension = os.path.splitext(message.document.file_name)
        file_name = real_file_name.lower()
        file_extension = real_file_extension.lower()

        if file_extension == '.txt':  # проверяем расширение txt
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = SRC + file_name + '_' + str(chat_id) + '_' + str(os.times().system)
            # создаем папку в которой будем временно размещать файл, если таковой не существует
            if not os.path.exists(src):
                os.makedirs(src)
            # создаем путь конечного файла
            local_src = src + '/' + real_file_name + real_file_extension
            # пишем файл на диск
            with open(local_src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Конвертирую 😉")

            convert_text_pdf(local_src)
            send_document(convert_text_pdf(local_src), chat_id)
        if file_extension == '.xls' or '.xlsx':  # проверяем расширение excel
            bot.reply_to(message, "xls")
        if file_extension == '.doc' or '.docx':  # проверяем расширение excel
            bot.reply_to(message, "doc")
        else:
            bot.reply_to(message, f"я не знаю такого '{file_extension}' формата 😶‍🌫️😇")

        clear_catalog(SRC)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True)  # Бот на любое сообщение пользователя, кроме файла
# и команды отвечает списком всех доступных команд.
def echo(message):
    chat_id = message.from_user.id  # user_id берется из id_сообщения.
    text = '/start - bot info.\n/help - tips.'
    bot.send_message(chat_id, text)



bot.polling(none_stop=True, interval=0)
