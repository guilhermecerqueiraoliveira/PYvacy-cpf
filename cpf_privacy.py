#!/usr/bin/env python
import re
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def ocultar_cpf(input_pdf):
    # Criar o diretório "pdfs" se não existir
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    # Extração do texto do PDF usando pdfminer
    text = extract_text(input_pdf)

    # Ofuscar os CPFs
    cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
    text_ocultado = re.sub(cpf_pattern, 'XXX.XXX.XXX-XX', text)

    # Criar um PDF novo com o texto modificado
    output_pdf = f"pdfs/{os.path.splitext(os.path.basename(input_pdf))[0]} (CPF OCULTO).pdf"
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Definir a fonte e o tamanho para o texto
    c.setFont("Helvetica", 10)
    c.drawString(100, 750, text_ocultado)  # Posicionamento simples

    c.save()

    # Voltar a carregar o novo conteúdo em um PDF
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Abrir o PDF original e mesclar com o novo conteúdo
    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            # Mesclar a página original com o conteúdo modificado
            page.merge_page(new_pdf.pages[0])

            writer.add_page(page)

        # Salvar o novo arquivo PDF
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    print(f"Arquivo PDF gerado com CPF oculto: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cpf_privacy.py <input_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    ocultar_cpf(input_pdf)
