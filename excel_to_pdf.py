from win32com import client


def excel_to_pdf(path_to_excel, path_to_save_pdf):  # TODO сделать

    app = client.Dispatch("Excel.Application")

    book = app.Workbooks.Open(path_to_excel)

    book.ExportAsFixedFormat(0, path_to_save_pdf + "result.pdf")

