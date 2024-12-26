import spacy
import os
import subprocess
from datetime import datetime
import time

# função para carregar os dados de CPFs esperados
def load_expected_cpfs(file_path):
    with open(file_path, "r") as file:
        expected_cpfs = set(line.strip() for line in file)  # Usando set para evitar duplicados
    return expected_cpfs

# função para detectar CPFs no texto
def detect_cpf(text, nlp):
    doc = nlp(text)  # Processa o texto com o modelo

    detected_cpfs = set()  # Conjunto para armazenar os CPFs detectados

    for ent in doc.ents:
        if ent.label_ == "CPF":
            detected_cpfs.add(ent.text)  # Adiciona o CPF detectado ao conjunto

    return detected_cpfs

# função para avaliar o modelo
def evaluate_model(nlp, expected_cpfs, test_cpfs):
    detected_cpfs = set()

    for cpf in test_cpfs:
        detected_cpfs.update(detect_cpf(cpf, nlp))  # Detecta os CPFs do arquivo

    # cálculos de precisão
    correct_cpfs = detected_cpfs.intersection(expected_cpfs)
    missed_cpfs = expected_cpfs - detected_cpfs
    accuracy = len(correct_cpfs) / len(expected_cpfs) * 100

    print(f"\nTotal de CPFs esperados: {len(expected_cpfs)}")
    print(f"Total de CPFs detectados: {len(detected_cpfs)}")
    print(f"CPFs detectados corretamente: {len(correct_cpfs)}")
    print(f"CPFs não detectados: {len(missed_cpfs)}")
    print(f"Taxa de acerto: {accuracy:.2f}%")

# função para executar os testes e salvar o log
def run_tests_and_log():
    test_dir = "./tests"
    log_file = "log.md"

    with open(log_file, "w") as log:
        log.write(f"# Log de Testes\n")
        log.write(f"Data e Hora: {datetime.now()}\n\n")

        for filename in os.listdir(test_dir):
            if filename.endswith(".py") and filename != "test_model.py":
                filepath = os.path.join(test_dir, filename)
                log.write(f"## Executando {filename}\n\n")
                log.write("```\n")

                result = subprocess.run(["python", filepath], capture_output=True, text=True)
                log.write(result.stdout)
                log.write(result.stderr)

                log.write("```\n\n")

if __name__ == "__main__":
    start_time = time.time()  # Inicia o cronômetro

    # caminho do arquivo com os CPFs esperados
    cpf_file_path = "../models/cpf_data.txt"

    # carregar CPFs esperados
    expected_cpfs = load_expected_cpfs(cpf_file_path)

    # carregar o modelo treinado
    model_path = "../models/ner_model"
    nlp = spacy.load(model_path)

    # testar o modelo com os CPFs do arquivo
    evaluate_model(nlp, expected_cpfs, expected_cpfs)

    # executar os testes e salvar o log
    run_tests_and_log()

    end_time = time.time()  # Finaliza o cronômetro
    total_time = end_time - start_time
    print(f"Tempo total de execução: {total_time:.2f} segundos")
