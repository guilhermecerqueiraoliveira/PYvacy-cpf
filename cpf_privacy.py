#!/usr/bin/env python
import re
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def ocultar_cpf(input_pdf):
    # Criar o diretório "pdfs" se não existir
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    # Abrir o arquivo PDF
    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        # Iterar por todas as páginas do PDF
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            # Extrair o texto da página (se possível)
            text = page.extract_text()

            if text:
                # Ofuscar o CPF
                cpf_pattern = r'\d{3}\.\d{3}\.\d{3}-\d{2}'
                text_ocultado = re.sub(cpf_pattern, 'XXX.XXX.XXX-XX', text)

                # Criar um novo PDF com o texto modificado
                packet = BytesIO()
                c = canvas.Canvas(packet, pagesize=letter)

                # Adicionar o texto modificado ao novo PDF
                c.drawString(100, 750, text_ocultado)  # Posições e layout podem precisar de ajustes
                c.save()

                # Voltar a carregar o novo conteúdo em um PDF
                packet.seek(0)
                new_pdf = PdfReader(packet)

                # Mesclar a página original com a página modificada
                page.merge_page(new_pdf.pages[0])

            # Adicionar a página ao escritor
            writer.add_page(page)

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
