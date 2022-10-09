# importing necessary libraries
import img2pdf
import pillow_heif  # pip install pillow-heif
from PIL import Image
import os
import io
import whatimage
from PIL import Image
from start_bot import bot
from pillow_heif import register_heif_opener
import numpy as np
import cv2  # pip install opencv-python


def get_file_path(input_path: str):
    file = open(input_path, 'r')  # открываем файл по указанному пути
    file_path, file_extension = os.path.splitext(file.name)  # получаем имя файла и расширение
    file.close()  # закрываем файл
    return file_path


def get_file_extension(input_path: str):
    file = open(input_path, 'r')  # открываем файл по указанному пути
    file_path, file_extension = os.path.splitext(file.name)  # получаем имя файла и расширение
    file.close()  # закрываем файл
    return file_extension


def img_to_pdf(input_image_path: str):
    try:
        pdf_path = get_file_path(input_image_path) + '.pdf'  # storing pdf path
        image = Image.open(input_image_path)  # opening image
        pdf_bytes = img2pdf.convert(image.filename)  # converting into chunks using img2pdf
        file = open(pdf_path, "wb")  # opening or creating pdf file
        file.write(pdf_bytes)  # writing pdf files with chunks
        image.close()  # closing image file
        file.close()  # closing pdf file
    except Exception as e:
        bot.reply_to(e)
    return pdf_path


def ios_img_to_pdf(input_ios_src: str):
    output_src = ''
    heif_file = pillow_heif.open_heif("images/rgb12.heif", convert_hdr_to_8bit=False)
    heif_file.convert_to("BGRA;16" if heif_file.has_alpha else "BGR;16")
    np_array = np.asarray(heif_file)
    cv2.imwrite("rgb16.png", np_array)
    return output_src
# TODO: сделать функцию принимающую путь файла/ файл проверяющую если jpg то по
#  одной ветке, если  heif то по другой ветке конверт и возвращающую путь где лежит конечный файл
