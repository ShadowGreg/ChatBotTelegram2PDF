import os
import threading

import jpype
import asposecells

from start_bot import bot

thread = threading.Thread(jpype.startJVM())
thread.start()

from asposecells.api import Workbook, SaveFormat


# получаем путь файла, что бы переделать из него конечный путь на выдачу
def get_file_path(input_path: str):
    # открываем файл по указанному пути
    file = open(input_path, 'r')
    # получаем имя файла и расширение
    file_path, file_extension = os.path.splitext(file.name)
    # закрываем файл
    file.close()
    return file_path


# получаем расширения файла, что бы направить на нужную ветку конвертера
def get_file_extension(input_path: str):
    # открываем файл по указанному пути
    file = open(input_path, 'r')
    # получаем имя файла и расширение
    file_path, file_extension = os.path.splitext(file.name)
    # закрываем файл
    file.close()
    return file_extension


# формируем путь файла c нужным расширением <file_extension>
def do_pdf_path(input_image_path, file_extension: str):
    # обрезаем полученный путь до расширения и прибавляем заданное расширение
    pdf_path = get_file_path(input_image_path) + file_extension
    return pdf_path


def excel_to_pdf(path_to_excel_file):
    # получаем путь pdf
    pdf_path = do_pdf_path(path_to_excel_file, '.pdf')
    workbook = Workbook(path_to_excel_file)
    workbook.save(pdf_path, SaveFormat.PDF)
    thread.join()
    #jpype.shutdownJVM()
    return pdf_path
