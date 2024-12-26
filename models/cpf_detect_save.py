import spacy
import json
import os

# Carrega o modelo treinado
nlp = spacy.load("models/spacy_cpf_model")

# Função para detectar CPFs em um texto
def detect_cpfs(text):
    doc = nlp(text)
    cpf_detections = []
    
    for ent in doc.ents:
        if ent.label_ == "CPF":
            cpf_detections.append({
                "cpf": ent.text,
                "start": ent.start_char,
                "end": ent.end_char
            })
    return cpf_detections

# Função para salvar as detecções no arquivo JSON
def save_detections_to_file(detections, file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            all_detections = json.load(file)
    else:
        all_detections = []

    all_detections.extend(detections)
    
    with open(file_path, "w") as file:
        json.dump(all_detections, file, indent=4)

# Exemplo de uso: Detecção em um texto de exemplo
text_to_analyze = "O CPF de João é 123.456.789-00 e o CPF de Maria é 987.654.321-00."
detected_cpfs = detect_cpfs(text_to_analyze)

# Salva as detecções no arquivo JSON
file_path = "models/cpf_detections.json"
save_detections_to_file(detected_cpfs, file_path)

print(f"Detections saved to {file_path}")
