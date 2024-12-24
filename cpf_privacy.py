#!/usr/bin/env python
import PyPDF2
import re
import os
import sys

def ocultar_cpf(input_pdf):
    # Criar o diretório "pdfs" se não existir
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    # Abrir o arquivo PDF
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        writer = PyPDF2.PdfFileWriter()

        # Iterar por todas as páginas do PDF
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extract_text()

            # Ofuscar o CPF
            cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
            text_ocultado = re.sub(cpf_pattern, 'XXX.XXX.XXX-XX', text)

            # Adicionar a página modificada ao writer
            page.merge_text(text_ocultado)
            writer.addPage(page)

        # Salvar o novo arquivo PDF no diretório "pdfs" com o nome modificado
        output_pdf = f"pdfs/{os.path.splitext(os.path.basename(input_pdf))[0]} (CPF OCULTO).pdf"
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cpf_privacy.py <input_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    ocultar_cpf(input_pdf)
