import telebot
import os


# Чтение токена. Для того что бы работало надо в папке хранения исполняемого файла создать файл
# с названием TOKEN в нём прописать свой токен без пробелов энтров - только то что скопировано у BotFather
def add_token(path):
    bot_token_env = os.environ.get('TG_TOKEN', None)
    if bot_token_env:
        return bot_token_env
    
    try:
        with open(path, 'r') as f:
            token = f.read().rstrip()
    except Exception as e:
        bot.reply_to(e)
    return token


bot = telebot.TeleBot(add_token('TOKEN.env'))
