from datetime import datetime
import os
import shutil

SRC = './tmp_files/'

# прочищаем каталог от всего что бы не засорять диск и сам каталог тоже удаляем
def clear_catalog(folder):
    shutil.rmtree(folder, ignore_errors=True)


def file_save(chat_id, file_name, file):
    cur_datetime = datetime.today().strftime('%Y%m%d%H%M%S')
    path = os.path.join(SRC, f"{chat_id}_{cur_datetime}")
    # создаем папку в которой будем временно размещать файл, если таковой не существует
    if not os.path.exists(path):
        os.makedirs(path)
    # создаем путь конечного файла - думаю надо переделать - это временный вариант
    full_file_name = os.path.join(path, file_name)
    print(full_file_name)
    # пишем файл на диск
    with open(full_file_name, 'wb') as new_file:
        new_file.write(file)
    return full_file_name