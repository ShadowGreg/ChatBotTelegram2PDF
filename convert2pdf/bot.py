import telebot
import database as d
import os
from utils import file_save, clear_catalog
import converters as c
import messages as m
import logging

LOG_LEVEL = logging.DEBUG
START_CMD = 'start'
HELP_CMD = 'help'
HELP_ADMIN_CMD = 'help_admin'
INFO_CMD = 'info'
USER_COMMANDS = [START_CMD, HELP_CMD, HELP_ADMIN_CMD, INFO_CMD]
GET_FILES_CMD = 'get_files_info'
GET_CONVERTS_CMD = 'get_converts_info'
GET_SUMMARY_CMD = 'get_summary'
PRIV_COMMANDS = [GET_FILES_CMD, GET_CONVERTS_CMD, GET_SUMMARY_CMD]
ADD_ADMIN = 'add_admin'
REMOVE_ADMIN = 'remove_admin'
GET_ADMINS = 'get_admins'
ADMIN_COMMANDS = [ADD_ADMIN, REMOVE_ADMIN, GET_ADMINS]


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
@bot.message_handler(commands=USER_COMMANDS)
def send_welcome(message):
    cmd = message.text.lstrip('/')
    if cmd == HELP_CMD:
        bot.reply_to(message, m.HELP_MESSAGE)
    elif cmd == HELP_ADMIN_CMD:
        bot.reply_to(message, m.HELP_ADMIN_MESSAGE)
    elif cmd == START_CMD:
        bot.reply_to(message, m.START_MESSAGE)
    else:
        bot.reply_to(message, m.INFO_MESSAGE)


@bot.message_handler(commands=PRIV_COMMANDS)
def priv_commands(message):
    if d.check_is_admin(message.chat.id):
        chat_id = message.chat.id
        cmd = message.text.lstrip('/')
        if cmd == GET_FILES_CMD:
            report_type = d.GET_FILES_REPORT
        elif cmd == GET_CONVERTS_CMD:
            report_type = d.GET_CONVERTS_REPORT
        else:
            report_type = d.GET_SUMMARY_REPORT
        full_file_name = d.export_data_to_csv(message, report_type)
        send_file(bot, chat_id, full_file_name)
        clear_catalog(os.path.dirname(full_file_name))
    else:
        bot.send_message(message.chat.id, m.NOT_ADMIN_MESSAGE)


@bot.message_handler(commands=ADMIN_COMMANDS)
def manage_admins(message):
    if d.check_is_admin(message.chat.id):
        cmd = message.text.lstrip('/')
        if cmd == GET_ADMINS:
            full_file_name = d.export_data_to_csv(message, d.GET_ADMINS_REPORT)
            send_file(bot, message.chat.id, full_file_name)
            clear_catalog(os.path.dirname(full_file_name))
        else:
            bot.send_message(message.chat.id, m.ASK_ID_MESSAGE)        
            bot.register_next_step_handler(message, update_admin, bot, cmd)
    else:
        bot.send_message(message.chat.id, m.NOT_ADMIN_MESSAGE)
    

def update_admin(message, bot, cmd):
    try:
        user_id = int(message.text)
        chat_id = message.chat.id
        enabled = True if cmd == ADD_ADMIN else False
        d.update_admin(user_id, enabled)
        msg = m.ADD_ADMIN_MESSAGE if enabled else m.REMOVE_ADMIN_MESSAGE
        bot.send_message(message.chat.id, msg) 
        full_file_name = d.export_data_to_csv(message, d.GET_ADMINS_REPORT)
        send_file(bot, chat_id, full_file_name)
    except ValueError as e:
        bot.send_message(message.chat.id, m.BAD_ID_RECEIVED_MESSAGE)
    except Exception as e:
        logging.warning(e)
        bot.reply_to(message, e)
    clear_catalog(os.path.dirname(full_file_name))

# Чат бот принимает файлы.
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    """
    сохранение любого типа файла на компьютер в указанную директорию
    :type message: object
    """
    full_file_name = ''
    try:
        file_info = bot.get_file(message.document.file_id)        
        file_name, file_extension = os.path.splitext(message.document.file_name)
        file_size = file_info.file_size
        orig_file_info = (file_name, file_extension.lstrip("."), file_size, False)
        downloaded_file = bot.download_file(file_info.file_path)
        full_file_name = file_save(message.chat.id, message.document.file_name, downloaded_file)
        result = file_switcher(full_file_name, message)
        if result:
            with open(result, 'rb') as result_file :
                bot.send_document(message.chat.id, result_file)                
            d.save_to_db(message, orig_file_info, True)
    except Exception as e:
        logging.warning(e)
        d.save_to_db(message, orig_file_info, False)
        bot.reply_to(message, e)
    
    clear_catalog(os.path.dirname(full_file_name))


# Чат бот принимает картинки.
@bot.message_handler(content_types=['photo', 'sticker'])
def photo(message):
    content_type = message.content_type
    if content_type == 'photo':
        file_id = message.photo[-1].file_id
    else:
        file_id = message.sticker.file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_unique_id
    file_size = file_info.file_size
    if content_type == 'photo':
        file_extension = '.' + file_info.file_path.split('.')[1]
    else:
        file_extension = ".webp"
    orig_file_info = (file_name, file_extension.lstrip("."), file_size, False)        
    full_file_name = ''
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        full_file_name = file_save(message.chat.id, file_name + file_extension, downloaded_file)
        result = file_switcher(full_file_name, message)
        if result:
            with open(result, 'rb') as result_file:
                bot.send_document(message.chat.id, result_file)
            d.save_to_db(message, orig_file_info, True)
        clear_catalog(os.path.dirname(full_file_name))
    except Exception as e:
        logging.warning(e)
        d.save_to_db(message, orig_file_info, False)
        bot.reply_to(message, e)
    
    clear_catalog(os.path.dirname(full_file_name))


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
        raise Exception(m.UNSUPPORTED_MESSAGE)


def send_file(bot, chat_id, filepath):
    with open(filepath, 'rb') as result_file :
        bot.send_document(chat_id, result_file)


def start_bot():
    if not os.path.exists(d.DB_FILE):
        d.init_db()
    logging.basicConfig(filename='./convert2pdf.log', encoding='utf-8', level=LOG_LEVEL,
                        format='%(asctime)s %(message)s')
    bot.polling(none_stop=True, interval=0)
