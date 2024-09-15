# Projeto LibSale

O projeto "LibSale: Sistema de Ponto de Venda" foi desenvolvido para atender às necessidades de pequenos empresários do ramo de livrarias, proporcionando uma solução simples e eficiente para o gerenciamento de vendas. A aplicação, construída com Python, Flask e SQLite, foi projetada para otimizar operações como busca de produtos, registro de vendas, e abertura e fechamento de caixa.


# Tecnologias utilizadas

- [Python] (https://www.python.org/)
- [Flask] (https://flask.palletsprojects.com/en/3.0.x/)
- [SQLite] (https://www.sqlite.org/)
- [SQLAlchemy] (https://www.sqlalchemy.org/)


# Passos para instalação:

É recomendado antes de tudo abrir um [ambiente virtual] (https://docs.python.org/pt-br/3/library/venv.html) Python para proceder com a instalação das dependências.

1. Clone este repositório

   ```bash
    $ git clone https://github.com/luizagraciano/LibSale.git
     ```
   

2. Instale as dependências através do arquivo **requirements.txt**:

  ```bash
    $ pip install requirements.txt
     ```


3. Incialize o banco de dados:

     ```bash
    $ flask --app src init-db
     ```

Você verá ser adicionada a pasta **instance** ao projeto, contendo o arquivo do banco de dados.


4. Alimente o banco de dados com uma prévia de produtos:

     ```bash
    $ flask --app src seed-db
     ```


5. Rode o projeto:

     ```bash
    $ flask --app src run
     ```