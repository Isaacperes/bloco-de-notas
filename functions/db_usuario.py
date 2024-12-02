from flask import g


def get_usuario(mysql, form):

    # Pesquisa se os dados existem no banco de dados → usuario
    sql = '''
        SELECT *,
            -- Gera uma versão das datas em pt-BR para salvar no cookie
            DATE_FORMAT(u_data, '%%d/%%m/%%Y às %%H:%%m') AS u_databr,
            DATE_FORMAT(u_nascimento, '%%d/%%m/%%Y') AS u_nascimentobr
        FROM usuario
        WHERE u_email = %s
            AND u_senha = SHA1(%s)
            AND u_status = 'on'
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (form['email'], form['senha'],))
    usuario = cur.fetchone()
    cur.close()

    return usuario


def get_by_email_birth(mysql, form):
    # Pesquisa pelo email e nascimento informados, no banco de dados
    sql = '''
        SELECT u_id
        FROM usuario
        WHERE u_email = %s
            AND u_nascimento = %s
            AND u_status = 'on'
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (form['email'], form['nascimento'],))
    row = cur.fetchone()
    cur.close()

    return row


def save_new_password(mysql, novasenha, id):
    # Salva a nova senha no banco de dados

    sql = "UPDATE usuario SET u_senha = SHA1(%s) WHERE u_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(sql, (novasenha, id,))
    mysql.connection.commit()
    cur.close()

    return True

def delete_user(mysql):
    sql = "UPDATE usuario SET u_status = 'del' WHERE u_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    mysql.connection.commit()
    cur.close()
    return True


def update_user(mysql, form):
    sql = '''
        UPDATE usuario
        SET u_nome = %s, u_nascimento = %s, u_email = %s
        WHERE u_id = %s AND u_senha = SHA1(%s)
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (
        form['nome'],
        form['nascimento'],
        form['email'],
        g.usuario['id'],
        form['senha1'],
    ))
    mysql.connection.commit()
    cur.close()
    return True


def update_password(mysql, form):
    sql = "UPDATE usuario SET u_senha = SHA1(%s) WHERE u_id = %s AND u_senha = SHA1(%s)"
    cur = mysql.connection.cursor()
    cur.execute(sql, (
        form['senha2'],
        g.usuario['id'],
        form['senha1'],
    ))
    mysql.connection.commit()
    cur.close()
    return True


def get_user_data(mysql):
    sql = "SELECT * FROM usuario WHERE u_id = %s AND u_status = 'on'"
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    row = cur.fetchone()
    cur.close()
    return row
