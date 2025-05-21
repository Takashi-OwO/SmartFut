1-acesse o site https://www.football-data.org/ e crie uma conta gratuita para conseguir uma api para poder pegar dados que vai alimentar o site
2-Instale Bibliotecas :

    flask	Framework principal para web	pip install flask
    flask_sqlalchemy	ORM (banco de dados com Python)	pip install flask_sqlalchemy
    flask_login	Gerenciamento de login e sessão de usuário	pip install flask_login
    flask_wtf	Integração entre Flask e formulários WTForms	pip install flask_wtf
    wtforms	Criação e validação de formulários em HTML	pip install wtforms
    werkzeug.security	Criptografia de senha	já vem com Flask
    os	Módulo interno do Python para lidar com o sistema	já vem com Python
    sqlite3	Acesso manual a banco de dados SQLite	já vem com Python
    Request Serve para fazer requisições HTTP (GET, POST, etc.) a APIs e sites externos. pip install requests
    
3- rode os codigos :
      
      app.py : codigo que pega dados dos 10 melhores atacantes da la liga e salva no banco de dados laliga.db
      standing_laliga: pega os 20 times da la liga e salva no banco de dados.
      Serie_A : pega os times do serie A e salva no banco de dados
      scorers_Brasil: pegas os 10 melhores jogadores da seie A
      
4 - rode o codigo Data.py que e o nosso site, o codigo principal


para mudança no site pode editar HTML que esta na pasta template:

        index.html: pagina principal do site
        login.html: tela de login
        register: tela de registro

Na pasta static temos a parte visual

    style.css e o estilo da pagina principal
    style_user.css estilo da tela de login e registro

dentro da pasta static tem outra pasta chamado images que tem a imagem de fundo da tela de login e registro e logo da La liga e Serie A


o codigo consulta.py pode ser utilizado para fazer consulta de algum dado de alguma tabela do banco de dado laliga que estao salvos os dados do projeto

status.py ver os dados que podemos pegar de certa tabela do nosso api 

usuario_teste ver os usuarios cadastrado
