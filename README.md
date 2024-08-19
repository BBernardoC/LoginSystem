Desafio CSLR WGA



Como executar:

1. Certifique-se de que você tenha as bibliotecas Flask e Flask-MySQLdb instaladas 
"(pip install flask,pip install flask-mysqldb)"

2. No MySQL workbench execute o arquivo desafio.sql 

3. Confira se o MySQL está funcionando na porta 3306 para evitar erros de conexão

4. No arquivo app.py, configure a conexão com o banco de dados inserindo nessas linhas:
"app.config['MYSQL_HOST'] = 'localhost' "- seu hostname
"app.config['MYSQL_USER'] = 'root'  "- seu nome de usuário
"app.config['MYSQL_PASSWORD'] = '' "- sua senha para conexão


5. Com o MySQL e Python configurado, no terminal/prompt utilize o comando "flask run"
no diretorio em que o projeto está para inciar o servidor e entre no URL disponibilizado

6. Usar o programa!

