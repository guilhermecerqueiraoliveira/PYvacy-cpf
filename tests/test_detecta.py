

import re

# Função para detectar CPFs em um arquivo de texto
def detectar_cpfs_em_arquivo(nome_arquivo):
    # Definindo o padrão do CPF (XXX.XXX.XXX-XX)
    padrao_cpf = r'\d{3}\.\d{3}\.\d{3}-\d{2}'

    try:
        with open(nome_arquivo, 'r') as file:
            # Lê todo o conteúdo do arquivo
            conteudo = file.read()

            # Encontra todos os CPFs no conteúdo do arquivo
            cpfs_encontrados = re.findall(padrao_cpf, conteudo)

            return cpfs_encontrados

    except FileNotFoundError:
        print(f"[ERROR] O arquivo '{nome_arquivo}' não foi encontrado.")
        return []

# Função para testar a detecção de CPFs
def testar_detectar_cpfs():
    nome_arquivo = "cpf_test.txt"  # Arquivo gerado pelo cpf_name_synthetic.py

    print(f"Iniciando teste de detecção de CPFs no arquivo '{nome_arquivo}'...\n")

    # Detectar CPFs no arquivo
    cpfs = detectar_cpfs_em_arquivo(nome_arquivo)

    # Exibir os CPFs encontrados
    if cpfs:
        print(f"CPFs encontrados ({len(cpfs)}):")
        for cpf in cpfs:
            print(cpf)
    else:
        print("[INFO] Nenhum CPF encontrado ou o arquivo está vazio.")

# Rodar o teste
if __name__ == "__main__":
    testar_detectar_cpfs()
