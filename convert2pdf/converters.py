from PIL import Image
import pillow_heif
import numpy as np
import cv2
import img2pdf
import re
import os
import subprocess
import pandas as pd
import pdfkit
import messages as m


IMG_EXT = {'.jpg', '.jpeg', '.jpg2', '.png', '.tiff'}
IMG_EXT_IOS = {'.heif', '.heic'}
DOC_EXT = {'.doc', '.docx', '.odt'}
XLS_EXT = {'.xls', '.xlsx', '.ods'}
TXT_EXT = {'.txt', '.csv'}


def get_pdf_path(doc_path):
    return re.sub(r'\.[^.]*$', ".pdf", doc_path, flags=re.IGNORECASE)


def get_html_path(doc_path):
    return re.sub(r'\.[^.]*$', ".html", doc_path, flags=re.IGNORECASE)


def txt_to_pdf(doc_path):
    _, ext = os.path.splitext(doc_path)
    pdf_path = get_pdf_path(doc_path)
    html_path = get_html_path(doc_path)
    if ext == ".txt":
        with open(doc_path, 'r', encoding='utf-8') as txt_file:
            with open(html_path, 'w') as res:
                res.write(m.HTML_HEAD)
                for line in txt_file.readlines():
                    res.write("<p>" + line + "</p>\n")
                print("imhere")
                res.write(m.HTML_TAIL)
    else:
        CSV = pd.read_csv(doc_path)
        CSV.to_html(html_path)

    pdfkit.from_file(html_path, pdf_path)
    return pdf_path


def img_to_pdf(doc_path: str):
    # получаем путь pdf
    pdf_path = get_pdf_path(doc_path)
    
    # открываем картинку
    with Image.open(doc_path) as image:
        # используем конвертер img2pdf
        pdf_bytes = img2pdf.convert(image.filename)
        # создаем pdf файл
        with open(pdf_path, "wb") as file:
            # пишем куски pdf файла
            file.write(pdf_bytes)
    
    return pdf_path


def ios_img_to_png(doc_path: str):
    # try:
    heif_file = pillow_heif.open_heif(doc_path, convert_hdr_to_8bit=False)
    heif_file.convert_to("BGRA;16" if heif_file.has_alpha else "BGR;16")
    np_array = np.asarray(heif_file)
    png_path = re.sub(r'\.[^.]*$', ".png", doc_path, flags=re.IGNORECASE)
    cv2.imwrite(png_path, np_array)
    np.allclose
    output_src = img_to_pdf(png_path)
    return output_src


def excel_to_pdf(doc_path, path):
    subprocess.call(['soffice',
                 '--headless',
                 '--nologo',
                 '--nofirststartwizard',
                 '--norestore',
                 doc_path,
                 'macro:///Standard.Module1.FitToPage'])    
    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])    
    return get_pdf_path(doc_path)


def word_to_pdf(doc_path, path):
    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])    
    return get_pdf_path(doc_path)
