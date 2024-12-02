from flask import g


def get_all_anotaçoes(mysql):
    # Obtém todos os registros válidos

    sql = '''
        SELECT t_id, t_nome, t_anotacao
        FROM notas
        WHERE t_usuario = %s
            AND t_nome = 'on'
        ORDER BY t_anotacao DESC
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    rows = cur.fetchall()
    cur.close()

    return rows


def create_anotação(mysql, form):
    # Cadastra um novo registro no banco de dados

    sql = '''
        INSERT INTO notas (
            t_usuario, t_nome, t_anotacao
        ) VALUES (
            %s, %s, %s
        )
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (
        g.usuario['id'],
        form['nome'],
        form['anotacao'],
    ))
    mysql.connection.commit()
    cur.close()

    return True


def get_one_anotação(mysql, id):
    # Obtém um registro pelo id

    sql = '''
        SELECT * FROM notas
        WHERE t_id = %s
            AND t_usuario = %s
            AND t_status = 'on'
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (id, g.usuario['id'],))
    row = cur.fetchone()
    cur.close()

    return row


def update_anotação(mysql, form, id):
    # Salva atualização do registro

    sql = '''
            UPDATE notas 
            SET t_nome = %s,
                t_anotacao = %s
            WHERE t_id = %s
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (
        form['nome'],
        form['anotacao'],
        id,
    ))
    mysql.connection.commit()
    cur.close()

    return True


def delete_anotação(mysql, id):
    # apaga um registro pe ID

    # (des)comente o método para apagar conforme o seu caso
    # Apaga completamente o treco (CUIDADO!)
    # sql = 'DELETE FROM treco WHERE t_id = %s'
    # Altera o status do treco para 'del' (Mais seguro)
    sql = "UPDATE notas SET t_status = 'del' WHERE t_id = %s"

    # Executa o SQL
    cur = mysql.connection.cursor()
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()

    return True


def get_count_user_anotações(mysql):
    sql = "SELECT count(t_id) AS total FROM notas WHERE t_usuario = %s AND t_status = 'on'"
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    row = cur.fetchone()
    cur.close()

    return row
