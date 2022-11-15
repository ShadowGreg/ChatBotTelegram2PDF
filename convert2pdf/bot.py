import telebot
import data_base
import os
from utils import file_save, clear_catalog
import converters as c
import messages as m
import logging

LOG_LEVEL = logging.DEBUG


# Чтение токена. Для того что бы работало надо в папке хранения исполняемого файла создать файл
# с названием TOKEN в нём прописать свой токен без пробелов энтров - только то что скопировано у BotFather
def add_token(path='TOKEN.env'):
    bot_token_env = os.environ.get('TG_TOKEN', None)
    if bot_token_env:
        return bot_token_env

    try:
        with open(path, 'r') as f:
            token = f.read().rstrip()
    except Exception as e:
        bot.reply_to(e)
    return token


# Инициализация бота
bot = telebot.TeleBot(add_token())


# Сообщение пользователю, что бот приступил к конверсии файла.
def conversion_message(message):
    bot.reply_to(message, m.CONVERT_MESSAGE)


# 2 реакции на команды для бота.
@bot.message_handler(commands=['start', 'help', 'info'])  # tab-ы не трогать!
def send_welcome(message):
    if message.text == '/help':
        bot.reply_to(message, m.HELP_MESSAGE)
    elif message.text == '/start':
        bot.reply_to(message, m.START_MESSAGE)
    else:
        bot.reply_to(message, m.INFO_MESSAGE)


# Чат бот принимает файлы.
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    """
    сохранение любого типа файла на компьютер в указанную директорию
    :type message: object
    """
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        full_file_name = file_save(message.chat.id, message.document.file_name, downloaded_file)
        result = file_switcher(full_file_name, message)
        if result:
            with open(result, 'rb') as result_file :
                bot.send_document(message.chat.id, result_file)
                data_base.connect_db(message)
        clear_catalog(os.path.dirname(full_file_name))
    except Exception as e:
        logging.warning(e)
        bot.reply_to(message, e)


# Чат бот принимает картинки.
@bot.message_handler(content_types=['photo'])
def photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_unique_id
    file_extension = '.' + file_info.file_path.split('.')[1]

    downloaded_file = bot.download_file(file_info.file_path)
    try:
        full_file_name = file_save(message.chat.id, file_name + file_extension, downloaded_file)
        result = file_switcher(full_file_name, message)
        if result:
            with open(result, 'rb') as result_file:
                bot.send_document(message.chat.id, result_file)
                data_base.connect_db(message)
        clear_catalog(os.path.dirname(full_file_name))
    except Exception as e:
        logging.warning(e)
        bot.reply_to(message, e)


# Бот на любое сообщение пользователя, кроме файла
# и команды отвечает списком всех доступных команд.
@bot.message_handler(func=lambda message: True)
def echo(message):
    chat_id = message.from_user.id
    text = m.ANSWER_MESSAGE
    bot.send_message(chat_id, text)


def file_switcher(full_file_name, message):
    conversion_message(message)

    doc_path, base_name = os.path.split(full_file_name)
    _, file_extension = os.path.splitext(base_name)

    if file_extension in c.TXT_EXT:  # проверяем расширения txt/csv
        return c.txt_to_pdf(full_file_name)
    elif file_extension in c.IMG_EXT:  # проверяем расширения картинок
        return c.img_to_pdf(full_file_name)
    elif file_extension in c.IMG_EXT_IOS:  # проверяем расширения картинок IOS
        return c.ios_img_to_pdf(full_file_name)
    elif file_extension in c.XLS_EXT:  # проверяем расширения excel
        return c.excel_to_pdf(full_file_name, doc_path)
    elif file_extension in c.DOC_EXT:  # проверяем расширения doc
        return c.word_to_pdf(full_file_name, doc_path)
    else:
        text = m.UNSUPPORTED_MESSAGE  # {file_extension} еще бы добавить в сообщение
        bot.reply_to(message, text)


def start_bot():
    logging.basicConfig(filename='./convert2pdf.log', encoding='utf-8', level=LOG_LEVEL,
                        format='%(asctime)s %(message)s')
    bot.polling(none_stop=True, interval=0)
