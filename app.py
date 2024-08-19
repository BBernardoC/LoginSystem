from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Criação da instância da aplicação Flask
app = Flask(__name__)

# Definindo a chave secreta para sessões (deve ser uma chave segura)
app.secret_key = '0281U3HJSDAHHAS09U012JDSPAJV'

# Configurações para a conexão com o banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost' #host 
app.config['MYSQL_USER'] = 'root' #user 
app.config['MYSQL_PASSWORD'] = '' #sua senha
app.config['MYSQL_DB'] = 'desafio' #nome do banco de dados

# Inicializa a conexão com o MySQL
mysql = MySQL(app)

# Rota para a página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''  # Mensagem de erro ou sucesso

    # Verifica se a requisição é POST e contém "username" e "password"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Consulta ao banco de dados para verificar se o usuário existe
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()  # Busca o usuário correspondente

        if account:
            # Se o usuário existe, cria dados de sessão
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redireciona para a página inicial
            return redirect(url_for('home'))
        else:
            # Caso contrário, exibe uma mensagem de erro
            msg = 'Senha/Usuário incorreto'
    
    # Renderiza a página de login com a mensagem de erro (se houver)
    return render_template('index.html', msg=msg)

# Rota para logout
@app.route('/logout')
def logout():
    # Remove os dados da sessão, efetivamente deslogando o usuário
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redireciona para a página de login
    return redirect(url_for('login'))

# Rota para a página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''  # Mensagem de erro ou sucesso

    # Verifica se a requisição é POST e contém "username", "password" e "genero"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'genero' in request.form:
        username = request.form['username']
        password = request.form['password']
        genero = request.form['genero']
        pronomes = request.form.get('pronomes', '')  # Captura pronomes se existirem

        # Verifica se o usuário já existe
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Conta já existe'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Usuário deve conter apenas letras e números'
        elif len(password) < 6:
            msg = 'Senha precisa de 6 caractéres'
        elif not username or not password or not genero:
            msg = 'Preencha o formulário'
        else:
            # Define pronomes com base no gênero selecionado
            if genero == 'masculino':
                pronomes = 'ele/dele'
            elif genero == 'feminino':
                pronomes = 'ela/dela'
            elif genero == 'desconhecido':
                pronomes = 'Não identificado'
            elif genero == 'outro' and not pronomes:
                msg = 'Insira pronomes'
                return render_template('register.html', msg=msg)

            # Insere a nova conta no banco de dados
            cursor.execute('INSERT INTO accounts (username, password, genero, pronomes) VALUES (%s, %s, %s, %s)', (username, password, genero, pronomes))
            mysql.connection.commit()
            msg = 'Conta criada'

    elif request.method == 'POST':
        # Caso o formulário esteja vazio (nenhum dado POST)
        msg = 'Preencha o formulário'
    
    # Renderiza a página de registro com a mensagem (se houver)
    return render_template('register.html', msg=msg)

# Rota para a página inicial (após login)
@app.route('/home')
def home():
    # Verifica se o usuário está logado
    if 'loggedin' in session:
        # Consulta ao banco de dados para obter informações da conta do usuário
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Renderiza a página inicial com as informações da conta
        return render_template('home.html', username=session['username'], account=account)
    
    # Se o usuário não estiver logado, redireciona para a página de login
    return redirect(url_for('login'))
