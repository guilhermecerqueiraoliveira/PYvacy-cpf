#!/usr/bin/env python
import re
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image, ImageFilter, ImageDraw
import spacy
from pdf2image import convert_from_path

# Carregar o modelo de NLP em português
nlp = spacy.load("pt_core_news_sm")

def detectar_cpfs(texto):
    """
    Detecta CPFs no texto usando NER (Named Entity Recognition) do spaCy.
    """
    doc = nlp(texto)
    cpfs_detectados = []

    # Exibe as localizações e CPFs detectados
    for ent in doc.ents:
        if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', ent.text):
            cpfs_detectados.append(ent.text)
            print(f"CPF detectado: {ent.text} na posição {ent.start_char}-{ent.end_char}")

    return cpfs_detectados

def obter_posicoes_cpfs(input_pdf, cpfs_detectados):
    """
    Recebe o PDF e as entidades CPF e retorna suas posições no texto da página.
    """
    positions = []
    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = extract_text(input_pdf, page_numbers=[page_num])

            for cpf in cpfs_detectados:
                start_index = text.find(cpf)
                if start_index != -1:
                    x = start_index % 500  # Exemplo de cálculo de posição (ajustar conforme necessário)
                    y = 500 - (start_index // 500) * 15  # Exemplo de linha de texto (ajustar conforme necessário)
                    positions.append((x, y))
                    print(f"Posição do CPF {cpf}: {x}, {y}")  # Exibindo a posição no texto
    return positions

def aplicar_blur_na_imagem(image, cpfs_detectados, posicoes_cpfs):
    """
    Aplica um efeito de blur nas posições dos CPFs detectados na imagem.
    """
    for (x, y) in posicoes_cpfs:
        # Definir uma área para aplicar o blur (em torno da posição do CPF)
        cropped_area = image.crop((x, y, x + 100, y + 20))  # A área a ser desfocada
        blurred_area = cropped_area.filter(ImageFilter.GaussianBlur(radius=5))
        image.paste(blurred_area, (x, y))  # Coloca o blur na imagem
    return image

def ocultar_cpf(input_pdf):
    """
    Função principal para ocultar CPFs em um arquivo PDF com blur.
    """
    # Criar o diretório "pdfs" se não existir
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")

    # Extração do texto do PDF usando pdfminer
    texto = extract_text(input_pdf)

    # Detectar CPFs no texto extraído
    cpfs_detectados = detectar_cpfs(texto)

    # Obter as posições dos CPFs no PDF
    posicoes_cpfs = obter_posicoes_cpfs(input_pdf, cpfs_detectados)

    # Converter a primeira página do PDF para imagem
    imagens = convert_from_path(input_pdf)

    # Aplicar blur na imagem
    for i, image in enumerate(imagens):
        image_com_blur = aplicar_blur_na_imagem(image.copy(), cpfs_detectados, posicoes_cpfs)

        # Salvar as imagens modificadas
        output_image_path = f"pdfs/{os.path.splitext(os.path.basename(input_pdf))[0]}_page_{i + 1}.png"
        image_com_blur.save(output_image_path)

        # Converter as imagens de volta para PDF
        pdf_path = f"pdfs/{os.path.splitext(os.path.basename(input_pdf))[0]}_CPF_OCULTO.pdf"
        image_com_blur.save(pdf_path, "PDF", resolution=100.0)

    print(f"Arquivo PDF gerado com CPF oculto: {pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cpf_privacy.py <input_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    ocultar_cpf(input_pdf)
