import os
import glob, os.path
import textwrap

import telebot
from fpdf import FPDF
from settings import TG_TOKEN  # создать файл settings.py и в переменную TG_TOKEN завести свой токен

# добавить settings.py в .gitignore

bot = telebot.TeleBot(TG_TOKEN)
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

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = SRC + message.document.file_name
        local_src = src  # это зачем?
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Конвертирую 😉")
        convert_text_pdf(local_src)
        sendDocument(convert_text_pdf(local_src), chat_id)
        clear_catalog(SRC)
    except Exception as e:
        bot.reply_to(message, e)


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
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fantasize_mm, wrap, ln=1)

    pdf.output(filename, 'F')


# конвертация текста в pdf
def convert_text_pdf(local_src):
    output_filename = local_src + '.pdf'
    file = open(local_src)
    text = file.read()
    file.close()
    text_to_pdf(text, output_filename)
    return output_filename


# прочищаем каталог что бы не засорять диск
def clear_catalog(folder):
    filelist = glob.glob(os.path.join(folder, "*.*"))
    for f in filelist:
        os.remove(f)


# отправка документа
def sendDocument(file_name: str, chat_id: str):
    doc = open(file_name, 'rb')
    bot.send_document(chat_id, doc)
    # bot.send_document(chat_id, "FILEID")
    doc.close()


bot.polling(none_stop=True, interval=0)
