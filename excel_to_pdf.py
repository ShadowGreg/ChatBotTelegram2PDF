import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, SaveFormat


def excel_to_pdf(path_to_excel_file):

    workbook = Workbook(path_to_excel_file)

    workbook.save("result.pdf", SaveFormat.PDF)

    jpype.shutdownJVM()

