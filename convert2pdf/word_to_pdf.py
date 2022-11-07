import re
import subprocess


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
    return re.sub(r'xls.?|csv$', "pdf", doc_path, flags=re.IGNORECASE)


def word_to_pdf(doc_path, path):
    subprocess.call(['soffice',
                 # '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])    
    return re.sub(r'doc.?$', "pdf", doc_path, flags=re.IGNORECASE)