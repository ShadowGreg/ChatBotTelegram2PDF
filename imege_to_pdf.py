import img2pdf
# pip install pillow-heif
import pillow_heif
import os
from PIL import Image
from start_bot import bot
import numpy as np
# pip install opencv-python
import cv2

""""
что бы вставить в условия файла main - надо проверить файл на расширения
'.jpg' or '.jpeg' or '.png' or '.tiff' or '.jpg2' or '.heif' or '.heic'
и вставить функцию файла img2pdf(сюда передавать адрес файла в str)
 выходное значение адрес файла в c .pdf
"""""


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


# конвертируем обычные фото форматы в pdf
def img_to_pdf(input_image_path: str):
    try:
        # получаем путь pdf
        pdf_path = get_file_path(input_image_path) + '.pdf'
        # открываем картинку
        image = Image.open(input_image_path)
        # используем конвертер img2pdf
        pdf_bytes = img2pdf.convert(image)
        # создаем pdf файл
        file = open(pdf_path, "wb")
        # пишем куски pdf файла
        file.write(pdf_bytes)
        # закрываем файл картинки
        image.close()
        # закрываем файл pdf
        file.close()
    except Exception as e:
        # ловим ошибку и даем её боту
        bot.reply_to(e)
    return pdf_path


# конвертер форматов iOs в pdf
def ios_img_to_pdf(input_ios_src: str):
    output_src = ''
    heif_file = pillow_heif.open_heif("images/rgb12.heif", convert_hdr_to_8bit=False)
    heif_file.convert_to("BGRA;16" if heif_file.has_alpha else "BGR;16")
    np_array = np.asarray(heif_file)
    cv2.imwrite("rgb16.png", np_array)
    return output_src


# функция выбора направления конвертера
def img2pdf(input_img2pdf_path: str):
    output_path = '0'
    try:
        # получаем расширение файла
        file_extension = get_file_extension(input_img2pdf_path)
        # проверяем стандарт картинки и передаем в нужную функцию
        if file_extension == '.jpg' or '.jpeg' or '.png' or '.tiff' or '.jpg2':
            output_path = img_to_pdf(input_img2pdf_path)
        elif file_extension == '.heif' or '.heic':
            output_path = ios_img_to_pdf(input_img2pdf_path)
    except Exception as e:
        # ловим ошибку и даем её боту
        bot.reply_to(e)
    return output_path
