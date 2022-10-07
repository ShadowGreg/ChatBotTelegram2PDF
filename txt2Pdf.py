import textwrap

from fpdf import FPDF


# сам конвертер txt to pdf
def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fantasize_pt = 10
    fantasize_mm = fantasize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fantasize_pt)
    split = text.split('\n')
    for line in split:
        lines = textwrap.wrap(line, int(width_text))  # перенос
        if len(lines) == 0:
            pdf.ln()
        for wrap in lines:
            pdf.cell(0, fantasize_mm, wrap, ln=1)
    pdf.output(filename, 'F')


# конвертация текста в pdf
def convert_text_pdf(local_src):
    output_filename = local_src + '.pdf'
    file = open(local_src, encoding="utf-8")  # если конвертировать UTF-16 - работает на файлах в UTF-16,
    # но при этом не работает UTF-8, и французский. Надо как-то проверять кодировку файла и разным веткам декодировать
    # painting.txt пока нигде не работает
    text = file.read()
    file.close()
    text_to_pdf(text, output_filename)
    return output_filename
