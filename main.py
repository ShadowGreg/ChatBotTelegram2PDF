import os
import os.path

from send_doc import send_document
from start_bot import bot
from clear_catalog import clear_catalog
from txt_to_pdf import convert_text_pdf
from excel_to_pdf import excel_to_pdf
from picture_to_pdf import img_2_pdf
from datetime import datetime

local_src = ""
SRC = './tmp_files/'
clear_time = '14'


# 2 реакции на команды для бота.
@bot.message_handler(commands=['start', 'help', 'info'])  # tab-ы не трогать!
def send_welcome(message):
    if message.text == '/help':
        bot.reply_to(message, '''Список поддерживаемых конверсий:
Поддерживаемые кодировки текста: ANSI, UTF-8
* .txt -> .pdf

Конвертирует фото, отправленные как файл: нажмите скрепку -> снизу в списке выберите "Файл" -> выберите фото
* .jpg -> .pdf
* .png -> .pdf
* .tiff -> .pdf
* .jpeg -> .pdf
* .jpg2 -> .pdf
* .heif -> .pdf
* .heic -> .pdf
''')
    elif message.text == '/start':
        bot.reply_to(message, '''Этот бот конвертирует файлы с различными расширениями в pdf.\n
Чтобы посмотреть список поддерживаемых конвертий используйте /help''')
    else:
        bot.reply_to(message, '''converToPDF - это некоммерческий проект.
Создан исключетельно на энтузиазме и любви к разработке.\n
Бот принимает файл, конвертирует его в PDF и отправляет обратно пользователю.
После чего удаляет ваш файл с сервера и очищает директорию.
Бот не собирает никакие данные о пользователе и не сохраняет никакую информацию.
Статистика работы и обработки сценариев не ведется.
Мы уважаем конфиденциальность информации пользователей и поддерживаем политику telegram в отношении приватности.\n
Если вам нравится converToPDF и вы хотите подкинуть нам денег на кофе ☕
То поддержите проект, отправив на (реквезиты) произвольную сумму в рублях.
Мы сделали этот проект для вас и для наших друзей и близких! Приятного использования 😇''')


# чистка папки назначения
def clear_src():
    if datetime.now().strftime("%H") == clear_time:
        clear_catalog(SRC)
        if not os.path.exists(SRC):
            os.makedirs(SRC)


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
        get_object = message.document  # получаемый объект
        real_file_name, real_file_extension = os.path.splitext(get_object.file_name)  # бот не понимает картинку
        file_name = real_file_name.lower()
        file_extension = real_file_extension.lower()
        file_info = bot.get_file(get_object.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = SRC + str(chat_id) + '_' + str(datetime.today().strftime('%Y%m%d%H%M%S'))
        # создаем папку в которой будем временно размещать файл, если таковой не существует
        bot.reply_to(message, f"Пожалуй сохраню {file_name} 😉")  # Нужно ли это писать? Выглядит перебором!
        if not os.path.exists(src):
            os.makedirs(src)
        # создаем путь конечного файла - думаю надо переделать - это временный вариант
        local_src = src + '/' + real_file_name + real_file_extension
        # пишем файл на диск
        with open(local_src, 'wb') as new_file:
            new_file.write(downloaded_file)
        file_switcher(chat_id, file_extension, local_src, message, src)
    except Exception as e:
        bot.reply_to(message, e)


def file_switcher(chat_id, file_extension, local_src, message, src):
    clear_src()
    if file_extension == '.txt':  # проверяем расширение txt
        bot.reply_to(message, "Конвертирую ⚙️⚙")  # Нужно ли это писать? Выглядит перебором! Предлагаю минимализм
        convert_text_pdf(local_src)  # и весь лишний вывод вообще убрать. Оставим пока так, для наглядности.
        send_document(convert_text_pdf(local_src), chat_id)
    elif file_extension == '.xls' \
            or file_extension == '.xlsx':  # проверяем расширение excel
        bot.reply_to(message, "xls")
    elif file_extension == '.doc' \
            or file_extension == '.docx':  # проверяем расширение doc
        bot.reply_to(message, "doc")
    elif file_extension == '.jpg' \
            or file_extension == '.jpeg' \
            or file_extension == '.png' \
            or file_extension == '.tiff' \
            or file_extension == '.jpg2' \
            or file_extension == '.heif' \
            or file_extension == '.heic':  # картинок
        # отсылаем файл пользователю (используем модуль конвертера)
        bot.reply_to(message, "Конвертирую картинку в pdf ⚙️⚙️")
        img_2_pdf(local_src)
        send_document(img_2_pdf(local_src), chat_id)
    else:
        bot.reply_to(message, f"я не знаю такого '{file_extension}' формата 😶‍🌫️😇")
        # теперь функция удаляет и файлы и папки - пути писать аккуратно что бы не затерло системные файлы
    clear_catalog(src)  # ВНИМАНИЕ!


@bot.message_handler(content_types=['photo'])
def photo(message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_extension = '.' + bot.get_file(file_id).file_path.split('.')[1]
    downloaded_file = bot.download_file(file_info.file_path)
    src = SRC + str(chat_id) + '_' + str(datetime.today().strftime('%Y%m%d%H%M%S'))
    # создаем папку в которой будем временно размещать файл, если таковой не существует
    if not os.path.exists(src):
        os.makedirs(src)
    # создаем путь конечного файла - думаю надо переделать - это временный вариант
    local_src = src + '/' + 'image' + file_extension
    with open(local_src, 'wb') as new_file:
        new_file.write(downloaded_file)
    file_switcher(chat_id, file_extension, local_src, message, src)


@bot.message_handler(func=lambda message: True)  # Бот на любое сообщение пользователя, кроме файла
# и команды отвечает списком всех доступных команд.
def echo(message):  # нельзя трогать tab-ы у текста!
    chat_id = message.from_user.id  # user_id берется из id_сообщения.
    text = '''Основные команды:
/start - Приветствие
/help - Список поддерживаемых конверсий, подсказки по использованию бота
/info - Пояснения о работе бота'''
    bot.send_message(chat_id, text)


bot.polling(none_stop=True, interval=0)
