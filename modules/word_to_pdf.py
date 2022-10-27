#from win32com import client  # крос платворменные библиотеки
from docx2pdf import convert
#import pythoncom

#pythoncom.CoInitializeEx(0)


def word_to_pdf(input_file_name):  # TODO сделать
    doc2pdf_filename = convert(input_file_name)
    # convert("my_docx_folder/")
    print(input_file_name)
    return doc2pdf_filename
