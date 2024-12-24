#!/usr/bin/env python
import PyPDF2
import re
import os
import sys

def ocultar_cpf(input_pdf):
    # abrir o arquivo PDF
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        writer = PyPDF2.PdfFileWriter()

        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extract_text()

            # ocultar o CPF
            cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
            text_ocultado = re.sub(cpf_pattern, 'XXX.XXX.XXX-XX', text)

            # adicionar a página modificada ao writer
            page.merge_text(text_ocultado)
            writer.addPage(page)

        # salvar o novo arquivo PDF com o nome modificado
        output_pdf = f"{os.path.splitext(input_pdf)[0]} (CPF OCULTO).pdf"
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cpf_privacy.py <input_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    ocultar_cpf(input_pdf)
