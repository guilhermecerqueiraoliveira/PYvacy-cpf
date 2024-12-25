# Use uma imagem base do Python 3.12
FROM python:3.12-slim

# Atualiza o repositório e instala o poppler-utils (necessário para pdf2image)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*  # Limpar arquivos de cache após a instalação

# Definir diretório de trabalho para o projeto
WORKDIR /app

# Copiar o arquivo de dependências para o container
COPY requirements.txt /app/

# Instalar as dependências Python a partir do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto para dentro do container
COPY . /app/

# Comando para rodar o script principal do projeto
CMD ["python", "cpf_privacy.py"]
