# Projeto PyPrivacy
> **Nota:**
> Ao interagir com o projeto, você concorda em cumprir nosso código de conduta e seguir as diretrizes e etiquetas de contribuição de [código aberto](https://opensource.how/)

<div align="center">

![versão](https://img.shields.io/github/release/guilhermecerqueiraoliveira/PyPrivacy.svg?style=flat-square&label=Release&logo=github&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)
![Changelog](https://img.shields.io/badge/changelog-1.0.0-brightgreen?style=flat-square&logo=git&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)
![Docs](https://img.shields.io/badge/docs-1.0.0-brightgreen?style=flat-square&logo=read-the-docs&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)



![spaCy version](https://img.shields.io/pypi/v/spacy.svg?style=flat-square&label=spaCy&logo=pypi&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)
![scikit-learn version](https://img.shields.io/pypi/v/scikit-learn.svg?style=flat-square&label=scikit-learn&logo=pypi&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)
![PyPDF2 version](https://img.shields.io/pypi/v/PyPDF2.svg?style=flat-square&label=PyPDF2&logo=pypi&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)
![reportlab version](https://img.shields.io/pypi/v/reportlab.svg?style=flat-square&label=reportlab&logo=pypi&logoColor=black&colorA=F4E5B9&colorB=F4E5B9)

</div>


<!-- Pensando nessas bibliotecas:

![TensorFlow version](https://img.shields.io/pypi/v/tensorflow.svg?style=flat-square&label=TensorFlow&logo=tensorflow&logoColor=white&colorA=F4E5B9&colorB=F4E5B9)

![pdfminer version](https://img.shields.io/pypi/v/pdfminer.six.svg?style=flat-square&label=pdfminer&logo=pypi&logoColor=white&colorA=F4E5B9&colorB=F4E5B9)

![Pillow version](https://img.shields.io/pypi/v/Pillow.svg?style=flat-square&label=Pillow&logo=pypi&logoColor=white&colorA=F4E5B9&colorB=F4E5B9)

![pdf2image version](https://img.shields.io/pypi/v/pdf2image.svg?style=flat-square&label=pdf2image&logo=pypi&logoColor=white&colorA=F4E5B9&colorB=F4E5B9)

-->

<center>

**PyPrivacy** é como um canivete suiço. O objetivo deste projeto é utilizar um
modelo de rede neural para encontrar dados pessoais, como CPF e ocultar em documentos.
O modelo já foi treinado com 600 mil CPFs sintéticos.

</center>

## Indice
> **Note:**
>	Indice com links para o projeto

[Funcinalidades](#funcionalidades)</br>
[Estrutura do Projeto](#estrutura-do-projeto)</br>
[Dependências](#dependências)</br>
[Como usar](#como-usar)</br>
[Como funciona](#como-funciona)</br>
[Contribuições](#contribuições)</br>
[Licença](#licença)</br>

## Funcionalidades

- **Leitura de PDF**: Extrai o texto de arquivos PDF.
- **Detecção de CPF**: Usa reconhecimento de entidades nomeadas (NER) para localizar CPFs no texto.
- **Criação de PDF com CPF oculto**: Gera novos PDFs com os CPFs ocultos.

## Estrutura do projeto

A estrutura do projeto está organizada da seguinte forma:

```plaintext
privacy_cpf/                      
│
├── Certificados Gui/             
│   ├── Certificado - Curso.pdf   
│   └── ... (outros certificados)
│
├── examples/                    
│   ├── exemplo_entrada.pdf
│   ├── exemplo_saida.pdf
│
├── pdfs/                         
│   ├── CPF_OCULTO.pdf
│
├── tests/                        
│   ├── test_extraction.py        
│   ├── test_detecta.py           
│   ├── test_model.py             
│   └── test_ocultar.py           
│
├── models/                       
│   ├── ner_model                 
│   ├── __init__.py               
│   ├── cpfs_sinteticos.txt       
│   ├── detect_and_save.py        
│   └── cpf_detections.json       
│
├── venv/ 
│
├── cpp.py                        
├── cpf_privacy.py                
├── train_model.py                
├── generate_fake_cpfs.py         
├── check_duplicates.py           
├── requirements.txt              
├── Dockerfile                   
├── .gitignore                    
├── LICENSE                      
└── readme.md                    
```

## Dependências

Este projeto usa algumas bibliotecas do Python.

- [PyPDF2](https://pypi.org/project/PyPDF2/): Para manipulação de arquivos PDF. [x]
- [reportlab](https://pypi.org/project/reportlab): Para gerar novos arquivos PDF. [x]
- [spaCy](https://pypi.org/project/spaCy): Para processamento de linguagem natural e detecção de entidades nomeadas (NER).
- [scikit-learn](https://pypi.org/project/scikit-learn): Para treinamento de modelos de aprendizado de máquina.

## Como usar

### 1. Instalar Dependências
Antes de rodar o código, é necessário instalar as dependências. Basta executar:

```python
python setup.py
```

### 2. Processar um PDF
Para processar um arquivo PDF e ocultar os CPFs, basta executar o script `cpf_privacy.py` passando o caminho do arquivo PDF como argumento:

```bash
python cpf_privacy.py "Certificado - Curso.pdf"
```
*Isso vai gerar um novo arquivo PDF no diretório `/pdfs`, com os CPFs ocultos.*

### 3. Treinamento do Modelo de IA
Se você quiser treinar um **modelo de IA** para melhorar a detecção de CPFs, execute o script `train_model.py`

```bash
python train_model.py
```
*Este script vai treinar o modelo para identificar CPFs no texto. O modelo treinado será salvo para ser utilizado na detecção de CPFs.*

## Como funciona

- **Leitura e Extração de Texto:** O script `cpf_privacy.py` usa a biblioteca [pdfminer]() para extrair o texto do PDF.
- **Detecção de CPF:** Usando o modelo de NER do [spaCy](), o texto extraído é analisado em busca de CPFs. Caso sejam encontrados, suas localizações no texto são armazenadas.
- **Aplicação de Blur:** O script converte as páginas do PDF em imagens usando pdf2image, aplica o blur nas áreas correspondentes aos CPFs e cria um novo PDF.
- **Treinamento de IA (Opcional):** O script train_model.py permite treinar um modelo para detectar CPFs com base em exemplos de texto extraído de PDFs.
- **Docker (Opcional):**
Se você deseja rodar o projeto em um ambiente isolado e reproduzível, pode usar o Docker. O Dockerfile está configurado para criar uma imagem com todas as dependências do projeto. Para construir e rodar a imagem Docker, siga os passos:

### Construir a Imagem Docker:

```bash
docker build -t PyPrivacy .
```
### Rodar o Container Docker:

```bash
docker run -v $(pwd):/app PyPrivacy python cpf_privacy.py "Certificado - Curso de PHP.pdf"
```
*Este comando irá rodar o script dentro do container Docker, com o diretório atual montado como volume.*

## Contribuições
> **Nota:**
> Por favor, entenda que os contribuintes do projeto são apenas humanos normais que gastam do seu tempo livre em projetos de código aberto como este, ao lado de seu trabalho e atividades diárias e, portanto, estão disponíveis apenas de forma limitada para resolver questões gerais do projeto. Você não tem direito a suporte gratuito e os mantenedores de projetos de código aberto não lhe devem nada!


Somos um projeto de **código aberto** e adoramos receber contribuições.
</br>Seu envolvimento pode ser uma grande ajuda para melhorar o projeto e torná-lo cada vez mais eficiente e seguro.

> **Nota:**
> Antes de Contribuir, por favor, reserve um momento para ler nosso **guia de contribuição completo**. Ele vai te ajudar a entender o processo de desenvolvimento do projeto, nossos **guias de estilo** e como organizamos as **ramificações** e o **modelo de versão**.

Além disso, temos um **Código de Conduta** que garante um ambiente respeitoso e colaborativo para todos os envolvidos. Pedimos que você o leia e siga ao participar da comunidade. A ideia é que todos se sintam à vontade para contribuir de forma positiva e produtiva.

**Maneiras de contribuir:**

- **Melhorar a documentação**: Se você sabe mais sobre o projeto ou tem sugestões para melhorar a explicação de algumas partes, a documentação é um ótimo ponto de partida.
- **Relatar bugs**: Encontrou um erro? Nos avise! Assim conseguimos corrigir e melhorar a experiência de todos.
- **Enviar sugestões**: Se você tem ideias para novas funcionalidades ou melhorias, não hesite em compartilhar conosco.
- **Pull Requests (PRs)**: A maneira mais poderosa de contribuir! Se você desenvolveu uma melhoria ou corrigiu um erro, envie um PR. Vamos analisar com atenção e, se aprovado, sua contribuição será integrada ao projeto.

### Contribuições no Aprendizado de Máquina

Se você tem interesse ou experiência em **aprendizado de máquina _(machine learning)_**, há uma grande oportunidade para contribuir nesse aspecto do projeto! </br>O modelo de IA para detecção de CPFs pode ser aprimorado com técnicas de aprendizado supervisionado, extração de características do texto e até mesmo com dados de treinamento adicionais.

**Maneiras de contribuir:**

- **Treinamento de modelos de IA**: Se você conhece técnicas para melhorar a precisão do modelo, envie suas sugestões ou contribuições de código.
- **Ajustes no pré-processamento de dados**: Uma parte crucial de qualquer modelo de IA é a forma como os dados são tratados antes de serem alimentados no modelo. Se você tiver ideias para melhorar o processamento do texto ou dos dados de entrada, sua ajuda será muito bem-vinda.
- **Geração de dados de treinamento**: O modelo de IA precisa de bons dados para ser treinado. Você pode ajudar gerando ou sugerindo **novos dados de treinamento** para aprimorar a detecção de CPFs em diferentes contextos de PDFs.

### Outras Formas de Contribuir

Não está com tempo para escrever código, mas quer ajudar de alguma forma? Sem problemas! Existem outras maneiras de contribuir, como:

- **Resolver issues existentes**: Se você sabe como resolver algum dos problemas já listados no repositório, sua ajuda será muito bem-vinda.
- **Dar feedback**: Comentários sobre as funcionalidades ou ideias de melhorias são sempre bem recebidos. Eles ajudam a direcionar o projeto na melhor direção.
- **Divulgar o projeto**: Se você conhece pessoas ou organizações que poderiam se beneficiar do projeto, ou se tem um público que poderia se interessar, compartilhar o projeto nas redes sociais ou com colegas é uma **contribuição valiosa**.

Cada contribuição, por menor que pareça, faz a diferença! Então, sinta-se à vontade para nos ajudar a construir algo incrível.

### Objetivo
> **Nota:**
> Se você está pronto para contribuir, abra um **issue** ou envie um **pull request**. Estamos ansiosos para ter você como parte do nosso projeto!

Nosso objetivo é criar uma ferramenta que realmente ajude a proteger dados sensíveis, e **sua contribuição pode fazer a diferença**. Estamos ansiosos para ver o que você pode trazer para o projeto.


## Licença

<div align="center">

Este projeto está licenciado sob a [MIT License](https://github.com/guilhermecerqueiraoliveira/guilhermecerqueiraoliveira.github.io/blob/master/license.md).
</br>

Copyright © 2024 - Presente  
<a href="mailto:aluno.jose.cerqueira@doctum.edu.br">José Guilherme Cerqueira de Oliveira</a>  

![License: MIT](https://img.shields.io/badge/License-MIT-F4E5B9?style=for-the-badge&labelColor=F4E5B9&logo=creative-commons&logoColor=black)




<details>
	<summary><em>MIT License</em></summary>

Copyright (c) 2024 José Guilherme Cerqueira de Oliveira <aluno.jose.cerqueira@doctum.edu.br>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

</details>
</div>
