from setuptools import setup, find_packages

def load_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()

with open('readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyPrivacy',
    version='1.0.0',
    author='José Guilherme Cerqueira de Oliveira',
    author_email='aluno.jose.cerqueira@doctum.edu.br',
    description='Projeto para detecção e manipulação de CPFs utilizando aprendizado de máquina.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/guilhermecerqueiraoliveira/PyPrivacy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Natural Language Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
        'Framework :: spaCy',
        'Framework :: scikit-learn',
        'Environment :: Console',
    ],
    python_requires='>=3.12.5',
    install_requires=load_requirements(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # Adicionar scripts do console aqui, por exemplo:
            # 'pyprivacy-cli=pyprivacy.cli:main',
        ],
    },
)
