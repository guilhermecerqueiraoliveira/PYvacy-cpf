import spacy
from spacy.training.example import Example
import random
import os
import re


# Função para carregar os dados de treinamento
def load_training_data(file_path):
    training_data = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                text = line.strip()
                # Regex para capturar CPFs no formato XXX.XXX.XXX-XX
                cpf_matches = re.finditer(r'\d{3}\.\d{3}\.\d{3}-\d{2}', text)

                entities = []
                for match in cpf_matches:
                    start, end = match.span()
                    entities.append((start, end, "CPF"))

                # Se encontrou algum CPF, adiciona o exemplo
                if entities:
                    training_data.append((text, entities))

        print(f"[INFO] Dados de treinamento carregados de {file_path}")
    except FileNotFoundError:
        print(f"[ERRO] Arquivo {file_path} não encontrado!")
    except Exception as e:
        print(
            f"[ERRO] Ocorreu um erro ao carregar os dados de treinamento: {e}")
    return training_data


# Função para treinar o modelo com regularização e treinamento contínuo
def train_model(training_data, model_dir="models/ner_model", epochs=10):
    # Verificar se o diretório do modelo existe
    if os.path.exists(model_dir):
        print(
            f"[INFO] Diretório '{model_dir}' já existe. Carregando modelo existente..."
        )
        nlp = spacy.load(model_dir)  # Carrega o modelo treinado
    else:
        print(
            f"[INFO] Diretório '{model_dir}' não encontrado. Criando um novo modelo..."
        )
        nlp = spacy.blank("pt")  # Cria um modelo vazio

    # Criar ou carregar o componente NER
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Adicionar a label "CPF"
    ner.add_label("CPF")

    # Configurar o otimizador
    optimizer = nlp.begin_training()

    # Embaralhar os dados para evitar overfitting
    random.shuffle(training_data)

    # Treinamento com regularização e avaliação
    for epoch in range(epochs):
        print(f"[INFO] Iniciando época {epoch+1} de {epochs}...")
        losses = {}

        # Atualizar o modelo com exemplos de treinamento
        for text, annotations in training_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, {"entities": annotations})

            # Atualize o modelo com a instância Example
            nlp.update([example], drop=0.5, losses=losses)

        # Imprimir as perdas para cada época
        print(
            f"[INFO] Perda (loss) na época {epoch+1}: {losses.get('ner', 'Sem perda')}"
        )

        # Avaliar o modelo a cada 5 épocas
        if (epoch + 1) % 5 == 0:
            evaluate_model(nlp)

    # Salvar o modelo treinado
    try:
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        nlp.to_disk(model_dir)
        print(f"[INFO] Modelo treinado salvo em {model_dir}")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro ao salvar o modelo: {e}")


# Função para avaliar o modelo com um conjunto de testes sintéticos
def evaluate_model(nlp, test_file="models/cpf_data.txt"):
    # Carregar dados de teste (dados sintéticos)
    test_data = load_training_data(test_file)

    correct = 0
    total = 0

    for text, annotations in test_data:
        doc = nlp(text)
        detected_cpf = [ent.text for ent in doc.ents if ent.label_ == "CPF"]

        # Agora corrigimos o acesso aos CPFs na variável 'annotations'
        actual_cpf = [
            text[start:end] for start, end, label in annotations
            if label == "CPF"
        ]

        # Comparar CPFs detectados com os corretos
        for cpf in detected_cpf:
            if cpf in actual_cpf:
                correct += 1
        total += len(actual_cpf)

    accuracy = (correct / total) * 100 if total > 0 else 0
    print(f"[INFO] Precisão (Accuracy): {accuracy:.2f}%")


# Função para detectar CPFs em um novo texto
def detect_cpf(text, model_dir="models/ner_model"):
    # Verificar se o diretório do modelo existe
    if not os.path.exists(model_dir):
        print(
            f"[ERRO] O diretório '{model_dir}' não existe! Carregue um modelo treinado primeiro."
        )
        return

    # Carregar o modelo treinado
    try:
        nlp = spacy.load(model_dir)
        print(f"[INFO] Modelo carregado de {model_dir}")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro ao carregar o modelo: {e}")
        return

    # Processar o texto
    doc = nlp(text)

    # Detectar e imprimir os CPFs encontrados
    print("\n[INFO] Detecção de CPFs no texto:")
    for ent in doc.ents:
        if ent.label_ == "CPF":
            print(
                f"CPF detectado: {ent.text} (Posição: {ent.start_char}-{ent.end_char})"
            )


if __name__ == "__main__":
    # Caminho do arquivo com os dados de CPFs sintéticos
    file_path = "models/cpf_data.txt"

    # Verificar se o arquivo de dados de treinamento existe
    if not os.path.exists(file_path):
        print(f"[ERRO] O arquivo '{file_path}' não existe!")
    else:
        # Carregar dados de treinamento
        training_data = load_training_data(file_path)

        # Treinar o modelo com os dados carregados
        train_model(training_data)

        # Testar o modelo em um texto de exemplo
        text_to_test = "O CPF de Guilherme é 123.456.789-00 e o de João é 987.654.321-00."
        detect_cpf(text_to_test)
