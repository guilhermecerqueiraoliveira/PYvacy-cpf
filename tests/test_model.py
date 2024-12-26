import spacy
from spacy.training.example import Example
import os

# Função para carregar os dados de CPFs esperados
def load_expected_cpfs(file_path):
    with open(file_path, "r") as file:
        expected_cpfs = set(line.strip() for line in file)  # Usando set para evitar duplicados
    return expected_cpfs

# Função para detectar CPFs no texto
def detect_cpf(text, nlp):
    doc = nlp(text)  # Processa o texto com o modelo

    detected_cpfs = set()  # Conjunto para armazenar os CPFs detectados

    for ent in doc.ents:
        if ent.label_ == "CPF":
            detected_cpfs.add(ent.text)  # Adiciona o CPF detectado ao conjunto

    return detected_cpfs

# Função para avaliar o modelo
def evaluate_model(nlp, expected_cpfs, test_cpfs):
    detected_cpfs = set()

    for cpf in test_cpfs:
        detected_cpfs.update(detect_cpf(cpf, nlp))  # Detecta os CPFs do arquivo

    # Cálculos de precisão
    correct_cpfs = detected_cpfs.intersection(expected_cpfs)
    missed_cpfs = expected_cpfs - detected_cpfs
    accuracy = len(correct_cpfs) / len(expected_cpfs) * 100

    print(f"\nTotal de CPFs esperados: {len(expected_cpfs)}")
    print(f"Total de CPFs detectados: {len(detected_cpfs)}")
    print(f"CPFs detectados corretamente: {len(correct_cpfs)}")
    print(f"CPFs não detectados: {len(missed_cpfs)}")
    print(f"Taxa de acerto: {accuracy:.2f}%")

if __name__ == "__main__":
    # Caminho do arquivo com os CPFs esperados
    cpf_file_path = "models/cpf_data.txt"

    # Carregar CPFs esperados
    expected_cpfs = load_expected_cpfs(cpf_file_path)

    # Carregar o modelo treinado
    model_path = "models/ner_model"
    nlp = spacy.load(model_path)

    # Testar o modelo com os CPFs do arquivo
    evaluate_model(nlp, expected_cpfs, expected_cpfs)
