from datetime import datetime
import os
import shutil
from csv import writer

SRC = './tmp_files/'
CSV_DELIMITER = ";"
CSV_ENCODING = 'utf-8'

# прочищаем каталог от всего что бы не засорять диск и сам каталог тоже удаляем
def clear_catalog(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)


def create_tmp_dir(chat_id):
    cur_datetime = datetime.today().strftime('%Y%m%d%H%M%S')
    dir_path = os.path.join(SRC, f"{chat_id}_{cur_datetime}")
    # создаем папку в которой будем временно размещать файл, если таковой не существует
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def file_save(chat_id, file_name, file):
    dir_path = create_tmp_dir(chat_id)
    # создаем путь конечного файла - думаю надо переделать - это временный вариант
    full_file_name = os.path.join(dir_path, file_name)
    # пишем файл на диск
    with open(full_file_name, 'wb') as new_file:
        new_file.write(file)
    return full_file_name

def export_csv(filepath, columns, data):
    with open(filepath, 'w', encoding=CSV_ENCODING) as f:
        csv_writer = writer(f, delimiter=CSV_DELIMITER)
        csv_writer.writerow(columns)
        csv_writer.writerows(data)