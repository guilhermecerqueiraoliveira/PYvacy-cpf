import random
import os

# Verifica se a pasta 'models' existe, caso contrário cria
if not os.path.exists("models"):
    os.makedirs("models")

def calculate_verification_digits(cpf_base):
    """
    Calcula os dois dígitos verificadores de um CPF com base nos 9 primeiros dígitos.
    """
    # Cálculo do primeiro dígito verificador
    sum1 = sum([int(cpf_base[i]) * (10 - i) for i in range(9)])
    digit1 = 11 - (sum1 % 11)
    digit1 = digit1 if digit1 < 10 else 0

    # Cálculo do segundo dígito verificador
    sum2 = sum([int(cpf_base[i]) * (11 - i) for i in range(9)]) + digit1 * 2
    digit2 = 11 - (sum2 % 11)
    digit2 = digit2 if digit2 < 10 else 0

    return f"{digit1}{digit2}"

def generate_cpf():
    """
    Gera um CPF válido e retorna como uma string no formato 'xxx.xxx.xxx-xx'.
    """
    cpf_base = ''.join([str(random.randint(0, 9)) for _ in range(9)])  # Gera os 9 primeiros dígitos
    verification_digits = calculate_verification_digits(cpf_base)  # Calcula os dígitos verificadores
    generated_cpf = f"{cpf_base[:3]}.{cpf_base[3:6]}.{cpf_base[6:9]}-{verification_digits}"  # Formato final
    return generated_cpf

def save_cpfs_to_file(quantity):
    """
    Gera uma quantidade de CPFs válidos e os salva no arquivo 'cpf_data.txt' dentro da pasta 'models'.
    Os CPFs são adicionados ao final do arquivo existente.
    """
    file_path = "models/cpf_data.txt"
    
    with open(file_path, "a") as file:
        for _ in range(quantity):
            cpf = generate_cpf()
            file.write(cpf + "\n")
            print(f"Generated CPF: {cpf}")

# salva os CPFs gerados e guarda no arquivo cpf_data.txt
save_cpfs_to_file(100000)
