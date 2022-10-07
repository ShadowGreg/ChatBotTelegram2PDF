import os
import glob, os.path  # Multiple import in one line.
import shutil
import textwrap
import telebot
from fpdf import FPDF


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
        bot.reply_to(message, "Я умею конвертировать из .txt в .pdf, отправь мне файл c расширением .txt")
    else:
        bot.reply_to(message, "Этот бот конвертирует файлы с расширением .txt в .pdf")


# Чат бот принимает файлы.
@bot.message_handler(content_types=['document'])
def handle_docs_photo_docs_photo(message):
    """
    сохранение любого типа файла на компьютер в указанную директорию
    :type message: object
    """
    try:
        chat_id = message.chat.id
        real_file_name, real_file_extension = os.path.splitext(
            message.document.file_name)  # получаем имя и расширение файла, так что бы пронести переменные до конца
        file_name = real_file_name.lower()
        file_extension = real_file_extension.lower()

        if file_extension == '.txt':  # проверяем расширение
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = SRC + file_name + '_' + str(chat_id) + '_' + str(os.times().system)
            # создаем папку в которой будем временно размещать файл, если таковой не существует
            if not os.path.exists(src):
                os.makedirs(src)
            # создаем путь конечного файла
            local_src = src + '/' + real_file_name + real_file_extension  # это зачем?
            # пишем файл на диск
            with open(local_src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Конвертирую 😉")

            convert_text_pdf(local_src)
            sendDocument(convert_text_pdf(local_src), chat_id)
            clear_catalog(SRC)
        else:
            bot.reply_to(message, f"я не знаю такого '{file_extension}' формата 😶‍🌫️😇")

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True)  # Бот на любое сообщение пользователя, кроме файла
# и команды отвечает списком всех доступных команд.
def echo(message):
    chat_id = message.from_user.id  # user_id берется из id_сообщения.
    text = '/start - bot info.\n/help - tips.'
    bot.send_message(chat_id, text)


# сам конвертер
def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fantasize_pt = 10
    fantasize_mm = fantasize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fantasize_pt)
    split = text.split('\n')
    for line in split:
        lines = textwrap.wrap(line, int(width_text))  # перенос
        if len(lines) == 0:
            pdf.ln()
        for wrap in lines:
            pdf.cell(0, fantasize_mm, wrap, ln=1)
    pdf.output(filename, 'F')


# конвертация текста в pdf
def convert_text_pdf(local_src):
    output_filename = local_src + '.pdf'
    file = open(local_src, encoding="utf-8")  # если конвертировать UTF-16 - работает на файлах в UTF-16,
    # но при этом не работает UTF-8, и французский. Надо как-то проверять кодировку файла и разным веткам декодировать
    # painting.txt пока нигде не работает
    text = file.read()
    file.close()
    text_to_pdf(text, output_filename)
    return output_filename


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
