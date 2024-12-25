#!/usr/bin/env python
import re
import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import spacy

# Carregar o modelo de NLP em português
nlp = spacy.load("pt_core_news_sm")

def detectar_cpfs(texto):
    """
    Detecta CPFs no texto usando NER (Named Entity Recognition) do spaCy.
    """
    doc = nlp(texto)
    cpfs_detectados = []

    # Verifica se a entidade detectada é um CPF (padrão: 000.000.000-00)
    for ent in doc.ents:
        if re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', ent.text):
            cpfs_detectados.append(ent.text)

    return cpfs_detectados

def obter_posicoes_cpfs(input_pdf, cpfs_detectados):
    """
    Recebe o PDF e as entidades CPF e retorna suas posições no texto da página.
    """
    # Usar o pdfminer para obter as posições das palavras no texto
    positions = []
    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = extract_text(input_pdf, page_numbers=[page_num])

            # Para cada CPF detectado, verificar a posição no texto
            for cpf in cpfs_detectados:
                # Usar uma expressão regular para identificar a posição do CPF
                start_index = text.find(cpf)
                if start_index != -1:
                    # Simulação de cálculo da posição no texto (mais simples)
                    x = start_index % 500  # Exemplo de cálculo de posição
                    y = 500 - (start_index // 500) * 15  # Exemplo de linha de texto
                    positions.append((x, y))
    return positions

def ocultar_cpf(input_pdf):
    """
    Função principal para ocultar CPFs em um arquivo PDF com blocos pretos ou blur.
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

    # Nome do arquivo de saída
    output_pdf = f"pdfs/{os.path.splitext(os.path.basename(input_pdf))[0]} (CPF OCULTO).pdf"

    # Abrir o PDF original
    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        # Para cada página do PDF original
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            # Criar um novo canvas para a página modificada
            packet = BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)

            # Desenhar um bloco preto sobre os CPFs detectados
            c.setFillColorRGB(0, 0, 0)  # Cor preta
            for x, y in posicoes_cpfs:
                c.rect(x, y, 100, 15, fill=True)  # Desenha um retângulo preto sobre o CPF

            # Salvar o novo canvas como um arquivo em memória
            c.save()
            packet.seek(0)
            new_pdf = PdfReader(packet)

            # Mesclar a página original com o conteúdo modificado
            page.merge_page(new_pdf.pages[0])

            # Adicionar a página ao escritor
            writer.add_page(page)

        # Salvar o novo arquivo PDF
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    print(f"Arquivo PDF gerado com CPF oculto: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cpf_privacy.py <input_pdf>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    ocultar_cpf(input_pdf)

