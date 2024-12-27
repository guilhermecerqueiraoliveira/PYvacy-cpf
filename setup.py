# Copyright (c) 2024 José Guilherme Cerqueira de Oliveira <aluno.jose.cerqueira@doctum.edu.br>
# This source code is licensed under the MIT license found in the license file.
# Veja https://packaging.python.org/pt-br/latest/guides/distributing-packages-using-setuptools/ para mais informações.

from setuptools import setup, find_packages

def load_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()

setup(
    name='privacy_cpf',
    version='0.1.0',
    author='José Guilherme Cerqueira de Oliveira',
    author_email='aluno.jose.cerqueira@doctum.edu.br',
    description='Projeto para detecção e manipulação de CPFs utilizando aprendizado de máquina.',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/guilhermecerqueiraoliveira/privacy_cpf',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12.5',
    install_requires=load_requirements(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # adicionar scripts do console aqui
        ],
    },
)
