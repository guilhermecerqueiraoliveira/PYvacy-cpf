import os

# Função para verificar e remover duplicatas de CPFs no arquivo grande
def remove_duplicates_large_file(file_path):
    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        print(f"O arquivo {file_path} não existe.")
        return

    seen_cpfs = set()  # Usado para armazenar CPFs já vistos
    duplicates = []     # Lista para armazenar CPFs duplicados
    temp_file_path = file_path + ".temp"  # Arquivo temporário para armazenar CPFs únicos

    with open(file_path, "r") as file, open(temp_file_path, "w") as temp_file:
        for line in file:
            cpf = line.strip()
            if cpf in seen_cpfs:
                duplicates.append(cpf)  # CPF duplicado encontrado
            else:
                seen_cpfs.add(cpf)  # Adiciona CPF único ao set
                temp_file.write(cpf + "\n")  # Grava no arquivo temporário

    # Informar os CPFs duplicados encontrados
    if duplicates:
        print("CPFs Duplicados encontrados:")
        duplicate_count = {}
        for cpf in duplicates:
            duplicate_count[cpf] = duplicate_count.get(cpf, 0) + 1
        for cpf, count in duplicate_count.items():
            print(f"CPF: {cpf} - Aparece {count} vezes.")
        
        # Perguntar se o usuário deseja manter os dados do arquivo original ou sobrescrever
        remove = input("\nDeseja substituir o arquivo original removendo as duplicatas? (s/n): ").strip().lower()
        if remove == "s":
            os.replace(temp_file_path, file_path)  # Substitui o arquivo original pelo arquivo sem duplicatas
            print("Arquivo original substituído, duplicatas removidas.")
        else:
            os.remove(temp_file_path)  # Remove o arquivo temporário
            print("Arquivo temporário excluído. O arquivo original não foi alterado.")
    else:
        print("Nenhum CPF duplicado encontrado.")

if __name__ == "__main__":
    # Caminho do arquivo com os CPFs
    file_path = "models/cpf_data.txt"
    
    # Remover duplicatas de um arquivo grande
    remove_duplicates_large_file(file_path)
