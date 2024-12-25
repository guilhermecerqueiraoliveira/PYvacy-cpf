# cpp.py
import sys
from cpf_privacy import ocultar_cpf

# verificar se o arquivo PDF foi passado como argumento
if len(sys.argv) != 2:
    print("Uso: cpf <arquivo_pdf>")
    sys.exit(1)

# pega o nome do arquivo PDF passado como argumento
input_pdf = sys.argv[1]
# chama a função para ocultar o CPF
ocultar_cpf(input_pdf)
