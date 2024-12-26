# Copyright (c) 2024 José Guilherme Cerqueira de Oliveira <aluno.jose.cerqueira@doctum.edu.br>
# This source code is licensed under the MIT license found in the license file.

# Script de otimização para o treinamento de IA no GitHub Codespace.
# Ajusta o uso de CPU, memória e configurações para maximizar o desempenho.
# Veja https://github.com/guilhermecerqueiraoliveira/privacy_cpf/blob/readme.md para mais detalhes.

#!/bin/bash

# Função para verificar e usar a GPU se disponível
check_gpu() {
    echo "Verificando se a GPU está disponível..."
    if command -v nvidia-smi &> /dev/null; then
        # Se o comando nvidia-smi estiver disponível, significa que a GPU está configurada
        echo "GPU detectada!"
        export CUDA_VISIBLE_DEVICES=0
    else
        echo "GPU não detectada, utilizando apenas a CPU."
    fi
}

# Função para ajustar a prioridade do processo (melhor desempenho)
adjust_priority() {
    echo "Ajustando a prioridade do processo de treinamento..."
    # Usar `nice` para dar maior prioridade ao processo
    # Isso faz com que o script use mais recursos da CPU
    nice -n -10 python train_model.py &
}

# Função para configurar a quantidade de threads para o treinamento
adjust_threads() {
    echo "Ajustando a quantidade de threads para o treinamento..."
    # Limitar o número de threads se necessário, por padrão o spaCy usa todos os núcleos
    # Vamos configurar para usar todos os núcleos (ajustar conforme necessário)
    export OMP_NUM_THREADS=4  # Ajuste esse número de threads conforme necessário
}

# Função para liberar memória cache
free_memory() {
    echo "Liberando memória cache..."
    sudo sync; sudo sysctl -w vm.drop_caches=3
}

# Função para iniciar o treinamento em segundo plano usando tmux
start_training_in_tmux() {
    echo "Iniciando o treinamento em segundo plano com tmux..."
    # Verifica se o tmux está instalado
    if ! command -v tmux &> /dev/null; then
        echo "O tmux não está instalado. Tentando instalar..."
        sudo apt-get install -y tmux
    fi

    # Cria uma nova sessão tmux chamada "training_session"
    tmux new-session -d -s training_session 'python train_model.py'
    echo "O treinamento foi iniciado em segundo plano usando tmux. Para acessá-lo, use: tmux attach -t training_session"
}

# Função principal para otimizar o ambiente de treinamento
optimize_environment() {
    # Ajustar a prioridade do processo
    adjust_priority

    # Ajustar a quantidade de threads para o treinamento
    adjust_threads

    # Verificar se a GPU está disponível e configurar
    check_gpu

    # Liberar memória cache
    free_memory

    # Iniciar o treinamento em tmux
    start_training_in_tmux

    # Executar os testes e salvar o log
    tmux new-session -d -s log_session 'python ./tests/test_model.py'
}

# Executa a função de otimização
optimize_environment
