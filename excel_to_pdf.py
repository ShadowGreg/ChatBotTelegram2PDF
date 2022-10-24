from win32com import client


def excel_to_pdf(path_to_excel_file):

    app = client.Dispatch("Excel.Application")

    book = app.Workbooks.Open(path_to_excel_file)

    book.ExportAsFixedFormat(0, path_to_excel_file)
