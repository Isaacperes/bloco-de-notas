import json
from flask import Flask, g, render_template, request
from flask_mysqldb import MySQL

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

    # Simula um usuário logado. Apague quando tiver login
    g.usuario = {
        'id': '1',
        'data': '2024-11-20 10:11:22',
        'nome': 'Joca da Silva',
        'nascimento': '1980-09-18',
        'email': 'joca@email.com',
        'status': 'on',
        'pnome': 'Joca'
    }


@app.route('/')
def home():

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


if __name__ == '__main__':
    app.run(debug=True)
