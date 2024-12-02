import json
from flask import Flask, g, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

from modules.apaga import mod_apaga
from modules.apagausuario import mod_apagausuario
from modules.edita import mod_edita
from modules.editaperfil import mod_editaperfil
from modules.login import mod_login
from modules.logout import mod_logout
from modules.novo import mod_novo
from modules.perfil import mod_perfil

app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blocodenotas'

# Setup da conexão com MySQL
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8mb4'

# Variável de conexão com o MySQL
mysql = MySQL(app)


@app.before_request
def start():
    # Inicializa o aplicativo para cada rota acessada

    # Setup do MySQL para corrigir acentuação
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")

    # Setup do MySQL para dias da semana e meses em português
    cur.execute("SET lc_time_names = 'pt_BR'")

    # Lê o cookie do usuário → 'usuario'
    cookie = request.cookies.get('usuario')

    if cookie:
        # Se o cookie existe, Converte o valor dele de JSON para dicionário
        g.usuario = json.loads(cookie)
    else:
        # Se o cookie não existe, a variável do ususário está vazia
        g.usuario = ''

   
    


@app.route('/')
def home():
    if g.usuario == "":
        return redirect(url_for('login'))




    sql = '''
        SELECT `t_id`, `t_data`, `t_usuario`, `t_nome`, `t_anotacao`, `t_status`
        FROM notas
        WHERE `t_usuario` = %s
            AND t_status = 'on'
        ORDER BY t_data DESC
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    rows = cur.fetchall()
    cur.close()

    print('\n\n ROW:', rows, '\n\n')

    pagina = {
        'notas': rows,
        'titulo': 'Bloco de Notas',
        'usuario': g.usuario
    }

    # return 'Bem-vindo ao Bloco de Notas!'
    return render_template('index.html', **pagina)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.usuario != '':
        return redirect(url_for('perfil'))
    
    return mod_login(mysql)
    
@app.route('/perfil')
def perfil():
    if g.usuario == "":
        return redirect(url_for('login'))
    return mod_perfil(mysql)

@app.route('/editaperfil', methods=['GET', 'POST'])
def editaperfil():
    return mod_editaperfil(mysql)

@app.route('/logout')
def logout():
    return mod_logout()

@app.route('/apagausuario')
def apagausuario():
    return mod_apagausuario(mysql=mysql)

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    return mod_novo(mysql=mysql)


@app.route('/apaga/<id>')
def apaga(id):
    return mod_apaga(mysql, id)

@app.route('/edita/<id>', methods=['GET', 'POST'])
def edita(id):
    return mod_edita(mysql=mysql, id=id)

if __name__ == '__main__':
    app.run(debug=True)
