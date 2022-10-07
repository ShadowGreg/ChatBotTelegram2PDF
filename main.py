import os
import os.path
import shutil
import telebot

from win32com import client

from txt2Pdf import convert_text_pdf


# Чтение токена. Для того что бы работало надо в папке хранения исполняемого файла создать файл
# с названием TOKEN в нём прописать свой токен без пробелов энтров - только то что скопировано у BotFather
def add_token(path):
    try:
        with open(path, 'r') as f:
            token = f.read().rstrip()
    except Exception as e:
        bot.reply_to(e)
    return token


bot = telebot.TeleBot(add_token('TOKEN'))
local_src = ""
SRC = './tmp_files/'


# 2 реакции на команды для бота.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == '/help':
        bot.reply_to(message, "Этот бот конвертирует файлы с расширением .txt в .pdf")
    else:
        bot.reply_to(message, "Я умею конвертировать из .txt в .pdf, отправь мне файл :)")


# Чат бот принимает файлы.
@bot.message_handler(content_types=['document'])
def handle_docs_photo_docs_photo(message):
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
            sendDocument(convert_text_pdf(local_src), chat_id)
        if file_extension == '.xls' or '.xlsx':  # проверяем расширение excel
            bot.reply_to(message, "xls")
        else:
            bot.reply_to(message, f"я не знаю такого '{file_extension}' формата 😶‍🌫️😇")

        clear_catalog(SRC)
    except Exception as e:
        bot.reply_to(message, e)


# сам конвертер excel to pdf
def excel_to_pdf():  # TODO сделать
    excel2pdf_filename = '0'
    xlApp = client.Dispatch("Excel.Application")
    books = xlApp.Workbooks.Open('C:\\excel\\trial.xls')
    ws = books.Worksheets[0]
    ws.Visible = 1
    ws.ExportAsFixedFormat(0, 'C:\\excel\\trial.pdf')
    return excel2pdf_filename


# прочищаем каталог от всего что бы не засорять диск
def clear_catalog(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# отправка документа
def sendDocument(file_name: str, chat_id: str):
    doc = open(file_name, 'rb')
    bot.send_document(chat_id, doc)
    # bot.send_document(chat_id, "FILEID")
    doc.close()


bot.polling(none_stop=True, interval=0)
