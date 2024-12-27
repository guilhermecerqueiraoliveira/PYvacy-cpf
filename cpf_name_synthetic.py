import random

# Função para gerar um CPF válido
def gerar_cpf():
    # Gera 9 primeiros números aleatórios
    numeros = [random.randint(0, 9) for _ in range(9)]

    # Cálculo dos dois últimos dígitos verificadores (DV)
    def calcular_dv(numeros):
        # Cálculo do primeiro DV
        d1 = sum((i + 1) * numeros[i] for i in range(9)) % 11
        d1 = 0 if d1 < 2 else 11 - d1

        # Cálculo do segundo DV
        d2 = sum((i + 1) * numeros[i] for i in range(9)) + 2 * d1
        d2 = 0 if d2 < 2 else 11 - (d2 % 11)

        return (d1, d2)

    d1, d2 = calcular_dv(numeros)
    return f"{''.join(map(str, numeros[:3]))}.{''.join(map(str, numeros[3:6]))}.{''.join(map(str, numeros[6:9]))}-{d1}{d2}"

# Listas de nomes comuns para gerar frases variadas
nomes_masculinos = ["João", "Carlos", "Felipe", "Lucas", "Pedro", "Guilherme", "Rafael", "André", "Marcos", "Bruno"]
nomes_femininos = ["Maria", "Ana", "Laura", "Carla", "Juliana", "Renata", "Camila", "Paula", "Fernanda", "Mariana"]

# Função para gerar frases com CPFs sintéticos e nomes variados
def gerar_frases_com_cpfs(num_frases=50):
    frases = [
        "O CPF de {nome} é {cpf}.",
        "{nome} tem o CPF {cpf}.",
        "O número do CPF de {nome} é {cpf}.",
        "A {nome} tem o CPF {cpf}.",
        "CPF de {nome}: {cpf}.",
        "O CPF registrado para {nome} é {cpf}.",
        "O CPF de {nome} é {cpf}.",
        "{nome} tem o CPF {cpf}.",
        "Este é o CPF de {nome}: {cpf}.",
        "O CPF de {nome} é {cpf}."
    ]

    dados_gerados = []

    for _ in range(num_frases):
        nome = random.choice(nomes_masculinos + nomes_femininos)  # Escolhe aleatoriamente um nome masculino ou feminino
        frase = random.choice(frases)  # Escolhe aleatoriamente uma frase
        cpf = gerar_cpf()  # Gera um CPF aleatório
        dados_gerados.append(frase.format(nome=nome, cpf=cpf))  # Preenche a frase com o nome e CPF

    return dados_gerados

# Função para salvar os dados gerados em um arquivo
def salvar_dados_em_arquivo(dados, nome_arquivo="cpf_test.txt"):
    with open(nome_arquivo, "w") as file:
        for linha in dados:
            file.write(linha + "\n")
    print(f"[INFO] Dados gerados salvos em '{nome_arquivo}'.")

if __name__ == "__main__":
    # Gerar 50 frases com CPFs
    dados_gerados = gerar_frases_com_cpfs(50)

    # Salvar os dados gerados em um arquivo de texto
    salvar_dados_em_arquivo(dados_gerados)
