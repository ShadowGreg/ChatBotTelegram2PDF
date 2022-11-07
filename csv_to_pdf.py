import pandas as pd
import pdfkit
import re


def csv_to_pdf(doc_path):
    html_path = re.sub(r'csv$', "html", doc_path, flags=re.IGNORECASE)
    pdf_path = re.sub(r'csv$', "pdf", doc_path, flags=re.IGNORECASE)

    CSV = pd.read_csv(doc_path)
    CSV.to_html(html_path)

    pdfkit.from_file(html_path, pdf_path)
    return pdf_path

